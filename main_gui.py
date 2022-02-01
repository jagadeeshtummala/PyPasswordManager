import tkinter as tk
import sys,os
from hashlib import sha256
from passHandling_gui import *

def genHash(secret_key):
    hash = sha256(secret_key.encode()).hexdigest()
    return hash[1::2]+hash[::2]
def Clear():
    for widget in main_window.winfo_children():
        widget.destroy()
    #main_window.destroy()
def Clear_Exit():
    for widget in main_window.winfo_children():
        widget.destroy()
    sys.exit()
def retriveAppPassword():
    register_pass=tk.StringVar()
    appname = menu.get()
    Clear()
    retrived_password = getPasswordbyApp(appname,password)
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text=appname+" Password is:",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    tk.Entry(main_window,textvariable=register_pass,width=50, borderwidth=10).pack(padx=(20,20))
    register_pass.set(retrived_password)
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Continue",command=searchByApp,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
def displayPasswords(pass_list):
    frame = tk.Frame(main_window)
    frame.pack()
    tk.Label(frame,text="App Name",font=('bold')).grid(row=0,column=0,padx=(10,10))
    tk.Label(frame,text="User Name",font=('bold')).grid(row=0,column=1,padx=(10,10))
    tk.Label(frame,text="Email Id",font=('bold')).grid(row=0,column=2,padx=(10,10))
    tk.Label(frame,text="Password",font=('bold')).grid(row=0,column=3,padx=(10,10))
    tk.Label(frame,text="WebLink",font=('bold')).grid(row=0,column=4,padx=(10,10))
    for i in range(len(pass_list)):
        text = tk.Entry(frame,width=30, borderwidth=2)
        text.insert(0,pass_list[i][0])
        text.grid(row=i+1,column=0,padx=(10,10),pady=(5,5))
        text = tk.Entry(frame,width=30, borderwidth=2)
        text.insert(0,pass_list[i][1])
        text.grid(row=i+1,column=1,padx=(10,10),pady=(5,5))
        text = tk.Entry(frame,width=35, borderwidth=2)
        text.insert(0,pass_list[i][2])
        text.grid(row=i+1,column=2,padx=(10,10),pady=(5,5))
        text = tk.Entry(frame,width=30, borderwidth=2)
        text.insert(0,pass_list[i][3])
        text.grid(row=i+1,column=3,padx=(10,10),pady=(5,5))
        text = tk.Entry(frame,width=30, borderwidth=2)
        text.insert(0,pass_list[i][4])
        text.grid(row=i+1,column=4,padx=(10,10),pady=(5,5))

def retriveAllPasswords():
    Clear()
    pass_list = getAllPasswords(password)
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="All Stored Passwords!",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    displayPasswords(pass_list)
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Continue",command=retrivePassword_gui,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()

def retriveEmailPassword():
    emailId = menu.get()
    Clear()
    pass_list = getPasswordbyEmail(emailId.rstrip('\x00'),password.strip())
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Passwords Related to "+emailId,font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    displayPasswords(pass_list)
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Continue",command=searchByEmail,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
def generateRandomPassword():
    length=int(passLen.get())
    alphabetSelect = alphabets.get();capsSelect=caps.get();numberSelect=number.get();specialSelect=specialChar.get();puncSelect=punctuationChar.get()
    gen_password=RandomPasswordGenerator(length,alphabetSelect,capsSelect,numberSelect,specialSelect,puncSelect)
    autoGenerated.set(gen_password)

