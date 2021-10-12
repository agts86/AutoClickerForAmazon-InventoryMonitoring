import re

#バリデーション関係のクラス
class CheckUtiltys():
    #メールアドレスかどうか確認する
    #mail : メールアドレス
    #return : True(ok)/False(ng)
    def CheckMailAddress(mail:str):
        return re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", mail)
    
    #半角英数字記号かどうか確認する
    #target : 対象の文字列
    #return : True(ok)/False(ng)
    def CheckHankakuEisuziKigou(target:str):
        return re.match("^[a-zA-Z0-9!-/:-@¥[-`{-~]*$", target)

    #URLかどうか確認する
    #target : 対象の文字列
    #fqdn : 指定のFQDN
    #return : True(ok)/False(ng)  
    def CheckURL(target:str,fqdn:str):
        return re.match("https?://" + fqdn + "+", target)
    
    #電話番号かどうか確認する
    #phoneNumber : 電話番号
    #return : True(ok)/False(ng)
    def CheckPhoneNumber(phoneNumber:str):
        #ハイフンありの場合
        if re.match(r"[\(]{0,1}[0-9]{2,4}[\)\-\(]{0,1}[0-9]{2,4}[\)\-]{0,1}[0-9]{3,4}", phoneNumber):
            return True
        #ハイフンなしの場合
        elif re.match("[0-9]{10,11}", phoneNumber):
            return True
        else:
            return False