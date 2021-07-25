from hashlib import sha256
import random, string

from dBHandle import writeToFile, getPassword

def passwordCheck(passwd):
    alphaLower= 'abcdefghijklmnopqrstuvwxyz'
    alphaUpper= 'ABCDEFGHIJKLMNOPQRSTYVWXYZ'
    numeric = '0123456789'
    special = '(._-*~<>/|!@#$%^&)+='+'0123456789'
    small = False;caps=False;number=False;specialchar=False
    for i in passwd:
        if (small and caps and number and specialchar):
            return True
        if not small:
            if i in alphaLower:
                small=True
        if not caps:
            if i in alphaUpper:
                caps=True
        if not number:
            if i in numeric:
                number=True
        if not specialchar:
            if i in special:
                specialchar=True
    return False

def hexHashCode(text):
    return sha256(text.encode('utf-8')).hexdigest()

def hashToPassword(final_hash, maxLength):
    alp = 'abcdefghijklmnopqrstuvwxyz'+'ABCDEFGHIJKLMNOPQRSTYVWXYZ'+'0123456789'+'(._-*~<>/|!@#$%^&)+='+'0123456789'+'_*~/|!@#$%^&)='
    alp = ''.join(random.sample(alp,len(alp)))
    iters = len(final_hash)//maxLength
    passwd = ''
    for i in range(0,len(final_hash),iters):
        passwd+=alp[int(final_hash[i:i+iters],16)%106]
    if passwordCheck(passwd):
        return passwd
    else:
        return hashToPassword(final_hash, maxLength)

def saveNewPassword(secretKey):
    '''
    It asks for appName, userName, emailId as input and generated a Password
    '''
    appName = input('Enter Name of the App or Service: ')
    userName = input('Enter User name for the Account: ')
    emailId = input('Enter your connected Email Id: ')
    weblink = input('Enter Link to the Website: ')
    try:
        maxLength = int(input('Enter Length of Password (Default is 16): '))
    except:
        maxLength=16
    random_plaintext = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    salt = hexHashCode(appName)
    final_hash = hexHashCode(random_plaintext+salt)
    password = hashToPassword(final_hash, maxLength)
    print("Generated Password is:",password, end="\n\n\n")
    #uncomment after importings
    writeToFile(appName, userName, emailId, weblink, password, hexHashCode(secretKey))

def retrivePassword(secretKey):
    getPassword(hexHashCode(secretKey))
    return

