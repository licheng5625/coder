import path
import os
import shutil
for  root, dirs, files in os.walk(path.userrawpath):
    for name in files:
        if ".html" in name:
            if not os.path.isdir(path.userrawpath+name[0]):
                os.mkdir(path.userrawpath+name[0])
            shutil.move(path.userrawpath+name,path.userrawpath+name[0]+'/'+name)