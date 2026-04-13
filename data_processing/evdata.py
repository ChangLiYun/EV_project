import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import pandas as pd

# # 讀取 Excel，指定工作表
# df = pd.read_excel("EVDataExplorer2025.xlsx", sheet_name="GEVO_EV_2025")
#
# 用 Windows 驗證連線到 SQL Server
engine = create_engine(
    "mssql+pyodbc://localhost/EVProjectDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# # 把 DataFrame 匯入 SQL Server
# df.to_sql("ev_data", con=engine, if_exists="replace", index=False)
#----------------------------------------------------------------------
# # 讀 Excel
df = pd.read_excel(
    "EVDataExplorer2025.xlsx",
    sheet_name="EV sales countries",
    header=7,

)
# print(df)

# 展開(年份欄位)
df_long = df.melt(
    id_vars=["region_country"],
    var_name="year",
    value_name="sales"
)

# 處理 year 欄位
df_long["year"] = df_long["year"].astype(int)

# 控制 sales 精度：四捨五入到整數，允許 NaN
df_long["sales"] = df_long["sales"].round(0).astype("Int64")

# 匯入 SQL Server
df_long.to_sql("ev_sales_countries", con=engine, if_exists="replace", index=False)

#--------------------------------------------------------------------------------------------------------
df_macro = pd.read_excel(
    "EVDataExplorer2025.xlsx",
    sheet_name="EV sales macro regions",
    header=6  # 第 7 列當欄位名稱
)
# 填補 mode 欄位的空白值

df_macro["mode"] = df_macro["mode"].ffill()

df_macro_long = df_macro.melt(
    id_vars=["mode", "region_country"],
    var_name="year",
    value_name="sales"
)

df_macro_long["year"] = df_macro_long["year"].astype(int)
df_macro_long["sales"] = df_macro_long["sales"].round(0).astype("Int64")

# 匯入 SQL
df_macro_long.to_sql("ev_sales_macro", con=engine, if_exists="replace", index=False)
#--------------------------------------------------------------------------------------
df_other = pd.read_excel(
    "EVDataExplorer2025.xlsx",
    sheet_name="Other than sales and stock",
    header=6,
)

# 先補齊 mode 欄位
df_other["mode"] = df_other["mode"].ffill()

# 展開
df_other_long = df_other.melt(
    id_vars=["mode", "region_country"],
    var_name="year",
    value_name="indicator"
)

# 型別轉換
df_other_long["year"] = df_other_long["year"].astype(int)
df_other_long["indicator"] = pd.to_numeric(df_other_long["indicator"], errors="coerce").round().astype("Int64")


# 匯入 SQL
df_other_long.to_sql("other_than_sales_and_stock", con=engine, if_exists="replace", index=False)

#--檢查有哪些非數字
#mask = pd.to_numeric(df_other_long["indicator"], errors="coerce").isna()
#print(df_other_long.loc[mask, "indicator"].unique())
#--------------------------------------------------------------------------------------
df_r = pd.read_excel(
    "EVDataExplorer2025.xlsx",
    sheet_name="Regions and countries",
    header=0  # 第一列就是欄位名稱
)

# 匯入
from sqlalchemy.types import String

df_r.to_sql(
    "regions_and_countries",
    con=engine,
    if_exists="replace",
    index=False,
    dtype={
        "region_country": String(),
        "Agg_group": String()
    }
)


#--------------------------------------------------------------------------------------
# conn = pyodbc.connect(
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=localhost;"
#     "DATABASE=EVProjectDB;"
#     "Trusted_Connection=yes;"
# )
# cursor = conn.cursor()
#-------------------------------------------------------------------------------------
# 筆記:

#if_exists="replace" → 每次執行都會先刪掉舊的表格，再建立新的表格，然後把 DataFrame 的內容整批匯入。
# 👉 所以不會「重複寫入」，而是「覆蓋」。
#
# 如果用的是 if_exists="append" → 每次執行都會把 DataFrame 的資料加到表格後面，這樣就會重複寫入。

#  ffill() 填補 mode 欄位的空白值

# header → 指定哪一列是欄位名稱。
# skiprows → 指定要跳過哪些列。

#errors="coerce"：把非數字強制轉成 NaN（缺漏值），不會報錯。
#errors="ignore"：保留原始值，不做轉換。
#--------------------------------------------------------------------------------------
