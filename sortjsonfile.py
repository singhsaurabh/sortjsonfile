#! /usr/local/bin/python3
import json
import argparse
import os, sys
import time

def checkArgs():
    """ Argument check """
    parser = argparse.ArgumentParser(description='Sort JSON File or File List. Use one option at a time')
    parser.add_argument("-p", "--path", help='JSON files location')
    parser.add_argument("-f", "--file", help='Specific JSON file')
    parser.add_argument("-l", "--filelist", help='File name which has list of JSON file')

    try:
        args = parser.parse_args()
    except IOError as msg:
        raise parser.error(str(msg))

    if (args.path == None and args.file == None and args.filelist == None) or (len(sys.argv) > 3):
        parser.print_help()
        return False
    else :
        return(args)


def sortedLocation(destination):
    """ Create the directory in current working directory with the 'sortedfiles_EPOCHTime'. """
    try:
        os.mkdir(destination)
    except OSError as exc:
        raise exc


def sortJSONFile(filelist, destination):
    """ Read each file in <filelist> and sort it. """
    try:
        for filename in filelist:
            with open(filename, 'r', encoding='utf-8') as fl:
                loadfile = json.load(fl)
                with open(os.path.join(destination, os.path.basename(filename)), 'w', encoding='utf-8') as fw:
                    fw.write(json.dumps(loadfile, indent=4, sort_keys=True))
                print(f'{filename} is sorted')
    except ValueError as e:
        print(f'Error : {e}\nDecoding JSON has failed, Please check {filename} if all expression closed.')        
     
if __name__ == '__main__' :
    # check the arguments
    args = checkArgs()
    if ( args == False):
        exit(0)

    # get epoch time
    epoch = time.time()

    # construct destination name
    destname="sortedfiles"
    destination = f'{destname}_{epoch}'

    # create destination
    sortedLocation(destination)

    filelist=[]
    if (args.path is not None):
        # get all json files in directory
        for file in os.listdir(args.path):
            if file.endswith(".json"):
                filelist.append((os.path.join(args.path, file)))

    if (args.file is not None):
        filelist.append(args.file)

    if (args.filelist is not None):
        with open(args.filelist, 'r') as fp:
            for filename in fp.readlines():
                filelist.append(filename.strip())

    # call sortJSONFile method with filelist and destination
    if sortJSONFile(filelist, destination):
        print(f'Sorted file destination at {destination}')
