'''
Created on Dec 31, 2017

@author: joshu
'''
from tkinter import *
from tkinter import messagebox

def answer():
    messagebox.showerror("Answer", "Sorry, no answer available")

def callback():
    if messagebox.askyesno('Verify', 'Really quit?'):
        messagebox.showwarning('Yes', 'Not yet implemented')
    else:
        messagebox.showinfo('No', 'Quit has been cancelled')

Button(text='Quit', command=callback).pack(fill=X)
Button(text='Answer', command=answer).pack(fill=X)
mainloop()