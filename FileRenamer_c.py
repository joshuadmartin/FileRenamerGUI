'''
Created on Dec 30, 2017

@author: joshu
'''

import shutil, os, sys

class FileRenamer_c(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.SPACE_REPLACEMENT = "_"
        self.undoDict = {}
        
    def appendFiles(self, path, stringToAppend):
        '''
        Append a string to the end of a file name
        '''      
        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
            for fileNamePath in os.listdir(os.getcwd()):
                fileName, fileExt = os.path.splitext(fileNamePath)
                newFileName = fileName + stringToAppend
                self.moveFile(fileName, newFileName, fileExt)

        else:
            fileName, fileExt = os.path.splitext(path)
            newFileName = fileName + stringToAppend
            self.moveFile(fileName, newFileName, fileExt)
        
        
    def numberFiles(self, path, title, countStart):
        '''
        Number files in sequencial order
        '''
        count = countStart
        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
            #Loop over the files in the working directory
            for fileName in os.listdir(os.getcwd()):
                if(os.path.isfile(fileName)):
                    countStr = ("%03d" %count)
                    self.numberAFile(fileName, title, countStr)
                    count += 1
        else:
            parent = os.path.abspath(os.path.join(path, os.pardir))
            os.chdir(parent)
            fileName = os.path.basename(path)
            self.numberAFile(fileName, title, count)
                                
    def formatTV(self, path, title, season, episode):
        '''
        Number files in sequential TV order
        '''
        season = int(season)
        episode = int(episode)
        tvFormat = ("S%02dE%02d" %(season, episode))

        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
            #Loop over the files in the working directory
            for fileName in os.listdir(os.getcwd()):
                if(os.path.isfile(fileName)):
                    self.numberAFile(fileName, title, tvFormat)
                    episode += 1
                    tvFormat = ("S%02dE%02d" %(season, episode))

        else:
            parent = os.path.abspath(os.path.join(path, os.pardir))
            os.chdir(parent)
            fileName = os.path.basename(path)
            self.numberAFile(fileName, title, tvFormat)
          
    def numberAFile(self, path, title, count):
        '''
        Append a counter to the end of a file name
        '''
        fileName, fileExt = os.path.splitext(path)
        newFileName = title + self.SPACE_REPLACEMENT + str(count)
        if(fileName != newFileName):
            self.moveFile(fileName, newFileName, fileExt)   
            
    def removeWhiteSpace(self, path):
        '''
        Remove white space from a path
        '''
        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
    
            #Loop over the files in the working directory
            for fileName in os.listdir(os.getcwd()):
                self.removeWhiteSpaceFromFile(fileName)
    
        else:
            fileName = os.path.basename(path)
            self.removeWhiteSpaceFromFile(fileName)
                
    def removeWhiteSpaceFromFile(self, path):
        '''
        Remove white space from file
        '''
        fileName, fileExt = os.path.splitext(path)
        newFileName = fileName.replace(' ', self.SPACE_REPLACEMENT)
        if(fileName != newFileName):
            self.moveFile(fileName, newFileName, fileExt)
        
    
    def moveFile(self, fileName, newFileName, fileExt):   
        '''
        Move a file to a new file name
        '''
        #get the full path names
        absWorkingDir = os.path.abspath('.')
        fileName = os.path.join(absWorkingDir, (fileName + fileExt))
        newFileName = os.path.join(absWorkingDir, (newFileName + fileExt))
        
        if(os.path.exists(newFileName)):
            exists = True
            count = 1
            while(exists):
                filepath, fileExt = os.path.splitext(newFileName)
                tempFileName = filepath + "_(" + str(count) +")" + fileExt
                if(os.path.exists(tempFileName)):
                    count += 1
                else:
                    newFileName = tempFileName
                    exists = False
                    
#         print("filename: " + fileName)
#         print("newFileName: " + newFileName)

        #rename the files
        shutil.move(fileName, newFileName)
        self.undoDict[fileName] = newFileName
        
    def printUndoDict(self):
        '''
        Print out the files in the undo dictionary
        '''
        for fileName, newFileName in self.undoDict.items():
            print("file: " + fileName)
            print("new: " + newFileName)
            
    def undoFileChanges(self):
        '''
        Undo the file changes previous done
        '''
        for fileName, newFileName in self.undoDict.items():
#             print("Moving: " + newFileName + " to " + fileName)
            shutil.move(newFileName, fileName)
        self.clearUndoDict()
        
    def clearUndoDict(self):
        '''
        Clear out the undo dictionary
        '''
        self.undoDict.clear()
        
        