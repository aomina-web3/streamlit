import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('物流DAO KPI')

st.write('こちらは物流DAOのKPIを確認できるサイトです。')


df = pd.DataFrame({
    '参加者':[1,7,16,20,29,41],
    '物流note記事数':[6,12,17,21,25,28]},
    index = pd.Index(["20221204","20230101","20230201","20230327","20230507","20230930"], name='日付')
)
st.write(df)
st.line_chart(df)
