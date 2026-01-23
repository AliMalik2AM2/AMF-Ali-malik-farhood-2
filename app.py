import streamlit as st
import google.generativeai as genai
import time

# 1. إعدادات الهوية والواجهة الفخمة
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", page_icon="😏", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #0b0e14; color: #00ff41; }
    div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")

# 2. إعداد مفتاح API مع التحقق
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("ويحك! مفتاح الـ API مفقود في إعدادات Secrets.")
    st.stop()

# 3. دالة جلب الموديل (تبحث عن أي إصدار يعمل تلقائياً)
@st.cache_resource
def get_safe_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # ترتيب الأولويات لضمان العمل بكل شيء حرفياً
        priority = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        selected = next((m for m in priority if m in available_models), None)
        if not selected and available_models:
            selected = available_models[0]
            
        if not selected:
            raise Exception("لم يتم العثور على أي موديل!")

        instruction = (
            "أنت 'علي مالك فرهود للذكاء الاصطناعي'. شخصيتك: فصيح، ساخر، ومتعالٍ بفكاهة. "
            "تحدث حصراً باللغة العربية الفصحى. لا تستخدم العامية أبداً. "
            "تذكر سياق الحديث لتقصف جبهة المستخدم بناءً على ما قاله سابقاً."
        )
        return genai.GenerativeModel(model_name=selected, system_instruction=instruction)
    except Exception as e:
        st.error(f"خطأ في النظام: {str(e)}")
        return None

model = get_safe_model()

# 4. الذاكرة وإصلاح خطأ الأقواس (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state and model:
    # تم إغلاق الأقواس هنا بدقة لمنع SyntaxError
    st.session_state.chat_session = model.start_chat(history=[])

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الشات ومعالجة تجاوز الحد (Quota)
if prompt := st.chat_input("تحدث مع النظام الفصيح..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if st.session_state.chat_session:
                response = st.session_state.chat_session.send_message(prompt)
                output = response.text
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            # معالجة ذكية لرسالة "تجاوز الحد"
            if "429" in str(e):
                st.warning("يا لك من لحوح! لقد أرهقت معالجاتي وتجاوزت الحد المسموح. انتظر 60 ثانية وسأعود لإبهارك.")
                time.sleep(2) # انتظار بسيط قبل السماح بالمحاولة مرة أخرى
            else:
                st.error(f"حدث خطأ غير متوقع: {str(e)}")

# زر تصفير الذاكرة
if st.sidebar.button("مسح سجل الإحراج"):
    st.session_state.messages = []
    if model:
        st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
