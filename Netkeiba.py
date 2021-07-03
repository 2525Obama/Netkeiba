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