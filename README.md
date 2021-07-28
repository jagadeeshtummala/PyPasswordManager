# PyPassword Manager (PyPass)
- It is a command line tool for managing (creating, saving, retriving) passwords using ***Python***.

- It generates random password with alpha numeric characters of required length (default is 16 characters).

- On using it for the first time, it  requires to create a master password required to acccess the passwords stored.

- The hash (very difficult to get password from hash, [SHA256](https://en.wikipedia.org/wiki/SHA-2) is used as Hash function) of the master password is saved instead of actual password for future authentication.

- When a new password is generated the encrypted form of the password ( [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard), using hash of master password as key) is stored in the Database/CSV file, actual password is never saved. 

- Can retirve password based on serice name or all passwords connected to an email or display all passwords.

---

- **Requirements**
    - [***Python***](https://www.python.org/) version 3
    - [***pycryptodome***](https://pycryptodome.readthedocs.io/en/latest/) module (can be installed automatically while running for the first time if python is installed.)

---

- Running the Code
    - Download the code from this Github Page or [click here](https://github.com/jagadeeshtummala/PyPasswordManager/archive/refs/heads/main.zip) to downlaod the zip file.
    
    - if Git is installed open terminal or command prompt or Gitbash and run
    >`git clone https://github.com/jagadeeshtummala/PyPasswordManager.git`
    
    - Open the termianl or command prompt in the downloaded folder and run
        - for windows
            >`python main.py`
        - for Linux
            >`python3 main.py`
    - or Run the [main.py](https://github.com/jagadeeshtummala/PyPasswordManager/blob/main/main.py) Python file in the way you are familiar with.

---
