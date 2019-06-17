import os
import glob
import argparse
import re
from functions import find_functions
from functions import find_callers
from utils import Function,Files,show_output


def parse_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("--parent_dir",default="./",
                        help="full path of parent directory",
                        required=True)
    parser.add_argument("--output_type",default="terminal",
                        help="how to show the map",
                        required=False)
    args=parser.parse_args()
    return args

def main():
    args=parse_arguments()
    if(args.parent_dir.endswith("/")):
        args.parent_dir=args.parent_dir[:-1]

    fmap,files=find_functions(args)
    find_callers(fmap,files)
    
    show_output(fmap,args.output_type)

if __name__=='__main__':
    main()
