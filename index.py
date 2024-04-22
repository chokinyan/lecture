import requests
from bs4 import BeautifulSoup
import sqlite3
import signal
import bs4

class Chapitre:
    def __init__(self,chap : str,url: str) -> None:
        self.info = [chap,url]

chap : list[Chapitre] = []
nomSerie : str = "kumo-desu-ga-nani-ka"
dbNomSerie  : str= nomSerie.replace('-','_')
BasedUrl  : str = f'https://kisswood.eu/category/traductions/{nomSerie}/page/'
connexion  : sqlite3.Connection = sqlite3.connect('lnList.db')
cursor : sqlite3.Cursor = connexion.cursor()
ProgramEnd = False

def ForceEnd(sig,frame):
    global ProgramEnd
    ProgramEnd = True
    exit(0)

signal.signal(signal.SIGINT,ForceEnd)

def GetChaptOnPage(url : str) -> str:
    try:
        rep = requests.get(url)
        soup = BeautifulSoup(rep.text,'html.parser')
        title : bs4.element.ResultSet = soup.findAll("h1")
        for i in title:
            if(i.text.find("Chapitre") != 1 or i.text.find("chapitre") != 1):
                return i.text.split(' ')[-1]
    except:
        print("erreur")
        return GetChaptOnPage(url)

def ChapGet(url : str) -> None:
    global chap,ProgramEnd
    if(ProgramEnd):
        exit(1)
    try:
        rep : requests.Response = requests.get(url)
        if rep.status_code == 200:
            soup : BeautifulSoup = BeautifulSoup(rep.text,'html.parser')
            text : bs4.element.ResultSet = soup.findAll('article')
            for i in text:
                if(i.text.find('Chapitre') != -1 or i.text.find('chapitre') != -1):
                    chapLink : str= i.find('a')['href'][:-1]
                    
                    if((lastChap != []) and (chapLink == lastChap[0][0])):
                        print("chapter update")
                        return None        
                    else:
                        if(chapLink.find('chapitre') == -1):
                            chap.append(Chapitre(GetChaptOnPage(chapLink),chapLink))
                        else:
                            chap.append(Chapitre(chapLink[chapLink.find('chapitre')+9:].replace('-','.'),chapLink))
            
            newIndex = str(eval(f"{url.split('/')[-1]}+1"))
            ChapGet(BasedUrl+newIndex)
            
        return None
    
    except:
        print("Erreur")
        ChapGet(url)

cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{dbNomSerie}'""")

if cursor.fetchall() == []:
    cursor.execute(f"""CREATE TABLE {dbNomSerie}(cahpitre VARCHAR(255),url VARCHAR(255),lue BOOL)""")
    connexion.commit()
    lastChap = cursor.execute(f"""SELECT url FROM {dbNomSerie} ORDER BY rowid DESC LIMIT 1""").fetchall()
    ChapGet(url=BasedUrl+"1")
elif(cursor.execute(f"""SELECT COUNT(rowid) FROM {dbNomSerie}""").fetchone()[0] != 0):
    print("table already filled,checking for new chapter")
    lastChap = cursor.execute(f"""SELECT url FROM {dbNomSerie} ORDER BY rowid DESC LIMIT 1""").fetchall()
    ChapGet(url=BasedUrl+"1")
else:
    lastChap = cursor.execute(f"""SELECT url FROM {dbNomSerie} ORDER BY rowid DESC LIMIT 1""").fetchall()
    ChapGet(url=BasedUrl+"1")

chap.reverse()

for i in chap:
    print(f"Chapter {i.info[0]} add")
    cursor.execute(f""" INSERT INTO {dbNomSerie} VALUES(?,?,?) """,i.info+[False])
    connexion.commit()


cursor.execute(f""" SELECT MAX(rowid) FROM {dbNomSerie} """)
print(cursor.fetchall())

connexion.close()