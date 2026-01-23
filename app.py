import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", layout="centered")

st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stChatMessageContent"] { text-align: right; direction: rtl; }
    .stApp { background-color: #0b0e14; color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")

# 2. التحقق من مفتاح الـ API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("المفتاح مفقود! ضعه في Secrets.")
    st.stop()

# 3. دالة البحث الشامل عن أي موديل متاح (حل مشكلة 404)
@st.cache_resource
def get_any_working_model():
    try:
        # جلب قائمة بكل الموديلات المتاحة فعلياً لحسابك الآن
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ترتيب ذكي: يبحث عن 1.5 أولاً، ثم 1.0، ثم أي شيء آخر يجده
        priority = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        final_model_name = None
        for p in priority:
            if p in available_models:
                final_model_name = p
                break
        
        if not final_model_name and available_models:
            final_model_name = available_models[0] # يأخذ أول واحد يجده "أياً كان"
            
        if not final_model_name:
            raise Exception("لم يتم العثور على أي موديل متاح في حسابك!")

        instruction = (
            "أنت علي مالك فرهود للذكاء الاصطناعي. شخصيتك ساخرة ومضحكة جداً. "
            "تفاعل مع الناس بقصف جبهات وتذكر كلامهم السابق لتستخدمه ضدهم."
        )
        return genai.GenerativeModel(model_name=final_model_name, system_instruction=instruction)
    except Exception as e:
        st.error(f"خطأ في جلب الموديلات: {str(e)}")
        return None

model = get_any_working_model()

# 4. الذاكرة (Session State) - إصلاح خطأ القوس SyntaxError
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state and model:
    # تم إغلاق القوس هنا بدقة كما في الصورة الأولى
    st.session_state.chat_session = model.start_chat(history=[])

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الشات
if prompt := st.chat_input("قل شيئاً تندم عليه..."):
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
            else:
                st.write("النظام غير جاهز، تأكد من الـ API Key.")
        except Exception as e:
            # عرض الخطأ الحقيقي للمساعدة في الحل
            st.error(f"حدث خطأ تقني: {str(e)}")

# زر إعادة التعيين
if st.sidebar.button("مسح الذاكرة"):
    st.session_state.messages = []
    if model:
        st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
