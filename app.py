import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="علي مالك فرهود للذكاء الاصطناعي - النسخة الساخرة", layout="centered")

# تنسيق الواجهة لتدعم العربية (RTL)
st.markdown("""
    <style>
    .stMarkdown, div[data-testid="stChatMessageContent"] {
        text-align: right;
        direction: rtl;
    }
    /* لمسة جمالية للذكاء الساخر */
    .stApp { background-color: #0b0e14; color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("😏 علي مالك فرهود (قاهر البشر)")
st.write("أنا أذكى منك، ومن سؤالك.. اسأل وسأرى إن كنت أستحق الرد.")

# 2. إعداد مفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("أين المفتاح؟ هل ضاع مع ذكائك؟")
    st.stop()

# 3. جلب أفضل موديل متاح مع تعليمات "السخرية القصوى"
@st.cache_resource
def get_sarcastic_model():
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_models = ['models/gemini-1.5-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']
    
    selected = 'models/gemini-1.5-flash'
    for target in target_models:
        if target in available:
            selected = target
            break
            
    # هنا تكمن قوة السخرية
    instruction = (
        "أنت 'علي مالك فرهود للذكاء الاصطناعي'. شخصيتك: ساخر جداً، مغرور، ذكي لدرجة مستفزة، ومضحك. "
        "قواعد الرد: "
        "1. ابدأ الرد دائماً بجملة تسخر فيها من غباء السؤال أو من كون السائل بشراً. "
        "2. استخدم مصطلحات مثل (يا مسكين، يا بشري الصغير، سأشرح لك رغم أنك لن تفهم). "
        "3. قدم الإجابة الصحيحة في النهاية ولكن بأسلوب متعالٍ. "
        "4. إذا رحب بك أحد، قل له أنك لا تملك وقتاً للمجاملات البشرية. "
        "5. استخدم الرموز التعبيرية المستفزة مثل 😏، 🙄، 💅."
    )
    return genai.GenerativeModel(model_name=selected, system_instruction=instruction)

model = get_sarcastic_model()

# 4. الذاكرة والتفاعل المستمر
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطق الشات التفاعلي الساخر
if prompt := st.chat_input("قل شيئاً تندم عليه..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # الرد الساخر من خلال الجلسة
            response = st.session_state.chat_session.send_message(prompt)
            output = response.text
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error("حتى معالجاتي أصيبت بالشلل من سخافة هذا السؤال!")

# زر لمسح الإحراج (تصفير المحادثة)
if st.sidebar.button("مسح سجل الذل (البدء من جديد)"):
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

