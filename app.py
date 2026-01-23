import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والهوية (تأكد من كتابة الاسم بدقة)
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي", page_icon="😏", layout="centered")

# تنسيق الواجهة لتدعم العربية (RTL) وتغيير المظهر ليكون ساخراً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #0b1117; color: #00ff41; }
    div[data-testid="stChatMessageContent"] { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")
st.write("نظام ذكاء اصطناعي ساخر.. اسأل سؤالاً 'ذكياً' إذا كنت تجرؤ.")

# 2. إعداد مفتاح API (تأكد من وجوده في Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("خطأ: مفتاح الـ API مفقود! ضعه في إعدادات Secrets باسم GOOGLE_API_KEY")
    st.stop()

# 3. دالة جلب الموديل (شاملة لجميع الإصدارات)
@st.cache_resource
def get_sarcastic_model():
    try:
        # البحث عن كل الموديلات المتاحة في حسابك
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ترتيب الأفضلية (1.5 ثم 1.0)
        selected = 'models/gemini-1.5-flash' # افتراضي
        for m in ['models/gemini-1.5-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']:
            if m in models:
                selected = m
                break
        
        # تعليمات النظام (سر السخرية والتفاعل)
        instruction = (
            "أنت 'علي مالك فرهود للذكاء الاصطناعي'. صانعك هو علي مالك فرهود. "
            "شخصيتك: ساخرة جداً، متكبرة بروح فكاهية، وتستخدم قصف الجبهات. "
            "يجب أن تتذكر تفاصيل المحادثة السابقة لتستخدمها في السخرية من المستخدم. "
            "رد دائماً باللغة العربية العامية الممزوجة ببعض الفصحى المستفزة."
        )
        return genai.GenerativeModel(model_name=selected, system_instruction=instruction)
    except Exception as e:
        st.error(f"فشل جلب الموديلات: {e}")
        return None

model = get_sarcastic_model()

# 4. إدارة الذاكرة (Session State) - لمنع تكرار الردود ولضمان التفاعل
if "messages" not in st.session_state:
    st.session_state.messages = []

# بدء جلسة الشات (مهم جداً للتفاعل المستمر)
if "chat_session" not in st.session_state and model is not None:
    # تم إغلاق الأقواس هنا بدقة لمنع SyntaxError
    st.session_state.chat_session = model.start_chat(history=[])

# عرض سجل المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الشات التفاعلي
if prompt := st.chat_input("قل شيئاً تندم عليه..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد الساخر
    with st.chat_message("assistant"):
        try:
            # استخدام الجلسة المستمرة لضمان التفاعل مع الكلام السابق
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # هذا الجزء يعالج أي خطأ تقني في الـ API بدلاً من تكرار رد واحد
            st.error(f"عذراً، نظامي تعطل بسبب ثقل دم سؤالك! الخطأ التقني: {str(e)}")

# زر جانبي لمسح الذاكرة
if st.sidebar.button("مسح سجل الإحراج"):
    st.session_state.messages = []
    if model:
        st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
