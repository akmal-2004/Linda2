from bs4 import BeautifulSoup
import urllib
import requests

def getjokes():
    jokes=[]
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}

    response = requests.get('https://anekdoty.ru/pro-programmistov/', headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    joke = soup.find_all('div', {'class':"holder-body"})

    for x in joke:
        jokes.append(x.text)

    return jokes