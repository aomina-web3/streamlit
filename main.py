import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.title('該非判定アプリ テスト')


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
    st.write("You didn\'t select anything.")

option = st.selectbox(
    '利用するマトリクス表を選択してください。',
    ("2023/04","2023/01")
)

'現在のマトリクス表は',option,'のものです。'

'該当する項番を選択してください。'


data = {
    '該当項番': ['第1項(1)','第1項(2)','第1項(3)','第1項(4)'],
    '項目名': ['銃砲若しくはこれに用いる銃砲弾（発光又は発煙のために用いるものを含む。）若しくはこれらの附属品又はこれらの部分品',
           '爆発物（銃砲弾を除く。）若しくはこれを投下し、若しくは発射する装置若しくはこれらの附属品又はこれらの部分品',
           '火薬類（爆発物を除く。）又は軍用燃料',
           '火薬又は爆薬の安定剤']
}

df = pd.DataFrame(data)
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gridoptions = gd.build()

grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

st.write('## Selected')
st.write('以下の項番が該当として選ばれました。')
selected_row = grid_table["selected_rows"]
st.dataframe(selected_row)
