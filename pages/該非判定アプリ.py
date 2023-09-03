import streamlit as st
import numpy as np
import pandas as pd
# from PIL import Image
# import time
# from st_aggrid import AgGrid, GridUpdateMode
# from st_aggrid.grid_options_builder import GridOptionsBuilder

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

st.title('該非判定アプリ プロトタイプ')


with st.sidebar:
    koban = st.radio(
    "項番を選択してください。",
    ('', '１．武器',
      '２．原子力',
      '３．化学兵器',
      '３の２．生物兵器',
      '４．ミサイル',
      '５．先端素材',
      '６．材料加工',
      '７．エレクトロニクス',
      '８．電子計算機',
      '９．通信',
      '１０．センサー',
      '１１．航法装置',
      '１２．海洋関連',
      '１３．推進装置',
      '１４．その他',
      '１５．機微品目'
      ))

if koban == '１．武器':
    st.write('## 第１項　武器')
elif koban == '２．原子力':
    st.write('## 第２項　原子力')
elif koban == '３．化学兵器':
    st.write('## 第３項　化学兵器')
elif koban == '３の２．生物兵器':
    st.write('## 第３項の２ 生物兵器')
elif koban == '４．ミサイル':
    st.write('## 第4項　ミサイル')
elif koban == '５．先端素材':
    st.write('## 第5項　先端素材')
elif koban == '６．材料加工':
    st.write('## 第6項　材料加工')
elif koban == '７．エレクトロニクス':
    st.write('## 第7項　エレクトロニクス')
elif koban == '８．電子計算機':
    st.write('## 第8項　電子計算機')
elif koban == '９．通信':
    st.write('## 第9項　通信')
elif koban == '１０．センサー':
    st.write('## 第10項　センサー')
elif koban == '１１．航法装置':
    st.write('## 第11項　航法装置')
elif koban == '１２．海洋関連':
    st.write('## 第12項　海洋関連')
elif koban == '１３．推進装置':
    st.write('## 第13項　推進装置')
elif koban == '１４．その他':
    st.write('## 第14項　その他')
elif koban == '１５．機微品目':
    st.write('## 第15項　機微品目')
else:
    st.write("You didn't select anything.")

option = st.selectbox(
    '利用するマトリクス表を選択してください。',
    ("2023/04","2023/01")
)

'現在のマトリクス表は',option,'のものです。'

'該当する項番を選択してください。'


username = st.secrets["mongo"]["username"]
password = st.secrets["mongo"]["password"]
host1 = st.secrets["mongo"]["host1"]

uri = "mongodb+srv://"+username+":"+password+"@"+host1+".mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db3 = client.gaihi
collection = db3.posts
df = pd.DataFrame.from_records(collection.find())
# 順番を入れ替えたい列を保持
target_col = "checkbox1"
df_target = df[target_col]
# 入れ替え対称の列を削除
df = df.drop(target_col, axis=1)
df = df.drop('_id', axis=1)
# 任意の場所に対象の列を挿入
df.insert(0, target_col, df_target)

df_cust = df.sort_index()

st.write('## Selected')
st.write('以下の項番が該当として選ばれました。')

# edited_df = st.data_editor(df_cust)

# checked_koban = edited_df.loc[edited_df["checkbox1"].idxmax()]
# st.markdown(f"Your checked list is **{checked_koban}** ")

st.data_editor(
    df_cust,
    column_config={
        "checkbox1": st.column_config.CheckboxColumn(
            "該当をチェック",
            help="Select your **favorite** widgets",
            default=False,
        )
    },
    disabled=["項番1", "項目1", "項番2", "項目2", "用語", "解説"],
    hide_index=True,
)

if st.button('登録'):
    st.write(koban, '登録しました。')
else:
    st.write('登録されていません')