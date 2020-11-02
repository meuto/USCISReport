import requests as rq
from bs4 import BeautifulSoup
import smtplib
import os
import datetime
import pandas as pd
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
situacion=''
comentarios=''
password = str(os.environ.get('pa'))
email = str(os.environ.get('email'))
emailTo='tomeu.clapes@gmail.com'
dataForm={'changeLocale': None,
          'appReceiptNum': os.environ.get('uscis') ,
          'initCaseSearch': 'CHECK+STATUS'}
currentDirectory=os.getcwd()
url='https://egov.uscis.gov/casestatus/mycasestatus.do'
r=rq.post(url,data=dataForm,headers=headers)
soup=BeautifulSoup(r.content,'html5lib')
#print(r.url)
fecha=soup.find("div", {"class": "rows text-center"}).select('p')[0].text.split(',')
soup.find("div", {"class": "rows text-center"})
print(soup.find("div", {"class": "rows text-center"}).select('h1')[0].text)
print(fecha)
fecha=fecha[0]+fecha[1]
fecha=fecha[3:]
data=datetime.datetime.strptime(fecha,'%B %d %Y')
deltaDays=abs((data-datetime.datetime.now()).days)
print(f'Days since las update: {deltaDays}')
path='C:\\Users\\tomeu\\Source\\Repos\\USCISReport'
tome=os.listdir(path)
situation=[soup.find("div", {"class": "rows text-center"}).select('h1')[0].text]
coments=[soup.find("div", {"class": "rows text-center"}).select('p')[0].text]
def funcemail(email,password,emailTo,subject,Body):
    smtp=smtplib.SMTP('smtp.gmail.com',587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(email,password)
    msg=f'Subject:{subject}\n\n{Body}'
    smtp.sendmail(email,emailTo,msg)

if 'historic.csv' not in tome:
    historic={'situation':situation,'coments':coments,'USCISCase':dataForm['appReceiptNum']}
    historic=pd.DataFrame(historic)
    historic.to_csv(path+'\\historic.csv',header=True,index=False,sep=';')
    asunto='Change of Status-'+soup.find("div", {"class": "rows text-center"}).select('h1')[0].text
    cuerpo=soup.find("div", {"class": "rows text-center"}).select('p')[0].text+f'\n \n Days Since last Update: {deltaDays}'
    funcemail(email,password,emailTo,asunto,cuerpo)

else:
    historic=pd.read_csv(path+'\\historic.csv',sep=';')
    if len(historic)==1:
        print('nothing')
    else:
        historicChange=[situation,coments,dataForm['appReceiptNum']]
        if (historic.iloc[-1,:][0]==situation) and (historic.iloc[-1,:][1]==coments):
            print('nothing')
        else:
            historic=pd.concat([historic,pd.DataFrame(historicChange)],ignore_index=True)
            historic.to_csv(path+'\\historic.csv',header=True,index=False,sep=';')
            asunto='Change of Status-'+soup.find("div", {"class": "rows text-center"}).select('h1')[0].text
            cuerpo=soup.find("div", {"class": "rows text-center"}).select('p')[0].text+f'\n \n Days Since last Update: {deltaDays}'
            funcemail(email,password,emailTo,asunto,cuerpo)


