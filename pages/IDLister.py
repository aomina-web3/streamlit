import streamlit as st
import zipfile
import os
import tempfile
import pdfplumber
import pandas as pd
import re


st.title("📄 PDF帳票抽出ツール（35項目対応）")
st.markdown("ZIPファイル（PDF複数入り）をアップロードすると、必要な情報をCSVで出力します。")

# 正規表現パターン（35項目）
patterns = {
    "輸入許可日": r"(?:輸入許可日|審査終了日)[\s:：]*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})",
    "輸入申告番号": r"申\s*告\s*番\s*号[^\n]*\n[^\n]*?([0-9０-９]{3})(?:\s|\n|　|\-)*([0-9０-９]{4})(?:\s|\n|　|\-)*([0-9０-９]{4})",
    "荷送人": r"仕\s*出\s*人[\s:：\-]*([^\n]+)",
    "納税額合計": r"納税額合計[\s:：¥\\]*([\d,]+)",
    "インボイス番号": r"(FX[0-9]{4,}/[0-9A-Z]+)",
    "仕入書価格": r"A\s*-\s*CIF\s*-\s*USD\s*-\s*([\d\.]+)",
    "品名": r"品名[\s:：]*([^\n]+)",
    "原産国": r"原産地[\s:：]*([A-Z]+)",
    "仕入書番号": r"申告番号[\s:：]*([0-9 ]{10,})",
    "通関金額（CIF）": r"申告価格（ＣＩＦ）[\s:：¥\\]*([\d,]+)",
    "あて先税関": r"あて先税関[\s:：]*([A-Z]+)",
    "代理人": r"代理人[\s:：]*([^\n]+)",
    "貨物個数": r"貨物個数[\s:：]*([0-9]+)",
    "貨物重量": r"貨物重量[\s:：]*([\d\.]+)",
    "仕入書価格のターム": r"A\s*-\s*([A-Z]+)\s*-\s*USD\s*-\s*[\d\.]+",
    "通関金額の通貨": r"A\s*-\s*[A-Z]+\s*-\s*([A-Z]{3})\s*-\s*[\d\.]+",
    "申告番号": r"申告番号[\s:：]*([0-9 ]{10,})",
    "輸入者": r"輸\s*入\s*者[\s:：\-]*([^\n]+)",
    "輸入者住所": r"輸\s*入\s*者[\s:：\-]*[^\n]+\n([^\n]+)",
    "仕出人住所": r"仕\s*出\s*人[\s:：\-]*[^\n]+\n([^\n]+)",
    "AWB番号": r"ＡＷＢ番号[\s:：\-]*([^\n]+)",
    "MAWB番号": r"ＭＡＷＢ番号[\s:：\-]*([^\n]+)",
    "積出港": r"積\s*出\s*港[\s:：\-]*([^\n]+)",
    "取卸港": r"取\s*卸\s*港[\s:：\-]*([^\n]+)",
    "積載機名": r"載\s*機\s*名[\s:：\-]*([^\n]+)",
    "入港年月日": r"入港年月日[\s:：\-]*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2})",
    "関税": r"関税[\s:：¥\\]*([\d,]+)",
    "関税欄数": r"関税.*?欄数[\s:：\-]*([0-9]+)",
    "消費税": r"消費税[\s:：¥\\]*([\d,]+)",
    "消費税欄数": r"消費税.*?欄数[\s:：\-]*([0-9]+)",
    "地方消費税": r"地方消費税[\s:：¥\\]*([\d,]+)",
    "地方消費税欄数": r"地方消費税.*?欄数[\s:：\-]*([0-9]+)",
    "品目番号": r"品目番号[\s:：]*([A-Z0-9\-\.]+)",
    "関税率": r"関税率[\s:：]*([0-9\.]+%)",
    "記事(通関)": r"記事\(通関\)[\s:：\-]*([^\n]+)"
}

uploaded_zip = st.file_uploader("📦 PDFが入ったZIPファイルをアップロード", type="zip")

if uploaded_zip:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        # ZIPを解凍
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # # PDF処理
        # results = []
        # for root, _, files in os.walk(temp_dir):
        #     for file in files:
        #         if file.lower().endswith('.pdf'):
        #             file_path = os.path.join(root, file)
        #             with pdfplumber.open(file_path) as pdf:
        #                 text = "\n".join([p.extract_text() or "" for p in pdf.pages])
        #                 row = {"ファイル名": file}
        #                 for key, pattern in patterns.items():
        #                     match = re.search(pattern, text)
        #                     row[key] = match.group(1).strip() if match else ""
        #                 results.append(row)

        # PDF処理
        results = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    try: # Start of the error handling block
                        with pdfplumber.open(file_path) as pdf: # This is the line [1] where the error occurs
                            text = "\n".join([p.extract_text() or "" for p in pdf.pages])
                            row = {"ファイル名": file}
                            for key, pattern in patterns.items():
                                match = re.search(pattern, text)
                                row[key] = match.group(1).strip() if match else ""
                        results.append(row)
                    except Exception as e: # Catch any exception that occurs during PDF processing
                        st.warning(f"⚠️ Error processing file '{file}': {e}. Skipping this file.")
                         # You can choose to add a placeholder row for the problematic file
                         # For example:
                        # row = {"ファイル名": file, "Status": f"Error: {e}"}
                        # results.append(row)
                        continue # Continue to the next file in the loop

        df = pd.DataFrame(results)
        st.success(f"✅ {len(df)} 件のPDFから抽出しました。")
        st.dataframe(df)

        # CSV出力
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("⬇️ 抽出結果CSVをダウンロード", data=csv, file_name="pdf抽出一覧.csv", mime="text/csv")