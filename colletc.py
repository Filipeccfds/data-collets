# %% 
import requests
from bs4 import BeautifulSoup


def get_content(url):
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

    resp = requests.get(url, headers=headers)
    return resp


# %%
def get_basic_info(soup):
    
    div_page = soup.find("div",class_="td-page-content")
    div_page
    paragrafo = div_page.find_all("p")[1]
    paragrafo
    ems= paragrafo.find_all("em")
    ems
    data = {}
    for i in ems:
        chave,valor = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

# %%
url = "https://www.residentevildatabase.com/personagens/ada-wong/"
resp =get_content(url)

if resp.status_code != 200:
    print("Nao foi possivel colerta os dados")
else:   
    soup = BeautifulSoup(resp.text, 'html.parser')
    get_basic_info(soup)