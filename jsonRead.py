import json
import pandas as pd
import pyodbc

dirPath = "C:\\Users\\OBM2525\\Documents\\Data\\"
listDataPath = "2016_2020_R2.txt"


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
    listData = "C:\\Users\\OBM2525\\Documents\\Workspace\\Netkeiba\\2016_2020_R2.txt"

    listData = []
    payOut = []

    f = open(listDataPath,"r")
    for line in f:
        listData.append(line.replace("\n",""))
    f.close()

    print("Read RaceList... OK!")

    jsonFilePath = dirPath + listData[0] + ".json"
    json_open = open(jsonFilePath, 'r')

    json_load = json.load(json_open)
    json_load["race_info"]["ID"] = listData[0]

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