def displayOptionsAfterPasswordSave(savedPassword):
    Clear()
    saved_pass = tk.StringVar()
    saved_pass.set(savedPassword)
    tk.Label(main_window,text="").pack()
    frame = tk.Frame(main_window);frame.pack()
    tk.Label(frame,text="EmailId: ",font=('bold')).grid(row=0,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=emailIdInput,width=50, borderwidth=10).grid(row=0,column=1,padx=(10,20))
    tk.Label(frame,text="AppName: ",font=('bold')).grid(row=1,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=appNameInput,width=50, borderwidth=10).grid(row=1,column=1,padx=(10,20))
    tk.Label(frame,text="Paswword: ",font=('bold')).grid(row=2,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=saved_pass,width=50, borderwidth=10).grid(row=2,column=1,padx=(10,20))
    tk.Label(main_window,text="").pack()
    frame = tk.Frame(main_window);frame.pack()
    tk.Button(frame,text="Save New Password",command=saveNewPassword_gui,fg="white",bg="green",font=("bold")).grid(row=3,column=0,padx=(20,10))
    tk.Button(frame,text="Retrive a Password",command=retrivePassword_gui,fg="white",bg="green",font=("bold")).grid(row=3,column=1,padx=(10,20))
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Quit",command=Clear_Exit,fg="white",bg="red",font=("bold")).pack()

def saveGeneratedPassword():
    writeGeneratedPass(appName,userName,emailId,autoGenerated.get(),weblink,password)
    displayOptionsAfterPasswordSave(autoGenerated.get())

def saveManualPassword():
    if manualPass.get()=='':
        tk.Label(main_window,text="Manual Password Empty!",font=('bold'),fg='red').pack(padx=(10,10))
    else:
        writeGeneratedPass(appName,userName,emailId,manualPass.get(),weblink,password)
        displayOptionsAfterPasswordSave(manualPass.get())

def generatePasswordOption():
    Clear()
    global alphabets,caps,number,specialChar,punctuationChar,autoGenerated,passLen;
    autoGenerated = tk.StringVar();passLen = tk.StringVar();
    alphabets = tk.IntVar();alphabets.set(1);caps = tk.IntVar();caps.set(1);number=tk.IntVar();number.set(1);
    specialChar = tk.IntVar();specialChar.set(1);punctuationChar = tk.IntVar();#punctuationChar.set(1);
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Select Options for Password Creation",font=('bold')).pack(padx=(10,10))
    tk.Checkbutton(main_window, text = "Alphabet(a-z)", variable = alphabets,onvalue = 1, offvalue = 0).pack(anchor="w",padx=(30,10),pady=(5,0))
    tk.Checkbutton(main_window, text = "Cap-Alphabet(A-Z)", variable = caps,onvalue = 1, offvalue = 0).pack(anchor="w",padx=(30,10),pady=(5,0))
    tk.Checkbutton(main_window, text = "Numbers", variable = number,onvalue = 1, offvalue = 0).pack(anchor="w",padx=(30,10),pady=(5,0))
    tk.Checkbutton(main_window, text = "Special Characters(!@#$%^&*()?<>[]_~/:;*^)", variable = specialChar,onvalue = 1, offvalue = 0).pack(anchor="w",padx=(30,10),pady=(5,0))
    tk.Checkbutton(main_window, text = "Punctuation Characters(.'+-`{+})", variable = punctuationChar,onvalue = 1, offvalue = 0).pack(anchor="w",padx=(30,10),pady=(5,0))
    tk.Label(main_window,text="").pack()
    frame = tk.Frame(main_window);frame.pack();
    tk.Label(frame,text="Length of Password >8 (default 15)",font=('bold')).grid(row=0,column=0,padx=(10,10))
    tk.OptionMenu(frame,passLen,*[9,10,11,12,13,14,15,16,17,18,19,20]).grid(row=0,column=1,padx=(5,10))
    passLen.set(15)
    tk.Label(main_window,text="").pack()
    tk.Entry(main_window,textvariable=autoGenerated,width=50, borderwidth=10).pack(padx=(10,20))
    tk.Label(main_window,text="").pack()
    frame = tk.Frame(main_window);frame.pack()
    tk.Button(frame,text="Generate",command=generateRandomPassword,fg="white",bg="green",font=("bold")).grid(row=3,column=0,padx=(20,10))
    tk.Button(frame,text="Save Password",command=saveGeneratedPassword,fg="white",bg="green",font=("bold")).grid(row=3,column=1,padx=(10,20))
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Back",command=savePasswordOptions,fg="white",bg="red",font=("bold")).pack()
    tk.Label(main_window,text="").pack()

