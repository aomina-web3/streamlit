import streamlit as st
import pandas as pd
from PIL import Image



img = Image.open('butsuryudao_logo.png')
st.image(img, caption='Butsuryu-DAO', use_column_width=True)

st.title('物流DAOアプリ')
st.title('プロトタイプサイト')

st.write('物流DAOのプロトタイプアプリを試す事ができるサイトです。')
st.write('各アプリを確認するには左のサイドバーのメニュー">"からアプリを選択してください。')
