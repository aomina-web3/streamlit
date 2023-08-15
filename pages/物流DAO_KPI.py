import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


username = st.secrets["mongo"]["username"]
password = st.secrets["mongo"]["password"]

uri = "mongodb+srv://"+username+":"+password+"@clusterbutsuryudao.whxfjnx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.BD_KPI
collection = db.posts
cust_df = pd.DataFrame.from_records(collection.find())
cust_df_s = cust_df.set_index('日付', drop=True).drop('_id', axis=1).sort_index()
cust_df_s2 = cust_df_s.drop('連番', axis=1).sort_index()

last = collection.find_one(
        sort=[('連番', -1)] 
    )
sanka = value = last['参加者']
Bnote = value = last['物流note記事数']
renban = value = last['連番']-1

last2 = collection.find_one(
    {'連番': renban}
    )
sanka2 = value = last2['参加者']
Bnote2 = value = last2['物流note記事数']

dif_sanka = sanka - sanka2
dif_Bnote = Bnote - Bnote2

st.title('物流DAO KPI')

st.write('こちらは物流DAOのKPIを確認できるサイトです。')

col1, col2= st.columns(2)
col1.metric("参加者", sanka, dif_sanka)
col2.metric("物流note記事数", Bnote, dif_Bnote)

st.write('from mongoDB')
st.write(cust_df_s2)

st.line_chart(cust_df_s2)

