import requests
from bs4 import BeautifulSoup
import sqlite3

chap : dict[int,list[str]] = {}
indexChap : int = 0


nomSerie : str = "kumo-desu-ga-nani-ka"
dbNomSerie  : str= nomSerie.replace('-','_')
url  : str = f'https://kisswood.eu/category/traductions/{nomSerie}/page/1'



connexion  : sqlite3.Connection = sqlite3.connect('lnList.db')
cursor : sqlite3.Cursor = connexion.cursor()

cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{dbNomSerie}';""")

if cursor.fetchall() == []:
    cursor.execute(f"""CREATE TABLE {dbNomSerie}(id INT PRIMARY KEY,cahpitre VARCHAR(255),url VARCHAR(255),lue BOOL)""")

def listeChap(url : str) -> None:
    global chap,indexChap
    newUrl : str = ""
    try:
        rep : requests.Response = requests.get(url)
        if rep.status_code == 200:
            soup : BeautifulSoup = BeautifulSoup(rep.text,'html.parser')
            text = soup.findAll('article')
            for i in text:
                if(i.text.find('Chapitre') != -1 or i.text.find('chapitre') != -1):
                    chaplink  : str = i.find('a')['href'][:-1]
                    chap[indexChap] = [chaplink[chaplink.find('chapitre')+9:].replace('-','.'),chaplink]
                    indexChap += 1
                    
            UrlSplited : list[str] = url.split('/')
            UrlSplited[-1] = str(eval(f'{UrlSplited[-1]} + 1'))
            for i in range(UrlSplited.__len__()):
                if(i == 0):
                    newUrl += UrlSplited[i]
                elif(i == 1):
                    newUrl += '//'
                elif(i == UrlSplited.__len__() - 1):
                    newUrl += UrlSplited[i]
                else:
                    newUrl += UrlSplited[i] + '/'
            return listeChap(newUrl,indexChap)
                    
        else:
            return None
                        
    except:
        listeChap(url)

listeChap(url)

print("finish get url and chap")
print("\n------------------------------------------------\n")

for i in range(chap.__len__()-1,-1,-1):
    print(i)
    cursor.execute(f"""INSERT INTO {dbNomSerie} VALUES(?,?,?,?)""",[None]+chap[i]+[False])
    connexion.commit()

connexion.close()