# ClearanceDesk.py
# Streamlit Wireframe: 通関MVP（Python 3.8 対応クリーンアップ版）
# run: streamlit run ClearanceDesk.py

import streamlit as st
import pandas as pd
from datetime import date
from typing import Optional, Dict, Any

st.set_page_config(page_title="Clearance Desk", layout="wide")

# ----------------------------
# Session State init
# ----------------------------
def init_state() -> None:
    if "page" not in st.session_state:
        st.session_state.page = "案件一覧"
    if "selected_case_id" not in st.session_state:
        st.session_state.selected_case_id = None

    if "cases" not in st.session_state:
        st.session_state.cases = pd.DataFrame(
            [
                {
                    "案件ID": "C-0001",
                    "申告番号(仮)": "N/A",
                    "MAWB/B/L": "123-45678901",
                    "輸送": "航空",
                    "取卸港": "NRT",
                    "到着日": str(date.today()),
                    "ステータス": "作業中",
                },
                {
                    "案件ID": "C-0002",
                    "申告番号(仮)": "N/A",
                    "MAWB/B/L": "B/L ABCD-9999",
                    "輸送": "海上",
                    "取卸港": "TYO",
                    "到着日": str(date.today()),
                    "ステータス": "要確認",
                },
            ]
        )

    # case_id -> dict
    if "case_master" not in st.session_state:
        st.session_state.case_master = {}  # type: Dict[str, Dict[str, Any]]

    # case_id -> df
    if "case_items" not in st.session_state:
        st.session_state.case_items = {}  # type: Dict[str, pd.DataFrame]

    # case_id -> dict
    if "case_checks" not in st.session_state:
        st.session_state.case_checks = {}  # type: Dict[str, Dict[str, Any]]

init_state()

# ----------------------------
# Helpers
# ----------------------------
def get_or_create_case_master(case_id: str) -> Dict[str, Any]:
    if case_id not in st.session_state.case_master:
        st.session_state.case_master[case_id] = {
            "申告種別": "輸入",
            "課税": "消費税あり",
            "輸送形態": "航空",
            "積出国": "",
            "積出港": "",
            "取卸港": "",
            "到着日": str(date.today()),
            "輸入者名": "",
            "輸入者住所": "",
            "仕出人名": "",
            "仕出人住所": "",
            "AWB番号": "",
            "MAWB番号": "",
            "備考": "",
        }
    return st.session_state.case_master[case_id]


def get_or_create_items(case_id: str) -> pd.DataFrame:
    if case_id not in st.session_state.case_items:
        st.session_state.case_items[case_id] = pd.DataFrame(
            columns=[
                "行",
                "品名(原文)",
                "品名(和訳)",
                "HSコード",
                "原産国",
                "数量",
                "単位",
                "単価",
                "金額",
                "課税価格(円)",
                "備考",
            ]
        )
    return st.session_state.case_items[case_id]


def get_or_create_checks(case_id: str) -> Dict[str, Any]:
    if case_id not in st.session_state.case_checks:
        st.session_state.case_checks[case_id] = {
            "輸入規制対象": False,
            "他法令該当": False,
            "EPA適用": False,
            "関税率メモ": "",
            "消費税区分": "課税",
            "要確認フラグ": False,
            "コメント": "",
        }
    return st.session_state.case_checks[case_id]


def header_case_context(case_id: str) -> None:
    m = get_or_create_case_master(case_id)
    st.markdown(
        """
        <div style="padding:10px 12px;border:1px solid #eee;border-radius:10px;">
        <b>案件ID:</b> {case_id}　
        <b>申告種別:</b> {shinkoku}　
        <b>課税:</b> {kazei}　
        <b>輸送形態:</b> {yuso}　
        <b>取卸港:</b> {port}　
        <b>到着日:</b> {arrival}
        </div>
        """.format(
            case_id=case_id,
            shinkoku=m.get("申告種別", ""),
            kazei=m.get("課税", ""),
            yuso=m.get("輸送形態", ""),
            port=m.get("取卸港", ""),
            arrival=m.get("到着日", ""),
        ),
        unsafe_allow_html=True,
    )
    st.write("")


def goto(page: str, case_id: Optional[str] = None) -> None:
    st.session_state.page = page
    if case_id is not None:
        st.session_state.selected_case_id = case_id
    # rerun は streamlit 1.x でOK
    st.rerun()


