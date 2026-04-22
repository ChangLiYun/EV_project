import pdfplumber
import pandas as pd
import os
import re


def pdf_to_excel(pdf_path, excel_path):
    # 已知的分類值
    regions = [
        "Europe", "Africa", "Asia Pacific", "Central and South America",
        "North America", "Southeast Asia", "Middle East", "Eurasia"
    ]
    levels = ["National", "Subnational", "Supranational", "Multi-national"]
    policy_types = ["Legislation", "Proposal", "Announced target", "Objective"]

    all_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF 共 {len(pdf.pages)} 頁")

        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"正在處理第 {page_num} 頁...")
            text = page.extract_text()
            if text:
                all_text += text + "\n"

    # 逐行解析
    lines = [l.strip() for l in all_text.split('\n') if l.strip()]

    records = []
    current = None

    skip_lines = [
        "Global EV Outlook 2025 Policy Explorer",
        "Region Country / Economy Policy Level Policy Type"
    ]

    for line in lines:
        # 跳過標題行和頁碼行
        if any(skip in line for skip in skip_lines):
            continue
        if re.match(r'^Page \d+ of \d+$', line):
            continue

        # 判斷是否是新記錄的開頭
        found_region = None
        for region in regions:
            if line.startswith(region + " "):
                found_region = region
                break

        if found_region:
            # 儲存上一條記錄
            if current and current.get('國家'):
                records.append(current)

            rest = line[len(found_region):].strip()

            # 找政策層級
            found_level = None
            found_country = None
            for level in levels:
                if level in rest:
                    idx = rest.index(level)
                    found_country = rest[:idx].strip()
                    rest = rest[idx + len(level):].strip()
                    found_level = level
                    break

            # 找政策類型
            found_type = None
            for pt in policy_types:
                if rest.startswith(pt):
                    found_type = pt
                    rest = rest[len(pt):].strip()
                    break

            current = {
                '地區': found_region,
                '國家': found_country or '',
                '政策層級': found_level or '',
                '政策類型': found_type or '',
                '政策內容': rest,
                '年份': ''
            }

        elif current:
            # 繼續累積政策內容
            current['政策內容'] += ' ' + line

    # 儲存最後一筆
    if current and current.get('國家'):
        records.append(current)

    if not records:
        print("未解析到任何資料")
        return

    # 從政策內容提取年份
    for r in records:
        years = re.findall(r'\b(20\d{2})\b', r['政策內容'])
        if years:
            r['年份'] = years[0]  # 取第一個年份

    # 建立 DataFrame
    df = pd.DataFrame(records)
    df = df[df['國家'] != '']  # 移除空白國家

    # 匯出 Excel
    df.to_excel(excel_path, index=False, engine='openpyxl')

    print(f"\n轉換完成！")
    print(f"總計 {len(df)} 筆政策記錄")
    print(f"涵蓋國家數：{df['國家'].nunique()}")
    print(f"欄位：{list(df.columns)}")
    print(f"\n前 5 行預覽：")
    print(df[['國家', '政策類型', '年份', '政策內容']].head().to_string(index=False))


if __name__ == "__main__":
    pdf_file = r"D:\Users\User\Desktop\專題\EV_project\GlobalEVOutlook2025PolicyExplorer.pdf"
    excel_file = r"D:\Users\User\Desktop\專題\EV_project\GlobalEVPolicyExplorer.xlsx"

    if not os.path.exists(pdf_file):
        print(f"找不到 PDF 檔案：{pdf_file}")
    else:
        pdf_to_excel(pdf_file, excel_file)