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
        self.badCharacters = ['*','\\','/',':','<','>','?','|','"']
        self.undoDict = {}
        
    def appendFiles(self, path, stringToAppend):
        '''
        Append a string to the end of a file name
        '''    
        success = False
        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
            for fileNamePath in os.listdir(os.getcwd()):
                fileName, fileExt = os.path.splitext(fileNamePath)
                newFileName = fileName + stringToAppend
                result = self.moveFile(fileName, newFileName, fileExt)
                success = result or success
            return success

        else:
            fileName, fileExt = os.path.splitext(path)
            newFileName = fileName + stringToAppend
            return self.moveFile(fileName, newFileName, fileExt)
        return False
        
    def numberFiles(self, path, title, countStart):
        '''
        Number files in sequencial order
        '''
        success = False
        
        count = countStart
        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
            #Loop over the files in the working directory
            for fileName in os.listdir(os.getcwd()):
                if(os.path.isfile(fileName)):
                    countStr = ("_%03d" %count)
                    result = self.numberAFile(fileName, title, countStr)
                    count += 1
                    success = result or success
                    
            return success
        else:
            parent = os.path.abspath(os.path.join(path, os.pardir))
            os.chdir(parent)
            fileName = os.path.basename(path)
            return self.numberAFile(fileName, title, count)
            
        return False
                                
    def formatTV(self, path, title, season, episode):
        '''
        Number files in sequential TV order
        '''
        season = int(season)
        episode = int(episode)
        tvFormat = ("_S%02dE%02d" %(season, episode))
        
        success = False

        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
            #Loop over the files in the working directory
            for fileName in os.listdir(os.getcwd()):
                if(os.path.isfile(fileName)):
                    result = self.numberAFile(fileName, title, tvFormat)
                    episode += 1
                    tvFormat = ("_S%02dE%02d" %(season, episode))
                    success = result or result
            return success

        else:
            parent = os.path.abspath(os.path.join(path, os.pardir))
            os.chdir(parent)
            fileName = os.path.basename(path)
            return self.numberAFile(fileName, title, tvFormat)
        
        return False
          
    def numberAFile(self, path, title, count):
        '''
        Append a counter to the end of a file name
        '''
        fileName, fileExt = os.path.splitext(path)
        newFileName = title + str(count)
        if(fileName != newFileName):
            return self.moveFile(fileName, newFileName, fileExt)   
        return False
            
    def removeAndReplace(self, path, replace, replaceWith):
        '''
        Remove white space and replace
        '''
        success = False
        #if the directory given is valid then change it to that directory
        if os.path.isdir(path):
            os.chdir(path)
    
            #Loop over the files in the working directory
            for fileName in os.listdir(os.getcwd()):
                result = self.removeAndReplaceFromFile(fileName, replace, replaceWith)
                success = result or success
            return success
        else:
            fileName = os.path.basename(path)
            return self.removeAndReplaceFromFile(fileName, replace, replaceWith)
            
        return False
                
    def removeAndReplaceFromFile(self, path, replace, replaceWith):
        '''
        Remove white space from file
        '''
        if replace in self.badCharacters:
            return False
        if replaceWith in self.badCharacters:
            return False
        fileName, fileExt = os.path.splitext(path)
        newFileName = fileName.replace(replace, replaceWith)
        if(fileName != newFileName):
            return self.moveFile(fileName, newFileName, fileExt)
        return False
        
    
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
        
        try:
            #rename the files
            shutil.move(fileName, newFileName)
            self.undoDict[fileName] = newFileName
            return True
        except:
            return False
        
        return False
        
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
        
        