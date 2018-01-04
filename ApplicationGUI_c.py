'''
Name: ApplicationGUI_c

Purpose: To provide a GUI for manipulating file names

Description: Change files names.

TO-DO:
-Add more Error feedback
-Add the ability to pre-pend numbers
-Convert tagConfig.txt to tagConfig.json
-Add the ability to rename the parent folder
-Add the ability for text substitution
-Add the ability to remove characters or words
-Append dates
-Create and output a change log

BUGS:
-Fix white space remover/undo bug
-Fix add tag such that it doesn't reenable all tags previously used

Created on Dec 26, 2017

@author: joshu
'''
import os
from FileRenamer_c import FileRenamer_c
import pyperclip 
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename  
from tkinter import messagebox 

class ApplicationGUI_c:

    def __init__(self, master):
        '''
        Initialize the GUI
        '''
        self.DEBUG = False
        
        self.TAG_FILE = os.path.join(os.getcwd(), "TagConfig.txt")
        self.TAG_SEPARATOR = "+"
        self.DISABLE_STATE = 'disabled'
        self.NORMAL_STATE = 'normal'
        self.START_STATE_STRING = "1"
        self.NUMBER_FILE_EXAMPLE = '<FileName>_001'
        self.TV_FORMAT_EXAMPLE = '<FileName>_S01E01'
        self.TAG_EXAMPLE = '<FileName>'
        self.PADX = 2
        self.PADY = 2
        
        self.cFileRenamer = FileRenamer_c() 
        
        self.mPath = ''
        self.mExample = ''
        self.mTagString =''
        self.mAddToTags = False
        
        master.title('File Renamer Tool')
        master.resizable(0,0)
        
        #create Frames
        self.mInputButtonFrame = Frame(master)
        self.mInputFrame = Frame(master)
        self.mCenterFrame = Frame(master)
        self.mLeftCenterFrame = Frame(self.mCenterFrame)
        self.mRightCenterFrame = Frame(self.mCenterFrame)
        self.mTagButtonFrame = Frame(master)
        self.mOutputFrame = Frame(master)
        
        # layout all of the main containers
        self.mInputFrame.grid_columnconfigure(1, weight=1)
        self.mOutputFrame.grid_columnconfigure(1, weight=1)
        
        self.mInputButtonFrame.grid(row=0, sticky="NWE")
        self.mInputFrame.grid(row=1, sticky="NWE")
        self.mCenterFrame.grid(row=2, sticky="NWE")
        self.mLeftCenterFrame.grid(row=0, column=0, sticky="NWE")
        self.mRightCenterFrame.grid(row=0, column=1, sticky="NWE")
        self.mTagButtonFrame.grid(row=4, column=0, columnspan=2, sticky="NSWE")
        self.mOutputFrame.grid(row=5, sticky="SWE")
        
        #create mInputButtonFrame buttons
        self.mFileOpenButton = Button(self.mInputButtonFrame, text='File Open', command=self.askFile)
        self.mFolderOpenButton = Button(self.mInputButtonFrame, text='Folder Open', command=self.askDirectory)
        self.mInputOpenButton = Button(self.mInputButtonFrame, text='Paste', command=self.useInputEntry)
        self.mErrorLabel = Label(self.mInputButtonFrame)
        
        #create mInputFrame buttons
        self.mInputLabel = Label(self.mInputFrame, text="Input:")
        self.mInputEntry = Entry(self.mInputFrame, width=80)
        self.mClearButton = Button(self.mInputFrame, text='Clear', command=self.clearInput, state=DISABLED)
            
        #create mLeftCenterFrame buttons
        #create radio buttons
        self.vAction = tk.IntVar()
        self.vAction.set(2)  # initializing the choice, i.e. Python
        actions = ["Number Files","Format TV","Tag"]
        self.mActionRadioButtons = {}
        for val, action in enumerate(actions):
            radioButton = Radiobutton(self.mLeftCenterFrame,
                          text=action,
                          padx = 20, 
                          variable=self.vAction, 
                          command=self.showChoice,
                          value=val,
                          state=DISABLED)
            self.mActionRadioButtons[action] = radioButton
            
        #create mRightCenterFrame buttons
        self.mStartLabel = Label(self.mRightCenterFrame, text="Start:")
        self.mStartEntry = Entry(self.mRightCenterFrame, width=3, justify=RIGHT, state=DISABLED)
        self.mSeasonLabel = Label(self.mRightCenterFrame, text="Season:")
        self.mSeasonEntry = Entry(self.mRightCenterFrame, width=3, justify=RIGHT, state=DISABLED)
        self.mEpisodeLabel = Label(self.mRightCenterFrame, text="Episode:")
        self.mEpisodeEntry = Entry(self.mRightCenterFrame, width=3, justify=RIGHT, state=DISABLED)
        self.mTagLabel = Label(self.mRightCenterFrame, text="Tag:")
        self.mTagEntry = Entry(self.mRightCenterFrame, justify=RIGHT, state=DISABLED)
        self.mAddTagButton = Button(self.mRightCenterFrame, text="Add", state=DISABLED, command=self.addTag)
        self.mRemoveTagButton = Button(self.mRightCenterFrame, text="Remove", state=DISABLED, command=self.removeTag)
        
        #create mTagButtonFrame buttons
        self.mTags = self.readTagFile()
        self.mTagButtons = []
        self.loadTagButtons(self.DISABLE_STATE)
        
        #create mOutputFrame buttons
        self.mOutputLabel = Label(self.mOutputFrame, text="Example:")
        self.mExampleLabel = Label(self.mOutputFrame, state=DISABLED, justify=LEFT, relief=SUNKEN)
        self.mCommitButton = Button(self.mOutputFrame, text='Commit', state=DISABLED, command=self.commit)
        self.mClearTagButton = Button(self.mOutputFrame, text='Clear Tags', state=DISABLED, command=self.clearOutputLabel)
        self.mRemoveSpaces = IntVar()
        self.mRemoveSpacesCheckBox = Checkbutton(self.mOutputFrame, text="Remove Spaces", state=DISABLED, variable=self.mRemoveSpaces)
        self.mOpenLocation = IntVar()
        self.mOpenLocationCheckBox = Checkbutton(self.mOutputFrame, text="Open after Commit", state=DISABLED, variable=self.mOpenLocation)
        self.mQuitButton = Button(self.mOutputFrame, text='Quit', command=master.quit)
        
        
        #layout for mInputButtonFrame
        self.mFileOpenButton.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        self.mFolderOpenButton.grid(row=0, column=1, padx=self.PADX, pady=self.PADY)
        self.mInputOpenButton.grid(row=0, column=2, padx=self.PADX, pady=self.PADY)
        self.mErrorLabel.grid(row=0, column=3, padx=self.PADX, pady=self.PADY)
        
        # layout for mInputFrame
        self.mInputLabel.grid(row=0, column=0, padx=self.PADX, pady=self.PADY)
        self.mInputEntry.grid(row=0, column=1, padx=self.PADX, pady=self.PADY, sticky="WE")
        self.mClearButton.grid(row=0, column=2, sticky= "E", padx=self.PADX, pady=self.PADY)
        
        # layout for mCenterFrame
        self.mCenterFrame.grid_rowconfigure(0, weight=1)
        self.mCenterFrame.grid_columnconfigure(1, weight=1)
        
        #layout for mRightCenterFrame
        rowCount = 0
        for key, button in self.mActionRadioButtons.items():
            button.grid(row=rowCount, column=0, sticky="W")
            rowCount += 1
        
        #layout for mRightCenterFrame
        self.mStartLabel.grid(row=0, column=0, sticky="W", padx=self.PADX, pady=self.PADY)
        self.mStartEntry.grid(row=0, column=1, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mSeasonLabel.grid(row=1, column=0, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mSeasonEntry.grid(row=1, column=1, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mEpisodeLabel.grid(row=1, column=2, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mEpisodeEntry.grid(row=1, column=3, sticky="W", padx=self.PADX, pady=self.PADY,)
        
        # layout for mTagFrame
        self.mTagLabel.grid(row=2, column=0, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mTagEntry.grid(row=2, column=1, columnspan= 3, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mAddTagButton.grid(row=2, column=4, sticky="WE", padx=self.PADX, pady=self.PADY,)
        self.mRemoveTagButton.grid(row=2, column=5, sticky="WE", padx=self.PADX, pady=self.PADY,)
        
        self.drawTagButtons()
        
        #layout for mOutputFrame
        self.mOutputLabel.grid(row=0, column=0, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mExampleLabel.grid(row=0, column=1, columnspan=3, sticky="WE", padx=self.PADX, pady=self.PADY)
        self.mCommitButton.grid(row=0, column=4, sticky="WE", padx=self.PADX, pady=self.PADY)
        
        self.mRemoveSpacesCheckBox.grid(row=1, column=1, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mOpenLocationCheckBox.grid(row=1, column=2, sticky="W", padx=self.PADX, pady=self.PADY,)
        self.mClearTagButton.grid(row=1, column=3, sticky="E", padx=self.PADX, pady=self.PADY)
        self.mQuitButton.grid(row=1, column=4, sticky="WE", padx=self.PADX, pady=self.PADY,)
            
    def askFile(self):
        '''
        Ask for a file 
        '''
        self.mPath=askopenfilename() 
        if(self.mPath != ''):
            self.enableEditing()
            if(self.DEBUG): print("askFile", self.mPath)
        
    def askDirectory(self):
        '''
        Ask for a directory
        '''
        self.mPath= askdirectory() 
        if(self.mPath != ''):
            self.enableEditing()
            if(self.DEBUG): print("askDirectory", self.mPath)
            
    def useInputEntry(self):
        '''
        Grab input from the clipboard
        '''
        #grab path from mInputEntry
        self.mPath = self.mInputEntry.get()
        #grab from clipboard
        if(self.mPath == ''):
            self.mPath = pyperclip.paste() 
        if(os.path.exists(self.mPath)):
            self.enableEditing()
            if(self.DEBUG): print("useInputEntry")
        else:
            error = "No such file " + "..\\" + os.path.basename(self.mPath)
            self.setErrorLabel(error)
            self.clearInput()
            self.clearOutputLabel()
            self.setStateOutputframe(self.DISABLE_STATE)
            
    def enableEditing(self):
        '''
        Enable the buttons
        '''
        self.mInputEntry.delete(0, END)
        self.mInputEntry.insert(0, self.mPath)
        self.setStateClearButton(self.NORMAL_STATE)
        self.setStateRadioButtons(self.NORMAL_STATE)
        self.setStateOutputframe(self.NORMAL_STATE)
        self.showChoice()
        self.clearTagString()
        self.clearErrorLabel()
             
    def commit(self):
        '''
        Perform the edit
        '''
        if(self.DEBUG): print('Commit')
        if messagebox.askyesno('Verify', 'Are you sure you want to Commit?'):
            action = self.vAction.get()
            
            if(self.mRemoveSpaces.get() == 1):
                #remove spaces
                self.cFileRenamer.removeWhiteSpace(self.mPath)
            
            if(action == 0):
                #number files
                start = int(self.mStartEntry.get())
                if(os.path.isdir(self.mPath)):
                    #folder
                    self.cFileRenamer.numberFiles(self.mPath, os.path.basename(self.mPath), start)
                else:
                    #file
                    title = os.path.abspath(os.path.join(self.mPath, os.pardir))
                    self.cFileRenamer.numberFiles(self.mPath,  os.path.basename(title), start)
            if(action == 1):
                #format TV
                season = self.mSeasonEntry.get()
                episode = self.mEpisodeEntry.get()
                if(os.path.isdir(self.mPath)):
                    #folder
                    self.cFileRenamer.formatTV(self.mPath, os.path.basename(self.mPath), season, episode)
                else:
                    #file
                    title = os.path.abspath(os.path.join(self.mPath, os.pardir))
                    self.cFileRenamer.formatTV(self.mPath,  os.path.basename(title), season, episode)
            if(action == 2):
                #add Tags
                if(self.mAddToTags):
                    self.cFileRenamer.appendFiles(self.mPath, self.mTagString)
                    self.mAddToTags = False
                    
            if(self.mOpenLocation.get() == 1):
                #open location after commit
                if(os.path.isdir(self.mPath)):
                    os.startfile(self.mPath)
                else:
                    os.startfile( os.path.abspath(os.path.join(self.mPath, os.pardir)))
            
            #ask for an undo
            if messagebox.askyesno('Verify', 'Would you like to undo?'):
                self.cFileRenamer.undoFileChanges()
            
            self.cFileRenamer.clearUndoDict()
            self.clearInput()
            self.clearOutputLabel()
            self.setStateOutputframe(self.DISABLE_STATE)   
    
    def showChoice(self):
        '''
        Enable the relavent buttons based on the radio button selection
        '''
        if(self.DEBUG): print("showChoice")
        action = self.vAction.get()
#         print(action)
        if(action == 0):
            self.setStateNumberFiles(self.NORMAL_STATE)
            self.setStateFormatTV(self.DISABLE_STATE)
            self.setStateTag(self.DISABLE_STATE)
            self.setStateTagButtons(self.DISABLE_STATE)
            self.clearTagString()
            self.setOutputLabel(self.NUMBER_FILE_EXAMPLE)
        if(action == 1):
            self.setStateNumberFiles(self.DISABLE_STATE)
            self.setStateFormatTV(self.NORMAL_STATE)
            self.setStateTag(self.DISABLE_STATE)
            self.setStateTagButtons(self.DISABLE_STATE)
            self.clearTagString()
            self.setOutputLabel(self.TV_FORMAT_EXAMPLE)
        if(action == 2):
            self.setStateNumberFiles(self.DISABLE_STATE)
            self.setStateFormatTV(self.DISABLE_STATE)
            self.setStateTag(self.NORMAL_STATE)
            self.setStateTagButtons(self.NORMAL_STATE)
            self.setOutputLabel(self.TAG_EXAMPLE)
    
    def clearInput(self):
        '''
        Clear the input and disable all edit buttons
        '''
        if(self.DEBUG): print('clearInput')
        self.mPath = ''
        self.mTagString = ''
        self.mInputEntry.delete(0, END)
        self.mClearButton['state'] = self.DISABLE_STATE
        self.setStateRadioButtons(self.DISABLE_STATE)
        self.setStateOutputframe(self.DISABLE_STATE)
        
    def clearErrorLabel(self):
        '''
        clear the error label
        '''
        self.mErrorLabel['text'] = ''
        
    def setErrorLabel(self, error):
        '''
        set the error label
        '''
        self.mErrorLabel['text'] = "Error: " + error
            
    def setStateClearButton(self, state):
        '''
        Set the state of the clear button
        '''
        if(self.DEBUG): print("setStateClearButton")
        self.mClearButton['state'] = state
        
    def setStateNumberFiles(self, state):
        '''
        Set the state of the number files button
        '''
        if(self.DEBUG): print("setStateNumberFiles")
        if(state==self.DISABLE_STATE):
            self.mStartEntry.delete(0, END)
            
        self.mStartEntry['state'] = state
        
        if(state==self.NORMAL_STATE):
            self.mStartEntry.delete(0, END)
            self.mStartEntry.insert(END, self.START_STATE_STRING)
        
    def setStateFormatTV(self, state):
        '''
        Set the state of the format TV button
        '''
        if(self.DEBUG): print("setStateFormatTV")
        if(state==self.DISABLE_STATE):
            self.mSeasonEntry.delete(0, END)
            self.mEpisodeEntry.delete(0, END)
            
        self.mSeasonEntry['state'] = state
        self.mEpisodeEntry['state'] = state
        
        if(state==self.NORMAL_STATE):
            self.mSeasonEntry.delete(0, END)
            self.mSeasonEntry.insert(END, self.START_STATE_STRING)
            self.mEpisodeEntry.delete(0, END)
            self.mEpisodeEntry.insert(END, self.START_STATE_STRING)

    def setStateRadioButtons(self, state):
        '''
        Set the state of the Radio buttons
        '''
        if(self.DEBUG): print("setStateRadioButtons")
        for key, button in self.mActionRadioButtons.items():
            button['state'] = state
        self.vAction.set(2)
        self.setStateNumberFiles(state)
        if(state==self.DISABLE_STATE):
            self.setStateFormatTV(state)
            self.setStateTag(state)
            self.setStateTagButtons(state)
    
    def setStateTag(self, state):
        '''
        Set the state of the tag line buttons
        '''
        if(self.DEBUG): print("setStateTag")
        self.mTagEntry['state'] = state
        self.mAddTagButton['state'] = state
        self.mRemoveTagButton['state'] = state
        
    def setStateTagButtons(self, state):
        '''
        Set the state of all the tag buttons
        '''
        if(self.DEBUG): print("setStateTagButtons")
        for (tag, button) in self.mTagButtons:
            button['state'] = state  
            
    def setStateOutputframe(self, state):
        '''
        Set the state of the output frame
        '''
        if(self.DEBUG): print("setStateOutputframe")
        if(state==self.DISABLE_STATE):
            self.mExampleLabel['text'] = ''
        self.mExampleLabel['state'] = state
        self.mCommitButton['state'] = state
#         self.mClearTagButton['state'] = state
        self.setStateTagButtons(state)
        self.mRemoveSpacesCheckBox['state'] = state
        self.mOpenLocationCheckBox['state'] = state     

    def clearTagString(self):
        '''
        Clear the Tag String
        '''
        if(self.DEBUG): print("clearTagString")
        self.mAddToTags = False
        self.mTagString = ''
        self.mClearTagButton['state'] = self.DISABLE_STATE
        self.loadTagButtons(self.NORMAL_STATE)
        self.drawTagButtons()
           
    def setOutputLabel(self, string):
        '''
        Set the output label
        '''
        if(self.DEBUG): print("setOutputLabel:", string)
        self.mExample = string
        self.mExampleLabel['text'] = self.mExample
        
    def addToOutputLabel(self, stringToAdd):
        '''
        Append a string to the output label
        '''
        if(self.DEBUG): print("addToOutputLabel")
        newExample = self.mExample + stringToAdd
        self.setOutputLabel(newExample)

    def clearOutputLabel(self):
        '''
        Clear the output label
        '''
        if(self.DEBUG): print('Clear Output')
        self.clearTagString()
        self.setOutputLabel(self.TAG_EXAMPLE)
     
    def callback(self,i): 
        '''
        Call back for dertermining which tag button has been clicked
        This is the callback factory. Calling it returns a function.
        '''
        def _callback():
            self.mAddToTags = True
            self.mClearTagButton['state'] = self.NORMAL_STATE
            self.mTagButtons[i][1]['state'] = self.DISABLE_STATE
            tag = self.mTags[i]
            self.mTagString += self.TAG_SEPARATOR + tag
            example = self.TAG_EXAMPLE + self.mTagString
            self.setOutputLabel(example)
        return _callback   
        
    def loadTagButtons(self, state):
        '''
        Load tag Buttons
        '''
        if(self.DEBUG): print('loadTagButtons')
        self.mTagButtons.clear()
        for i, tag in enumerate(self.mTags):
            tagButton = Button(self.mTagButtonFrame, 
                               text=tag, 
                               width=10,  
                               command=self.callback(i),
                               state=state)
            self.mTagButtons.append(tuple((tag, tagButton)))
            
    def drawTagButtons(self):
        '''
        Draw the tag buttons on the GUI
        '''
        if(self.DEBUG): print("drawTagButtons")
        rowCount = 1
        colCount = 0
        for (tag, button) in self.mTagButtons:
            button.grid(row=rowCount, column=colCount, padx=self.PADX, pady=self.PADY, sticky="W")
            colCount +=1
            if(colCount == 6):
                colCount = 0
                rowCount +=1
                
    def addTag(self):
        '''
        Add a tag button
        '''
        if(self.DEBUG): print('Add Tag')
                
        add = False
        tempTag = self.mTagEntry.get()
        
        #iterate over list until the proper place is determined
        if(tempTag != ""):
            if(not self.mTags):
                #if the list is empty
                self.mTags.append(tempTag)
                add = True
            for i in range(len(self.mTags)):
                if(tempTag == self.mTags[i]):
                    #if the list contains the item
                    break
                if(tempTag < self.mTags[i]):
                    if(i == 0):
                        #if the tempTag is the new first item
                        self.mTags.insert(0, tempTag)
                    else:
                        self.mTags.insert(i, tempTag)
                    add = True
                    break
                if(i >= len(self.mTags)-1):
                    #if tempTag goes at the end
                    self.mTags.append(tempTag)
                    add = True
            if(add):
                self.loadTagButtons(self.NORMAL_STATE)
                self.drawTagButtons()
                self.writeTagFile()
        
    def removeTag(self):
        '''
        Remove a tag button
        '''
        if(self.DEBUG): print('Remove tag')
        tag = self.mTagEntry.get()
        if(tag != ""):
            for (tagKey, button) in self.mTagButtons:
                if(tagKey == tag):
                    button.destroy()
                    self.mTags.remove(tag)
                    self.mTagButtons.remove(tuple((tagKey, button)))
                    self.drawTagButtons()
                    self.writeTagFile()
                    break
                
    def removeSpaces(self):
        '''
        Remove Spaces from the file name
        '''
        if(self.DEBUG): print('Remove Spaces')
        self.mRemoveSpaces = True
        self.mExample = self.mExample.replace(' ', self.cFileRenamer.SPACE_REPLACEMENT)
        self.mExampleLabel['text'] = self.mExample
            
    def readTagFile(self):
        '''
        Read in the tag file
        '''
        if(self.DEBUG): print("readTagFile")
        tags = []
        if(os.path.exists(self.TAG_FILE)):
            with open(self.TAG_FILE) as f:
                for line in f:
                    line = line.rstrip('\n')
                    tags.append(line)
            f.closed
            tags.sort()
        return tags
    
    def writeTagFile(self):
        '''
        Write the tags to file
        '''
        if(self.DEBUG): print("writeTagFile")
        f = open(self.TAG_FILE, 'w')
        for (tagKey, button) in self.mTagButtons:
            f.write(tagKey + '\n')
        f.closed

        
root = Tk()
my_gui = ApplicationGUI_c(root)
root.mainloop()

