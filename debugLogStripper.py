#!user/bin/env python 3
#command line tool for parsing debug logs
#by Zach Palmer

import os
from DebugFile import DebugFile
from datetime import datetime
print('****DEBUG LOG STRIPPER****')
print('Seperate out lines from debug logs based on a demiliter')
print('defaults to filtering out lines such as manage pkg, var assigments, and statement execution lines.')
print('Add custom delimiters by adding delimiters seperated by commas when promoted.')
print('--------------------------------------------------------')


def main():
    try:

        fileName = getFile()
        while fileName != "":
            debugLog = DebugFile(fileName)
            if debugLog.getErrorMsg() != "":
                print(f"Debug File Error: {debugLog.getErrorMsg()}")
            else:
                delims = getDelims()
                filteredFileLines = debugLog.filterFile(delims)
                if len(filteredFileLines) > 0:
                    print('file was successfully filterd')
                    writeNewFile(filteredFileLines)
                else:
                    print('supplied file did not contain any delimiters to filter')
            fileName = getFile()
                        
    except RuntimeError as e:
        print(f'an error occurred while reading file please verify filepath is correct and retry: [{e}]')
             

def getDelims():
    delimiters = [
        'ENTERING_MANAGED_PKG',
        'STATEMENT_EXECUTE',
        'HEAP_ALLOCATE',
        'CUMULATIVE_LIMIT_USAGE',
        'CUMULATIVE_PROFILING',
        'VARIABLE_ASSIGNMENT',
        'LIMIT_USAGE_FOR'
    ]
    delims = []
    customDelimiters = input('Enter in custom delimiters seperated by commas (to use default enter none): ')
    if customDelimiters.lower() is not 'none':
        customDelims = customDelimiters.split(',')
        if len(customDelims) > 0:
            delims = [x for y in [delimiters, customDelims] for x in y]
        else:
            delims = delimiters
    return delims


def getFile():
    choice = ""
    while choice.lower() != 'q' and choice.lower() != 's':
        #get current working directory
        cwd = os.getcwd()
        print('Enter action (F, T, C, S, Q):')
        choice = str(input("Actions: show all <F>iles, <T>ext files, <C>hange directory, <S>elect file, <Q>uit: "))
        if choice.lower() == 'c':
            dirName = str(input("<..> for parent or new directory name: "))
            if dirName.lower() != "":
                try:
                    os.chdir(dirName)
                except Exception as e:
                    print(f"CD:Error: {e}")
            else:
                print("No directory entered")
        elif choice.lower() == 'f' or choice.lower() == 't':
            for entry in os.listdir(cwd):
                fullpath = os.path.join(cwd, entry)
                if choice.lower() == 'f' and os.path.isfile(fullpath):
                    print(f"File: {entry}")
                elif choice.lower() == 't' and os.path.isfile(fullpath) and entry.endswith('.txt'):
                    print(f"Text File: {entry}")
        elif choice.lower() == 's':
            fileName = str(input("Enter file name (with extension): "))
            #verify input is file
            fullpath = os.path.join(cwd, fileName)
            if not os.path.isfile(fullpath):
                print('Entered name is not a file')
                choice = ""
        elif choice.lower() == 'q':
            print('quiting...')
            return ""
        else:
            print('Error unrecognized command')
            print()

    return fullpath


def writeNewFile(lines):
    currDate = datetime.now()
    print('creating new file...')
    print()
    try:
        nf = open(f'fltDebug_{currDate.month}_{currDate.day}_{currDate.microsecond}', 'a')
        for line in lines:
            nf.write(line)
            #write empty line for formatting
            nf.write('\n')
        nf.close()
        print('file created successfully and is avaialbe in current directory.')
    except Exception as e:
        print(f"An error occurred while writing file: {e}")


if __name__ == '__main__':
    main()
            
