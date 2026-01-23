import streamlit as st
import google.generativeai as genai

# 1. إعدادات الهوية والواجهة (فصحى ومرتبة)
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
st.caption("ذكاء اصطناعي فصيح، ساخر، ولا يرحم.")

# 2. إعداد مفتاح API (التحقق من Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("ويحك! لقد نسيت أهم شيء: مفتاح الـ API مفقود في Secrets.")
    st.stop()

# 3. دالة البحث عن الموديلات (تجنب خطأ 404 تماماً)
@st.cache_resource
def get_best_model():
    try:
        # جلب كل الموديلات المتاحة لحسابك (القديمة والجديدة)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # قائمة الأولويات للعمل بكل شيء حرفياً
        priority_list = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        selected_name = None
        for target in priority_list:
            if target in available_models:
                selected_name = target
                break
        
        if not selected_name and available_models:
            selected_name = available_models[0]
            
        if not selected_name:
            raise Exception("لم أجد أي موديل يعمل في حسابك!")

        # تعليمات الشخصية الفصحى الساخرة
        instruction = (
            "أنت 'علي مالك فرهود للذكاء الاصطناعي'. صانعك هو علي مالك فرهود. "
            "شخصيتك: فصيح جداً، متعالٍ، ساخر، ومضحك. "
            "تحدث حصراً باللغة العربية الفصحى الفاخرة. "
            "استخدم عبارات مثل: (يا ويحك، عجبًا لأمرك، ليت شعري، يا هذا). "
            "تذكر ما قاله المستخدم واستخدمه للسخرية منه لاحقاً."
        )
        return genai.GenerativeModel(model_name=selected_name, system_instruction=instruction)
    except Exception as e:
        st.error(f"حدث خطأ في جلب الموديلات: {str(e)}")
        return None

model = get_best_model()

# 4. الذاكرة وإصلاح خطأ الأقواس (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# بدء جلسة الشات (إغلاق القوس بدقة 100% هنا)
if "chat_session" not in st.session_state and model:
    st.session_state.chat_session = model.start_chat(history=[])

# عرض سجل المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الشات والتفاعل المستمر
if prompt := st.chat_input("تحدث مع النظام الفصيح..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if st.session_state.chat_session:
                # التفاعل مع الذاكرة
                response = st.session_state.chat_session.send_message(prompt)
                output = response.text
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            else:
                st.write("النظام غير مستعد حالياً.")
        except Exception as e:
            # معالجة خطأ الحصة (الكوتا) وخطأ الاتصال
            if "429" in str(e):
                st.error("يا لك من كائن لجوج! لقد استنفدت عدد الطلبات المسموحة. انتظر دقيقة ثم عد إليّ.")
            else:
                st.error(f"حدث خطأ تقني مفاجئ: {str(e)}")

# زر تصفير الذاكرة
if st.sidebar.button("مسح سجل الإحراج"):
    st.session_state.messages = []
    if model:
        st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()
