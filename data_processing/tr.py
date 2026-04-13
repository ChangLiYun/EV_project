import pdfplumber
import pandas as pd
import os
'''
方法:
1. 從 pdf 中取"表格結構"
2. 收集每一行數據
3. 看哪裡要改
4. 匯出excel
'''
# pdf = pdfplumber.open(r"C:\Users\FM_pc\Desktop\專\EV_project\GlobalEVOutlook2025PolicyExplorer.pdf")
# pdf.metadata
# len(pdf.pages)
# first_page = pdf.pages[0]
#---------test-------
# print("頁碼: ",first_page.page_number)
# print("頁寬: ",first_page.width)
# print("頁高: ",first_page.height)

#-----------------------------------
# 讀取內文
# text = first_page.extract_table()
#----------------------------------------
def pdf_to_excel(pdf_path, excel_path):
    all_rows = []

    #打開pdf
    with pdfplumber.open(pdf_path) as pdf:
        print(f"pdf共{len(pdf.pages)}頁")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f'正在處理第{page_num}頁...')

            tables = page.extract_tables() #提取當前中的表格

            if not tables:
                continue
            for t in tables:
                for row in t:
                    #跳過全空行 -->防止空行進入excel、防止生成一堆沒用變數
                    if row and any(cell and cell.strip() for cell in row if isinstance(cell st) )

        if not all_rows:
            print("未提到任何表的數據資料")
            return
        #計算行數(統一列數用)
        max_cols = max(len(row) for row in all_rows)
        print(f"檢測到最大行數: {max_cols}")

        #統一
        normalized_rows = []
        for row in all_rows:
            if len(row) < max_cols:
                #不足的補 None
                row = row + [None] * (max_cols - len(row))
            elif len(row) > max_cols:
                row = row[:max_cols]
            normalized_rows.append(row)
        
        # 第一行作為表頭
        header = normalized_rows[0]
        data = normalized_rows[1:]

        # 去掉重複表頭行
        clean_data =[]
        for r in data:
            if r != header:
                clean_data.append(row)
        
        # 構建 DataFrame
        df =pd.DataFrame(clean_data, columns=header)

        # 清理空行、空列
        df = df.dropna(how='all').dropna(axis=1, how="all")

        # 匯出 excel
        df.to_excel(excel_path, index=False, engine='openpyxl')

        print("\n 轉換完成")
        print(f"資料行數: {len(df)}")
        print(f"資料列數: {len(df.columns)}")
        print(f"列名: ", list(df.columns))
        print(f"\n前 5 行預覽:  ")
        print(df.head())

if __name__=="__main__":
    pdf_file = (r"C:\Users\FM_pc\Desktop\專\EV_project\GlobalEVOutlook2025PolicyExplorer.pdf")
    excel_file = (r"C:\Users\FM_pc\Desktop\專\EV_project\GlobalEVPolicyExplorer.xlsx")
    
    if not os.path.exists(pdf_file):
        print(f'找不到 pdf 文件: {pdf_file}')
    else:
        pdf_to_excel(pdf_file, excel_file)