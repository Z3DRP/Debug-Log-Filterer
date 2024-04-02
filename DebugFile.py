#by zach palmer
import os

class DebugFile:
    def __init__(self, path):
        self.setFile(path)
        self._error = ""
        self._lines = []
        self._lineCount = 0
        self._filteredLines = []
        self._filteredLineCount = 0
        try:
            print('opening file...')
            file = open(path, 'r')
            EOF = False
            print('reading file...')
            while not EOF:
                currentLine = file.readline()
                if currentLine != "":
                    self._lines.append(currentLine)
                    self._lineCount += 1
                else:
                    EOF = True
            file.close()
        except OSError as e:
            self._error = f"DBE: {e}"

    def setFile(self, path):
        self._Path = path

    def getFile(self):
        return self._Path

    def getErrorMsg(self):
        return self._error

    def getFileLineCount(self):
        return self._lineCount

    def getFileLines(self):
        return self._lines

    def filterFile(self, delims):
        print(f"delims: {delims}")
        try:
            print('filtering file...')
            for line in self._lines:
                lineHasDelims = any(ele in line for ele in delims)
                if not lineHasDelims:
                    self._filteredLines.append(line)
        except Exception:
            raise Exception('An unexpected error occurred while filtering file.')
        return self._filteredLines

    def getFilteredFileLines(self):
        return self._filteredLines

    def getFilteredFileLineCount(self):
        return self._filteredLineCount
