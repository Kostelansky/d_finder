import os
import sys
import hashlib

__author__ = "Justin Kostelansky"
__copyright__ = "Copyright 2012, Justin Kostelansky    "
__version__ = "1.0.0"
__maintainer__ = "Justin Kostelansky"
__email__ = "hello@torched.org"
__description__ = "File Duplicator Finder"
__python_version__ = "3.3.0"

def dir_tree_mapper(basedir_root):
	for root, dirs, files in os.walk(basedir_root):
		for file in files:
			if '.pdf' or 'docx' in file:
				yield os.path.join(root, file)

def get_filesize(files):
	for file in files:
		yield os.path.getsize(file), file

def get_md5(files):
	for filepath in files:
		blocksize = 1024 * 1024
		size = os.path.getsize(filepath)
		yield hash_value(filepath, size, blocksize, hashlib.md5()), filepath
		
def hash_value(filename, filesize, maxsize, xhash):
	with open(filename, 'rb') as openfile:
		while True: 
			data = openfile.read(maxsize)
			if not data:
				break
			xhash.update(data)
	return xhash.hexdigest()

def remove_non_dups(basedir_root_mod):
	d = {} #Set Up Empty Dictionary
	r = []
	for new_tree_list in basedir_root_mod:
		#Set Dictionary Key
		key = new_tree_list[0]
		if key not in d:
			d.setdefault(key, []).append(new_tree_list[1]) #If Our Key Isn't In Our Dictionary Add It, and Our File Location.
		else:
			d[key].append(new_tree_list[1]) #If Our Key Is In Our Direcotry Append It To Our Dictionary Key With another File Location. 
	for keyvalues in d.values():
		if len(keyvalues) > 1:	#If There Is Multiple Entries On Our Key Add Location To Our r (results) list.
			r = r + keyvalues
	return r
	
def print_results(final):
	r_file = open("d_finder.txt", "wt")
	for files in final:
		size = str(os.path.getsize(files))
			print("\nFile Size: " + size + "				File Path: " + files)
			r_file.write("File Size: " + size + "		File Path: " + files + "\n")
	r_file.close()
	
if __name__ == '__main__':
	#Base Root Directory To Scan
	basedir_root = "/Users/Kostelansky/test" #DEFINE!

	if os.path.isdir(basedir_root):
		dir_tree = dir_tree_mapper(basedir_root) #Return Index of Base Root Dir
		file_size = get_filesize(dir_tree) #Returns [File Size, Location]
		dup_size_dir_tree = remove_non_dups(file_size) #Return Filtered Directory Tree With Files With Same Size
		md5_tree = get_md5(dup_size_dir_tree) #Return List With MD5 & File Location
		dup_md5_dir_tree = remove_non_dups(md5_tree) #Returns A File List Of Duplicated MD5 Hashed Files
		print_results(dup_md5_dir_tree) #Print Final Directory Locations		
		
	sys.exit(2)