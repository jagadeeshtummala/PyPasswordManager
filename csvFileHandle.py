import csv
import os
from hashlib import sha256
import sys
import binascii

if os.name == 'nt':
    clrcmd = 'cls'
else:
    clrcmd = 'clear'

def clrscreen():
    os.system(clrcmd)

#Try to install Packages if not found already ()
try:
    from Crypto.Cipher import AES
except:
    print('Trying to install required modules, this is required only once....')
    os.system('pip3 install pycryptodome')
    clrscreen()
    from Crypto.Cipher import AES

try:
    import pandas as pd
except:
    print('Trying to install required modules, this is required only once....')
    os.system('pip3 install pandas')
    clrscreen()
    import pandas as pd


def hexHashCode(text):
    return sha256(text.encode('utf-8')).hexdigest()

def Encrypt(cipher, plain):
    length = len(plain)//6
    plain = plain.ljust((length+1)*16,'\0')
    ciphertext = cipher.encrypt(plain.encode('utf-8'))
    return binascii.hexlify(ciphertext).decode()

def Decrypt(cipher, passcode):
    passcode = binascii.unhexlify(passcode)
    return cipher.decrypt(passcode).decode()

def getByName(df,cipher):
    print('The Id for each App is: ')
    print(df[df.columns[0]])
    print('Enter App ID: ')
    choice = int(input())
    passcode = df['Password'][choice]
    password = Decrypt(cipher, passcode)
    clrscreen()
    return (password,df['AppName'][choice])


def getByEmail(df, cipher):
    print('Enter Email ID to Retrive Password: ',end='')
    email = input()
    email_cipher = Encrypt(cipher, email)
    rows = []
    for i in range(len(df)):
        if email_cipher == df['EmailId'][i]:
            rows.append(i)
    for i in rows:
        print(df['AppName'][i],end="\t")
        print(df['UserName'][i],end="\t")
        print(Decrypt(cipher, df['EmailId'][i]),end="\t")
        print(Decrypt(cipher, df['Password'][i]),end="\t")
        print(df["Weblink"][i])
    print('Press any Key to continue!!!....')
    input()
    clrscreen()

def getAllPasswords(cipher, df):
    n=len(df)
    for i in range(n):
        print(f'\n{i+1}th Record: ')
        print(df['AppName'][i])
        print(df['UserName'][i])
        print(Decrypt(cipher, df['EmailId'][i]))
        print(Decrypt(cipher, df['Password'][i]))
        print(df['Weblink'][i])
        print('-'.center(35,'-'))
    print('Press any key to continue...!')
    input()
    clrscreen()
    return

        
def writeToFile(appName, userName, emailId, weblink, password, secretHash):
    aes_key = secretHash[::-1][1::2]
    cipher = AES.new(aes_key.encode('utf-8'),mode=AES.MODE_ECB)
    emailId = Encrypt(cipher, emailId)
    password = Encrypt(cipher, password)
    fields = ["AppName", "UserName", "EmailId", "Password", "Weblink"]
    if not os.path.exists('passwdData.csv'):
        file = open('passwdData.csv','w')
        csvwriter = csv.DictWriter(file,fields)
        csvwriter.writeheader()
        file.close()
    csvfile = open('passwdData.csv','a')
    csvwriter = csv.DictWriter(csvfile,fields)
    line = {"AppName":appName, "UserName":userName, "EmailId":emailId, "Password":password, "Weblink":weblink}
    csvwriter.writerow(line)
    csvfile.close()
    print('Saved Password Successfully!!! Press any key to continue')
    input()
    clrscreen()

def getPassword(secretHash):
    aes_key = secretHash[::-1][1::2]
    cipher = AES.new(aes_key.encode('utf-8'), mode=AES.MODE_ECB)
    df = pd.read_csv('passwdData.csv')
    while True:
        print("Menu\n1 for search by App\n2 for search by email")
        print("3 for Display all Passwords\nR for Return to Previous menu\nQ for Quit\n",end="")
        choice = input()
        clrscreen()
        if choice == '1':
            password, choice = getByName(df,cipher)
            print(f'The Password for APP {choice} is:  {password}')
            print('Enter to Continue....',end="")
            input()
            clrscreen()
        elif choice == '2':
            #Print Passwords linked to an Email
            getByEmail(df, cipher)
        elif choice == '3':
            master_password = input('Enter Master Password Again for Security: ')
            clrscreen()
            if secretHash == hexHashCode(master_password):
                getAllPasswords(cipher, df)
            else:
                print('Wrong Password Try Again!!!...')
        elif choice.lower() == 'r':
            return
        elif choice.lower()=='q':
            sys.exit('Existing the Program')
        else:
            print("Wrong Choice Try again")

    

