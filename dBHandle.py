import sqlite3
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

def getByName(cur,cipher):
    print('The Id for each App is: ')
    cur.execute("SELECT appName FROM passwd;")
    query = cur.fetchall()
    i=0
    for row in query:
    	print(f'{i}\t{row[0]}')
    	i+=1
    print('Enter App ID: ',end="")
    choice = int(input())
    appName = query[choice][0]
    cur.execute("""SELECT password FROM passwd WHERE appName=(?);""",(appName,))
    passcode = cur.fetchall()[0][0]
    print(type(passcode),passcode)
    password = Decrypt(cipher, passcode)
    clrscreen()
    return (password,appName)

def getByEmail(cur, cipher):
	print('Enter Email ID to Retrive Password: ',end='')
	emailId = input()
	email_cipher = Encrypt(cipher, emailId)
	cur.execute("""SELECT * FROM passwd WHERE emailId=(?);""",(email_cipher,))
	query = cur.fetchall()
	if len(query) == 0:
		print('No Record exists for given Email....!!!')
	else:
		for row in query:
			print(row[1],end="\t")
			print(row[2],end="\t")
			print(Decrypt(cipher, row[3]),end="\t")
			print(Decrypt(cipher, row[4]),end="\t")
			print(row[5])
			print('-'.center(110,'-'))
	print('Press any Key to continue!!!....')
	input()
	clrscreen()


def getAllPasswords(cipher, cur):
	cur.execute("""SELECT * FROM passwd;""")
	query = cur.fetchall()
	i=0
	for row in query:
		print(f'\n{i+1}th Record: ')
		print(f'Appname: {row[1]}')
		print(f'UserName: {row[2]}')
		print(f'EmailId: {Decrypt(cipher, row[3])}')
		print(f'Password: {Decrypt(cipher, row[4])}')
		print(f'Weblink: {row[5]}')
		print('-'.center(35,'-'))
		i+=1
	print('Press any key to continue...!')
	input()
	clrscreen()


def writeToFile(appName, userName, emailId, weblink, password, secretHash):
	aes_key = secretHash[::-1][1::2]
	cipher = AES.new(aes_key.encode(), mode=AES.MODE_ECB)
	emailId = Encrypt(cipher, emailId)
	password = Encrypt(cipher, password)
	if not os.path.exists('passwdData.db'):
		conn =sqlite3.connect('passwdData.db')
		cur = conn.cursor()
		sql_command = """CREATE TABLE passwd (Sno INTEGER PRIMARY KEY, appName VARCHAR(20), userName VARCHAR(20), emailId TEXT, password TEXT, webLink VARCHAR(30));"""
		cur.execute(sql_command)
		conn.commit()
		conn.close()
	conn = sqlite3.connect('passwdData.db')
	cur = conn.cursor()
	cur.execute("""INSERT INTO passwd (appName, userName, emailId, password, webLink) VALUES (?,?,?,?,?);""",(appName,userName,emailId,password,weblink))
	conn.commit()
	conn.close()
	print('Password Saved Successfully!!! Press any key to continue')
	input()
	clrscreen()

def getPassword(secretHash):
    aes_key = secretHash[::-1][1::2]
    cipher = AES.new(aes_key.encode('utf-8'), mode=AES.MODE_ECB)
    if not os.path.exists('passwdData.db'):
    	print('No Passwords Saved yet!!!...enter any key for previous menu')
    	input()
    	clrscreen()
    	return
    conn = sqlite3.connect('passwdData.db')
    cur = conn.cursor()
    while True:
        print("Menu\n1 for search by App\n2 for search by email")
        print("3 for Display all Passwords\nR for Return to Previous menu\nQ for Quit\n",end="")
        choice = input()
        clrscreen()
        if choice == '1':
            password, choice = getByName(cur,cipher)
            print(f'The Password for APP {choice} is:  {password}')
            print('Enter to Continue....',end="")
            input()
            clrscreen()
        elif choice == '2':
            #Print Passwords linked to an Email
            getByEmail(cur, cipher)
        elif choice == '3':
            master_password = input('Enter Master Password Again for Security: ')
            clrscreen()
            if secretHash == hexHashCode(master_password):
                getAllPasswords(cipher, cur)
            else:
                print('Wrong Password Try Again!!!...')
        elif choice.lower() == 'r':
            return
        elif choice.lower()=='q':
            sys.exit('Existing the Program')
        else:
            print("Wrong Choice Try again")