def safe_case_ids() -> list:
    df = st.session_state.cases
    if df is None or df.empty:
        return []
    return df["案件ID"].tolist()


def ensure_selected_case() -> None:
    ids = safe_case_ids()
    if not ids:
        st.session_state.selected_case_id = None
        return
    if st.session_state.selected_case_id not in ids:
        st.session_state.selected_case_id = ids[0]

# ----------------------------
# Sidebar Navigation
# ----------------------------
with st.sidebar:
    st.title("Clearance Desk")
    st.caption("通関MVP / Wireframe（Python 3.8対応）")

    pages = ["案件一覧", "案件基本情報", "インボイス&明細", "該非・税率チェック", "申告プレビュー"]
    if st.session_state.page not in pages:
        st.session_state.page = "案件一覧"

    nav = st.radio("画面", pages, index=pages.index(st.session_state.page))
    st.session_state.page = nav

    st.divider()

    ensure_selected_case()
    st.subheader("案件選択")
    ids = safe_case_ids()

    if not ids:
        st.info("案件がありません。新規案件を作成してください。")
        if st.button("＋新規案件"):
            new_id = "C-0001"
            st.session_state.cases = pd.DataFrame(
                [
                    {
                        "案件ID": new_id,
                        "申告番号(仮)": "N/A",
                        "MAWB/B/L": "",
                        "輸送": "航空",
                        "取卸港": "",
                        "到着日": str(date.today()),
                        "ステータス": "作業中",
                    }
                ]
            )
            st.session_state.selected_case_id = new_id
            goto("案件基本情報", new_id)
    else:
        picked = st.selectbox(
            "案件ID",
            ids,
            index=ids.index(st.session_state.selected_case_id) if st.session_state.selected_case_id in ids else 0,
        )
        st.session_state.selected_case_id = picked

        if st.button("＋新規案件"):
            new_id = "C-{0:04d}".format(len(st.session_state.cases) + 1)
            st.session_state.cases = pd.concat(
                [
                    st.session_state.cases,
                    pd.DataFrame(
                        [
                            {
                                "案件ID": new_id,
                                "申告番号(仮)": "N/A",
                                "MAWB/B/L": "",
                                "輸送": "航空",
                                "取卸港": "",
                                "到着日": str(date.today()),
                                "ステータス": "作業中",
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )
            st.session_state.selected_case_id = new_id
            goto("案件基本情報", new_id)

# ----------------------------
# Page: 案件一覧
# ----------------------------
def page_cases() -> None:
    st.header("案件一覧")

    colA, colB, colC = st.columns([2, 2, 2])
    with colA:
        q = st.text_input("検索（案件ID / MAWB/B/L / ステータス）", "")
    with colB:
        status = st.selectbox("ステータス絞り込み", ["(すべて)", "作業中", "要確認", "完了"], index=0)
    with colC:
        st.write("")
        st.write("")
        if st.button("選択案件を開く"):
            if st.session_state.selected_case_id is not None:
                goto("案件基本情報", st.session_state.selected_case_id)

    df = st.session_state.cases.copy()

    if q.strip():
        # contains match across row values
        mask = df.apply(lambda r: q in " ".join([str(v) for v in r.values]), axis=1)
        df = df[mask]
    if status != "(すべて)":
        df = df[df["ステータス"] == status]

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("※ 最短で作業案件に入るための一覧画面（MVP）")

# ----------------------------
# Page: 案件基本情報
# ----------------------------
def page_master() -> None:
    case_id = st.session_state.selected_case_id
    st.header("案件基本情報")

    if case_id is None:
        st.warning("案件が選択されていません。左メニューから案件を選んでください。")
        return

    header_case_context(case_id)
    m = get_or_create_case_master(case_id)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.subheader("通関条件")
        m["申告種別"] = st.selectbox("申告種別", ["輸入", "輸出"], index=0 if m["申告種別"] == "輸入" else 1)
        m["課税"] = st.selectbox("課税", ["消費税あり", "消費税なし"], index=0 if m["課税"] == "消費税あり" else 1)
        m["輸送形態"] = st.selectbox("輸送形態", ["航空", "海上"], index=0 if m["輸送形態"] == "航空" else 1)
        m["積出国"] = st.text_input("積出国", m["積出国"])
        m["積出港"] = st.text_input("積出港", m["積出港"])
        m["取卸港"] = st.text_input("取卸港", m["取卸港"])
        m["到着日"] = st.text_input("到着日（YYYY-MM-DD）", m["到着日"])

    with right:
        st.subheader("当事者情報")
        m["輸入者名"] = st.text_input("輸入者名", m["輸入者名"])
        m["輸入者住所"] = st.text_area("輸入者住所", m["輸入者住所"], height=90)
        m["仕出人名"] = st.text_input("仕出人名", m["仕出人名"])
        m["仕出人住所"] = st.text_area("仕出人住所", m["仕出人住所"], height=90)

        st.subheader("運送番号")
        m["AWB番号"] = st.text_input("AWB番号", m["AWB番号"])
        m["MAWB番号"] = st.text_input("MAWB番号", m["MAWB番号"])
        m["備考"] = st.text_area("備考", m["備考"], height=90)

    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("→ インボイス&明細へ"):
            goto("インボイス&明細", case_id)
    with c2:
        if st.button("ステータス：要確認にする"):
            st.session_state.cases.loc[st.session_state.cases["案件ID"] == case_id, "ステータス"] = "要確認"
            st.success("更新しました")
    with c3:
        if st.button("ステータス：完了にする"):
            st.session_state.cases.loc[st.session_state.cases["案件ID"] == case_id, "ステータス"] = "完了"
            st.success("更新しました")

# ----------------------------
# Page: インボイス&明細
# ----------------------------
def page_items() -> None:
    case_id = st.session_state.selected_case_id
    st.header("インボイス & 明細入力")

    if case_id is None:
        st.warning("案件が選択されていません。左メニューから案件を選んでください。")
        return

    header_case_context(case_id)

    st.subheader("書類アップロード（MVP: 保存→目視→修正の導線）")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.file_uploader("インボイスPDF/画像", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=False)
    with col2:
        st.file_uploader("パッキングリストPDF/画像", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=False)

    st.caption("※ 自動抽出は後で差し替え可能。いまは『アップ→修正』を最短に。")

    st.divider()

    if st.button("自動抽出（ダミー）"):
        df = get_or_create_items(case_id)
        if df.empty:
            df = pd.DataFrame(
                [
                    {
                        "行": 1,
                        "品名(原文)": "Sample Item A",
                        "品名(和訳)": "サンプルA",
                        "HSコード": "0000.00",
                        "原産国": "CN",
                        "数量": 10,
                        "単位": "PCS",
                        "単価": 5.0,
                        "金額": 50.0,
                        "課税価格(円)": "",
                        "備考": "",
                    }
                ]
            )
            st.session_state.case_items[case_id] = df
        st.success("ダミー抽出を反映しました（編集して使ってください）")

    st.subheader("明細テーブル（編集可）")
    df = get_or_create_items(case_id)

    if not df.empty and "行" in df.columns:
        df = df.copy()
        df["行"] = list(range(1, len(df) + 1))

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="editor_{0}".format(case_id),
    )
    st.session_state.case_items[case_id] = edited

    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("→ 該非・税率チェックへ"):
            goto("該非・税率チェック", case_id)
    with c2:
        st.download_button(
            "CSVダウンロード（明細）",
            data=edited.to_csv(index=False).encode("utf-8-sig"),
            file_name="{0}_items.csv".format(case_id),
            mime="text/csv",
        )
    with c3:
        st.caption("※ MVPでは“HS候補表示”“整合チェック”は後付けでOK")

# ----------------------------
# Page: 該非・税率チェック
# ----------------------------
def page_checks() -> None:
    case_id = st.session_state.selected_case_id
    st.header("該非・税率・注意点チェック")

    if case_id is None:
        st.warning("案件が選択されていません。左メニューから案件を選んでください。")
        return

    header_case_context(case_id)
    chk = get_or_create_checks(case_id)

    left, right = st.columns([1, 1], gap="large")
    with left:
        st.subheader("チェック項目")
        chk["輸入規制対象"] = st.checkbox("輸入規制対象？", value=bool(chk["輸入規制対象"]))
        chk["他法令該当"] = st.checkbox("他法令該当？", value=bool(chk["他法令該当"]))
        chk["EPA適用"] = st.checkbox("EPA適用？", value=bool(chk["EPA適用"]))
        chk["消費税区分"] = st.selectbox(
            "消費税区分",
            ["課税", "非課税", "免税"],
            index=["課税", "非課税", "免税"].index(chk["消費税区分"]),
        )
        chk["要確認フラグ"] = st.checkbox("要確認フラグ", value=bool(chk["要確認フラグ"]))

    with right:
        st.subheader("税率/判断メモ")
        chk["関税率メモ"] = st.text_area("関税率・適用理由メモ", chk["関税率メモ"], height=140)
        chk["コメント"] = st.text_area("コメント（判断根拠・保留理由・確認先）", chk["コメント"], height=200)

    st.session_state.case_checks[case_id] = chk

    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("→ 申告プレビューへ"):
            goto("申告プレビュー", case_id)
    with c2:
        if st.button("ステータス反映"):
            st.session_state.cases.loc[
                st.session_state.cases["案件ID"] == case_id, "ステータス"
            ] = "要確認" if chk["要確認フラグ"] else "作業中"
            st.success("案件ステータスを更新しました")
    with c3:
        st.caption("※ MVPの価値はここ：コメントが残る→後でDAOナレッジ化できる")

# ----------------------------
# Page: 申告プレビュー（疑似NACCS）
# ----------------------------
def page_preview() -> None:
    case_id = st.session_state.selected_case_id
    st.header("申告プレビュー（疑似NACCS）")

    if case_id is None:
        st.warning("案件が選択されていません。左メニューから案件を選んでください。")
        return

    header_case_context(case_id)
    m = get_or_create_case_master(case_id)
    items = get_or_create_items(case_id)
    chk = get_or_create_checks(case_id)

    missing = []
    for k in ["取卸港", "輸入者名", "輸入者住所"]:
        if not str(m.get(k, "")).strip():
            missing.append(k)
    if items is None or items.empty:
        missing.append("明細（1行以上）")

    st.subheader("入力チェック")
    if missing:
        st.error("未入力があります: " + " / ".join(missing))
    else:
        st.success("必須項目は埋まっています（MVPレベル）")

    st.subheader("申告イメージ（表示のみ）")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 基本情報")
        st.write(
            {
                "申告種別": m.get("申告種別"),
                "課税": m.get("課税"),
                "輸送形態": m.get("輸送形態"),
                "積出国": m.get("積出国"),
                "積出港": m.get("積出港"),
                "取卸港": m.get("取卸港"),
                "到着日": m.get("到着日"),
            }
        )
        st.markdown("### 当事者")
        st.write(
            {
                "輸入者名": m.get("輸入者名"),
                "輸入者住所": m.get("輸入者住所"),
                "仕出人名": m.get("仕出人名"),
                "仕出人住所": m.get("仕出人住所"),
            }
        )

    with col2:
        st.markdown("### チェック結果")
        st.write(
            {
                "輸入規制対象": chk.get("輸入規制対象"),
                "他法令該当": chk.get("他法令該当"),
                "EPA適用": chk.get("EPA適用"),
                "消費税区分": chk.get("消費税区分"),
                "要確認フラグ": chk.get("要確認フラグ"),
            }
        )
        st.markdown("### コメント")
        st.info(chk.get("コメント") if chk.get("コメント") else "（未入力）")

    st.markdown("### 明細")
    st.dataframe(items, use_container_width=True, hide_index=True)

    st.divider()
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("← 明細に戻る"):
            goto("インボイス&明細", case_id)
    with c2:
        if st.button("申告準備完了（完了フラグ）"):
            st.session_state.cases.loc[st.session_state.cases["案件ID"] == case_id, "ステータス"] = "完了"
            st.success("完了にしました（送信はしません）")
    with c3:
        st.caption("※ 実運用ではこの後にNACCS入力/CSV出力/連携を追加")

# ----------------------------
# Router
# ----------------------------
if st.session_state.page == "案件一覧":
    page_cases()
elif st.session_state.page == "案件基本情報":
    page_master()
elif st.session_state.page == "インボイス&明細":
    page_items()
elif st.session_state.page == "該非・税率チェック":
    page_checks()
elif st.session_state.page == "申告プレビュー":
    page_preview()
else:
    st.write("Unknown page")