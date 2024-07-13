import os
import shutil


def cp(fileA, fileB):
 shutil.copy(fileA, fileB)
 

def cp_R(pathA, pathB):
 files = []
 
 def dfs(cr):
  nonlocal files
  if os.path.isfile(join_paths(cr)):
   files.append(cr)
  else:
   for file in os.listdir(join_paths(cr)):
    dfs(cr + [file])
 
 dfs([pathA])
 
 for ls in files:
  x_paths([pathB] + ls[1:-1])
  shutil.copy(join_paths(ls), join_paths([pathB]+ls[1:]))

def join_paths(path = []):
 cr = ""
 for f in path:
  cr = os.path.join(cr, f) 
 return cr
 

def x_paths(path = []):
 cr = ""
 for f in path:
  cr = os.path.join(cr, f) 
  mkdir(cr)


def mkdir(dir):
 if not os.path.exists(dir):
  os.makedirs(dir)
  
  