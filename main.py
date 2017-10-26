import sys
import git
import csv
import time
from selenium import webdriver
from time import sleep
from datetime import datetime
from buildings import Building
from log import log
from configparser import SafeConfigParser

URL_CookieClicker = "http://orteil.dashnet.org/cookieclicker/"
EXECUTE_CLICK_BIGCOOKIE = "setInterval(function() {Game.ClickCookie(); Game.lastClick=0; }, 1000/1000);"
EXECUTE_CLICK_GOLDENCOOKIE = "setInterval(function(){for (var i in Game.shimmers) { Game.shimmers[i].pop(); }}, 500);"

# ConfigFile = ".config.ini"

def git_commit():
    repository = git.Repo("save")
    repository.git.add(".")
    commit_meessage = datetime.now().isoformat()
    repository.index.commit(commit_meessage)

class CookieCliker(object):
    Path = "save/savedata"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 500
    SAVE_INTERVAL = 30
    NUMBER_OF_BUY = 1000
    INTERVAL = 15
    PRODUCTS_LIST = ("Cursor", "Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Tower", "Shipment", "Lab", "Portal", "Time_Machine", "Condefsor", "Prism", "Chansemaker")
    def __init__(self, url):
        """
        try:
            config = SafeConfigParser()
            config.read("config.ini")
            CookieCliker.Path = config.get("settings", "SAVEFILE")
            CookieCliker.WINDOW_WIDTH = int(config.get("settings", "WINDOW_WIDTH"))
            CookieCliker.WINDOW_HEIGHT = int(config.get("settings", "WINDOW_HEIGHT"))
            CookieCliker.SAVE_INTERVAL = int(config.get("settings", "SAVE_INTERVAL"))
            CookieCliker.NUMBER_OF_BUY = int(config.get("settings", "NUMBER_OF_BUY"))
            CookieCliker.INTERVAL = int(config.get("settings", "INTERVAL"))
        except:
            print("cannot read config")
        """
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(CookieCliker.WINDOW_WIDTH, CookieCliker.WINDOW_HEIGHT)        
        self.driver.get(url)
        # 2秒待てば、ブラウザの読み込みが間に合う
        sleep(2)
        self.BigCookie = self.driver.find_element_by_id("bigCookie")
        self.products = []
        for id, name in enumerate(CookieCliker.PRODUCTS_LIST):
            self.products.append(Building(name = name, id = id, driver = self.driver))
        print("Cookie Clicker has been initialized")

    def Export_Savedata(self):
        OpenTextAreaScript = "Game.ExportSave();"
        self.driver.execute_script(OpenTextAreaScript)
        savedata = self.driver.find_element_by_id("textareaPrompt").text
        f = open(CookieCliker.Path, 'w')
        f.write(savedata)
        f.close()
        self.driver.execute_script("Game.ClosePrompt();")
        git_commit()

    def Import_Savedata(self):
        OpenTextAreaScript = "Game.ImportSave();"
        ImportScript = "Game.ImportSaveCode(l('textareaPrompt').value);"
        LoadScript = "Game.ClosePrompt();"

        # Importを開く
        self.driver.execute_script(OpenTextAreaScript)

        # 注意：savefileの中には1行しか記述されていないはず
        f = open(CookieCliker.Path, 'r')
        # savedataが読み込めないことがあったら、空のセーブデータでプレイ
        savefile = ""
        for a in f:
            savefile = a
        f.close()

        self.driver.find_element_by_id("textareaPrompt").send_keys(savefile)
        self.driver.execute_script(ImportScript)
        self.driver.execute_script(LoadScript)
        for p in self.products:
            p.Update(self.driver)

        print("/////////////////////////////////////")
        print("/           Load done               /")
        print("/////////////////////////////////////")

    def Auto_Clicker(self):
        print("set auto click")
        global EXECUTE_CLICK_BIGCOOKIE, EXECUTE_CLICK_GOLDENCOOKIE
        self.driver.execute_script(EXECUTE_CLICK_BIGCOOKIE)
        # self.driver.execute_script(EXECUTE_CLICK_GOLDENCOOKIE)

    def Buy_allUpgrades(self):
        print("Buy all upgrades")
        while True:
            try:
                upgrade = self.driver.find_element_by_id("upgrade0")
                if "enabled" in upgrade.get_attribute("class"):
                    upgrade.click()
                else:
                    return
            except:
                return

    def Standard_Strategy(self):
        # productsの中で、Cps_per_priceの高いもの順に並び替え
        temp = sorted(self.products, key=lambda p:-p.Cps_per_price)
        count = 0
        max_count = 3
        buythem = []
        # Cps_per_priceの高い順に、unlockされているものを4つ持ってくる
        for p in temp:
            if p.is_unlocked:
                buythem.append(p)
                count += 1
                if count > max_count:
                    break
        print("Standard Strategy begin")
        for p in buythem:
            if p.is_active(self.driver):
                # NUMBER_OF_BUYだけ購入
                p.Buy(CookieCliker.NUMBER_OF_BUY, self.driver)
        print("Standard Strategy end")

    def Run(self):
        print("#####################################")
        print("#        Running CookieCliker       #")
        print("#####################################")
        self.Import_Savedata()
        self.Auto_Clicker()
        fieldnames = ("time","Cookies", "Cps")          
        save_point = 0
        data = [0, 0, 0]
        start = time.time()
        while True:
            self.Buy_allUpgrades()
            self.Standard_Strategy()
            print("wait" + str(CookieCliker.INTERVAL) + "sec")
            sleep(CookieCliker.INTERVAL)
            save_point += 1
            if save_point > 5:
                self.Export_Savedata()
                print("Saved")
                data = log(self.driver, start)
                save_point = 0
                with open("log.csv", "a", newline="") as l:
                    temp = csv.DictWriter(l, fieldnames=fieldnames)
                    temp.writerow(data)
            print("--------------------------------------")
"""
    def Run_debug(self):
        print("#####################################")
        print("#        Running CookieCliker       #")
        print("#####################################")
        # self.Import_Savedata()
        # self.Auto_Clicker()
        fieldnames = ("time","Cookies", "Cps")          
        save_point = 0
        data = [0, 0, 0]
        start = time.time()
        while True:
            # self.Buy_allUpgrades()
            # self.Standard_Strategy()
            print("wait" + str(CookieCliker.INTERVAL) + "sec")
            sleep(CookieCliker.INTERVAL)
            save_point += 1
            if True:
                # self.Export_Savedata()
                print("Saved")
                data = log(self.driver, start)
                save_point = 0
                with open("log_debug.csv", "a", newline="") as l:
                    temp = csv.DictWriter(l, fieldnames=fieldnames)
                    temp.writerow(data)
            print("--------------------------------------")
"""

clicker = CookieCliker(URL_CookieClicker)

clicker.Run()
    
print("done")