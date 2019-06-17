from utils import Files,Function
import glob,os
import re

def find_functions(args):
    files=Files(args.parent_dir)
    fmap={}
    while files.not_empty():

        current_file=files.all_files.pop()
        if(os.path.isdir(current_file)):
           newfiles=glob.glob(current_file+"/*")
           files.add_file(newfiles)

        elif(current_file.endswith(".py")):
            with open(current_file) as f:
                lines=f.read().splitlines()

                for line in lines:
                    splits=line.split("def ")
                    if(len(splits)==1):
                        continue
                    fname=splits[1].split("(")[0]
                    fdef="def "+splits[1][:-1] 
                    function=Function()
                    function.path=current_file
                    function.name=fname
                    function.definition=fdef

                    fmap[fname]=function
                
    return fmap,files

def find_callers(fmap,files):
    while files.not_empty():

        current_file=files.all_files.pop()
        if(current_file.endswith(".py")):
            f=open(current_file,"r")
            lines=f.read().splitlines()
            for line in lines:
                for fname in list(fmap.keys()):
                    pattern=fname+r"(.*)"
                    if(not re.search(pattern,line)):
                        continue
                    if(len(line.split("def "))>1):
                        break
                    fmap[fname].add_caller(current_file)
            f.close()

