import pandas as pd
from utils.func import convert_amount_sold
import os
import streamlit as st

def rename_columns(data):
    return data.rename(columns={'itemid': 'itemId', 'shopid': 'shopId'})

def format_sales_data(data):
    data['amount_sold_format'] = data['amount_sold'].apply(convert_amount_sold)
    data['discount_price_format'] = data['discount_price'].fillna(0)
    data['total_value'] = data['amount_sold_format'] * data['discount_price_format']
    data['per_discount_format'] = data['per_discount']
    if data['per_discount'].dtype == 'object':
        data['per_discount_format'] = data['per_discount'].str.replace('-', '').str.replace('%', '')
        data['per_discount_format'] = pd.to_numeric(data['per_discount_format'], errors='coerce')
    else:
        data['per_discount_format'] = data['per_discount']

    data['per_discount_format'].fillna(0, inplace=True)
    data['original_price'] = data['original_price'].mask((data['original_price'].isna()) | (data['original_price'] == 0), data['discount_price_format'])
    data['product_nm'] = data['product_nm'].str.replace('-', ' ').str.replace('_', ' ')
    data['province'] = data['province'].str.replace('China', 'ต่างประเทศ').str.replace('Loei', 'เลย').str.replace('Bangkok', 'กรุงเทพมหานคร').str.replace('Phrae', 'แพร่').str.replace('Surin', 'สุรินทร์')
    data['province'] = data['province'].str.replace('จังหวัด', '')
    return data

def format_star_review(data):
    data['star_review'].fillna(0, inplace=True)
    data['star_review'] = data['star_review'].apply(lambda x: f"{x:.1f}")
    data['star_review'] = pd.to_numeric(data['star_review'], errors='coerce')
    return data

@st.cache_data
def load_data(src):
    dataframes = []
    folder = f'data/{src}'
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder, filename)
            df = pd.read_csv(file_path)
            dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

@st.cache_data
def get_data():
    shopee_data = load_data("shopee")
    lazada_data = load_data("lazada")

    # Rename columns
    shopee_data = rename_columns(shopee_data)
    lazada_data = rename_columns(lazada_data)

    # Format sales and discount data
    shopee_data = format_sales_data(shopee_data)
    lazada_data = format_sales_data(lazada_data)

    # Format star reviews
    shopee_data = format_star_review(shopee_data)
    lazada_data = format_star_review(lazada_data)

    return pd.concat([shopee_data, lazada_data])

def clean_data(data):
    data = rename_columns(data)
    data = format_sales_data(data)
    data = format_star_review(data)
    return data
