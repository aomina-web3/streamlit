import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



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
    ('部分一致', '完全一致', '前方一致', '後方一致'))

    option3 = st.selectbox(
    '(毒劇物 検索項目)',
    ('官報公示名', '化学物質（例）', 'CAS', '分類', '規定'))

    submitted = st.form_submit_button("検索")
     
     
if submitted:
    with st.spinner("検索中です..."):
        time.sleep(2)
    username = st.secrets["mongo"]["username"]
    password = st.secrets["mongo"]["password"]
    host1 = st.secrets["mongo"]["host1"]

    uri = "mongodb+srv://"+username+":"+password+"@"+host1+".mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))



    db2 = client.dokugeki
    collection = db2.posts

    if option2 == '部分一致':
        cust_df = pd.DataFrame.from_records(collection.find(filter={option3:{'$regex':name}}))
    elif option2 == '前方一致':
        name2 = "^"+name
        st.subheader(name2)
        cust_df = pd.DataFrame.from_records(collection.find(filter={option3:{'$regex':name2}}))
    elif option2 == '後方一致':
        name2 = name+"$"
        st.subheader(name2)
        cust_df = pd.DataFrame.from_records(collection.find(filter={option3:{'$regex':name2}}))
    else: # '完全一致'
        cust_df = pd.DataFrame.from_records(collection.find(filter={option3:name}))

    cust_df = pd.DataFrame.from_records(collection.find(filter={option3:{'$regex':name}}))
    # cust_df = pd.DataFrame.from_records(collection.find(filter={option3:name2}))
    # cust_df_s = cust_df.set_index('日付', drop=True).drop('_id', axis=1).sort_index()
    cust_df_s = cust_df.sort_index()

    
    st.text(option2)  
    st.text(option1)
    st.write(cust_df_s)

