import requests
import pandas as pd
from datetime import datetime
import urllib3


url = "https://www2.moeaea.gov.tw/oil111/Home/GetCrudeOilPrice"

print(" 開始執行爬蟲程式...")

try:
    #  發送請求
    response = requests.get(url, headers=headers, timeout=15, verify=False)
    response.raise_for_status()

    #  解析與轉換
    raw_data = response.json()
    df = pd.DataFrame(raw_data)

    #  資料清洗
    if not df.empty:
        # 轉換日期格式
        df['FieldDate'] = pd.to_datetime(df['FieldDate'])
        # 排序：最新日期在前
        df = df.sort_values(by='FieldDate', ascending=False)

        # 5. 儲存 CSV
        file_name = f"International_Oil_Prices_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')

        print("-" * 30)
        print(f" 成功！檔案已存至桌面/專題資料夾: {file_name}")
        print(f" 預覽前三筆資料：\n{df.head(3)}")
    else:
        print("⚠ 抓取成功，但網站回傳的資料內容是空的。")

# --- 這是你剛才缺少的區塊 ---
except Exception as e:
    print("-" * 30)
    print(f" 程式執行失敗，錯誤原因：{e}")
    print("提示：請檢查網路連線，或確認網站 API 是否有變動。")
# --------------------------