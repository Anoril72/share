#!/usr/bin/env python3

import os
import subprocess
from multiprocessing import Pool
from itertools import repeat
def clean_files(files):
    os.remove(files)
def sync_files(files,src,dest):
    fline="{}/{}".format(files["dir"],files["file"])
    backup_dir=files["dir"].replace(src,dest)
    subprocess.call(["rsync","-arq",fline,backup_dir])
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
    dirlist=[]           
    for dirpath,dirs,files in os.walk(src):
        for d in dirs:
            dline="{}/{}".format(dirpath,d).replace(src,dest)
            if not os.path.exists(dline):
                dirlist.append(dline)
        for f in files:
            filelist.append({"dir":dirpath,"file":f})
    for dirs in dirlist:
        os.mkdir(dirs)
    p=Pool(len(filelist))
    p.starmap(sync_files, zip(filelist, repeat(src),repeat(dest)))   

if __name__ == "__main__":
    src="For_walk"
    dest="For_walk_backup"
    clean(src,dest)
    sync(src,dest)
