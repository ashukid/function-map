import os
import glob

files=glob.glob(os.getcwd()+"/*")
function=[]
function_path={}
while files:
    current_file=files.pop()

    if(os.path.isdir(current_file)):
        newfiles=glob.glob(current_file+"/*")
        files.extend(newfiles)

    elif(current_file.endswith(".py") and not current_file.endswith('function_finder.py')):
        with open(current_file) as f:
            lines=f.read().splitlines()
            for line in lines:
                splits=line.split("def ")
                if(len(splits)>1):
                    function.append(splits[1].split("(")[0])
                    function_def="def "+splits[1][:-1]
                    function_path[splits[1].split("(")[0]]=[current_file,function_def]


files=glob.glob(os.getcwd()+"/*")
fd=open("function.csv","w+")
while files:
    current_file=files.pop()

    if(os.path.isdir(current_file)):
        newfiles=glob.glob(current_file+"/*")
        files.extend(newfiles)

    elif(current_file.endswith(".py") and not current_file.endswith('function_finder.py')):
        with open(current_file) as f:
            lines=f.read().splitlines()
            for line in lines:
                splits=line.lstrip().split("(")
                splits=splits[0].split("=")
                if(len(splits)>1):
                    splits=splits[1].lstrip()
                else:
                    splits=splits[0]
                splits=splits.split("if")
                if(len(splits)>1):
                    splits=splits[1].lstrip()
                else:
                    splits=splits[0]
                if(len(splits.split("def "))>1):
                        continue
                if(splits in function):
                    function_path[splits].append(current_file)

for k,v in function_path.items():
    path=v[0]
    funcdef=v[1]
    name=k
    calls=set(v[2:])

    towrite=path.split("/")[-1]+"\t"+name+"\t"+funcdef
    for c in calls:
        towrite += "\t"
        towrite += c.split("/")[-1]
    fd.write(towrite+"\n\n")

fd.close()
