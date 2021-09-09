import requests
import time

time_500 = [] #紀錄遍歷一次500種幣所需秒數list
high_price_temp_coin = []  #紀錄新高幣種list
high_price_temp_price = [] #紀錄新高幣種list對應之最高價list

#發送系統啟動通知
headers = {
"Authorization": "Bearer " + "V8UxCKX0F3G5mmvdjmEvWqAVWsQBWAGxXDFtTVbnl5X",
"Content-Type": "application/x-www-form-urlencoded"}
str1 = "<系統>"+"\n"+"啟動成功"
params = {"message": str1}
r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)

#系統啟動時間
system_starttime = datetime.datetime.now()

try:
    while 1==1: #無限迴圈
        starttime = datetime.datetime.now() #開始計時
        for i in range(0,2): #一次能處理250種幣，總共需兩次迴圈為500種幣(市值前500)          
            #抓取api
            page = str(i+1)
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page="+page+"&sparkline=false"
            r = requests.get(url)
            list_of_dicts = r.json()
            time.sleep(1) #休息一秒，避免過量ping api造成error

            for j in range(0,250): #api一頁有250個幣種 (幣種順序根據市值排行，api已處理)
                if list_of_dicts[j]["current_price"]!=None and list_of_dicts[j]["ath"]!=None: #現在價格與歷史新高價格皆不為None
                    if float(list_of_dicts[j]["current_price"])>float(list_of_dicts[j]["ath"]): #現在價格高於歷史新高價格(非即時)
                        
                        #若幣種未被記錄過(high_price_temp_coin list中沒有該幣種)則通知有歷史新高
                        if list_of_dicts[j]["symbol"] not in high_price_temp_coin:
                            #增加新幣種新高紀錄到high_price_temp_coin和high_price_temp_price list 中
                            high_price_temp_coin.append(list_of_dicts[j]["symbol"])
                            high_price_temp_price.append(float(list_of_dicts[j]["current_price"]))
                            #發送創新高通知
                            headers = {
                            "Authorization": "Bearer " + "V8UxCKX0F3G5mmvdjmEvWqAVWsQBWAGxXDFtTVbnl5X",
                            "Content-Type": "application/x-www-form-urlencoded"}
                            str1 = "<測試>"+"\n"+"代號: "+list_of_dicts[j]["symbol"]+"\n"+"名稱: "+list_of_dicts[j]["name"]+"\n"+"市值排名: "+str(list_of_dicts[j]["market_cap_rank"])+"\n"+"創歷史新高時間: "+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"+"歷史新高價格(美元): "+str(list_of_dicts[j]["current_price"])
                            params = {"message": str1}
                            r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
                            
                        #若幣種有被記錄過(high_price_temp_coin list中有該幣種) 且 現價高於幣種index對應於high_price_temp_price list的價格 則通知有歷史新高
                        elif (list_of_dicts[j]["symbol"] in high_price_temp_coin) and high_price_temp_price[high_price_temp_coin.index(list_of_dicts[j]["symbol"])]<float(list_of_dicts[j]["current_price"]):
                            #更新幣種新高紀錄到high_price_temp_coin對應的high_price_temp_price list 中
                            high_price_temp_price[high_price_temp_coin.index(list_of_dicts[j]["symbol"])] = float(list_of_dicts[j]["current_price"])
                            #發送創新高通知
                            headers = {
                            "Authorization": "Bearer " + "V8UxCKX0F3G5mmvdjmEvWqAVWsQBWAGxXDFtTVbnl5X",
                            "Content-Type": "application/x-www-form-urlencoded"}
                            str1 = "<測試>"+"\n"+"代號: "+list_of_dicts[j]["symbol"]+"\n"+"名稱: "+list_of_dicts[j]["name"]+"\n"+"市值排名: "+str(list_of_dicts[j]["market_cap_rank"])+"\n"+"創歷史新高時間: "+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n"+"歷史新高價格(美元): "+str(list_of_dicts[j]["current_price"])
                            params = {"message": str1}
                            r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
        
        #紀錄遍歷秒數(開發測試報告用)
        endtime = datetime.datetime.now()
        #print((endtime - starttime).total_seconds())
        time_500.append((endtime - starttime).total_seconds())

        #每個整點十分的 10~15 秒發送系統運行通知  
        if time.strftime("%M", time.localtime())=='10' and int(time.strftime("%S", time.localtime()))>=10 and int(time.strftime("%S", time.localtime()))<=15:              
            headers = {
            "Authorization": "Bearer " + "V8UxCKX0F3G5mmvdjmEvWqAVWsQBWAGxXDFtTVbnl5X",
            "Content-Type": "application/x-www-form-urlencoded"}
            str1 = "<系統>"+"\n"+"正常運行中"
            params = {"message": str1}
            r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)

#如有錯誤，發送系統結束通知，以及顯示測試報告
except:       
    #發送系統結束通知
    headers = {
    "Authorization": "Bearer " + "V8UxCKX0F3G5mmvdjmEvWqAVWsQBWAGxXDFtTVbnl5X",
    "Content-Type": "application/x-www-form-urlencoded"}
    str1 = "<系統>"+"\n"+"結束執行"
    params = {"message": str1}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    
    #發送系統測試報告通知
    headers = {
    "Authorization": "Bearer " + "V8UxCKX0F3G5mmvdjmEvWqAVWsQBWAGxXDFtTVbnl5X",
    "Content-Type": "application/x-www-form-urlencoded"}
    system_endtime = datetime.datetime.now() #系統結束時間
    str1 = "<系統 測試報告>"+"\n"+"啟動時間: "+str(system_starttime.strftime("%Y-%m-%d %H:%M:%S"))+"\n"+"結束時間: "+str(system_endtime.strftime("%Y-%m-%d %H:%M:%S"))+"\n"+"總運行時間: "+str(system_endtime-system_starttime).split(".")[0]+"\n"+"單次循環最大時間(秒): "+str(round(max(time_500),3))+"\n"
    str2 = "單次循環平均時間(秒): "+str(round(sum(time_500)/len(time_500),3))+"\n"+"總循環次數: "+str(len(time_500))
    params = {"message": str1+str2}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)