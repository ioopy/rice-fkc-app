import streamlit as st
from menu import menu_with_redirect
from utils.func import hide_header_icons
from utils.load_data import get_data
import pandas as pd
import plotly.graph_objects as go
import matplotlib.cm as cm
import matplotlib.colors as mcolors

st.set_page_config(page_title="Home")
menu_with_redirect()
hide_header_icons()

def build_hierarchical_dataframe(df, levels, value_column):
    df_list = []
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'marketplace'
        df_tree['value'] = dfg[value_column]
        # df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
        df_list.append(df_tree)
    total = pd.Series(dict(id='marketplace', parent='',value=df[value_column].sum()), name=0)
    df_list.append(total)
    df_all_trees = pd.concat(df_list, ignore_index=True)
    return df_all_trees

color_map = {
    'shopee': '#FE6132',  # Shopee color
    'lazada': '#0F0C76',  # Lazada color
}

def get_color_from_count(count):
    norm = mcolors.Normalize(vmin=df_all_trees['value'].min(), vmax=df_all_trees['value'].max())  # Normalize count values
    colormap = cm.get_cmap('RdBu')  # Color map to use (RdBu in this case)
    return mcolors.to_hex(colormap(norm(count)))  # Return hex color from the normalized count

def plot_sun_burst(data):
    fig = go.Figure(go.Sunburst(
        labels=data['id'],
        parents=data['parent'],
        values=data['value'],
        branchvalues='total',
        marker=dict(
            colors=data['color'],
            ),
        hovertemplate='<b>%{label} </b> <br> จำนวน: %{value}<br>',
        maxdepth=2
    ))

    fig.update_layout(
        width=300,  # Set width
        height=500,  # Set height
        margin = dict(t=5, l=10, r=10, b=10)
    )
    st.plotly_chart(fig, theme="streamlit")

st.title("MFU - เก็บข้อมูลผู้บริโภคข้าว")
st.write("")

data_all = get_data()
desc_msg = '''
    - **Shopee** เก็บข้อมูล ณ วันที่ 19/09/2567
    - **Lazada** เก็บข้อมูล ณ วันที่ 24/09/2567
'''
st.markdown(desc_msg)
with open("data/rice-mfu.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="📄 Export Report",
                    data=PDFbyte,
                    file_name="rice-online-market.pdf",
                    mime='application/octet-stream')

grouped_data = data_all[['marketplace', 'product_nm']]
grouped_data = grouped_data.groupby(['marketplace', 'product_nm']).size().reset_index(name='count')
grouped_data.rename(columns={'product_nm': 'keywords'}, inplace=True)

levels = ['keywords', 'marketplace'] # levels used for the hierarchical chart
value_column = 'count'
df_all_trees = build_hierarchical_dataframe(grouped_data, levels, value_column)
df_all_trees['color'] = df_all_trees['id'].map(color_map).fillna(df_all_trees['value'].apply(get_color_from_count))

col1, col2 = st.columns([1,1])
with col1:
    st.dataframe(grouped_data, hide_index=True)
with col2:
    plot_sun_burst(df_all_trees)

st.write("**Data**")
data_all = data_all[['product_nm', 'marketplace', 'province', 'star_review', 'original_price', 'discount_price_format', 'amount_sold_format']]
data_all.rename(columns={'product_nm': 'Keywords', 'province': 'จังหวัด', 'star_review': 'คะแนนรีวิว', 'original_price': 'ราคาก่อนลด (฿)', 'discount_price_format': 'ราคาหลังหักส่วนลด (฿)','amount_sold_format': 'ยอดขาย (ชิ้น)', 'total_value': 'ยอดขาย'}, inplace=True)
st.dataframe(data_all, hide_index=True)



