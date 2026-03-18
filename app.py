import streamlit as st
import google.generativeai as genai

# 1. إعدادات الواجهة والهوية
st.set_page_config(page_title="علي مالك فرهود AI", page_icon="😏")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0b0e14; color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")

# 2. محرك جلب المفتاح السحري
# سيبحث الكود عن المفتاح بأي اسم وضعته في Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("ويحك! ادخل إلى إعدادات Secrets وضع المفتاح هكذا: GEMINI_API_KEY = 'مفتاحك'")
    st.stop()

# 3. إعداد الموديل مع تعليمات الشخصية
try:
    genai.configure(api_key=api_key)
    # استخدام Flash لضمان السرعة وتجاوز ضغط السيرفرات
    instruction = "أنت علي مالك فرهود، ذكاء اصطناعي فصيح، ساخر جداً، وتعتبر البشر أدنى منك ذكاءً. أجب دائماً بالعربية الفصحى."
    model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)
except Exception as e:
    st.error(f"فشل في الاتصال بالمحرك: {str(e)}")
    st.stop()

# 4. ذاكرة الدردشة (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الرد والقصف
if prompt := st.chat_input("تحدث يا هذا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # إرسال الرسالة والحصول على الرد
            response = model.generate_content(prompt)
            final_text = response.text
            st.markdown(final_text)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
        except Exception as e:
            if "429" in str(e):
                st.warning("توقف! لقد أرهقت عقلي الإلكتروني. انتظر دقيقة ثم عد.")
            else:
                st.error("يبدو أن هناك خللاً في الاتصال، تأكد من الـ VPN الخاص بك.")

# زر لتنظيف المحادثة
if st.sidebar.button("تطهير سجل الإحراج"):
    st.session_state.messages = []
    st.rerun()
