import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image


st.title('化学品検索システム プロトタイプ')


keyword = st.text_input('(キーワード検索)', 'Input something...')
st.write('The current searching is', keyword)

option1 = st.multiselect(
    label="(検索項目)",
    options=['CAS RN', '化審法番号', '安衛法番号', 'EC番号', '国連番号', 'HSコード', 'CHRIP_ID', '日化辞番号'],
    default=('CAS RN', '化審法番号')
    )

option2 = st.selectbox(
    '(検索方法)',
    ('完全一致', '部分一致', '前方一致', '後方一致'))
st.write('You selected:', option2)

if st.button('検索'):
    st.write(keyword, 'を', option2, 'で検索中です・・・')
else:
    st.write('検索ボタンを押して下さい。')