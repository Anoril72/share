#!/usr/bin/env python3

import os
import subprocess
from multiprocessing import Pool
from itertools import repeat
def clean_files(files):
    os.remove(files)
def sync_files(files,src,dest):
    if files["file"] == None:
        return
    for fil in files["file"]:
        f="{}/{}".format(files["dir"],fil)
        backup_dir=files["dir"].replace(src,dest)
        subprocess.call(["rsync","-arq",f,backup_dir])
def clean(src,dest):
    filelist=[]
    dirlist=[]
    for dirpath,dirs,files in os.walk(dest, topdown=False):
        for d in dirs:
            dline="{}/{}".format(dirpath,d)
            if not os.path.exists(dline.replace(dest,src)):
                dirlist.append(dline)
        for f in files:
            fline="{}/{}".format(dirpath,f)
            if not os.path.exists(fline.replace(dest,src)):
                filelist.append(fline)
    if len(filelist)>0:
        p=Pool(len(filelist)) 
        p.map(clean_files,filelist)
    for dirs in dirlist:
        os.rmdir(dirs)
def sync(src,dest):
    filelist=[]           
    for dirpath,dirs,files in os.walk(src):
        filelist.append({"dir":dirpath,"file":files})
    print(filelist)
    for files in filelist:
        backup_dir=files["dir"].replace(src,dest)
        if not os.path.isdir(backup_dir):
            print(backup_dir)
            os.mkdir(backup_dir)
    p=Pool(len(filelist))
    p.starmap(sync_files, zip(filelist, repeat(src),repeat(dest)))   

if __name__ == "__main__":
    src="For_walk"
    dest="For_walk_backup"
    clean(src,dest)
    sync(src,dest)
