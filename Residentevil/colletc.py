# %% 
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'pt-BR,pt;q=0.7',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }


def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_info(soup):
    
    div_page = soup.find("div",class_="td-page-content")
    div_page
    paragrafo = div_page.find_all("p")[1]
    paragrafo
    ems= paragrafo.find_all("em")
    ems
    data = {}
    for i in ems:
        chave,valor, *_= i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

def get_aparicoes(soup):
    lis = soup.find("div",class_="td-page-content").find("h4").find_next().find_all("li")
    aparicao = [i.text for i in lis]
    
    return aparicao


def get_info(url):
    resp =get_content(url)

    if resp.status_code != 200:
        print("Nao foi possivel colertar os dados")
        return { }
    else:   
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = get_basic_info(soup)
        data["Aparicao"] = get_aparicoes(soup)
        return data
    

def get_links():
    url = "https://www.residentevildatabase.com/personagens"
    resp= requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)

    ancoras = (soup_personagens.find("div",class_="td-page-content").find_all("a"))
    links = [i["href"] for i in ancoras]
    return links

# %% 


links = get_links()
data = []
for i in tqdm(links):
    d = get_info(i)
    d['Link'] = i
    nome = i.strip("/").split("/").replace("-"," ").title()
    d["Nome"] = nome
    data.append(d)

# %%
# sempre que possovel evitar salvar em csv a nao ser algo simples pois os dados ficam bagunçados

df = pd.DataFrame(data)
df.to_parquet("dados_paquet", index=False)
# %% o pickle eu salvo o estado do objeto em python
df.to_pickle("dados_pickle.pkl")



