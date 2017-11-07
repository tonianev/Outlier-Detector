import zipfile
import shutil	
import os

host_drive = "xxx.xxx.xx.xx"
temp_dir = "xxx.xxx.xx.xx"

if not os.path.exists(temp_dir):
	os.mkdir(temp_dir)


usr_q = str(input("Which date are you looking for?\n(Format: YYMMDD) "))


def dem_parse(dem_file):
	""" - Opens .DEM file and targets "."
		- Splits line and stores the values preceeding "." in a list
		- List is parsed to only contain target values
	"""

	with open(dem_file) as f:
		read_data = []
		for line in f:
			if "." in line:
				split_line = line.split(".")
				read_data.append(split_line)

	raw_home = [i[0] for i in read_data]
	homem_no = [i[0:9] for i in raw_home]

	return homem_no


def transfer_n_compare():
	""" - Scans for reprocessed and overnight files in host_location
		- Copies target files to temp_dir
		- Extracts .DEM files and deletes everything else
		- Uses dem_parse function to parse .DEM files and store values in a list
		- Returns values found in overnight list but not reprocessed list 
	"""
	outliers = []
	reprocessed_list = []
	overnight_list = []
	audem_file = "AU" + usr_q + ".DEM"

	try: 
		for file in os.listdir(host_drive):
		    if file.startswith("XXXX_XXXX" + usr_q) and file.endswith(".zip"):
		    	shutil.copy(os.path.join(host_drive,file), temp_dir)
		    	zf = zipfile.ZipFile(os.path.join(temp_dir, file), 'r')
		    	zf.extract(audem_file, path = os.path.join(temp_dir,'Final'))
		    	os.chdir(os.path.join(temp_dir,'Final'))
		    	reprocessed_list = dem_parse(audem_file)

		    elif file.startswith("XXXX_XXXX" + usr_q) and file.endswith(".zip"): 
		    	shutil.copy(os.path.join(host_drive,file), temp_dir)
		    	zf = zipfile.ZipFile(os.path.join(temp_dir, file), 'r')
		    	zf.extract(audem_file, path = os.path.join(temp_dir,'Overnight'))
		    	os.chdir(os.path.join(temp_dir,'Overnight'))
		    	overnight_list = dem_parse(audem_file)

		for i in overnight_list:
			if i not in reprocessed_list:
				outliers.append(i)

		if len(outliers) != 0:
			print("Here are the outliers: ", outliers)
		elif len(outliers) == 0:
			print("Unable to find outliers.")

	finally:
		zf.close()
		for folder in os.listdir(temp_dir):
			if folder.endswith(".zip"):
				os.remove(os.path.join(temp_dir,folder))

		input("Press enter to exit...")


if __name__=="__main__":
	transfer_n_compare()
