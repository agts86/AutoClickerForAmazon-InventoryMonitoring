import stdiomask
from OperateAmazon import OperateAmazon 
from CheckUtiltys import CheckUtiltys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox,Tk
from sys import exit

#Amazonの自動購入プログラム
def main():
    
    Tk().withdraw()
    if not messagebox.askokcancel("確認", "このプログラムはGoogleChromeを使用します。\r\nインストール済みの方は「OK｝を押してください。\r\nまだの方は「キャンセル」を押してください。"):
        return
        
    print("★プログラムの説明★")
    print("・入力した商品のURLの在庫を監視して、購入するツールです。")
    print("・あらかじめカートの中身は空にしておいてください。")
    print("・あらかじめ購入決済方法は一つにしておいてください。「クレジットカード」を推奨します。")
    print("・各入力項目は入力後に「Enter」キーを押してください。")
    print("・[*]がある入力項目は必須です。ないものは任意で設定してください。")
    print("　")

    while True:  
        print("高速版を使用しますか？")
        print("初回起動は通常版をオススメします。")
        headless= input("*y/n>")
        if headless == "y" or headless == "n":
            break
        else:
            print("yかnを入力してください")

    while True:   
        login = input("*ログインID(半角)>")
        if login != "":
            if CheckUtiltys.CheckMailAddress(login):
                break
            elif CheckUtiltys.CheckPhoneNumber(login):
                break
            else:
                print("ログインIDが不正です。")
        else:
            print("ログインID(半角)は必須です。")
            
    while True:  
        password = stdiomask.getpass("*ログインPassWord(半角)>")
        if password != "":
            if CheckUtiltys.CheckHankakuEisuziKigou(password):
                break
            else:
                print("ログインpasswordが不正です。")
        else:
            print("ログインPassWord(半角)は必須です。")
    
    while True:
        purchaseGoodsUrl = input("*買いたい商品のURL>")
        if purchaseGoodsUrl != "":
            if CheckUtiltys.CheckURL(purchaseGoodsUrl,"www.amazon.co.jp"):
                break
            else:
                print("AmazonのURLを入力してください。")
        else:
            print("買いたい商品のURLは必須です。")
    while True:
        amount = input("希望価格を入力してください。未入力の場合は一番安いものを購入します。>")
        if amount == "" or amount.isnumeric():
            break
        else:
            print("入力する場合は数値を入力してください。")
    while True:
        primeEligible = input("*prime商品に絞り込みますか？y/n>")
        if primeEligible == "y" or primeEligible == "n":
            break
        else:
            print("yかnを入力してください")
    while True:
        freeShipping = input("*送料無料に絞り込みますか？y/n>")
        if freeShipping == "y" or freeShipping == "n":
            break
        else:
            print("yかnを入力してください")

    while True:
        new = input("*新品に絞り込みますか？y/n>")
        if new == "y" or new == "n":
            break
        else:
            print("yかnを入力してください")

    itmeOptions =[]
    if primeEligible == "y":
        itmeOptions.append("primeEligible")

    if freeShipping == "y":
        itmeOptions.append("freeShipping")

    if new == "y":
        itmeOptions.append("new")
    
    #chromeのバージョンに合せたドライバーをインストールする
    #まぁまぁ重いから先にやっておく
    driverPath = ChromeDriverManager().install()
    
    #シークレットブラウザ/画面サイズ最大/画像を読み込まない
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito') 
    options.add_argument('--start-maximized')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--lang=ja')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    #高速版の場合はヘッダーレス
    if headless =="y":
        options.add_argument("--headless")

    driver = webdriver.Chrome(driverPath,chrome_options=options)
   
    #指定したdriverに対して最大で10秒間待つように設定する
    driver.implicitly_wait(10)

    #ログイン処理
    OperateAmazon.Login(driver,login,password)

    OperateAmazon.Purchase(driver,OperateAmazon.MakeOffer_Listing_URL(purchaseGoodsUrl),login,password,amount,itmeOptions)
    

    while True:
        finish = input("終了するにはEnterキーを押してください")
        if not finish:
            break
    exit()

if __name__=='__main__':       
    main()
