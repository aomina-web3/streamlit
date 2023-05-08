import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('物流DAO KPI')

st.write('こちらは物流DAOのKPIを確認できるサイトです。')

col1, col2= st.columns(2)
col1.metric("参加者", "41", "12")
col2.metric("物流note記事数", "28", "3")

df = pd.DataFrame({
    '参加者':[1,7,16,20,29,41],
    '物流note記事数':[6,12,17,21,25,28]},
    index = pd.Index(["2212","2301","2302","2303","2304","2305"], name='日付')
)
st.write(df)
st.line_chart(df)

