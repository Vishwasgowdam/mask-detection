

# import the necessary packages


from tkinter import *
from tkinter.ttk import *
from PIL import  ImageTk, Image
import tkinter
import os
from tkinter import messagebox



def Ok():
    uname = e1.get()
    password = e2.get()
 
    if(uname == "" and password == "") :
        messagebox.showinfo("", "Blank Not allowed")
 
 
    elif(uname == "admin" and password == "123"):
 
        messagebox.showinfo("","Login Success")
        root.destroy()
        window=Tk()
        window.title("welcome admin")
        window.geometry("300x200")

        def live_cam():
            pass
        Label(window, text="camera feed").place(x=10, y=10)
        #Button(window, text="start", command= live_cam,height = 1, width = 13).place(x=180, y=10)
        btn2 = Button(root, text='camera feed', style='W.TButton', command=Ok)
        btn2.place(x=180, y=10)


        Label(window, text="mask detection").place(x=10, y=40)
        #Button(window, text="start", command= detect,height = 1, width = 13).place(x=180, y=40)
        btn2 = Button(root, text='Mask Deetection', style='W.TButton', command=Ok)
        btn2.place(x=180, y=40)


        window.mainloop()
 
    else :
        messagebox.showinfo("","Incorrent Username and Password")
 
 
root = Tk()
root.title("mask detector Login")
root.geometry("600x400")
global e1
global e2
 
Label(root, text="UserName").place(x=10, y=10)
Label(root, text="Password").place(x=10, y=40)
 
e1 = Entry(root)
e1.place(x=140, y=10)
 
e2 = Entry(root)
e2.place(x=140, y=40)
e2.config(show="*")
 
btn1 = Button(root, text='Login',style='W.TButton',command=Ok)
btn1.place(x=150,y=180)
#Button(root, text="Login", command=Ok , height = 3, width = 13).place(x=10, y=100)
 
root.mainloop()                     