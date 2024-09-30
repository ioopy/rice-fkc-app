import pandas as pd
import streamlit as st

from menu import menu_with_redirect

def convert_amount_sold(amount_str):
    if isinstance(amount_str, int):
        return amount_str
    if pd.isna(amount_str):
        return 0
    
    amount_str = amount_str.replace('ขายแล้ว', '').replace('ชิ้น', '').strip()
    if 'K' in amount_str:
        return int(float(amount_str.replace('K', '')) * 1000)
    elif 'พัน' in amount_str:
        return int(float(amount_str.replace('พัน', '')) * 1000)
    else:
        return int(amount_str)
    
def get_head_title(no, sub):
    st.set_page_config(page_title=f"การวิเคราะห์ที่ {no}", page_icon="📈")
    st.header(f":blue[การวิเคราะห์ที่ {no}]", divider=True)
    st.subheader(sub)

    menu_with_redirect()
    hide_header_icons()
    return None

def section_title(text):
    st.html(f"<strong style='font-size: 18px; text-decoration: underline;'>{text}</strong>")
    return None

def hide_header_icons():
    hide_github_icon = """
                    <style>
                    .stActionButton {
                        visibility: hidden;
                    }
                    </style>
                    """
    st.markdown(hide_github_icon, unsafe_allow_html=True)

def get_color_map():
    return {
        'shopee': '#FE6132',  
        'lazada': '#0F0C76', 
    }

def break_page():
    st.markdown(
        """
            <style type="text/css" media="print">
            div.page-break
            {
                page-break-after: always;
                page-break-inside: avoid;
            }
            </style>
            <div class="page-break">
                <!-- Content goes here -->
            </div>
        """,
        unsafe_allow_html=True,
    )