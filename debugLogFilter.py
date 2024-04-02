#!user/bin/env python 3
#command line tool for parsing debug logs
#by Zach Palmer

import os
from DebugFile import DebugFile
from datetime import datetime
print()
print('****DEBUG LOG Filterer****')
print('Seperate out lines from debug logs based on a demiliter')
print('defaults to filtering out lines such as manage pkg, var assigments, and statement execution lines.')
print('Add custom delimiters by adding delimiters seperated by commas when promoted.')
print('---------------------------------------------------------------------------------------------------')


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
        'USER_INFO',
        'HEAP_ALLOCATE',
        'CUMULATIVE_LIMIT_USAGE',
        'CUMULATIVE_PROFILING',
        'VARIABLE_ASSIGNMENT',
        'LIMIT_USAGE_FOR'
    ]
    delims = []
    customDelimiters = input('Enter in custom delimiters seperated by commas (to use default enter none): ')
    if customDelimiters.lower() != 'none':
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
        print(f"\nCurrent Direcotry: {cwd}")
        print()
        print('Enter action (F, T, D, L, C, S, Q):')
        choice = str(input("Actions: show all <F>iles, <T>ext files, <D>irectories, <L>ist Contents, <C>hange directory, <S>elect file, <Q>uit: "))
        if choice.lower() == 'c':
            dirName = str(input("\nEnter <..> for parent directory or enter new directory name: "))
            if dirName != "":
                try:
                    os.chdir(dirName)
                    print(f"Current Directory changed to: {os.getcwd()}")
                    print('--------------------------------------------')
                except Exception as e:
                    print(f"CD:Error: {e}")
            else:
                print("No directory entered")
        elif choice.lower() == 'f' or choice.lower() == 't' or choice.lower() == 'd' or choice.lower() == 'l':
            ftypes = {'f': 'Files', 't': 'Txt Files', 'd': 'Directories'}
            dirItems = os.listdir(cwd)
            totalItemCount = len(dirItems)
            itemCount = 0
            print()
            for entry in dirItems:
                fullpath = os.path.join(cwd, entry)
                if choice.lower() == 'f' and os.path.isfile(fullpath):
                    print(f"--File: {entry}")
                    itemCount += 1
                elif choice.lower() == 't' and os.path.isfile(fullpath) and entry.endswith('.txt'):
                    print(f"--Txt File: {entry}")
                    itemCount += 1
                elif choice.lower() == 'd' and os.path.isdir(fullpath):
                    print(f"--Dir: {entry}")
                    itemCount += 1
                elif choice.lower() == 'l':
                    print(f"--item: {entry}")
                    itemCount += 1
            if totalItemCount == 0:
                print("No items found")
            elif itemCount == 0:
                print(f"{cwd} does not contain any {ftypes[choice.lower()]}")
            elif totalItemCount != 0 and itemCount != 0:
                print(f"{totalItemCount} item(s) found" if choice.lower() == 'l' else f"{itemCount} {ftypes[choice.lower()]} found")
            print('-------------------------')
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
            
