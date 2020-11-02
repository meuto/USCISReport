import requests as rq
from bs4 import BeautifulSoup
import smtplib
import os
import datetime
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
situacion=''
comentarios=''
password = str(os.environ.get('pa'))
email = str(os.environ.get('email'))
emailTo='tomeu.clapes@gmail.com'
dataForm={'changeLocale': None,
          'appReceiptNum': os.environ.get('uscis') ,
          'initCaseSearch': 'CHECK+STATUS'}
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
path='C:\\users\\tomeu\\OneDrive\\Desktop\\USCIS\\'
tome=os.listdir(path)
if not tome:
    f=open(path+'situacion.txt',"w")
    h=open(path+'comentarios.txt',"w")
    f.write(soup.find("div", {"class": "rows text-center"}).select('h1')[0].text)
    h.write(soup.find("div", {"class": "rows text-center"}).select('p')[0].text)
    f.close()
    h.close()
else:
    f=open(path+'situacion.txt',"r")
    h=open(path+'comentarios.txt',"r")
    situacion=f.read()
    comentarios=h.read()
    f.close()
    h.close()
def funcemail(email,password,emailTo,subject,Body):
    smtp=smtplib.SMTP('smtp.gmail.com',587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(email,password)
    msg=f'Subject:{subject}\n\n{Body}'
    smtp.sendmail(email,emailTo,msg)

if situacion!=soup.find("div", {"class": "rows text-center"}).select('h1')[0].text:
    f=open(path+'situacion.txt',"w")
    h=open(path+'comentarios.txt',"w")
    f.write(soup.find("div", {"class": "rows text-center"}).select('h1')[0].text)
    h.write(soup.find("div", {"class": "rows text-center"}).select('p')[0].text)
    f.close()
    h.close()
    f=open(path+'situacion01.txt',"w")
    h=open(path+'comentarios01.txt',"w")
    f.write(situacion)
    h.write(comentarios)
    f.close()
    h.close()
    asunto='Change of Status-'+soup.find("div", {"class": "rows text-center"}).select('h1')[0].text
    cuerpo=soup.find("div", {"class": "rows text-center"}).select('p')[0].text

    funcemail(email,password,emailTo,asunto,cuerpo)
