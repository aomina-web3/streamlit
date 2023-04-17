import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('Streamlit テスト')

st.write('Interactive Widgets')

st.write('プログレスバーの表示')
'Start!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration{i+1}')
    bar.progress(i+1)
    time.sleep(0.1)
'Done!!!'

left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラム')

expander1 = st.expander('問い合わせ1')
expander1.write('問い合わせ1内容を書く')
expander2 = st.expander('問い合わせ2')
expander2.write('問い合わせ2内容を書く')
expander3 = st.expander('問い合わせ3')
expander3.write('問い合わせ3内容を書く')

#text = st.sidebar.text_input('あなたの趣味を教えて下さい。')
#condition = st.sidebar.slider('あなたの今の調子は？', 0,10,5)

text = st.text_input('あなたの趣味を教えて下さい。')
'あなたの趣味は：', text

condition = st.slider('あなたの今の調子は？', 0,10,5)
'コンディション：', condition

option = st.selectbox(
    'あなたが好きな数字を教えて下さい',
    list(range(1,11))
)

'あなたの好きな数字は',option,'です。'

if st.checkbox('Show Image'):
    st.write('Display Image')
    img = Image.open('sample.png')
    st.image(img, caption='Butsuryu-DAO', use_column_width=True)



df = pd.DataFrame(
    np.random.rand(100,2)/(50,50)+(35.69,139.70),
    columns=["lat","lon"]
)

st.map(df)
st.write(df)

df = pd.DataFrame(
    np.random.rand(20,3),
    columns={"a","b","c"}
)
st.write(df)
st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)

"""
# 章
## 節
### 項

```python
import streamlit as st
import numpy as np
import pandas as pd
```
"""

st.write('DataFrame')

df = pd.DataFrame({
    '1列目': [1,2,3,4],
    '2列目': [10,20,30,40]
})

st.write(df)

st.dataframe(df.style.highlight_max(axis=0), width=200, height=200)

st.table(df.style.highlight_max(axis=0))