def savePasswordOptions():
    global manualPass,appName,userName,emailId,weblink
    manualPass = tk.StringVar()
    if appNameInput.get()=='' or userNameInput.get()=='' or emailIdInput.get()=='' or weblinkInput.get()=='':
        tk.Label(main_window,text="Enter values for all fields!",font=('bold'),fg='red').pack(padx=(10,10))
    else:
        appName = appNameInput.get();userName = userNameInput.get();emailId=emailIdInput.get();weblink=weblinkInput.get();
        Clear()  
        tk.Label(main_window,text="").pack()
        tk.Label(main_window,text="Save a manual password or Auto Suggest",font=('bold')).pack(padx=(10,10))
        tk.Label(main_window,text="").pack()
        frame = tk.Frame(main_window)
        frame.pack()
        tk.Label(frame,text="Enter Manual Password: ",font=('bold')).grid(row=0,column=0,padx=(10,10))
        tk.Entry(frame,textvariable=manualPass,width=50, borderwidth=10).grid(row=0,column=1,padx=(10,20),pady=(10,10))
        tk.Label(frame,text="").grid(row=1,column=0)
        #Write for manual password save later
        tk.Button(frame,text="Save Manual Password",command=saveManualPassword,fg="white",bg="green",font=("bold")).grid(row=2,column=0,padx=(20,10))
        tk.Button(frame,text="Generate Random Password",command=generatePasswordOption,fg="white",bg="green",font=("bold")).grid(row=2,column=1,padx=(10,20))
        tk.Label(main_window,text="").pack()
        tk.Button(main_window,text="Back",command=saveNewPassword_gui,fg="white",bg="red",font=("bold")).pack()
        tk.Label(main_window,text="").pack()
       
# Need to copmplete save passworxd function afte rretrive 
def saveNewPassword_gui():
    Clear()
    global appNameInput;global userNameInput;global emailIdInput;global weblinkInput;
    appNameInput = tk.StringVar();userNameInput = tk.StringVar();emailIdInput = tk.StringVar();weblinkInput = tk.StringVar()
    appNameInput.set("");userNameInput.set("");emailIdInput.set("");weblinkInput.set("")
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Enter Details to Save Password",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    frame = tk.Frame(main_window)
    frame.pack()
    tk.Label(frame,text="AppName: ",font=('bold')).grid(row=0,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=appNameInput,width=50, borderwidth=10).grid(row=0,column=1,padx=(10,20),pady=(10,10))
    tk.Label(frame,text="UserName: ",font=('bold')).grid(row=1,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=userNameInput,width=50, borderwidth=10).grid(row=1,column=1,padx=(10,20),pady=(10,10))
    tk.Label(frame,text="EmailId: ",font=('bold')).grid(row=2,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=emailIdInput,width=50, borderwidth=10).grid(row=2,column=1,padx=(10,20),pady=(10,10))
    tk.Label(frame,text="WebLink: ",font=('bold')).grid(row=3,column=0,padx=(10,10))
    tk.Entry(frame,textvariable=weblinkInput,width=50, borderwidth=10).grid(row=3,column=1,padx=(10,20),pady=(10,10))
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Continue",command=savePasswordOptions,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Back",command=displayOptions,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
def retrivePassword_gui():
    Clear()
    if not os.path.exists('passwdData.db'):
        tk.Label(main_window,text="").pack()
        tk.Label(main_window,text="No Passwords Saved yet!!! click enter for Previous Menu",font=('bold')).pack()
        tk.Label(main_window,text="").pack()
        tk.Button(main_window,text="Previous",command=displayOptions,fg="white",bg="blue",font=("bold")).pack()
        tk.Label(main_window,text="").pack()
        return    
    global menu
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Select from Below Menu for Retriving Password",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    menu = tk.StringVar()
    menu.set("Select an Option")
    drop = tk.OptionMenu(main_window,menu,'Search by App','Search by email','Display all Passwords','Return to Previous menu','Quit')
    drop.pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Select",command=chk_option,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Back",command=displayOptions,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
