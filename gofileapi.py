import requests
import json
allurls={}
get_server_link = 'https://api.gofile.io/getServer'
upload_sever_link ='https://{0}.gofile.io/uploadFile'

def get_server():
    print('Fetching Server...')
    global upload_sever_link
    a=requests.get('https://api.gofile.io/getServer')
    status = a.json()['status']
    if status == 'ok':
        print('Succesfully Fetched Server using get_server()')
        server= a.json()['data']['server']
        upload_sever_link=upload_sever_link.format(server)
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
    urls=[]
    filenamelist=[]
    while True:
       filename=input('Enter Name of file to be uploaded : ')
       if filename == '':
           break
       filenamelist.append(filename)
    
    for filename in filenamelist:
       try:
           file=open(filename,"rb")
       except FileNotFoundError:
           print(filename,'is not found in current directory')
           continue
       filedict={filename:file}
       print(f'Started uploading {filename}')
       response = requests.post(upload_sever_link,files=filedict)
       status = response.json()['status']
       if status == 'ok':
           print(f'succesfully uploaded {filename}')
        
       else:
           print(f'something went wrong...\nCouldn\'t upload {filename}')
       urls.append(response.json()['data']['downloadPage'])
       allurls[filename]=response.json()['data']['downloadPage']
       file.close()
       
    return urls
def writelog():
    try:
        log=open('allurls.txt','a')
    except  FileNotFoundError:
        print('allurls.txt not found creating new file')
        log=open('allurls.txt','w')
        log.close()
        log=open('allurls.txt','a')
    for filename,link in allurls.items():
        log.write(filename+' : '+link+'\n')
    log.close()
    return True

    
get_server()
print(upload_sever_link)
print(upload())
writelog()
