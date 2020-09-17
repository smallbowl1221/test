import requests
import http
import string
import bs4
import re
import csv
import os,sys
from os.path import isfile, isdir, join
from os import listdir
import time,datetime
import pandas as pd
from time import sleep
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib.request as req
import urllib.error
import ssl
import socket
import http.client

#設定MAXHEADERS
http.client._MAXHEADERS = 1000

#導入ssl module 改成不驗證
ssl._create_default_https_context = ssl._create_unverified_context

#擷取 content.py 執行位置
Data_address = "D:\Regiser\Data\\6\\"

#載入隨機user agent
ua = UserAgent()

#擷取Data下所有資料夾
files = listdir(Data_address)


#num_key ==> 第幾個 keyword
#逐key run------------------------------------------------------------------------------------------------------------------------------------
for num_key in files:
    
    #輸出現在 key word
    print("key word: " + num_key + "="*150)

    if not os.path.isfile( Data_address + num_key + "\\"  + num_key + "_sentence.csv"):

        #二維向量 [	["URL","Title","sentence"]	, ...]
        sentence_reg = []
        
        #處理key word 分割
        keyset = re.split( "\+" , num_key )

        #開啟指定 key_url.csv------------------------------------------------------------------------------------------------------------------------------------
        with open( Data_address + num_key + "\\" + num_key + "_url.csv", newline="" , encoding="utf-8-sig" ) as csvFile:
            #用pandas讀取csv檔案
            dic = csv.DictReader(csvFile)#將.csv轉成dictionary
            Title_vector = []
            Url_vector = []
            for row in dic:
                Title_vector.append(row["Title"]) #將所有"Title" 存入Title_vector
                Url_vector.append(row["url"]) #將所有"url" 存入url_vector

        #再某key下 逐url run------------------------------------------------------------------------------------------------------------------------------------
        for num_url in range( len(Url_vector) ):
            
            #指定url位置
            url = Url_vector[num_url]
            #輸出現在URL

            print("-"*100)
            print(str(num_url+1) + ". " + "url:"+url)
            try:
                print("讀取開始")

                #緩衝
                sleep(5)

                #向url發出要求
                request = req.Request(url, headers = {"User-Agent" : ua.chrome})
                print("正在發出請求...")

                #緩衝
                sleep(5)

                with req.urlopen(request,timeout=60) as response:
                    print("等待中...")
                    data = response.read().decode("utf-8",errors='ignore')

                #緩衝
                sleep(5)

                print("正在轉換成bs4")

                #data = "<!-[if IE eq 9]>" + data + "<![end if]->"

                #取得文章bs4物件
                root = bs4.BeautifulSoup(data, "html.parser")

                print("正在處理文章")
                #article_content ==> 文章內容
                #去除空格，並以\n當作底 
                s = str(root.text).replace(" ","").replace("\\n","")
                article_content = s.split()
                article_content = "\n".join(article_content)

                #將文檔以 \n 和 。 來做分割
                article_content = re.split("([\n|。])",article_content)
                article_content.append("")
                article_content = ["".join(i) for i in zip(article_content[0::2],article_content[1::2])]
                #article_content ==> sentence list

                
                #針對所有sentence進行掃描，是否存在keyword
                for sentence in article_content:
                    for key in keyset:
                        if key in sentence:
                            reg = []
                            #去除\n
                            sentence = "".join( sentence.replace("\\n","").split() )

                            #存取資料
                            reg.append(url)
                            reg.append(Title_vector[num_url])
                            reg.append(sentence)
                            sentence_reg.append(reg)
                print("處理完成")

            except urllib.error.URLError as e:
                print("error")
                if hasattr(e,"code"):
                    print("Http Error")
                elif hasattr(e,"reason"):
                    print("URl Error => " + str(e.reason))

            except ConnectionResetError as e:
                print("ConnectionResetError")

            except socket.timeout as e:
                print("read timeout")

            except TimeoutError as e:
                print("TimeoutError")
            
            except TypeError as e:
                print("TypeError")

            except http.client.IncompleteRead as e:
                print("http_client.IncompleteRead")

            except http.client.RemoteDisconnected as e:
                print("RemoteDisconnected")

        # 將文章存入 dataname.csv 中------------------------------------------------------------------------------------------------------------------------------------
        with open( Data_address + num_key + "\\"  + num_key + "_sentence.csv","w",newline='',encoding="utf-8-sig") as csvfile:
            #建立寫入器
            writer = csv.writer(csvfile)
            #寫入標題
            writer.writerow(["URL","Title","Sentence"])
            #寫入資料
            for i in sentence_reg:
                writer.writerow([i[0],i[1],i[2]])

    else:
        print(num_key + "_sentence.csv is exist")
        print()

print("contemt6.py program finish")