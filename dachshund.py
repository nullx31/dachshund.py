#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# dis looks for things.

import os, sys, time
import win32api
import hashlib
import urllib2

# config
pastebinlink = 'http://pastebin.com/raw.php?i=b1Yz8vbD' #add your pastebin hash list url here


# functions

def print_dog():
	print """
	DACHSHUND 0.1
	by @pirate_security
	
	      				   \ | /		
    (\,----------------'()'--o ~ ~ ~ #dathash
     (_    ___________    /~'
      (_)_)           (_)_)

	"""
def get_pc_name():
	return os.environ['COMPUTERNAME']

def get_windows_drives():
	drives = win32api.GetLogicalDriveStrings()
	#drives = 'C:\\'
	windrives = drives.split('\000')[:-1] 
	return windrives # a list with all drives on pc

def get_system_drive():
	sysdrive = os.getenv("SystemDrive")
	return sysdrive #as string

def get_windows_user():
	winuser = win32api.GetUserName()
	return winuser # current user as string

def get_win_user_folder():
	win_user_folder = os.getenv("SystemDrive")+'\\Users\\'+win32api.GetUserName()+'\\'
	return win_user_folder # as listentry

def get_subdirectories_of(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def make_whole_path_of_dir(dirses):
	wholepathdirlist = []
	for x in dirses:
		x = os.getenv("SystemDrive")+'\\'+x+'\\'
		wholepathdirlist.append(x)
	return wholepathdirlist
		
def exculdethesefolders(sysdrive):
	folderstoexclude = [
	'Windows','Program Files','Programme','Program Files (x86)','ProgramData','System Volume Information','Recovery','$Recycle.Bin','Intel']
	return folderstoexclude #list of folders with junk not to scan

def hashme_md5_small_file(hashme):
	try:
		return hashlib.md5(open(hashme, 'rb').read()).hexdigest()
	except:
		pass

def hashme_sha256_small_file(hashme):
	return hashlib.sha256(open(hashme, 'rb').read()).hexdigest()

def hashmesha256(hashme, hashalgo=hashlib.sha256(), blocksize=65536):
	filetohash = open(hashme, 'rb') #binary
	chunky = filetohash.read(blocksize)
	while len(chunky) > 0:
		hashalgo.update(chunky)
		chunky = filetohash.read(blocksize)
	return hashalgo.hexdigest()

def clear_junk_folders(allfolderlist,junklist):
	return [z for z in allfolderlist if z not in junklist]

def dat_hash():
	targets = {
	'md5':'b7c17346d580d2231411151b0f39b261',
	'sha256':'...wrong...'}
	return targets

def get_cpu_load():
    result = []
    cmd = "WMIC CPU GET LoadPercentage "
    response = os.popen(cmd + ' 2>&1','r').read().strip().split("\r\n")
    for load in response[1:]:
       result.append(int(load))
    return 19 # result # 0-100% als liste

def create_txt_with_all_file_entrys(clean_folder_list): # fix folder list to contain path!!!!!!!!!!!!!
	all_files_list = []
	for xxx in clean_folder_list:
		for (paths, dirs, files) in os.walk(xxx):
			for file in files:
				#if file.endswith(".txt") or file.endswith(".doc") or file.endswith(".xls") or file.endswith(".xlsx") or file.endswith(".docx"): # filter by extension too
				#print os.path.join(paths, file)
				all_files_list.append(os.path.join(paths, file))
	return all_files_list

def hash_vs_file(all_files_list):
	#textfilewithlinks = open('hashmelater.txt', 'r')
	target='d357db0ae1d51d4457d5ff587530a54e'
	#print 'the md5 target is: ', target
	for entry in all_files_list:
		try:
			filehash = hashlib.md5(open(entry, 'rb').read()).hexdigest()
			if filehash == target:
				print 'file: ', entry, 'md5: ', filehash, '+++ [target found] +++'
				break
			else:
				print 'file: ', entry, 'md5: ', filehash, os.system('CLS')
		except:
			pass	

def gethashlistfromurl(pastebinlink):
	urltoparse = urllib2.urlopen(pastebinlink)
	urlhtml = urltoparse.read()
	all_hashes_list = urlhtml.split()
	urltoparse.close()
	
	return all_hashes_list

####################################################
# STUFF ABOVE HERE WORKS and below here is concept #
####################################################

def waiting():
	print 'Loading....  ',
	sys.stdout.flush()
	i = 0
	while i <= 16:
		if (i%4) == 0: 
			sys.stdout.write('\b/')
		elif (i%4) == 1: 
			sys.stdout.write('\b-')
		elif (i%4) == 2:
			sys.stdout.write('\b\\')
		elif (i%4) == 3: 
			sys.stdout.write('\b|')
		sys.stdout.flush()
		time.sleep(0.2)
		i+=1
	#print 'done!'

def urlhashes_vs_file(all_files_list,all_hashes_list):
	for entry in all_files_list:
		try:
			filehash = hashlib.md5(open(entry, 'rb').read()).hexdigest()
			if filehash in all_hashes_list:
				print 'file: ', entry, 'md5: ', filehash, '+++ [target found] +++'
				break
			else:
				print 'file: ', entry, 'md5: ', filehash	
		except:
			pass	

def checkforstring(all_files_list, whatchalookingfor):
	hit_link_file = open('filelist.txt', 'w')
	for link in all_files_list:
		try:
			content = (open(link,"r")).read()
		except:
			pass
		if whatchalookingfor in content or whatchalookingfor in link:
			hit_link_file.write(str(link) + '\n')
			#print str(link) # print job
	hit_link_file.close()
	return hit_link_file

###### Main Loop #######
if __name__ == '__main__':

	while get_cpu_load() <= 20:
		print  print_dog()
		print '[...] getting info about system... '
		print '[v] pc name: ',get_pc_name()
		print '[v] win user: ', get_windows_user()
		print '[v] all drives: ', get_windows_drives()
		print '[v] system drive: ', get_system_drive()
		print '[v] win user folder: ', get_win_user_folder()
		print ''
		print '[...] getting info about folder structure... '
		print '[v] all folders on system drive:\n', get_subdirectories_of('C://')
		print '[v] junk folders to exclude from search: ', exculdethesefolders(get_system_drive())
		boomerang = clear_junk_folders(get_subdirectories_of('C://'),exculdethesefolders(get_system_drive()))
		print '[v] clean list of folders to scan: ', make_whole_path_of_dir(boomerang)
		print ''
		print '[...] making a list with all files in clean folders. this might take a while.'#, waiting()
		print ''		
		all_files_list = create_txt_with_all_file_entrys(make_whole_path_of_dir(boomerang))
		print '[v] files on system: ', len(all_files_list)
		print '[...] getting the hashlist from %s.'%pastebinlink
		all_hashes_list = gethashlistfromurl(pastebinlink)
		print '[v] entries in hash list: ', len(all_hashes_list)
		print '[v] entries: ', all_hashes_list
		print ''
		print '[v] searching... ', urlhashes_vs_file(all_files_list,all_hashes_list)
		print ''	
		print 'done'
		break
