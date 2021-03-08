import requests
from bs4 import BeautifulSoup
import json as _json


def get_free_proxies():
    '''
    url to get us proxy
    '''
    url = "http://www.freeproxylists.net/?c=US&pt=&pr=HTTPS&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0"
    # get the HTTP response and construct soup object
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    proxies = []
    '''
    handels if some time site didnt't respond
    '''
    try:
        for row in soup.find("table").find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                host = f"{ip}:{port}"
                proxies.append(host)
            except IndexError:
                continue
        return proxies
    except:
        return None
def get_data(json=False):
    '''

    :param json:  to get json data
    :return: scrapped data of given url
    '''
    url="https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1"
    #url = "https://www.midsouthshooterssupply.com/dept/reloading/primers?itemsperpage=60"
    # url="https://www.midsouthshooterssupply.com/dept/reloading/primers"
    r = requests.get(url,proxies=get_free_proxies())

    soup = BeautifulSoup(r.content, 'html.parser')

    #soup.findall(class_=)
    all_divs = soup.findAll('div', {'id' : 'Div1','class':'product'})
    Data=[]
    for i in all_divs:
        data=dict()
        title=i.find('a',{'class':'catalog-item-name'}).contents[0]
        title=title[:title.find('#')]
        data['title'] = title
        price=i.find('span',{'class':'price'})
        price=price.find('span',{"class":""}).contents[0][1:]
        data['price']=float(price)
        status=i.find('span',{"class":"status"}).contents[0].contents[0]
        if status=="Out of Stock":
            data['stock']=False
        else:
            data['stock']=True
        mftr=i.find('a',{"class":"catalog-item-brand"}).contents[0]
        data['mftr']=mftr
        Data.append(data)
    if json:
        json_data=_json.dumps(Data)
        return json_data
    else:
        return Data

def main():
    '''
    To get json Data
    '''
    print(get_data(json=True))

    '''
    To get python Data
    '''
    print(get_data())

if __name__ == '__main__':
    main()