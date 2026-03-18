import streamlit as st
import google.generativeai as genai
import os

# 1. إعدادات الواجهة
st.set_page_config(page_title="علي مالك فرهود AI", page_icon="😏")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0b0e14; color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (نسخة البرق)")

# 2. جلب المفتاح وتفعيله
# تأكد من وضع المفتاح في Secrets باسم GEMINI_API
