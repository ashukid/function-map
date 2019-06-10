import os
import glob
import argparse
import re

def parse_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("--parent_dir",default="./",
                        help="full path of parent directory",
                        required=True)
    parser.add_argument("--output_type",default="print",
                        help="how to show the map",
                        required=False)
    args=parser.parse_args()
    return args

class Function:
    def __init__(self):
        self.definition=None
        self.name=None
        self.path=None
        self.callers=set()

    def add_caller(self,caller):
        self.callers.add(caller)

class Files:
    def __init__(self,parent_dir):
        self.meta=glob.glob(parent_dir+"/*")
        self.all_files=glob.glob(parent_dir+"/*")

    def add_file(self,filename):
        self.meta.extend(filename)
        self.all_files.extend(filename)

    def not_empty(self):
        if(self.all_files):
            return True
        self.all_files=self.meta[:]
        return False

def get_function_map(args):
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
                    pattern=fname+"(.*)"
                    if(not re.search(pattern,line)):
                        continue
                    if(len(line.split("def "))>1):
                        break
                    fmap[fname].add_caller(current_file)
            f.close()

def main():
    args=parse_arguments()
    if(args.parent_dir.endswith("/")):
        args.parent_dir=args.parent_dir[:-1]

    fmap,files=get_function_map(args)
    find_callers(fmap,files)
    for k in fmap.keys():
        func=fmap[k]
        print(func.name)
        print(" "*4,func.path)
        print(" "*4,func.definition)

        for c in func.callers:
            print(" "*8,"-->",c)


if __name__=='__main__':
    main()
