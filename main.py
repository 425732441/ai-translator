import streamlit as st
import time
from translator import translate_content

# Page Config
st.set_page_config(
    page_title="AI Talk | Bridging Tech & Biz",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- I18N CONFIG ---
I18N = {
    "English": {
        "title": "AI Translator",
        "subtitle": "Bridge the gap between Product Vision and Engineering Reality.",
        "neural_core": "🧠 Neural Core",
        "select_model": "Select Model",
        "translation_mode": "🔀 Translation Mode",
        "direction": "Direction",
        "auto_detect": "✨ Auto-Detect",
        "pm_to_dev": "PM ➡ Dev",
        "dev_to_pm": "Dev ➡ PM",
        "to_mgmt": "➡ Management",
        "tips_header": "🚀 Tips",
        "tips_content": "Uses sophisticated prompts to bridge the gap between business requirements and technical implementation.",
        "input_placeholder": "e.g., We need a recommendation engine to increase user retention...",
        "btn_translate": "🚀 Translate Message",
        "result_header": "🔮 Translation Result",
        "what_is_this": "🎯 What is this?",
        "what_is_this_content": """
        This tool helps:
        - **PMs** understand technical constraints.
        - **Devs** communicate business value.
        - **Leaders** see the big picture.
        """,
        "powered_by": "⚡ Powered By",
        "history_header": "📜 History",
        "new_chat": "➕ New Chat",
        "delete_confirm": "Delete?",
        "delete": "Delete",
        "cancel": "Cancel",
        "analyzing": "Analyzing context & generating translation...",
        "error": "An error occurred: "
    },
    "中文": {
        "title": "AI 职能翻译官",
        "subtitle": "连接产品愿景与工程实现的智能桥梁",
        "neural_core": "🧠 核心模型",
        "select_model": "选择模型",
        "translation_mode": "🔀 翻译模式",
        "direction": "翻译方向",
        "auto_detect": "✨ 智能识别",
        "pm_to_dev": "产品 ➡ 开发",
        "dev_to_pm": "开发 ➡ 产品",
        "to_mgmt": "汇报 ➡ 管理层",
        "tips_header": "🚀 提示",
        "tips_content": "使用精心设计的提示词工程，消除业务需求与技术实现之间的理解鸿沟。",
        "input_placeholder": "例如：我们需要一个推荐引擎来提高用户留存率...",
        "btn_translate": "🚀 开始翻译",
        "result_header": "🔮 翻译结果",
        "what_is_this": "🎯 这是什么？",
        "what_is_this_content": """
        这个工具致力于：
        - 帮助 **产品经理** 理解技术边界。
        - 帮助 **开发人员** 阐述商业价值。
        - 帮助 **管理者** 掌控全局视野。
        """,
        "powered_by": "⚡ 驱动核心",
        "history_header": "📜 历史记录",
        "new_chat": "➕ 新建会话",
        "delete_confirm": "确认删除?",
        "delete": "删除",
        "cancel": "取消",
        "analyzing": "正在分析语境并生成翻译...",
        "error": "发生错误："
    }
}

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap');

    /* Global */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(10, 10, 10) 0%, rgb(25, 25, 28) 90%);
        color: #F0F0F0;
        font-family: 'Inter', 'Noto Sans SC', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 15, 0.98);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Remove default Streamlit Header (Top White Bar) - Keep Content Visible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        /* visibility: hidden;  <-- REMOVED to show sidebar toggle */
    }
    
    /* Force header icons (like sidebar toggle) to be white/visible */
    header[data-testid="stHeader"] button {
        color: #FFFFFF !important;
    }
    header[data-testid="stHeader"] svg {
        fill: #FFFFFF !important;
    }
    
    /* Text Visibility Fixes */
    .stMarkdown, .stText, p, li {
        color: #E0E0E0 !important;
    }
    strong {
        color: #FFFFFF !important;
        font-weight: 700;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 800;
        letter-spacing: -0.01em;
    }
    
    .main-title {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #A18CD1 0%, #FBC2EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 900;
    }

    .subtitle {
        font-size: 1.3rem;
        color: #E0E0E0 !important; /* Fixed contrast */
        font-weight: 400;
        margin-bottom: 2.5rem;
        opacity: 0.9;
    }

    /* Inputs - Enforce Dark Background & White Text */
    .stTextArea textarea {
        background-color: #1E1E1E !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
        caret-color: #A18CD1 !important;
        border-radius: 12px !important;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #A18CD1 !important;
        box-shadow: 0 0 15px rgba(161, 140, 209, 0.4) !important;
        background-color: #252525 !important;
    }
    /* Placeholder Color */
    .stTextArea textarea::placeholder {
        color: #888888 !important;
    }

    /* Buttons - More Distinct Call to Action */
    .stButton button {
        background: linear-gradient(45deg, #FF512F 0%, #DD2476 100%); /* Vivid Red/Pink Gradient */
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
        box-shadow: 0 4px 15px rgba(221, 36, 118, 0.4);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(221, 36, 118, 0.6);
    }
    
    /* Selectbox & Radio Styles - FORCED DARK MODE VISIBILITY */
    .stSelectbox label, .stRadio label {
        color: #E0E0E0 !important;
    }
    
    /* Target the actual dropdown box (closed state) */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
    }
    
    /* Target svg icons in select box */
    .stSelectbox svg {
        fill: #FFFFFF !important;
    }

    /* Target the dropdown menu (open state) / Popover */
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }
    
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CCC !important;
    }
    
    /* AGGRESSIVE: Force EVERYTHING inside the dropdown to be black */
    div[data-baseweb="popover"] *,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] li,
    ul[data-baseweb="menu"] li *,
    li[data-baseweb="option"] * {
        color: #000000 !important;
        font-weight: 600 !important; /* Make it bold for better visibility */
    }
    
    /* Target individual options */
    li[data-baseweb="option"] {
        background-color: #FFFFFF !important;
    }
    
    /* Hover/Selected state */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #F0F0F0 !important;
    }
    
    /* Keep closed state text white (The box itself) */
    div[data-baseweb="select"] span {
        color: #FFFFFF !important; 
    }

    /* --- SIDEBAR HISTORY LIST STYLING --- */
    
    /* Target buttons specifically in the sidebar to remove the "Bubble" look */
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #E0E0E0 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        padding: 0.4rem 1rem !important;
        font-weight: 400 !important;
        font-size: 0.95rem !important;
        height: auto !important;
        text-transform: none !important; /* Don't uppercase history titles */
        letter-spacing: normal !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #FFFFFF !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Align text in sidebar buttons to the left for a "List" feel */
    section[data-testid="stSidebar"] .stButton button p {
        text-align: left !important;
        width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    /* Compact spacing for history items */
    div[data-testid="column"] {
        padding: 0 !important; 
    }
    div[data-testid="column"] > div {
       margin-bottom: 0.2rem !important;
    }
    
    /* Output Card */
    .output-container {
        background: rgba(30, 30, 35, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    .output-container h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        color: #FBC2EB !important; /* Highlight headers in output */
    }
    .output-container li {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

import locale
import json
import os

def get_system_language_index():
    try:
        lang, _ = locale.getdefaultlocale()
        if lang and "zh" in lang.lower():
            return 0 # Index for "中文"
    except:
        pass
    return 1 # Index for "English"

# --- PERSISTENCE HELPERS ---
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

def render_history_list(placeholder, t, key_suffix=""):
    with placeholder.container():
        st.markdown(f"### {t['history_header']}")
        
        # New Chat Button
        if st.button(t['new_chat'], key=f"new_chat{key_suffix}", use_container_width=True):
            st.session_state.current_input = ""
            st.session_state.current_output = ""
            st.rerun()

        if "delete_confirm_idx" not in st.session_state:
            st.session_state.delete_confirm_idx = None
            
        for idx, item in enumerate(st.session_state.history):
            # Check if this specific item is in "Confirmation Mode"
            if st.session_state.delete_confirm_idx == idx:
                col_mark, col_conf, col_canc = st.columns([0.4, 0.3, 0.3])
                with col_mark:
                    st.markdown(f":red[**{t['delete_confirm']}**]")
                with col_conf:
                    if st.button("✔", key=f"conf_{idx}{key_suffix}"):
                        st.session_state.history.pop(idx)
                        save_history(st.session_state.history)
                        st.session_state.delete_confirm_idx = None
                        st.rerun()
                with col_canc:
                    if st.button("✖", key=f"canc_{idx}{key_suffix}"):
                        st.session_state.delete_confirm_idx = None
                        st.rerun()
            else:
                # Normal Mode: Title + Delete Icon
                col_hist, col_del = st.columns([0.85, 0.15])
                with col_hist:
                    if st.button(f"{item['title']}", key=f"hist_{idx}{key_suffix}", use_container_width=True):
                        st.session_state.current_input = item['input']
                        st.session_state.current_output = item['output']
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{idx}{key_suffix}"):
                        st.session_state.delete_confirm_idx = idx
                        st.rerun()

# --- SESSION STATE INITIALIZATION ---
if "history" not in st.session_state:
    st.session_state.history = load_history()
if "current_input" not in st.session_state:
    st.session_state.current_input = ""
if "current_output" not in st.session_state:
    st.session_state.current_output = ""

# --- SIDEBAR & SETUP ---
with st.sidebar:
    # Language Selector (Top) - Auto-detect default
    lang_options = ["中文", "English"]
    lang_choice = st.selectbox(
        "🌐 Language / 语言", 
        lang_options, 
        index=get_system_language_index()
    )
    t = I18N[lang_choice]

    st.markdown(f"### {t['neural_core']}")
    model_choice = st.selectbox(t['select_model'], ["Qwen Plus", "Gemini 2.5 Pro"])
    
    st.markdown(f"### {t['translation_mode']}")
    
    # Map friendly names back to logic keys
    mode_options = [t['auto_detect'], t['pm_to_dev'], t['dev_to_pm'], t['to_mgmt']]
    mode_display = st.radio(t['direction'], mode_options)
    
    st.markdown("---")
    
    # --- HISTORY LIST FEATURE (Placeholder for dynamic updates) ---
    history_placeholder = st.empty()
    render_history_list(history_placeholder, t, key_suffix="_init")

    st.markdown("---")
    st.markdown(f"##### {t['tips_header']}")
    st.info(t['tips_content'])

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f'<h1 class="main-title">{t["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)

    # Input Area with Session State Binding
    # We use key='user_input_widget' to bind it, and we sync with st.session_state.current_input
    # Note: st.text_area key binds directly to session_state with that key.
    # So we need to ensure 'current_input' is updated when widget changes if we want two-way binding.
    # Simpler: Just use st.session_state.current_input as value, and separate widget key
    
    def update_input():
        st.session_state.current_input = st.session_state.user_input_widget

    input_text = st.text_area(
        "Input", 
        value=st.session_state.current_input,
        height=150,
        placeholder=t['input_placeholder'],
        label_visibility="collapsed",
        key="user_input_widget",
        on_change=update_input
    )

    translate_btn = st.button(t['btn_translate'])

    # Determine internal roles based on display selection
    source_role = "PM" 
    target_role = "DEV" 
    auto_detect = False

    if mode_display == t['auto_detect']:
        auto_detect = True
    elif mode_display == t['pm_to_dev']:
        source_role = "PM"; target_role = "DEV"
    elif mode_display == t['dev_to_pm']:
        source_role = "DEV"; target_role = "PM"
    elif mode_display == t['to_mgmt']:
        target_role = "MGMT"

    # OUTPUT SECTION
    st.markdown(f"### {t['result_header']}")
    output_placeholder = st.empty()
    
    # If we have a stored output (from history or previous run) AND we are NOT currently translating, show it
    if st.session_state.current_output and not translate_btn:
        output_placeholder.markdown(
            f"""<div class="output-container">{st.session_state.current_output}</div>""", 
            unsafe_allow_html=True
        )

    if translate_btn and input_text:
        # Update current input in case it wasn't captured (e.g. Ctrl+Enter)
        st.session_state.current_input = input_text
        
        # 1. GENERATE TITLE & CREATE HISTORY ITEM IMMEDIATELY
        title = input_text[:20].strip().replace("\n", " ") + ("..." if len(input_text) > 20 else "")
        new_history_item = {
            "title": title,
            "input": input_text,
            "output": "", # Initially empty
            "timestamp": time.time()
        }
        
        # Insert at top
        st.session_state.history.insert(0, new_history_item)
        save_history(st.session_state.history)
        
        # UPDATE SIDEBAR IMMEDIATELY
        render_history_list(history_placeholder, t, key_suffix="_live")
        
        full_response = ""
        
        # Stream logic
        try:
            with st.spinner(t['analyzing']):
                stream = translate_content(
                    input_text, 
                    source_role, 
                    target_role, 
                    model_choice,
                    auto_detect=auto_detect,
                    target_language=lang_choice
                )
                
                for chunk in stream:
                    full_response += chunk
                    # Real-time typing effect
                    output_placeholder.markdown(
                        f"""<div class="output-container">{full_response}</div>""", 
                        unsafe_allow_html=True
                    )
            
            # 2. UPDATE HISTORY ITEM WITH FINAL OUTPUT
            # (The item is already in the list, just update reference)
            new_history_item["output"] = full_response
            st.session_state.current_output = full_response
            
            # Persist update
            save_history(st.session_state.history)
            
            # No need to re-render sidebar history as the title didn't change, 
            # but usually good practice if we added status indicators.
                    
        except Exception as e:
            st.error(f"{t['error']}{str(e)}")
            # Remove the failed item if it didn't generate anything useful?
            # Or keep it as a failed log. Let's keep it.

with col2:
    st.markdown(f"### {t['what_is_this']}")
    st.markdown(t['what_is_this_content'])
    