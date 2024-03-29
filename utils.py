import glob,os

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

def show_output(fmap,output_type):
    
    if(output_type=='terminal'):    

        for k in fmap.keys():
            func=fmap[k]
            print(func.name)
            print(" "*4,func.path)
            print(" "*4,func.definition)
            for c in func.callers:
                print(" "*8,"-->",c)
    
    if(output_type=='csv'):
        f=open("output.csv","w+")
        for k in fmap.keys():
            func=fmap[k]
            s=func.name+","+func.definition+","+func.path
            for c in func.callers:
                s+= ","+c
            s+="\n" 
            f.write(s)
        f.close()
