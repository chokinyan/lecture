import requests
from bs4 import BeautifulSoup
import bs4
import sqlite3

#test = "https://kisswood.eu/farawaypain/kumo-desu-ga-nani-ka-chapitre-300/"[:-1]
#numChap = test[test.find('chapitre')+9:].replace('-','.')
#print(numChap)
#
#numChap = {0:6,1:5,2:3}
#
#for i in range(numChap.__len__()-1,-1,-1):
#    print(numChap[i])
#
#print([7,8]+[4])
#
#
#
#nomSerie : str = "kumo-desu-ga-nani-ka"
#dbNomSerie  : str= nomSerie.replace('-','_')
#
#connexion  : sqlite3.Connection = sqlite3.connect('lnList.db')
#cursor : sqlite3.Cursor = connexion.cursor()
#
#cursor.execute(f"""DELETE FROM {dbNomSerie} WHERE rowid = (SELECT MAX(rowid) FROM {dbNomSerie})""")
#connexion.commit()
#
#cursor.execute(f"""SELECT * FROM {dbNomSerie} ORDER BY rowid DESC LIMIT 1""")
#
#print(cursor.fetchall())
#
#connexion.close()