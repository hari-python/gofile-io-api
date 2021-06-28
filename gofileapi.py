import requests

# import json

# Global Variables
Token = 'Your token'
allurls = {}  # To write urls into a file
get_server_link = 'https://api.gofile.io/getServer'
upload_sever_link = 'https://{0}.gofile.io/uploadFile'


# gets Account details and prints it:
def check_token(token):
    response = requests.get('https://api.gofile.io/getAccountDetails', {'token': token})
    try:
        if response.json()['status'] == 'ok':
            return True
        else:
            return False
    except KeyError:
        return False


# Checks for in script token, asks to use it, or ask for a new token:
def get_token():
    global Token
    while True:
        answer = input("Enter Y to continue with Custom TOKEN or Enter N to continue with GLOBAL token")
        if answer == "N":
            token = Token
            if check_token(token):
                break
            else:
                print(f"Given token : {token} could be invalid")
                continue
        if answer == 'Y':
            token = input("Enter new token here >>> : ")
            if check_token(token):
                break
            else:
                print(f"Given token : {token} could be invalid")
                continue
    return token


def get_server():
    print('Fetching Server...')
    global upload_sever_link
    a = requests.get('https://api.gofile.io/getServer')
    status = a.json()['status']
    if status == 'ok':
        print('Successfully Fetched Server using get_server()')
        server = a.json()['data']['server']
        upload_sever_link = upload_sever_link.format(server)
        return True
    else:
        print('Error in retrieving server try Again')
        return False


'''def openfiles():
    filename=''
    filedict={}
    while True:
       filename=input('Enter Name of file to be uploaded : ')
       if filename == '':
           break
       file=open(filename,"rb")
       filedict[filename] = file
       file.close()
    return filedict'''


def upload():
    global upload_sever_link
    global allurls
    global Token
    urls = []
    filenamelist = []

    while True:  # for avaling all files to be uploaded
        filename = input('Enter Name of file to be uploaded : ')
        if filename == '':
            break
        filenamelist.append(filename)

    for filename in filenamelist:

        try:
            file = open(filename, "rb")
        except FileNotFoundError:
            print(filename, 'is not found in current directory')
            continue

        filedict = {filename:file}
        print(f'Started uploading {filename}')
        response = requests.post(upload_sever_link, files=filedict, data={'token':Token,'folderId':'c3ee9b9f-df5b-41f0-92e0-419db094c12f','private':True})
        status = response.json()['status']
        print(response.json().items())
        if status == 'ok':
            print(f'succesfully uploaded {filename}')
        else:
            print(f'something went wrong...\nCouldn\'t upload {filename}')

        urls.append(response.json()['data']['downloadPage'])
        allurls[filename] = response.json()['data']['downloadPage']
        file.close()

    return urls


def writeurl():
    try:
        log = open('allurls.txt', 'a')
    except FileNotFoundError:
        print('allurls.txt not found creating new file')
        log = open('allurls.txt', 'w')
        log.close()
        log = open('allurls.txt', 'a')
    for filename, link in allurls.items():
        log.write(filename + ' : ' + link + '\n')
    log.close()
    return True


get_server()
print(upload_sever_link)
print(upload())
writeurl()
