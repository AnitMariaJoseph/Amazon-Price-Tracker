from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import smtplib
import time
import datetime
import csv
import pandas as pd
import os


load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

FILE = 'AmazonWebScraper.csv'
  
def scrape():
  
   URL = 'https://www.amazon.ca/JBL-Tune-720BT-Lightweight-Comfortable/dp/B0CS8H4124/ref=sr_1_1_sspa?crid=3OH7M2S8FF1M8&dib=eyJ2IjoiMSJ9.K4pMZvCrQLLcpcHAZnHMen9Ye176S3LpUQmpGjT0_tgOaTX9JxyTIuq9COa_WxSy2Be_JoxKcXyVCaZ0XO_k-rGEb_S8PTBOyQbDvtWx5CXXUmbeZrQih9L_VEC_bNGeNw7HFh_mvBfhLfymRCOdqRMg-s9yXn7u6fwGVdV9NPeTwL95nHJmPC_c9Py8wspfXuSTk0w7IMB9jIVTnL84qbfeEhO1Qja0Z4_DDXgv730qSQ4ETvDxBCCmGDCrOLS6Nf3xIuR-VmET2456wfi0ER36PV7j9w9B1NsS6yQegPo.O1-yKv-_pdaCew5wiMibnH-_61LEK1Z10GFJSXDNboU&dib_tag=se&keywords=jbl%2Bheadphones&qid=1749497359&sprefix=jbl%2B%2Caps%2C157&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36", "Accept-Encoding":"gzip,deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","DNT":"1","Connection":"close","Upgrade-Insecure-Requests":"1"}

   resp = requests.get(URL, headers=headers, timeout=20)
   resp.raise_for_status()

   html = resp.text
   if "captcha" in html.lower():
        raise RuntimeError("Captcha page detected")

   soup1 = BeautifulSoup(html, "html.parser")
   soup2 = BeautifulSoup(soup1.prettify(),"html.parser")

   title_tag = soup2.select_one("span#productTitle")
   if title_tag is None:
        raise RuntimeError("Title span not found – markup changed?")
   title = title_tag.get_text(strip=True)

   price_symbol = soup2.find(class_='a-price-symbol').get_text(strip=True)
   price_whole_list = soup2.find_all(class_='a-price-whole')
   price_fraction_list = soup2.find_all(class_='a-price-fraction')

   price_whole = price_whole_list[-1].get_text(strip=True)
   price_fraction = price_fraction_list[-1].get_text(strip=True)
   price = f'{price_symbol}{price_whole}{price_fraction}'
   title = title.strip()


   today =datetime.date.today()
   header = ['Title','Price','Date']
   data = [title, price, today]

   file_exists = os.path.isfile(FILE)

   with open(FILE , 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    if not file_exists:                       
       writer.writerow(header)
    writer.writerow(data)

   price_value = float(price.replace('$','').replace(',',''))
   if price_value < 69.99:
    send_mail()
              


def send_mail():
  server = smtplib.SMTP_SSL('smtp.gmail.com',465)
  server.ehlo()
  server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
  subject = "The item is at its lowest!"
  body    = f"The item is on sale now, go ahead and check it out!!!!!"
  msg     = f"Subject: {subject}\n\n{body}"
  server.sendmail(EMAIL_ADDRESS,
                    EMAIL_ADDRESS,
                    msg)
  server.quit()


while(True):
  scrape()
  time.sleep(3600)

 
