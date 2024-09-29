import streamlit as st
from menu import menu_with_redirect
from utils.func import get_head_title, hide_header_icons, section_title
import plotly.express as px
from utils.load_data import get_data
from plotly.subplots import make_subplots

menu_with_redirect()
hide_header_icons()

def get_line_plot(data):
    fig = px.line(data, x='per_discount_format',
                y='total_value', color='product_nm',
                markers=True    
            )
    
    fig.update_layout(
        title={
            'text': '',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="ยอดขาย",
        xaxis_title="% ส่วนลด",
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

data_all = get_data()
data_all = data_all[['marketplace', 'product_name', 'product_nm', 'star_review', 'original_price', 'discount_price_format', 'per_discount_format', 'amount_sold_format', 'total_value']]
data_all = data_all[data_all['per_discount_format'] > 0]
data_all = data_all[data_all['amount_sold_format'] > 0]

get_head_title(3, "เพื่อโอกาสในการวางกลยุทธ์ทางการตลาด")
section_title("เปอร์เซ็นต์การลดราคามีความสัมพันธ์กับยอดขายของสินค้านี้อย่างไร")
# data_sorted = data_all.sort_values(by='per_discount_format', ascending=False)
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])

st.write("**ข้าวเหนียวพันธุ์ กข6**")
data_sorted1=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวพันธุ์ กข6']
get_line_plot(data_sorted1)

st.write("**ข้าวเหนียวก่ำ**")
data_sorted2=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวก่ำ']
get_line_plot(data_sorted2)

st.write("**ข้าวเหนียวเขี้ยวงู**")
data_sorted3=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวเขี้ยวงู']
get_line_plot(data_sorted3)

st.write("**ข้าวหอมนิลล้านนา**")
data_sorted4=data_sorted[data_sorted['product_nm'] == 'ข้าวหอมนิลล้านนา']
get_line_plot(data_sorted4)

st.write("**ข้าวเหนียวสันป่าตอง**")
data_sorted5=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวสันป่าตอง']
get_line_plot(data_sorted5)

st.write("**ข้าวหอมมะลิแท้เชียงราย100%**")
data_sorted6=data_sorted[data_sorted['product_nm'] == 'ข้าวหอมมะลิแท้เชียงราย100%']
get_line_plot(data_sorted6)


st.divider()
section_title("การลดราคามากกว่า 30% มีผลทำให้ยอดขายเพิ่มขึ้นหรือไม่")
data_all = data_all[data_all['per_discount_format'] > 30]
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])

st.write("**ข้าวเหนียวพันธุ์ กข6**")
data_sorted1=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวพันธุ์ กข6']
get_line_plot(data_sorted1)

st.write("**ข้าวเหนียวก่ำ**")
data_sorted2=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวก่ำ']
get_line_plot(data_sorted2)

st.write("**ข้าวเหนียวเขี้ยวงู**")
data_sorted3=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวเขี้ยวงู']
get_line_plot(data_sorted3)

st.write("**ข้าวหอมนิลล้านนา**")
data_sorted4=data_sorted[data_sorted['product_nm'] == 'ข้าวหอมนิลล้านนา']
get_line_plot(data_sorted4)

st.write("**ข้าวเหนียวสันป่าตอง**")
data_sorted5=data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวสันป่าตอง']
get_line_plot(data_sorted5)

st.write("**ข้าวหอมมะลิแท้เชียงราย100%**")
data_sorted6=data_sorted[data_sorted['product_nm'] == 'ข้าวหอมมะลิแท้เชียงราย100%']
get_line_plot(data_sorted6)
# get_line_plot(data_sorted)
