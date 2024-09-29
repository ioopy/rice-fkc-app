import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from menu import menu_with_redirect
from utils.func import break_page, get_head_title, hide_header_icons, section_title
from utils.load_data import get_data
import plotly.express as px
import numpy as np

menu_with_redirect()
hide_header_icons()
marketplace_colors = {
        'shopee': '#FE6132',
        'lazada': '#0F0C76 ',
}
def get_bar_plot(data, title, is_grop=False):
    if is_grop:
        data = data.sort_values(by=['marketplace', 'amount_sold_format'], ascending=[False, True])
        data.rename(columns={'amount_sold_format': 'ยอดขาย'}, inplace=True)
        fig = px.bar(
            data,
            x='ยอดขาย', 
            y='product_nm',
            color=data["marketplace"],
            color_discrete_map=marketplace_colors,
            orientation='h',
            barmode='group',
            height=700,
            text='ยอดขาย'
        )
    else:
        data = data.sort_values('total_value', ascending=False)
        data.rename(columns={'total_value': 'ยอดขาย'}, inplace=True)
        fig = px.bar(
            data,
            x='ยอดขาย', 
            y='marketplace',
            color=data["marketplace"],
            orientation='h',
            text='ยอดขาย',
            color_discrete_map=marketplace_colors,
        )         
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย",
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")

def get_bar_plot_group(data, title, is_grop=False):
    new_row = {'marketplace': 'shopee', 'product_nm': 'ข้าวพันธุ์ กข 10', 'amount_sold_format': 0}
    data = data._append(new_row, ignore_index=True)

    sorted_df_final = data.sort_values(by=['marketplace', 'amount_sold_format'], ascending=[False, True])
    sorted_df_final.rename(columns={'amount_sold_format': 'ยอดขาย'}, inplace=True)
    st.write(sorted_df_final)
    fig = px.bar(
        sorted_df_final,
        x='ยอดขาย', 
        y='product_nm',
        color=sorted_df_final["marketplace"],
        orientation='h',
        barmode='group',
        height=700,
        color_discrete_map=marketplace_colors,
        text='ยอดขาย')
    fig.update_traces(texttemplate='%{text:.2s} ชิ้น', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย",
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")

get_head_title(1, "เพื่อศึกษาแบรนด์ที่ยอดขายสูง")

# Prepare data
data_all = get_data()

data_all = data_all[['marketplace', 'product_nm', 'amount_sold_format', 'total_value']]
data_all = data_all[data_all['amount_sold_format'] > 0]

section_title("ระหว่าง Shopee และ Lazada แพลตฟอร์มใดที่มียอดขายเฉลี่ยของสินค้าสูงกว่ากัน")
grouped_df = data_all.groupby('marketplace')['total_value'].sum().reset_index()
get_bar_plot(grouped_df, "")


st.divider()
section_title("สินค้าที่ขายดีที่สุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")
grouped_df = data_all.groupby(['marketplace', 'product_nm'])['amount_sold_format'].sum().reset_index()
get_bar_plot_group(grouped_df, "", True)


