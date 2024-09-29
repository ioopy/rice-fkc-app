import streamlit as st
from menu import menu_with_redirect
import pandas as pd
import plotly.express as px
from utils.func import break_page, get_color_map, get_head_title, hide_header_icons, section_title
from utils.load_data import get_data
from utils.text_editor import generate
import plotly.graph_objects as go
from plotly.subplots import make_subplots

menu_with_redirect()
hide_header_icons() 

def get_bar_plot(data, title, is_grop=False):
    marketplace_colors = {
        'shopee': '#FE6132',
        'lazada': '#0F0C76 ',
    }
    data['color'] = data['marketplace'].map(marketplace_colors)
    fig = px.bar(
            data,
            x='total_value', 
            y='discount_range',
            color=data["marketplace"],
            color_discrete_map=marketplace_colors,
            orientation='h',
            barmode='group',
            height=600,
            text='total_value'
        )        
    fig.update_traces(texttemplate='%{text:,}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        yaxis_title="% ส่วนลด",
        xaxis_title="ยอดขาย (ชิ้น)",
        legend_title_text='',
    )
    st.plotly_chart(fig, theme="streamlit")

def get_bar_comparison(data, mean_total_value, mean_amount_sold):
    marketplace_colors = {
        'shopee': '#FE6132',
        'lazada': '#0F0C76 ',
    }
    data['color'] = data['marketplace'].map(marketplace_colors)

    fig = make_subplots(rows=1, cols=2, 
                        shared_yaxes=True,  # Share the y-axis (province)
                        column_titles=["ยอดขายรวม", "จำนวนขาย (ชิ้น)"],  # Titles for the subplots
                        horizontal_spacing=0.05)  # Adjust spacing between subplots

    fig.add_trace(
        go.Bar(
            y=data['marketplace'],  # Common y-axis (province)
            x=data['total_value'],  # 'total_value' on the x-axis
            orientation='h',  # Horizontal bars
            name='ยอดขายรวม',
            marker=dict(color=data['color'],line=dict(width=1)),  # Customize bar border (line width)
            text=data['total_value'],
            textposition='auto',texttemplate='%{text:,.0f}',
            textangle=0, cliponaxis=False
        ),
        row=1, col=1  # First subplot
    )

    fig.add_shape(
        type="line",
        x0=mean_total_value, x1=mean_total_value,  # Vertical line at mean value
        y0=0, y1=1.5,  # Full height of the graph (normalized y-coordinates)
        xref="x1", yref="paper",  # Refer to the first x-axis and full figure height
        line=dict(color="red", width=2, dash="dash"),  # Style of the mean line
        row=1, col=1  # First subplot
    )
    fig.add_annotation(
        x=mean_total_value * 1.5, 
        y=1.5,  # Position the annotation at the top of the graph
        showarrow=False,
        xref="x1", 
        yref="paper", 
        text=f"ค่าเฉลี่ย: {mean_total_value:,.2f}",  # Text showing the mean value
        font=dict(color="red", size=12),  # Customize font color and size
        row=1, col=1  # Apply to the first subplot
    )

    fig.add_trace(
        go.Bar(
            y=data['marketplace'],  # Common y-axis (province)
            x=data['amount_sold_format'],  # 'amount_sold_format' on the x-axis
            orientation='h',  # Horizontal bars
            name='จำนวนขาย (ชิ้น)',
            marker=dict(color=data['color'],line=dict(width=1)), # Customize bar border (line width)
            text=data['amount_sold_format'],
            textposition='auto',texttemplate='%{text:,.0f}',textangle=0, cliponaxis=False
        ),
        row=1, col=2  # Second subplot
    )

    fig.add_shape(
        type="line",
        x0=mean_amount_sold, x1=mean_amount_sold,  # Vertical line at mean value
        y0=0, y1=1.5,  # Full height of the graph (normalized y-coordinates)
        xref="x1", yref="paper",  # Refer to the first x-axis and full figure height
        line=dict(color="red", width=2, dash="dash"),  # Style of the mean line
        row=1, col=2  # First subplot
    )
    fig.add_annotation(
        x=mean_amount_sold * 1.5, 
        y=1.5,  # Position the annotation at the top of the graph
        showarrow=False,
        xref="x1", 
        yref="paper", 
        text=f"ค่าเฉลี่ย: {mean_amount_sold:,.2f}",  # Text showing the mean value
        font=dict(color="red", size=12),  # Customize font color and size
        row=1, col=2  # Apply to the first subplot
    )

    fig.update_layout(
        # barmode='group',
        showlegend=False,
        # height=1000,
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

data_all = get_data()
data_all = data_all[['marketplace', 'per_discount_format', 'amount_sold_format', 'total_value']]
data_all = data_all[data_all['amount_sold_format'] > 0]
get_head_title(5, "เพื่อหาช่องทางการขายที่เหมาะสม")
section_title("แพลตฟอร์มใด (Shopee หรือ Lazada) มีอัตราการลดราคาสินค้าโดยเฉลี่ยมากกว่ากัน และมีผลต่อยอดขายอย่างไร")
discount_stats = data_all.groupby('marketplace').agg({
    'amount_sold_format': 'sum',
    'per_discount_format': 'sum',
    'total_value': 'sum'
}).reset_index()

# avg_discount = data_all.groupby('marketplace')['per_discount_format'].mean()
# Calculate correlation between discount and sales for each marketplace
# correlation = data_all.groupby('marketplace').apply(lambda x: x['per_discount_format'].corr(x['total_value']))
# discount_stats.rename(columns={'per_discount_format': 'percent_discount', 'total_value': 'amount_sold'}, inplace=True)
# total_discount = discount_stats['percent_discount'].sum()
# discount_stats['percent_of_total_discount'] = (discount_stats['percent_discount'] / total_discount) * 100
# discount_stats['percent_of_total_discount'] = discount_stats['percent_of_total_discount'].map("{:.2f}%".format)
mean_total_value = discount_stats['total_value'].mean()
mean_amount_sold = discount_stats['amount_sold_format'].mean()
get_bar_comparison(discount_stats, mean_total_value, mean_amount_sold)

st.divider()
section_title("ยอดขายของสินค้าที่มีส่วนลดสูงสุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%']
data_all['discount_range'] = pd.cut(data_all['per_discount_format'], bins=bins, labels=labels, include_lowest=True)
discount_summary = data_all.groupby(['marketplace','discount_range'])['total_value'].sum().reset_index()
# discount_summary = discount_summary.sort_values(by=['total_value'], ascending=[True])
get_bar_plot(discount_summary, "")