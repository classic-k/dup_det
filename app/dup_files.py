import os
from hashlib import md5
import time
import argparse
import sys




def dup_det(dir):

    all_hash = []
    dup_hash = []
    dup_size = 0.00

  
   
    for root, sub, files in os.walk(dir):
        
        sub_files = [file for file in files]
       
        for file in sub_files:

            path = os.path.join(root, file)
            hash = file_hash(path)
            size = getSize(path)
            size = float(size)

            if hash in all_hash:
                
                print(f"{file} in {path} is duplicate")
                dup_hash.append({"name":file, "hash":hash, "path":path})
                dup_size += size

            all_hash.append(hash)
                
        
    return dup_hash, dup_size
   


def file_hash(file_loc):
    B_SIZE = 65536
    hasher = md5()
    with open(file_loc, "rb") as afile:

        buf = afile.read(B_SIZE)
        while len(buf) > 0:

            hasher.update(buf)
            buf = afile.read(B_SIZE)

    return hasher.hexdigest()



def getSize(path):

    size = os.stat(path).st_size

    size_mb = size / (1024 * 1024)

    return "{0:.2f}".format(size_mb)


def analyse(all_dup, dup_size):

    if len(all_dup) > 0:

        print("Total number of duplicate ", len(all_dup))
        print("Total size of duplicate {0:.2f}".format(dup_size))

        res = input("Press yes to delete duplicate files: ")
        res = res.lower()

        if res == "yes":
            
            for item in all_dup:
            
                print("Deleting... {}".format(item["name"]))
                os.remove(item['path'])
            print("{0:.2f} mb space freed".format(dup_size))
    else:
        print("No duplicate files in folder")

def main():

    parser = argparse.ArgumentParser(prog="Delete_Duplicate", description="Program to detect duplicat files in folder with delete ability")

    parser.add_argument("-d","--dir", help="Enter valid directory path to scan")

    args = parser.parse_args()

    if args.dir:
        dir = args.dir
        if os.path.isdir(dir):
            dup_hash, dup_size = dup_det(dir)
            analyse(dup_hash, dup_size)

        else:

            print("Invalid directory enter valid directory")
            sys.exit()
    else:
        parser.print_usage()

        sys.exit()

main()
