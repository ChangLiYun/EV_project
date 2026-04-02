import pandas as pd

# 1. 讀取下載的 IEA 政策檔
pams_df = pd.read_excel(r'C:\Users\FM_pc\Desktop\專\IEA_PAMS_Export.xlsx')

# 2. 清洗與標籤化 (針對地緣政治分析)
# 提取年份並篩選 2025 年以後的重點
pams_df['year'] = pd.to_numeric(pams_df['year'], errors='coerce')
recent_policies = pams_df[pams_df['year'] >= 2025].copy()

# 3. 新增分類標籤 (這在 Streamlit 篩選時很好用)
def policy_tag(title):
    title = str(title)
    if 'Carbon Tax' in title or '碳稅' in title: return '碳定價'
    if 'CAFE' in title or 'Standard' in title: return '排放規範'
    if 'Battery' in title or '電池' in title: return '供應鏈/儲能'
    return '轉型計畫'

recent_policies['分析分類'] = recent_policies['policyType'].apply(policy_tag)

# 4. 存成 CSV 準備匯入 SQL
recent_policies.to_csv(r'C:\Users\FM_pc\Desktop\專\Processed_IEA_Policies.csv', index=False, encoding='utf-8-sig')

print(f"整理完成！共有 {len(recent_policies)} 條 2025 年後的重點政策。")
