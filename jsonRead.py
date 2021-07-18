# 3.データを処理して結果DBにデータを保存する

import json
import pandas as pd
import pyodbc
import unicodedata

dirPath = "C:\\Users\\OBM2525\\Documents\\Data\\"
listDataPath = "2016_2020_R2.txt"

# 競馬場は中央のみ、今後地方対応
raceCourse = {"札幌":1,"函館":2,"福島":3,"中山":4,"東京":5,"新潟":6,"中京":7,"京都":8,"阪神":9,"小倉":10,"門別":11,"盛岡":12,"浦和":13,"船橋":14,"大井":15,"川崎":16}

# race_idリスト取得
def get_list_id(listData):
    f = open(listData,"r")
    count = 0
    getList = []
    for line in f:
        getList.append(line.replace("\n",""))
        count += 1
        if count == 3:
            break
    return getList

# SQLServerログイン情報
def login():
    instance = "DESKTOP-DDG5TLO\SQLEXPRESS"
    user=""
    password = ""
    db = "Sample"
    connection = "DRIVER={SQL Server};SERVER=" + instance + ";uid=" + user + \
                ";pwd=" + password + ";DATABASE=" + db
                
    return pyodbc.connect(connection)

# レース情報をDBへ登録する
def insert_execute(con, slq,data):
    print(data)
    con.execute(sql,
                data["ID"],data["no"],data["name"],data["time"],data["kind"],data["weather"],\
                data["state"],data["course"],data["etc_1"],data["etc_2"],data["etc_3"],data["etc_4"],\
                data["etc_5"],data["etc_6"],data["etc_7"],data["etc_8"])
    con.commit()

# 接続テストを実施
def select_execute(con, slq):
    cursor = con.cursor()
    cursor.execute(slq)
    rows = cursor.fetchall()
    cursor.close()

    return rows

if __name__ == "__main__":
    # listDataPath = "C:\\Users\\OBM2525\\Documents\\Workspace\\Netkeiba\\2016_2020_R2.txt"
    listDataPath = "C:\\Users\\OBM2525\\Documents\\Workspace\\Netkeiba\\NormalRace.txt"

    listData = []
    payOut = []

    f = open(listDataPath,"r")
    for line in f:
        listData.append(line.replace("\n",""))
    f.close()

    # print("Read RaceList... OK!")
    i = 0
    count = 0
    for line in listData:

        jsonFilePath = dirPath + listData[i] + ".json"
        json_open = open(jsonFilePath, 'r')
        json_load = json.load(json_open)
        
        try:
            hoge = json_load["race_info"]

            # 芝とダート判定
            if "芝" in json_load["race_info"]["kind"]:
                hoge["Turf"] = 1
            elif "ダ" in json_load["race_info"]["kind"]:
                hoge["Turf"] = 0
            else:
                print("exit")
                exit()

            hoge["etc_3"] = unicodedata.normalize("NFKC", hoge["etc_3"])
            # 各データ処理
            hoge["no"] = hoge["no"].replace("R","")
            hoge["time"] = hoge["time"].replace("発走","")
            hoge["kind"] = hoge["kind"].split(" (")[0].replace("m","")
            hoge["weather"] = hoge["weather"].replace("天候:","")
            hoge["state"] = hoge["state"].replace("馬場:","")
            hoge["etc_1"] = hoge["etc_1"].replace("回","")
            hoge["Distance"] = (int)(hoge["kind"][1:])
            hoge["etc_2"] = hoge["etc_2"].replace("日目","")
            hoge["etc_3"] = hoge["etc_3"].replace("サラ系","").replace("以","").replace("歳","")
            print(hoge["etc_3"][0:3])
        except:
            count += 1

        json_open.close()
        i += 1
    print(count)
    exit()


    jsonFilePath = dirPath + listData[0] + ".json"
    json_open = open(jsonFilePath, 'r')

    json_load = json.load(json_open)
    json_load["race_info"]["ID"] = listData[0]

    if raceCourse.get(json_load["race_info"]["course"]) == None:
        json_load["race_info"]["course"] = 99
    else:
        print(json_load["race_info"]["course"] )
        json_load["race_info"]["course"] = raceCourse.get(json_load["race_info"]["course"])
        print(json_load["race_info"]["course"] )
    exit()
    con = login()
    # DB・テーブル接続確認
    #sql =  '''select *
    #            from Race_Info'''
    #res = select_execute(con, sql)


    sql = """Insert INTO Race_Info(ID,no,name,time,kind,weather,
    state,course,etc_1,etc_2,etc_3,etc_4,etc_5,etc_6,etc_7,etc_8) VALUES(?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?)"""
    insert_execute(con,sql,json_load["race_info"])
    exit()

    #for line in json_load["race_order"]:
    #    print(line)
    #    print("\n=================\n")
    # print(json_load["race_info"])
    for line in json_load["payout"]:
        # Jsonの配当金の文字列処理を実施
        split = str(json_load["payout"][line]).replace("[","").replace("]","")
        split = split.replace("{","").replace("}","").split(",")
        print(split)
        #print(json_load["payout"][line])
        print("\n=================\n")
    print(json_load["payout"])
    print(json_load["rap_pace"])
    print("\n=================\n")
    print(json_load["race_info"])


    exit()