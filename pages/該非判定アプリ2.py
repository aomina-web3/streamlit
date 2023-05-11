import streamlit as st
import pandas as pd
from fpdf import FPDF

# マトリクス表を読み込む
matrix = pd.read_excel('matrix.xlsx')

# PDF出力用のクラスを作成する
class PDF(FPDF):
    def title(self, title):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', '', 12)
        self.cell(0, 6, title, 0, 1)

    def content(self, text):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, text)
        self.ln()

# 該非判定を行う関数を定義する
def is_applicable(section, item):
    row = matrix[(matrix['セクション'] == section) & (matrix['項目'] == item)]
    if len(row) == 0:
        return '不明'
    else:
        return row.iloc[0]['該非判定']

# Streamlitのアプリケーションを作成する
def main():
    # アプリケーションのタイトルを設定する
    st.title('経済産業省マトリクス表該非判定ツール')

    # セクションと項目を入力する
    section = st.text_input('セクションを入力してください')
    item = st.text_input('項目を入力してください')

    # 該非判定を実行する
    applicable = is_applicable(section, item)

    # 結果を表示する
    st.write('該非判定:', applicable)

    # PDF出力する
    if st.button('PDF出力'):
        pdf = PDF()
        pdf.add_page()
        pdf.title('該非判定結果')
        pdf.chapter_title('入力情報')
        pdf.content(f'セクション: {section}')
        pdf.content(f'項目: {item}')
        pdf.chapter_title('該非判定結果')
        pdf.content(f'該非判定: {applicable}')
        pdf.output('output.pdf')

if __name__ == '__main__':
    main()
