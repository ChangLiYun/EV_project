import pandas as pd
import openpyxl  # 確保有安裝此套件

# 1. 定義「純文字」的路徑 (不要在這裡寫 read_excel)
ev_path = r'C:\Users\FM_pc\Desktop\專\油價與EV銷售_年均.xlsx'
oil_path = r'C:\Users\FM_pc\Desktop\專\2010_2026國際原油價格.xlsx'

try:
    # 2. 執行讀取 (傳入的是路徑字串)
    # 讀 EV 
    ev_df = pd.read_excel(ev_path, sheet_name=0)

    # 讀取油價資料 (處理 N/A 並讀取第一個工作表)
    oil_df = pd.read_excel(oil_path, sheet_name=0, na_values=['N/A'])

    print("--- 讀取成功 ---")
    # print(f"EV 資料: {len(ev_df)} 筆, 欄位: {ev_df.columns.tolist()}")
    # print(f"油價資料: {len(oil_df)} 筆, 欄位: {oil_df.columns.tolist()}")
    print(ev_df)

except FileNotFoundError:
    print("錯誤：找不到檔案，請確認路徑或檔名是否完全符合（包含副檔名）。")
except Exception as e:
    print(f"發生其他錯誤: {e}")

