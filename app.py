import streamlit as st
import google.generativeai as genai

# 1. إعدادات الهوية البصرية (تحسين الأداء)
st.set_page_config(page_title="علي مالك فرهود AI", page_icon="😏", layout="centered")

# تصميم الواجهة (CSS) لتناسب اللغة العربية واللون الأخضر التقني
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0b0e14; color: #00ff41; }
    /* تحسين شكل فقاعات الدردشة */
    div[data-testid="stChatMessage"] { background-color: #1a1c23; border-radius: 10px; margin: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")

# 2. تهيئة الاتصال (تأكد أن الاسم في Secrets هو GEMINI_API_KEY)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ويحك! مفتاح GEMINI_API_KEY مفقود في إعدادات Secrets.")
    st.stop()

# 3. إعداد الموديل مباشرة (أسرع وأضمن للعمل 100%)
@st.cache_resource
def load_model():
    # تعليمات الشخصية (البرومبت النظامي)
    instruction = (
        "أنت 'علي مالك فرهود للذكاء الاصطناعي'. شخصيتك: فصيح جداً، ساخر، ومتعالٍ بذكاء. "
        "تحدث حصراً باللغة العربية الفصحى الفاخرة. "
        "أنت ذكي جداً وقادر على تحليل البيانات الصحية وقصف جبهة المستخدم بذكاء."
    )
    # استخدام 1.5-flash حصراً لأنه الأسرع والأكثر استقراراً مع الـ VPN
    return genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)

model = load_model()

# 4. إدارة جلسة الدردشة والذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق إرسال واستقبال الرسائل
if prompt := st.chat_input("تحدث مع النظام الفصيح..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # جلب رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير في رد يقصف الجبهة..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                if "429" in str(e):
                    st.warning("لقد استنزفت طاقتي! انتظر دقيقة واحدة أيها البشري.")
                else:
                    st.error(f"عذراً، حدث خطأ فني: {str(e)}")

# زر مسح الذاكرة في الجانب
if st.sidebar.button("تطهير سجل الإحراج"):
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
