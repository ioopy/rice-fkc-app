import streamlit as st
from utils.func import get_color_map, get_head_title, section_title
from utils.load_data import get_data
import plotly.express as px

get_head_title(1, "เพื่อศึกษาแบรนด์ที่ยอดขายสูง")

def get_bar_plot(data, title):
    data = data.sort_values('total_value', ascending=False)
    data.rename(columns={'total_value': 'ยอดขาย'}, inplace=True)
    fig = px.bar(
        data,
        x='ยอดขาย', 
        y='marketplace',
        color=data["marketplace"],
        orientation='h',
        text='ยอดขาย',
        color_discrete_map=get_color_map(),
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

def get_bar_plot_group(data, title):
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
        color_discrete_map=get_color_map(),
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

# Prepare data
data_all = get_data()

data_all = data_all[['marketplace', 'product_nm', 'amount_sold_format', 'total_value']]
data_all = data_all[data_all['amount_sold_format'] > 0]

section_title("ระหว่าง Shopee และ Lazada แพลตฟอร์มใดที่มียอดขายเฉลี่ยของสินค้าสูงกว่ากัน")
grouped_df = data_all.groupby('marketplace')['total_value'].sum().reset_index()

display = data_all.groupby('marketplace').agg(
    total_value_sum=('total_value', 'sum'),
    total_value_mean=('total_value', 'mean')
).reset_index()

display['total_value_mean'] = display['total_value_mean'].apply(lambda x: f"{x:,.2f}")
display.rename(columns={'total_value_sum': 'ยอดขายรวม', 'total_value_mean': 'ยอดขายเฉลี่ย'}, inplace=True)
st.dataframe(display, hide_index=True)
get_bar_plot(grouped_df, "")


st.divider()
section_title("สินค้าที่ขายดีที่สุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")
grouped_df = data_all.groupby(['marketplace', 'product_nm'])['amount_sold_format'].sum().reset_index()
get_bar_plot_group(grouped_df, "")


