import os
import sys
from hashlib import sha256
from passHandling import saveNewPassword, retrivePassword
from csvFileHandle import clrscreen


def genHash(secret_key):
    hash = sha256(secret_key.encode()).hexdigest()
    return hash[1::2]+hash[::2]

def main():
    try:
        file = open('master_secret.dat','r')
        saved_key = file.read()
        file.close()
    except:
        print('Welcome, this is your First Time enter a Master Password: ')
        secret_key = input()
        secret_hash = genHash(secret_key)
        file = open('master_secret.dat','w+')
        file.write(secret_hash)
        file.close()
        print('Saving your Password!!!...& restarting...')
        main()
    print('Hello Enter your Master Password: ',end="")
    secret_key=input()
    clrscreen()  #used to Clear after entering password
    secret_hash = genHash(secret_key)
    if secret_hash != saved_key:
        print('Wrong Password Try Again!!!...')
        main()
    else:
        print('Welcome, Choose your Option')
        while True:
            print('Menu\n1 to save new Password\n2 to retrive saved password\nQ to exit')
            choice = input('Enter your Choice: ')
            clrscreen()
            if choice == '1':
                saveNewPassword(secret_key)
            elif choice == '2':
                retrivePassword(secret_key)
            elif choice.lower()=='q':
                sys.exit('Existing the Program')
            else:
                print('Wong Choice!')


if __name__ == '__main__':
    main()

