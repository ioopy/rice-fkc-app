import streamlit as st
from menu import menu_with_redirect
import pandas as pd
import plotly.express as px
from utils.func import break_page, get_color_map, get_head_title, hide_header_icons, section_title
from utils.load_data import get_data
from utils.text_editor import generate
import plotly.graph_objects as go

from plotly.subplots import make_subplots


get_head_title(4, "เพื่อดึงดูดลูกค้า")

def get_scatter_plot(data):
    mean_discount_price = data['discount_price_format'].mean()
    fig = px.scatter(data, x='star_review', y='original_price', color='product_nm',
                # symbol='product_nm',
                # trendline='ols'
                hover_name="product_nm",
                labels={'product_nm': 'สินค้า', 'original_price': 'ราคา', 'star_review': 'คะแนน', 'total_sale': 'sale value', 'province': 'จังหวัด', 'amount_sold_format': 'ยอดขาย'},
            )
    fig.add_shape(type="line",
                x0=0, x1=5,
                y0=mean_discount_price, y1=mean_discount_price,
                line=dict(color="Red", width=2, dash="dash"),
                name="Mean Price")
    fig.add_annotation(x=data_sorted['star_review'].min(), y=mean_discount_price,
                    text=f"ราคาเฉลี่ย: {mean_discount_price:.2f}",
                    showarrow=False, 
                    yshift=10,  # Shift the annotation up slightly
                    font=dict(color="Red", size=12))
    fig.update_layout(
        # shapes=[dict(
        #     type="line",
        #     xref="x", yref="y",
        #     x0=mean_discount_price, y0=data_sorted['star_review'].maxmin(),
        #     x1=mean_discount_price, y1=data_sorted['star_review'].min(),
        #     line=dict(color="Red", width=2, dash="dash"),
        #     name="ราคาเฉลี่ย"
        # )],
        title={
            'text': '',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="ราคาสินค้า",
        xaxis_title="คะแนนรีวิว",
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
        margin=dict(
            t=100  # Add space at the top (increase this value as needed)
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")
    return None


def get_bar_comparison(data, mean_total_value, mean_amount_sold, is_shopee=False):
    # data = data.sort_values(by='value', ascending=False).head(10)
    fig = make_subplots(rows=1, cols=2, 
                        shared_yaxes=True,  # Share the y-axis (province)
                        column_titles=["ยอดขายรวม", "จำนวนขาย (ชิ้น)"],  # Titles for the subplots
                        horizontal_spacing=0.05)  # Adjust spacing between subplots

    filtered_data_total_value = data[data['metric'] == 'total_value']
    filtered_data_total_value = filtered_data_total_value.sort_values(by='value', ascending=False).head(10)
    filtered_data_total_value = filtered_data_total_value.sort_values(by='value', ascending=True)
    
    fig.add_trace(
        go.Bar(
            y=filtered_data_total_value['province'],  # Common y-axis (province)
            x=filtered_data_total_value['value'],  # 'total_value' on the x-axis
            orientation='h',  # Horizontal bars
            name='ยอดขายรวม',
            marker=dict(line=dict(width=2)),  # Customize bar border (line width)
            text=filtered_data_total_value['value'],
            textposition='auto',texttemplate='%{text:,.0f}',
        ),
        row=1, col=1  # First subplot
    )
    # fig.add_shape(
    #     type="line",
    #     x0=mean_total_value, x1=mean_total_value,  # Vertical line at mean value
    #     y0=0, y1=len(filtered_data_total_value['province']),  # Full height of the graph (normalized y-coordinates)
    #     xref="x1", yref="paper",  # Refer to the first x-axis and full figure height
    #     line=dict(color="red", width=2, dash="dash"),  # Style of the mean line
    #     row=1, col=1  # First subplot
    # )
    # fig.add_annotation(
    #     x=mean_total_value * 0.5, 
    #     y=len(filtered_data_total_value['province']),  # Position the annotation at the top of the graph
    #     showarrow=False,
    #     xref="x1", 
    #     yref="paper", 
    #     text=f"ค่าเฉลี่ย: {mean_total_value:,.2f}",  # Text showing the mean value
    #     font=dict(color="red", size=12),  # Customize font color and size
    #     row=1, col=1  # Apply to the first subplot
    # )

    top_10_total_value_provinces = filtered_data_total_value['province'].unique()
    filtered_data_amount_sold = data[
        (data['metric'] == 'amount_sold_format') & 
        (data['province'].isin(top_10_total_value_provinces))
    ].sort_values(by='value', ascending=False).head(10)

    filtered_data_amount_sold = filtered_data_amount_sold.sort_values(by='value', ascending=True)
    fig.add_trace(
        go.Bar(
            y=filtered_data_amount_sold['province'],  # Common y-axis (province)
            x=filtered_data_amount_sold['value'],  # 'amount_sold_format' on the x-axis
            orientation='h',  # Horizontal bars
            name='จำนวนขาย (ชิ้น)',
            marker=dict(line=dict(width=2)),  # Customize bar border (line width)
            text=filtered_data_amount_sold['value'],
            textposition='auto',texttemplate='%{text:,.2f}',
        ),
        row=1, col=2  # Second subplot
    )
    # fig.add_shape(
    #     type="line",
    #     x0=mean_amount_sold, x1=mean_amount_sold,  # Vertical line at mean value
    #     y0=0, y1=len(filtered_data_total_value['province']),  # Full height of the graph (normalized y-coordinates)
    #     xref="x2", yref="paper",  # Refer to the second x-axis and full figure height
    #     line=dict(color="red", width=2, dash="dash"),  # Style of the mean line
    #     row=1, col=2  # Second subplot
    # )
    # fig.add_annotation(
    #     x=mean_amount_sold, 
    #     y=len(filtered_data_total_value['province']),  # Position the annotation at the top of the graph
    #     showarrow=False,
    #     xref="x1", 
    #     yref="paper", 
    #     text=f"ค่าเฉลี่ย: {mean_amount_sold:,.2f}",  # Text showing the mean value
    #     font=dict(color="red", size=12),  # Customize font color and size
    #     row=1, col=2  # Apply to the first subplot
    # )

    fig.update_layout(
        showlegend=False,
        height=1000,
        title={
            'text': '',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        yaxis_title="",
        font=dict(size=18),
        legend_title_text='',  # Legend title
        xaxis=dict(title=""),  # Title for first x-axis
        xaxis2=dict(title=""),  # Title for second x-axis
    )

    st.plotly_chart(fig, theme="streamlit")
    return None

desc_msg1 = '''
    จากการวิเคราะห์พบว่า: \n
    - สินค้าที่มีราคาหลังหักส่วนลดต่ำกว่าค่าเฉลี่ยได้รับคะแนนรีวิวเฉลี่ยอยู่ที่ **4.63**
    - สินค้าที่มีราคาหลังหักส่วนลดสูงกว่าค่าเฉลี่ยได้รับคะแนนรีวิวเฉลี่ยอยู่ที่ **4.47**
'''
summary1 = '''
    สรุป:\n
    สินค้าที่มีราคาหลังหักส่วนลดต่ำกว่าค่าเฉลี่ยมีแนวโน้มได้รับรีวิวดีกว่าสินค้าที่มีราคาหลังหักส่วนลดสูงกว่าค่าเฉลี่ย
'''

desc_msg2 = '''
    จากการวิเคราะห์พบว่า: \n
    - **Shopee**: จังหวัดที่มียอดใช้จ่ายสูงสุดคือ **นครราชสีมา** มียอดขายรวม 33,338,669 บาท
    - **Lazada**: จังหวัดที่มียอดใช้จ่ายสูงสุดคือ **นนทบุรี** แต่มียอดขายต่ำกว่า Shopee อย่างมาก
'''
summary2 = '''
    สรุป:\n
    จังหวัดนครราชสีมาเป็นพื้นที่ที่มียอดใช้จ่ายสูงสุดใน Shopee ในขณะที่ Lazada ทำยอดขายสูงสุดในกรุงเทพฯ แสดงถึงความแตกต่างในกลุ่มเป้าหมายแต่ละแพลตฟอร์ม
'''

data_all = get_data()
data_all = data_all[['marketplace', 'product_nm', 'star_review', 'original_price', 'discount_price_format', 'per_discount_format', 'amount_sold_format', 'province', 'total_value']]
data_all = data_all[data_all['amount_sold_format'] > 0]

data_all['province'] = data_all['province'].str.replace('China', 'ต่างประเทศ').str.replace('Loei', 'เลย')
section_title("สินค้าที่มีราคาหลังหักส่วนลดต่ำกว่าค่าเฉลี่ยได้รับรีวิวดีขึ้นหรือไม่") #discount_price, star_review
data_sorted = data_all.sort_values(by='discount_price_format', ascending=False)
get_scatter_plot(data_sorted)
st.markdown(desc_msg1)
st.markdown(summary1)

st.divider()
section_title("ร้านในพื้นที่ใดมีแนวโน้มที่จะมีลูกค้าใช้จ่ายมากที่สุดในสินค้าที่มีราคาสูงหลังหักส่วนลด") #province, original_price, amount_sold

st.write("**Shopee**")
data_all1 = data_all[data_all['marketplace'] == 'shopee']  
# data_stat = data_all1.describe()
# st.write(data_stat)
mean_total_value = data_all1['total_value'].mean()
mean_amount_sold = data_all1['amount_sold_format'].mean()
discount_stats = data_all1.groupby(['marketplace', 'province']).agg({
    'amount_sold_format': 'sum',
    'total_value': 'sum'
}).reset_index()
df_melted = pd.melt(discount_stats, 
                    id_vars=['marketplace', 'province'], 
                    value_vars=['amount_sold_format', 'total_value'], 
                    var_name='metric', 
                    value_name='value')
df_melted = df_melted.sort_values(by=['metric', 'value'], ascending=[False, True])
# mean_total_value = df_melted[df_melted['metric'] == 'total_value']['value'].mean()
# mean_amount_sold = df_melted[df_melted['metric'] == 'amount_sold_format']['value'].mean()
get_bar_comparison(df_melted, mean_total_value, mean_amount_sold, True)

st.write("**Lazada**")
data_all = data_all[data_all['marketplace'] == 'lazada']  
# data_stat = data_all.describe()
# st.write(data_stat)
mean_total_value = data_all['total_value'].mean()
mean_amount_sold = data_all['amount_sold_format'].mean()
discount_stats = data_all.groupby(['marketplace', 'province']).agg({
    'amount_sold_format': 'sum',
    'total_value': 'sum'
}).reset_index()
df_melted = pd.melt(discount_stats, 
                    id_vars=['marketplace', 'province'], 
                    value_vars=['amount_sold_format', 'total_value'], 
                    var_name='metric', 
                    value_name='value')
df_melted = df_melted.sort_values(by=['metric', 'value'], ascending=[False, True])
# mean_total_value = df_melted[df_melted['metric'] == 'total_value']['value'].mean()
# mean_amount_sold = df_melted[df_melted['metric'] == 'amount_sold_format']['value'].mean()
get_bar_comparison(df_melted, mean_total_value, mean_amount_sold)
st.markdown(desc_msg1)
st.markdown(summary1)
