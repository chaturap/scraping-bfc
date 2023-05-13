import os
import json
import math
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas

#url = "https://www.bcf.com.au/camping/tents/family-tents"
# https://www.bcf.com.au/camping?prefn1=category&prefv1=Camping&start=0&sz=60
#key1 =  input('Please Input Category Camping : ')
#key2 =  input('Please Input Category Camping : ')
#url = "https://www.bcf.com.au/{}?prefn1=category&prefv1={}&start=0&sz=60".format(key1,key2)
#url = "https://www.bcf.com.au/camping/"
url = ""
params = {
    'prefn1': 'category',
    #'prefv1': 'Camping',
    'src': '201',
    'sz': '60',
    #'keyword': searches,
    #'pgn': 1,
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/112.0.0.0 Safari/537.36"
}

result = []
def get_list(url: str):
    #key = input('Please Input Category Camping/fhising : ')
    #url = "https://www.bcf.com.au/camping?prefn1=category&prefv1={}&start=0&sz=60".format(key)
    key = input('Please Input Category Camping : ')
    key1 = key.lower()
    key2 = key.title()
    url = "https://www.bcf.com.au/{}?prefn1=category&prefv1={}&start=0&sz=60".format(key1, key2)

    res = requests.get(url, params=params,  headers=headers)
    if res.status_code == 200:
        print(f"Status Code is Ok , status code is : {res.status_code}")
        #soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)

        try:
            os.mkdir('json_result')
        except FileExistsError:
            pass

        for i in result:
            print(i)
        # proses scraping
        # contents = soup.find_all('li', {'class': 'grid-tile'})

        count_page = 0
        page : int = 0


        res = requests.get(url, params=params, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        contents_paging = soup.find('div', {'class': 'results-hits'}).text.strip()
        print(f"contents_paging: {contents_paging}")
        print("cek showing", str.find(contents_paging, "Showing", 7))
        print("cek total page : ", str.find(contents_paging, "-"))
        awal = str.find(contents_paging, "-") + 1
        akhir = str.find(contents_paging, "of")
        awal_totalitem = str.find(contents_paging, "of") + 2
        akhir_totalitem = str.find(contents_paging, " Results")
        #print(f"awal:{awal} , akhir:{akhir}")
        #print(f"awal:{awal_totalitem} , akhir:{akhir_totalitem}")

        print("cek position of : ", str.find(contents_paging, "of"))
        total_page = contents_paging[awal:akhir].strip()
        print("total Page:", total_page)
        total_item = contents_paging[awal_totalitem:akhir_totalitem].strip().replace(",", "")
        print("total Item:", total_item)

        last_page = math.ceil(int(total_item) / 60) * 60
        print(f"last_page : {last_page}")

        # 0 60 120 180 240    ...  3600
        #3600 last_page
        i = 1
        while page < 180:

            #res = requests.get(url, params=params, headers=headers)
            #soup = BeautifulSoup(res.text, 'html.parser')
            contents = soup.find_all('li', {'class': 'grid-tile'})

            for content in contents:
                brand = content.find('div', attrs={'class': 'brand-name'}).text.strip()
                name = content.find('div', attrs={'class': 'product-name'}).text.strip()
                salesPrices = content.find('span', attrs={'class': 'product-sales-price'}).text.lstrip().rstrip().replace(" ","").replace("\r\n^","").replace("^","")
                linkDetail = content.find('a', attrs={'class': 'thumb-link'})['href']
                if "http" in linkDetail:
                    linkDetail = content.find('a', attrs={'class': 'thumb-link'})['href']
                else:
                    linkDetail = url + content.find('a', attrs={'class': 'thumb-link'})['href']

                sku = content.find('a', attrs={'class': 'thumb-link'})['href']

                # print(f"name : {name}")
                # print(f"salesPrices : {salesPrices}")
                # print(f"brand : {brand}")
                # print(f"linkDetail : {linkDetail}")

                data_dict = {
                    'name' : name,
                    'salesprices' : salesPrices,
                    'brand' : brand,
                    'linkDetail' : linkDetail,
                }

                #print(data_dict)
                result.append(data_dict)
                #print(f"result : {result}")
                try:
                    os.mkdir('json_result')
                except FileExistsError:
                    pass
                with open('json_result/final_data.json', 'w+') as json_data:
                    json.dump(result, json_data)
            #print(f'Json Created page : {page}')
            print(f"Scraping page ke :{i}")
            i = i + 1
            page = page+60

        # create csv file
        df = pd.DataFrame(result)
        df.to_csv('data.csv', index=False)
        df.to_excel('data.xlsx', index=False)
        # data created
        print("data csv and xlsx created success")

    else:
        print(f"Status Code Not Ok , status code is : {res.status_code}")
    print("Jumlah Record : ",len(result))

def get_total_pages():
    url = "https://www.bcf.com.au/camping/"
    params = {
        'prefn1': 'category',
        'prefv1': 'Camping',
        'src': '201',
        'sz': '60',
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/112.0.0.0 Safari/537.36"
    }


    res = requests.get(url, params=params, headers=headers)
    if res.status_code == 200:
        print(f"Status Code is Ok , status code is : {res.status_code}")
        soup = BeautifulSoup(res.text, 'html.parser')

        pages = []
        contents = soup.find('div', {'class': 'results-hits'}).text.strip()
        print("cek showing",str.find(contents,"Showing",7))
        print("cek total page : ",str.find(contents,"-"))
        awal = str.find(contents,"-")+1
        akhir = str.find(contents,"of")
        awal_totalitem = str.find(contents,"of")+2
        akhir_totalitem = str.find(contents," Results")
        print(f"awal:{awal} , akhir:{akhir}")
        print(f"awal:{awal_totalitem} , akhir:{akhir_totalitem}")

        print("cek position of : ",str.find(contents,"of"))
        total_page = contents[awal:akhir].strip()
        print("total Page:",total_page)
        total_item = contents[awal_totalitem:akhir_totalitem].strip().replace(",","")
        print("total Item:", total_item)

        last_page = math.ceil(int(total_item) / 60) * 60
        print(f"last_page : {last_page}")


        print("i=")

    return



if __name__ == '__main__':
    pass
    get_list(url)
    #get_total_pages()

#web
#https://www.bcf.com.au/p/tahwalhi-inflatable-stand-up-paddle-board-106---pearl-beach/635123.html?cgid=BCF04#main=&prefn1=isSale&prefv1=Featured&start=1

#excel
#https://www.bcf.com.au/watersports?prefn1=category&prefv1=Watersports&start=0&sz=60/p/tahwalhi-inflatable-stand-up-paddle-board-106---pearl-beach/635123.html?cgid=BCF04