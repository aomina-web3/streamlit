import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time


st.title('化学品検索システム プロトタイプ')


with st.form("my_form", clear_on_submit=False):
    name = st.text_input('(キーワード検索)')
    option1 = st.multiselect(
    label="(検索項目)",
    options=['CAS RN', '化審法番号', '安衛法番号', 'EC番号', '国連番号', 'HSコード', 'CHRIP_ID', '日化辞番号'],
    default=('CAS RN', '化審法番号')
    )
    option2 = st.selectbox(
    '(検索方法)',
    ('完全一致', '部分一致', '前方一致', '後方一致'))

    submitted = st.form_submit_button("検索")
     
     
if submitted:
    with st.spinner("検索中です..."):
        time.sleep(3)
    image = Image.open('search_result.png')
    st.subheader(name)
    st.image(image)
    st.text(option2)  
    st.text(option1)

