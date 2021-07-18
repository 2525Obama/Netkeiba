# https://self-development.info/netkeiba%E3%82%92%E3%82%B9%E3%82%AF%E3%83%AC%E3%82%A4%E3%83%94%E3%83%B3%E3%82%B0%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%E3%82%92%E8%A7%A3%E8%AA%AC%E3%80%90%E6%BA%96%E5%82%99%E7%B7%A8%E3%80%91/
# https://self-development.info/netkeiba%e3%81%aeweb%e3%82%b9%e3%82%af%e3%83%ac%e3%82%a4%e3%83%94%e3%83%b3%e3%82%b0%e3%82%92python%e3%81%a7%e8%a1%8c%e3%81%86%e3%80%90%e7%ab%b6%e9%a6%ac%e9%96%8b%e5%82%ac%e6%97%a5%e3%81%ae%e6%8a%bd/
# 0.競馬開催日を求めるプログラム
# 標準出力で出力されるので別に保存してください


import bs4
import traceback
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
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
        table = soup.find(class_="Calendar_Table")
 
        if table:
            elems = table.find_all("td", class_="RaceCellBox")
 
            for elem in elems:
                a_tag = elem.find("a")
 
                if a_tag:
                    href = a_tag.attrs['href']
                    match = re.findall("\/top\/race_list.html\?kaisai_date=(.*)$", href)
 
                    if len(match) > 0:
                        item_id = match[0]
                        info.append(item_id)
 
        return info
 
    except Exception as e:
        print("Exception\n" + traceback.format_exc())
 
        return None


# 競馬開催日リストを作成するプログラム
# 標準出力されるため何かしらにアウトプットをすること
if __name__ == "__main__":

    # ブラウザdriver取得
    driver = get_driver()
    page_counter = 0

    for year in YEAR:
        for month in range(1,13):
            page_counter = page_counter + 1
            # 対象ページURL
            page = "https://race.netkeiba.com/top/calendar.html?year=" + str(year) + "&month=" + str(month)
            # ページのソース取得
            source = get_source_from_page(driver, page)
            # ソースからデータ抽出
            data = get_data_from_source(source)

            for line in data:
                print(line)

            # 間隔を設ける(秒単位）
            time.sleep(INTERVAL_TIME)

    # driverを閉じる
    driver.quit()