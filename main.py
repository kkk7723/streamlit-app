import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# タイトル
st.title("SQLite データビューア with 拡張機能")

# データベースファイルのパス
db_path = "gigaslot.db"

# SQLiteデータベースに接続
try:
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM processed_data"
    df = pd.read_sql_query(query, conn)

    # データフレームを表示
    st.subheader("データフレーム")
    st.dataframe(df)

    # データの概要表示
    st.subheader("データの概要")
    st.write(df.describe())

    # 列の選択機能
    st.subheader("列の選択")
    columns = st.multiselect("表示する列を選択してください", df.columns.tolist())
    if columns:
        st.dataframe(df[columns])
    else:
        st.dataframe(df)

    # 検索機能
    st.subheader("データ検索")
    filter_value = st.text_input("フィルタリングする値を入力してください")
    if filter_value:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(filter_value).any(), axis=1)]
        st.dataframe(filtered_df)

    # データ可視化
    st.subheader("データの可視化")
    column_to_plot = st.selectbox("グラフ化する列を選択してください", df.columns)
    if column_to_plot:
        fig, ax = plt.subplots()
        df[column_to_plot].hist(ax=ax, bins=20)
        ax.set_title(f"ヒストグラム: {column_to_plot}")
        st.pyplot(fig)

except Exception as e:
    st.error(f"エラーが発生しました: {e}")

finally:
    conn.close()
