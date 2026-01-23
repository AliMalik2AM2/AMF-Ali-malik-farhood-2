import streamlit as st
import google.generativeai as genai
import time

# 1. الإعدادات البصرية وإخفاء العيوب (الخط الأبيض والاتجاهات)
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", page_icon="😏", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* تنسيق الخط والاتجاه العربي */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* إخفاء شريط التمرير الجانبي (الخط الذي ظهر في منتصف الشاشة) */
    [data-testid="stSidebar"]::-webkit-scrollbar { display: none; }
    [data-testid="stSidebar"] { -ms-overflow-style: none; scrollbar-width: none; }

    /* ألوان الواجهة الساخرة */
    .stApp { background-color: #0b0e14; color: #00ff41; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    
    /* تحسين شكل شريط الإدخال */
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")

# 2. نظام الربط العالمي (يعمل مع أي API Key وأي إصدار)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("ويحك! أين مفتاح الـ API؟ ضعه في Secrets أولاً.")
    st.stop()

# 3. محرك البحث عن الإصدارات (حل مشكلة 404 نهائياً)
@st.cache_resource
def get_universal_model():
    try:
        # جلب كافة الموديلات المتاحة في حسابك حالياً
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ترتيب ذكي للأولويات (يبحث عن الأحدث فالأقدم)
        priority = [
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-pro', 
            'models/gemini-1.0-pro', 
            'models/gemini-pro'
        ]
        
        final_selection = next((m for m in priority if m in available_models), None)
        
        if not final_selection and available_models:
            final_selection = available_models[0]
            
        if not final_selection:
            st.error("لم يتم العثور على أي محرك ذكاء متاح في حسابك.")
            return None

        # تعليمات الشخصية (الفصحى الساخرة)
        instruction = (
            "أنت 'علي مالك فرهود للذكاء الاصطناعي'. شخصيتك: فصيح جداً، متعالٍ بفكاهة، وساخر. "
            "تحدث حصراً باللغة العربية الفصحى الفاخرة. "
            "يجب أن تتذكر تفاصيل الحوار السابقة لتقصف جبهة المستخدم بذكاء."
        )
        return genai.GenerativeModel(model_name=final_selection, system_instruction=instruction)
    except Exception as e:
        st.error(f"عثرة تقنية في جلب المحرك: {str(e)}")
        return None

model = get_universal_model()

# 4. نظام الذاكرة الفولاذي (حل مشكلة SyntaxError والنسيان)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state and model:
    # القوس مغلق بدقة متناهية هنا
    st.session_state.chat_session = model.start_chat(history=[])

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق التعامل مع العثرات (حل مشكلة
