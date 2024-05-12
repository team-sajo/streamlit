import pandas as pd
import streamlit as st

st.set_page_config(page_title="시각화어쩌구", layout='wide')

df = pd.read_excel("240510_df_2.xlsx")

st.dataframe(df, height=1500)
