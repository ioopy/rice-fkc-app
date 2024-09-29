import streamlit as st
from menu import menu_with_redirect
from utils.func import get_head_title, hide_header_icons, section_title
import plotly.express as px
from utils.load_data import get_data
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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

def get_line_trace(data, product_name):
    trace = go.Scatter(
        x=data['per_discount_format'],
        y=data['total_value'],
        mode='lines+markers',
        name=product_name
    )
    return trace

# Create a subplot with 3 rows and 2 columns (adjust if needed)
fig = make_subplots(rows=3, cols=2, subplot_titles=[
    "ข้าวเหนียวพันธุ์ กข6", "ข้าวเหนียวก่ำ", "ข้าวเหนียวเขี้ยวงู", 
    "ข้าวหอมนิลล้านนา", "ข้าวเหนียวสันป่าตอง", "ข้าวหอมมะลิแท้เชียงราย100%"
])

# Add the traces to the subplot grid
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวพันธุ์ กข6'], 'ข้าวเหนียวพันธุ์ กข6'), row=1, col=1)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวก่ำ'], 'ข้าวเหนียวก่ำ'), row=1, col=2)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวเขี้ยวงู'], 'ข้าวเหนียวเขี้ยวงู'), row=2, col=1)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวหอมนิลล้านนา'], 'ข้าวหอมนิลล้านนา'), row=2, col=2)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวสันป่าตอง'], 'ข้าวเหนียวสันป่าตอง'), row=3, col=1)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวหอมมะลิแท้เชียงราย100%'], 'ข้าวหอมมะลิแท้เชียงราย100%'), row=3, col=2)

# Update X and Y axes titles for each subplot
# Row 1
fig.update_xaxes(title_text="% ส่วนลด", row=1, col=1)
fig.update_yaxes(title_text="ยอดขาย", row=1, col=1)
fig.update_xaxes(title_text="% ส่วนลด", row=1, col=2)
fig.update_yaxes(title_text="ยอดขาย", row=1, col=2)

# Row 2
fig.update_xaxes(title_text="% ส่วนลด", row=2, col=1)
fig.update_yaxes(title_text="ยอดขาย", row=2, col=1)
fig.update_xaxes(title_text="% ส่วนลด", row=2, col=2)
fig.update_yaxes(title_text="ยอดขาย", row=2, col=2)

# Row 3
fig.update_xaxes(title_text="% ส่วนลด", row=3, col=1)
fig.update_yaxes(title_text="ยอดขาย", row=3, col=1)
fig.update_xaxes(title_text="% ส่วนลด", row=3, col=2)
fig.update_yaxes(title_text="ยอดขาย", row=3, col=2)
# Update layout for the entire subplot figure
fig.update_layout(
    height=900,  # Adjust height for your subplots
    title_text="",
    showlegend=False,  # Hide the legend (optional)
    yaxis_title="ยอดขาย",
    xaxis_title="% ส่วนลด"
)

# Display in Streamlit
st.plotly_chart(fig, theme="streamlit")

st.divider()
section_title("การลดราคามากกว่า 30% มีผลทำให้ยอดขายเพิ่มขึ้นหรือไม่")
data_all = data_all[data_all['per_discount_format'] > 30]
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])
# Add the traces to the subplot grid
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวพันธุ์ กข6'], 'ข้าวเหนียวพันธุ์ กข6'), row=1, col=1)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวก่ำ'], 'ข้าวเหนียวก่ำ'), row=1, col=2)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวเขี้ยวงู'], 'ข้าวเหนียวเขี้ยวงู'), row=2, col=1)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวหอมนิลล้านนา'], 'ข้าวหอมนิลล้านนา'), row=2, col=2)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวเหนียวสันป่าตอง'], 'ข้าวเหนียวสันป่าตอง'), row=3, col=1)
fig.add_trace(get_line_trace(data_sorted[data_sorted['product_nm'] == 'ข้าวหอมมะลิแท้เชียงราย100%'], 'ข้าวหอมมะลิแท้เชียงราย100%'), row=3, col=2)

# Update X and Y axes titles for each subplot
# Row 1
fig.update_xaxes(title_text="% ส่วนลด", row=1, col=1)
fig.update_yaxes(title_text="ยอดขาย", row=1, col=1)
fig.update_xaxes(title_text="% ส่วนลด", row=1, col=2)
fig.update_yaxes(title_text="ยอดขาย", row=1, col=2)

# Row 2
fig.update_xaxes(title_text="% ส่วนลด", row=2, col=1)
fig.update_yaxes(title_text="ยอดขาย", row=2, col=1)
fig.update_xaxes(title_text="% ส่วนลด", row=2, col=2)
fig.update_yaxes(title_text="ยอดขาย", row=2, col=2)

# Row 3
fig.update_xaxes(title_text="% ส่วนลด", row=3, col=1)
fig.update_yaxes(title_text="ยอดขาย", row=3, col=1)
fig.update_xaxes(title_text="% ส่วนลด", row=3, col=2)
fig.update_yaxes(title_text="ยอดขาย", row=3, col=2)
# Update layout for the entire subplot figure
fig.update_layout(
    height=900,  # Adjust height for your subplots
    title_text="",
    showlegend=False,  # Hide the legend (optional)
    yaxis_title="ยอดขาย",
    xaxis_title="% ส่วนลด"
)

# Display in Streamlit
st.plotly_chart(fig, theme="streamlit")