def searchByApp():
    Clear()
    global menu
    menu = tk.StringVar()
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Select App Name from below",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    options=getAppNames()
    menu.set('Select any App')
    drop = tk.OptionMenu(main_window,menu,*options)
    drop.pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Select",command=retriveAppPassword,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Back",command=retrivePassword_gui,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
def searchByEmail():
    Clear()
    global menu
    menu = tk.StringVar()
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Select Email form below!!..",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    options=getEmails(password)
    menu.set('Select any Email')
    drop = tk.OptionMenu(main_window,menu,*options)
    drop.pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Select",command=retriveEmailPassword,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Back",command=retrivePassword_gui,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()

def chk_option():
    option = menu.get()
    if option=='Save New Password':
        saveNewPassword_gui()
    elif option=='Retrive Saved Password':
        retrivePassword_gui()
    elif option=='Search by App':
        searchByApp()
    elif option=='Search by email':
        searchByEmail()
    elif option=='Display all Passwords':
        retriveAllPasswords()
    elif option=='Return to Previous menu':
        displayOptions()
    elif option=='Quit':
        over = tk.Label(main_window,text="Exiting!!....",font=('bold'),fg="blue")
        over.pack()
        over.after(2000,Clear_Exit)

def displayOptions():
    Clear()
    global menu
    tk.Label(main_window,text="Welcome, Choose your Option",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Select from Below Menu",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    menu = tk.StringVar()
    menu.set("Select an Option")
    drop = tk.OptionMenu(main_window,menu,'Save New Password','Retrive Saved Password','Quit')
    drop.pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Select",command=chk_option,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Quit",command=Clear_Exit,fg="white",bg="red",font=("bold")).pack()
    tk.Label(main_window,text="").pack()

def reg_success():
    secret_hash = genHash(str(register_pass.get()))
    print("Secret Key: "+register_pass.get())
    file = open('master_secret.dat','w+')
    file.write(secret_hash)
    file.close()
    #print(secret_hash)
    password_entry.delete(0,'end')
    success = tk.Label(main_window,text="Password Saved Successfully!..",fg="green",font=('bold'))
    success.pack()
    success.after(2000,createLogin)
    
def createNewLogin():
    global password_entry
    global register_pass
    register_pass = tk.StringVar()
    tk.Label(main_window,text="Welcome, this is your First Time enter a Master Password: ",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    tk.Label(main_window,text="Enter Password: ",font=('bold')).pack()
    tk.Label(main_window,text="").pack(padx=(10,10))
    password_entry = tk.Entry(main_window,textvariable=register_pass,width=50, borderwidth=10)
    password_entry.pack(padx=(20,20))
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Submit",command=reg_success,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Quit",command=Clear_Exit,fg="white",bg="red",font=("bold")).pack()
    tk.Label(main_window,text="").pack()



def chk_password():
    global password
    password=register_pass.get()
    secret_hash = genHash(str(register_pass.get()))
    file = open('master_secret.dat','r')
    saved_key = file.read()
    if secret_hash==saved_key:
        displayOptions()
    else:
        password_entry.delete(0,'end')
        retry = tk.Label(main_window,text="Wrong Password Try Again!..",fg="red",font=('bold'))
        retry.pack()

def createLogin():
    Clear()
    global register_pass
    global password_entry
    register_pass = tk.StringVar()
    tk.Label(main_window,text="Hello Enter your Master Password!.. ",font=('bold')).pack()
    tk.Label(main_window,text="").pack()
    password_entry = tk.Entry(main_window,textvariable=register_pass,width=50, borderwidth=10)
    password_entry.pack(padx=(20,20))
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Submit",command=chk_password,fg="white",bg="green",font=("bold")).pack()
    tk.Label(main_window,text="").pack()
    tk.Button(main_window,text="Quit",command=Clear_Exit,fg="white",bg="red",font=("bold")).pack()
    tk.Label(main_window,text="").pack()

def main():
    try:
        file = open('master_secret.dat','r')
        createLogin()
    except:
        createNewLogin()


global main_window
global register_passc
global secret_key 
main_window = tk.Tk()
main_window.title("PyPass")
main()
main_window.mainloop()
