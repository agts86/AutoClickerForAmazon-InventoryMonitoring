from typing import List
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from sys import exit

#Amazonの画面操作を行なうクラス
class OperateAmazon():
    #ログイン処理
    #driver : chromeのドライバー
    #login : ログインID
    #password : ログインパスワード
    #loginUrl : アマゾンのログイン画面のURL
    def Login(driver:webdriver.Chrome,login:str,password:str):
        
        try:
            driver.get("https://www.amazon.co.jp/")
            driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
            driver.find_element_by_id("nav-link-accountList").click()
            certification = False
            OperateAmazon.LoginMain(driver,login,password)
           
            #ログインできてトップ画面にアカウント名が表示されているか確認
            if len(driver.find_elements_by_id("nav-link-accountList-nav-line-1")) > 0:
                span:WebElement = driver.find_element_by_id("nav-link-accountList-nav-line-1")
                print("アカウント名:" + span.text[:-2])
            else:
                #リクエストエラー
                if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
                    raise Exception()
                #認証エラー
                else:
                    certification= True
                    raise Exception()
                           
            print(datetime.now())
            print("ログイン出来ました。")
        except Exception as e:
            print("ログインできませんでした。")
            
            if certification :
                while True:  
                    print("Amazonから認証メールが届いてますか？")
                    certificationMail= input("*y/n>")
                    if certificationMail == "y" or certificationMail == "n":
                        break
                    else:
                        print("yかnを入力してください")

                if certificationMail == "y":
                    while True:
                        finish = input("認証処理後にエンターキーを押してください。")
                        if not finish:
                            break
                else:
                    while True:
                        finish = input("Enterキーを押して、最初からやり直してください。")
                        if not finish:
                            exit()
            else:
                while True:
                    finish = input("Enterキーを押して、最初からやり直してください。")
                    if not finish:
                        exit()                      
            

    #購入処理
    #driver : chromeのドライバー
    #purchaseGoodsUrl : 在庫監視するURL
    #login : ログインID
    #password : ログインパスワード
    #amount : 指定された価格
    #itmeOptions : 絞り込みするリスト
    def Purchase(driver:webdriver.Chrome,purchaseGoodsUrl:str,login:str,password:str,amount:str,itmeOptions:list[str]):
        
        try:

            #いったんログアウトする
            driver.get("https://www.amazon.co.jp/gp/flex/sign-out.html?path=%2Fgp%2Fyourstore%2Fhome&useRedirectOnSuccess=1&signIn=1&action=sign-out&ref_=nav_signout")
            #navigator.webdriver=true回避　botだとばれないようにする
            driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
            print("一度ログアウトします。")
            
            while True:
                driver.get(purchaseGoodsUrl)
                
                #navigator.webdriver=true回避　botだとばれないようにする
                driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
                
                if len(itmeOptions) > 0:
                    driver.find_element_by_class_name("a-button-inner.aod-filter-button-div").click()
                    for option in itmeOptions:
                        check:WebElement = driver.find_element_by_xpath('//*[@id="' + option + '"]/div/label/input')
                        driver.execute_script("arguments[0].click();",check)

                if len(driver.find_elements_by_id("aod-offer")) > 0:
                    ItemList:List[WebElement] = driver.find_elements_by_id("aod-offer")
                    #価格指定があった場合は指定価格以下の値段のものを購入する
                    if amount !="":
                        for item in ItemList:
                            price = int(item.find_element_by_class_name("a-price-whole").text.replace(",",""))
                            if int(amount) >= price:
                                print("購入価格:" + str(price) + "円")
                                item.find_element_by_name("submit.addToCart").click()
                                break
                        else:
                            sleep(1)
                            continue
                    else:
                        priceList = []
                        #表示されている価格をリストに追加していく
                        for item in ItemList:
                            priceList.append(int(item.find_element_by_class_name("a-price-whole").text.replace(",","")))
                        for item in ItemList:
                            #リストに追加された価格の中で一番安いものを購入する
                            if min(priceList) == int(item.find_element_by_class_name("a-price-whole").text.replace(",","")):
                                print("購入価格:" + str(min(priceList)) + "円")
                                item.find_element_by_name("submit.addToCart").click()
                                break
                        else:
                            sleep(1)
                            continue
                    break
                else:
                    sleep(1)
            sleep(1)
            #カート画面に遷移
            driver.get("https://www.amazon.co.jp/gp/cart/view.html/ref=nav_cart")
            driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
            driver.find_element_by_name("proceedToRetailCheckout").click()

            OperateAmazon.LoginMain(driver,login,password)
            
            #navigator.webdriver=true回避　botだとばれないようにする
            driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
            driver.find_element_by_name("placeYourOrder1").click()  
            OperateAmazon.SuccessProsess(driver) 
        
        except Exception as e:
            print(e)
            print("何らかの不具合が発生してます")
            driver.quit()

    #購入成功時の処理
    #driver : chromeのドライバー
    def SuccessProsess(driver:webdriver):
        print(datetime.now())
        print("[success]購入成功")
        sleep(5)
        driver.quit()

    #入力されたURLから商品IDを取り出して監視するURLを生成しなおす
    #URL : 入力されたURL
    def MakeOffer_Listing_URL(URL:str):
        array = URL.split("/")
        NextOfTarget = False
        for item in array:
            if NextOfTarget:
                id = item
                break
            if item == "dp" or item == "product":
                NextOfTarget = True
        if id =="":
            while True:
                    print("商品IDが見つかりませんでした。")
                    print("別の商品URLを試してください。")
                    finish = input("Enterキーを押して終了してください。")
                    if not finish:
                        exit() 
        else:     
            return "https://www.amazon.co.jp/dp/" + id + "/ref=olp-opf-redir?aod=1&ie=UTF8&condition=ALL&th=1"

    #ログイン画面の遷移処理
    #driver : chromeのドライバー
    #login : ログインID
    #password : ログインパスワード
    def LoginMain(driver:webdriver.Chrome,login:str,password:str):
        #navigator.webdriver=true回避　botだとばれないようにする
        driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
        driver.find_element_by_name("email").send_keys(login)
        driver.find_element_by_id("continue").click()
        driver.execute_script('const newProto = navigator.__proto__;delete newProto.webdriver;navigator.__proto__ = newProto;')
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_name("rememberMe").click()
        driver.find_element_by_id("signInSubmit").click()

        

