import streamlit as st
from utils.func import break_page, get_color_map, get_head_title, section_title
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
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย (ชิ้น)",
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


desc_msg1 = '''
    จากผลการวิเคราะห์ พบว่า **Shopee** มียอดขายเฉลี่ยของสินค้าสูงกว่าที่ **186,093.12** บาท หรือประมาณ 48,756,397 บาท ในขณะที่ **Lazada** มียอดขายเฉลี่ยอยู่ที่ **54,334.93** บาท หรือประมาณ 9,399,943 บาท
'''
summary1 = '''
    สรุป:\n
    Shopee มียอดขายเฉลี่ยสูงกว่า Lazada อย่างมีนัยสำคัญในชุดข้อมูลนี้
'''

desc_msg2 = '''
    จากการวิเคราะห์ข้อมูล สินค้าที่ขายดีที่สุดในแต่ละแพลตฟอร์มมีดังนี้:\n
    - **Shopee**: สินค้าที่ขายดีที่สุดคือ "ข้าวเหนียวพันธุ์ กข6" มียอดขายจำนวน 155,436 หน่วย
    - **Lazada**: สินค้าที่ขายดีที่สุดคือ "ข้าวเหนียวเขี้ยวงู" มียอดขายจำนวน 18,545 หน่วย
    
'''
summary2 = '''
    สรุป:\n
    สินค้าที่ขายดีที่สุดใน Shopee และ Lazada แตกต่างกันอย่างมาก โดย Shopee มียอดขายสูงกว่า Lazada มากกว่า 8 เท่าตัว
'''

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

st.markdown(desc_msg1)
st.markdown(summary1)

st.divider()
break_page()
section_title("สินค้าที่ขายดีที่สุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")
grouped_df = data_all.groupby(['marketplace', 'product_nm'])['amount_sold_format'].sum().reset_index()
get_bar_plot_group(grouped_df, "")
st.markdown(desc_msg2)
st.markdown(summary2)



