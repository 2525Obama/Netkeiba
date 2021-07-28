# 3.データを処理して結果DBにデータを保存する

import json
import pandas as pd
import pyodbc
import unicodedata
import csv

dirPath = "C:\\Users\\OBM2525\\Documents\\Data\\"
listDataPath = "2016_2020_R2.txt"

# 競馬場は中央+一部地方のみ、今後地方対応
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

# 文字列を整形したデータを返す
def updateRaceData(hoge):
    # 芝とダート判定
    if "芝" in hoge["kind"]:
        hoge["Turf"] = 1
    elif "ダ" in hoge["kind"]:
        hoge["Turf"] = 0
    else:
        print("exit")
        exit()

    hoge["etc_3"] = unicodedata.normalize("NFKC", hoge["etc_3"])
    # 各データ整形処理
    hoge["no"] = hoge["no"].replace("R","")
    hoge["time"] = hoge["time"].replace("発走","")
    hoge["kind"] = hoge["kind"].split(" (")[0].replace("m","")
    hoge["Distance"] = (int)(hoge["kind"][1:])
    hoge["weather"] = hoge["weather"].replace("天候:","")
    hoge["state"] = hoge["state"].replace("馬場:","")
    hoge["etc_1"] = hoge["etc_1"].replace("回","")
    hoge["etc_2"] = hoge["etc_2"].replace("日目","")
    hoge["etc_3"] = hoge["etc_3"].replace("サラ系","").replace("以","").replace("歳","")
    return hoge

# 1頭のデータ編集 
def updateHorseData(hoge,race_name):
    listData = []
    for line in hoge:
        if line["rank"] == "除外" or line["rank"] == "中止" or line["rank"] == "取消"or line["rank"] == "失格":
            line["rank"] = 99
        else:
            line["rank"] = int(line["rank"])

        if line["waku"] == "" or line["umaban"] == "" or line["jockey_weight"] == "":
            print(race_name)
        else:
            line["waku"] = int(line["waku"])
            line["umaban"] = int(line["umaban"])
            line["jockey_weight"] = float(line["jockey_weight"])
        
        if line["horse_weight"] == "":
            line["Increase"] = 0
            line["horse_weight"] = 0
        else:
            if line["horse_weight"][len(line["horse_weight"])-1] != ")":
                line["Increase"] = 0
                line["horse_weight"] = int(line["horse_weight"])
            else:
                line["Increase"] = int(line["horse_weight"].split("(")[1].replace(")","").replace("+",""))
                line["horse_weight"] = int(line["horse_weight"].split("(")[0])
        line["horse_id"] = int(line["horse_id"])
        line["jockey_id"] = line["jockey_id"]
        if line["odds_1"] == "":
            line["odds_1"] = 0
        else:
            line["odds_1"] = int(line["odds_1"])
        if line["odds_2"] == "":
            line["odds_2"] = 0
        else:
            line["odds_2"] = float(line["odds_2"])

        if line["time_3"] == "":
            line["time_3"] = 0
        else:
            line["time_3"] = float(line["time_3"])

        if line["horse_age"][0] == "牡":
            #line["sex"] = 0
            line["sex"] = "牡"
        elif line["horse_age"][0] == "牝":
            #line["sex"] = 1
            line["sex"] = "牝"
        else:
            #line["sex"] = 2
            line["sex"] = "セ"
        line["horse_age"] = int(line["horse_age"][1:])
        line["RaceID"] = race_name
        listData.append(line)
    return listData

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
    with open("test.csv","w",newline="") as f:
        jsonFilePath = dirPath + listData[0] + ".json"
        json_open = open(jsonFilePath, 'r')
        json_load = json.load(json_open)
        line = updateHorseData(json_load["race_order"],listData[0])
        writer = csv.DictWriter(f, fieldnames=line[0].keys(),delimiter=",",quotechar='"')
        writer.writeheader()
        for line in listData:

            jsonFilePath = dirPath + listData[i] + ".json"
            json_open = open(jsonFilePath, 'r')
            json_load = json.load(json_open)
            
            try:
                hoge = updateRaceData(json_load["race_info"])
                #print(hoge)
            except:
                count += 1

            # レースの出走馬ごとのデータ整形
            line = updateHorseData(json_load["race_order"],listData[i])

            json_open.close()
            i += 1

            save_row = {}
            for l1 in line:
                for k, vs in l1.items():
                    save_row[k] = vs
                writer.writerow(l1)
            print("\r"+str(i),end="")
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