import os
import random
import re
import shutil
import threading
import requests
from django.core.management import BaseCommand
from fake_useragent import UserAgent
from mydownloader.settings import BASE_DIR
from bs4 import BeautifulSoup
class Command(BaseCommand):
    def handle(self, *args, **options):
        '''直接m3u8網址下載'''
        # url = 'https://cp2.hboav.com/check/hbo8/hls/files/mp4/q/I/v/qIvUh.mp4/index.m3u8?key=B08z-je2HCIQvkKtipxFvw&expires=1658674607'
        # name = '大神南橘子約炮非常有趣的八字奶少婦不讓拍臉看到鏡頭就躲'
        # currentname = re.sub('[\/:*?"<>|]', " ",name)  # 獲取標題 以window檔案命名規則 當作檔名
        # self.downloadm3u8(url,currentname)

        '''透過txt讀取5278網址下載'''
        with open('text3.txt', 'r', encoding='UTF-8') as fh:
            linelist = fh.readlines()
        for idx,ls in enumerate(linelist):
            if idx != 0:
                print(ls.replace('\n', ''))
                self.get5278m3u8(ls.replace('\n', ''), '')
        return
    def get5278m3u8(self, strurl, strname):
        url = strurl
        user_agent = UserAgent().random
        headers = {
            "User-Agent": user_agent
        }
        session_requests = requests.session()  # 建立連接session
        res = session_requests.get(url, headers=headers)  # 獲取網頁
        # print(res.headers)
        soup = BeautifulSoup(res.text, 'html5lib')
        title = soup.find_all('title')  # 獲取標頭
        currentname = re.sub('[\/:*?"<>| ]', "", str(title[0])).replace('title', '') if strname == '' else strname # 獲取標題 以window檔案命名規則 當作檔名
        print(currentname)
        iframexx = soup.find_all('iframe')  # 獲取所有嵌入頁面網址
        # for iframe in iframexx:
        #     print(iframe)
        # print(iframexx[4])
        # print(iframexx[4].attrs['src'])
        h2 = {
            "Host": 'hbo6.hboav.com',
            "Referer": url
        }
        # print(iframexx)
        ahbo6http = []
        for iframe in iframexx:
            if "Player" in iframe.attrs['src']:
                ahbo6http.append(iframe.attrs['src'])
        print(ahbo6http)
        for idx,hbo6http in enumerate(ahbo6http):
            if idx != 0:
                currentname = currentname + str(idx)
            res2 = session_requests.get(hbo6http, headers=h2)  # 獲取子頁面html
            # print(res2.text)
            # for line in res2.text:
            #     r = re.match("http", line)
            #     if r != None:
            #         print(line)
            soup = BeautifulSoup(res2.text, 'html5lib')
            videotag = soup.find_all('video')
            # datalist = re.findall('\[.[^]]*]', res2.text)  # 抓出所有以[]包起來的字串
            allhttp = []
            for vt in videotag:
                allhttp.append(re.findall('https:.*', str(vt)))  # 獲取所有http連結
            # print(allhttp)
            # print(httm)
            m3u8http = []
            for ah in allhttp:
                for h in ah:
                    # print(h)
                    if 'm3u8' in h:
                        m3u8http.append(h.replace('\');', ''))  # 處理http連結
            print(m3u8http)
            for idx, mh in enumerate(m3u8http):
                if idx != 0:
                    currentname = currentname + str("({0})", idx)
                print(currentname)
                self.downloadm3u8(mh, currentname)
        return

    def downloadm3u8(self, m3u8listUrl, fileName):
        print(m3u8listUrl)
        maxexecutenum = 10
        mysession = requests.session()
        tsUrl = m3u8listUrl.split('?')[0]
        videoTag = tsUrl.split("/")[-1]
        rests = mysession.get(m3u8listUrl, headers={"User-Agent": "Mozilla/5.0"})  # 獲取.ts list網址
        folder_path = str(BASE_DIR) + '\\m3u8_download\\' + fileName + '\\'
        print(folder_path)

        upfolder_path = str(BASE_DIR) + '\\m3u8_download\\result\\'
        if os.path.exists(folder_path) == False:  # 判斷資料夾是否存在
            os.makedirs(folder_path)  # 創建資料夾

        temptsfile = open(folder_path + 'tslisttemp.txt', 'w', encoding='UTF-8')  # 將.ts list儲存成檔案
        temptsfile.write(rests.text)
        temptsfile.close()

        aryts = []  # 存放ts網址
        arytsfilename = []  # 存放ts檔案名
        count = 0
        with open(folder_path + 'tslisttemp.txt', 'r') as file:  # 讀取tslist
            lines = file.readlines()
            for line in lines:
                if line.endswith('.ts\n'):  # 判斷結為為.ts
                    count += 1
                    tsUrltmp = line.strip('\n') if line.startswith('http') else tsUrl.replace(videoTag, line.strip('\n'))
                    aryts.append(tsUrltmp)  # 字串處理變成.ts下載網址
                    name = "%05d" % count + ".ts"
                    arytsfilename.append(name)  # 檔案名列表
            file.close()
        print(aryts)
        print(arytsfilename)
        threads = []
        for ts, name in zip(aryts, arytsfilename):  # 下載ts列表
            print(ts,name)
            t = threading.Thread(target=self.downloadtsfile, args=[ts, name, folder_path])
            t.start()
            threads.append(t)
            print("+" + t.name)
            if len(threads) >= int(maxexecutenum):
                for thread in threads:
                    thread.join()
                    print("-" + t.name)
                threads.clear()
        for thread in threads:
            thread.join()
        threads.clear()
        self.alltscombination(folder_path, fileName, upfolder_path)  # 將所有.ts合併成mp4
        # shutil.rmtree(folder_path)  # 移除下載.ts的資料夾

    def downloadtsfile(self, url, filename, folder_path=None):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            if folder_path != None:
                if os.path.exists(folder_path) == False:  # 判斷資料夾是否存在
                    os.makedirs(folder_path)  # 創建資料夾
                total_path = folder_path + filename
            else:
                total_path = filename
            if len(response.content) == int(response.headers['Content-Length']):
                with open(total_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                    f.close()
        response.close()

    def alltscombination(self, folder_path, savefile_name, savefile_dir=None):
        if os.path.exists(folder_path) != False:
            os.chdir(folder_path)  # cmd切換到此資料夾
            if savefile_dir != None and os.path.exists(savefile_dir) == False:
                os.makedirs(savefile_dir)  # 創建資料夾
            savepath = savefile_name + '.mp4' if savefile_dir == None else savefile_dir + savefile_name + '.mp4'
            shell_str = 'copy /b *.ts ' + savepath
            print(shell_str)
            os.system(shell_str)
            os.chdir(savefile_dir)  # 改變正在使用的目錄 防止使用中
