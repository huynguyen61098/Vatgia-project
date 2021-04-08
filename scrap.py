#import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
filepath = "F:\data learn/"
baseurl = "https://vatgia.com/"
headers = {
    "_User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

#get all products links from the website
linklst = []
for x in range(1,19):
    r = requests.get(f"https://vatgia.com/319/may-anh-so.html?verified=1&page={x}")
    soup = BeautifulSoup(r.content, "lxml")


    productlist = soup.find_all("div", class_ = "more_content")
    for picture in productlist:
        for link in picture.find_all("a", href = True):
            linklst.append(baseurl + link["href"])
    

    
#scrapping information from each link respectively
product_contain = []
for link in linklst:
    urllink = f"{link}"
    r = requests.get(urllink, headers = headers)
    soup = BeautifulSoup(r.content, "lxml")
    
    try:
        name = soup.find("h1", {"id": "detail_product_name"}).text.strip()
    except:
        name = None
        
    try:
        price = soup.find("b", class_="product_price").text.strip()
    except AttributeError as error:
        price = None
    
    try:
        stars = soup.find("div", class_="rating_review_main fl").text.split("/")[0].strip()
    except AttributeError as error: 
        stars = None
        
    try:
        reviews = soup.find("div", class_="rating_review_main fl").text.split("/")[1].strip()
    except AttributeError as error:
        reviews = None
    product = {"name": name,
              "price": price,
              "stars rate": stars,
              "reviews": reviews,
              
              }
    print(name, price, stars, reviews)
    print("DONE")
    product_contain.append(product)

#create a dataframe to contain data
df = pd.DataFrame(product_contain)

#save the data
df.to_csv(f"{filepath}data6.csv", index = False)
        
  
   
