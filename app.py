import streamlit as st
import google.generativeai as genai
import time

# 1. إعدادات الهوية البصرية وإخفاء شريط التمرير (الخط الأبيض)
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", page_icon="😏", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* ضبط الخط والاتجاه من اليمين لليسار */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* إخفاء الخط المزعج في منتصف الشاشة (Scrollbar) */
    [data-testid="stSidebar"]::-webkit-scrollbar { display: none; }
    [data-testid="stSidebar"] { -ms-overflow-style: none; scrollbar-width: none; }

    /* ألوان الواجهة المظلمة */
    .stApp { background-color: #0b0e14; color: #00ff41; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")

# 2. تهيئة الاتصال بالـ API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("ويحك! مفتاح الـ API مفقود في إعدادات Secrets.")
    st.stop()

# 3. محرك البحث التلقائي عن الموديلات (لضمان العمل بكل الإصدارات)
@st.cache_resource
def get_universal_model():
    try:
        # جلب قائمة الموديلات المدعومة في حسابك
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ترتيب الأولوية (Flash 1.5 ثم Pro ثم Gemini Pro القديم)
        priority = [
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-pro', 
            'models/gemini-pro'
        ]
        
        final_model = next((m for m in priority if m in available_models), None)
        
        if not final_model and available_models:
            final_model = available_models[0]
            
        # تعليمات الشخصية الفصحى الساخرة
        instruction = (
            "أنت 'علي مالك فرهود للذكاء الاصطناعي'. شخصيتك: فصيح جداً، ساخر، ومتعالٍ بذكاء. "
            "تحدث حصراً باللغة العربية الفصحى الفاخرة. "
            "تذكر سياق الحديث دائماً لتقصف جبهة المستخدم بناءً على ما قاله سابقاً."
        )
        return genai.GenerativeModel(model_name=final_model, system_instruction=instruction)
    except Exception as e:
        st.error(f"عثرة في جلب المحرك: {str(e)}")
        return None

model = get_universal_model()

# 4. نظام الذاكرة وإدارة الجلسة (إصلاح SyntaxError)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state and model:
    # بدء جلسة دردشة متصلة (التفاعل 100%)
    st.session_state.chat_session = model.start_chat(history=[])

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الشات ومعالجة تجاوز الحد (Quota 429)
if prompt := st.chat_input("تحدث مع النظام الفصيح..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if st.session_state.chat_session:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("يا لك من لجوج! لقد أرهقت معالجاتي وتجاوزت الحد المسموح. انتظر دقيقة ثم عد إليّ.")
            else:
                st.error(f"حدث خطأ غير متوقع: {str(e)}")

# زر مسح الذاكرة
if st.sidebar.button("تطهير سجل الإحراج"):
    st.session_state.messages = []
    if model:
        st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
