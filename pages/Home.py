import streamlit as st
from menu import menu_with_redirect
from utils.func import hide_header_icons
from utils.load_data import get_data

st.set_page_config(page_title="Home")
menu_with_redirect()
hide_header_icons()

st.title("MFU - เก็บข้อมูลผู้บริโภคข้าว")
st.write("")

data_all = get_data()
desc_msg = '''
    - **Shopee** เก็บข้อมูล ณ วันที่ 19/09/2567
    - **Lazada** เก็บข้อมูล ณ วันที่ 24/09/2567
'''
st.markdown(desc_msg)

grouped_data = data_all[['marketplace', 'product_nm']]
grouped_data = grouped_data.groupby(['marketplace', 'product_nm']).size().reset_index(name='count')
grouped_data.rename(columns={'product_nm': 'keywords'}, inplace=True)
st.dataframe(grouped_data, hide_index=True)
st.write("**Data**")
data_all = data_all[['product_nm', 'marketplace', 'province', 'star_review', 'original_price', 'discount_price_format', 'amount_sold_format']]
st.dataframe(data_all, hide_index=True)

# with open("data/doh-clay.pdf", "rb") as pdf_file:
#     PDFbyte = pdf_file.read()

# st.download_button(label="📄 Export Report",
#                     data=PDFbyte,
#                     file_name="doh-clay.pdf",
#                     mime='application/octet-stream')