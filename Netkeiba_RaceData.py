# https://self-development.info/netkeiba%E3%82%92%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%E3%82%92%E8%A7%A3%E8%AA%AC%E3%80%90%E6%BA%96%E5%82%99%E7%B7%A8%E3%80%91/
# https://self-development.info/netkeiba%e3%81%aeweb%e3%82%b9%e3%82%af%e3%83%ac%e3%82%a4%e3%83%94%e3%83%b3%e3%82%b0%e3%82%92python%e3%81%a7%e8%a1%8c%e3%81%86%e3%80%90%e7%ab%b6%e9%a6%ac%e9%96%8b%e5%82%ac%e6%97%a5%e3%81%ae%e6%8a%bd/
# 開催レースデータを作成する
# これをもとにデータURLを求める


import bs4
import traceback
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ドライバーのフルパス
CHROMEDRIVER = "C:\\chromedriver.exe"
# 改ページ（最大）
PAGE_MAX = 2
# 遷移間隔（秒）
INTERVAL_TIME = 2
# 対象年度
YEAR = [2016,2017,2018,2019,2020]

# ドライバー準備
def get_driver():
    # ヘッドレスモードでブラウザ起動
    options = Options()
    options.add_argument('--headless')

    # ブラウザを起動
    driver = webdriver.Chrome(CHROMEDRIVER,options=options)

    return driver

# 対象ページのソース取得
def get_source_from_page(driver, page):
    try:
        # ターゲット
        driver.get(page)
        # id="RaceTopRace"の要素が見つかるまで10秒は待つ
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'RaceTopRace')))
        page_source = driver.page_source
        
        return page_source
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None

# ソースからスクレイピングする
def get_data_from_source(src):
    # スクレイピングする
    soup = bs4.BeautifulSoup(src, features='lxml')
    try:
        info = []
        elem_base = soup.find(id="RaceTopRace")

        if elem_base:
            elems = elem_base.find_all("li", class_="RaceList_DataItem")
            for elem in elems:
                # 最初のaタグ
                a_tag = elem.find("a")
                if a_tag:
                    href = a_tag.attrs['href']
                    match2 = re.findall("\/race\/result.html\?race_id=(.*)&rf=race_list", href)
                    # match2 = re.findall("race_id=(.*)", href)
                    if len(match2) > 0:
                        item_id = match2[0]
                        info.append(item_id)
        return info
 
    except Exception as e:
 
        print("Exception\n" + traceback.format_exc())
 
        return None

# レースの日付リストを取得
def getRaceDate(dateListPath):
    raceDateList = []
    f = open(dateListPath, 'r')
    for line in f:
        raceDateList.append(line.replace("\n",""))
    f.close()
    return raceDateList

# 競馬開催日リストを作成するプログラム
# 標準出力されるため何かしらにアウトプットをすること
if __name__ == "__main__":

    raceDateListPath = "C:\\Users\\OBM2525\\Documents\\Workspace\\Netkeiba\\2016_2020_schedule.txt"
    
    raceDateList = getRaceDate(raceDateListPath)

    # ブラウザdriver取得
    driver = get_driver()

     # ページカウンター制御
    page_counter = 0
 
    for kaisai_date in raceDateList:
 
        page_counter = page_counter + 1
    
        # 対象ページURL
        page = "https://race.netkeiba.com/top/race_list.html?kaisai_date=" + str(kaisai_date)
        # ページのソース取得
        source = get_source_from_page(driver, page)

        # ソースからデータ抽出
        data = get_data_from_source(source)
        # データ保存
        # print(data)

        for line in data:
            print(line)
        # 間隔を設ける(秒単位）
        time.sleep(INTERVAL_TIME)
 
        # 改ページ処理を抜ける
        # if page_counter == PAGE_MAX:
        #     break

    # driverを閉じる
    driver.quit()