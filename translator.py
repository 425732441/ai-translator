import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API Keys
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AIClient:
    def generate(self, system_prompt, user_prompt):
        raise NotImplementedError

class QwenClient(AIClient):
    def __init__(self):
        if not DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY not found in environment variables.")
        self.client = OpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.model = "qwen-plus"

    def generate(self, system_prompt, user_prompt):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                stream=True
            )
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error calling Qwen API: {str(e)}"

class GeminiClient(AIClient):
    def __init__(self, model_name="gemini-2.5-pro"):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model_name = model_name

    def generate(self, system_prompt, user_prompt):
        try:
            # Instantiate model per-call to support dynamic system instructions
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            
            response = model.generate_content(user_prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error calling Gemini API: {str(e)}"

def get_client(model_name):
    if model_name == "Qwen Plus":
        return QwenClient()
    elif model_name == "Gemini 2.5 Pro":
        return GeminiClient("gemini-2.5-pro")
    else:
        # Default or fallback
        return GeminiClient("gemini-2.5-pro")

# --- PROMPTS ---

AUTO_DETECT_PROMPT = """
You are an expert intent classifier.
Analyze the following input text and determine the most likely SPEAKER ROLE.

Options:
1. "PM" (Product Manager): **Requirement Discussion**, user scenarios, business goals, "we need...", "users want...".
2. "DEV" (Developer): **Technical Solution**, implementation details, databases, APIs, performance, "optimized...", "QPS...".
3. "MGMT" (Management): Discussing ROI, costs, timelines, "when will it be done...", "budget...".

Return ONLY the role code (PM, DEV, or MGMT). If unclear, default to PM.
"""

TRANSLATION_PROMPTS = {
    "PM_TO_DEV": """
You are a deeply experienced CTO who understands both product vision and engineering reality.
Your goal is to translate **Product Manager (PM)** language into **Developer** technical specifications.

**Context**: A PM has described a feature or requirement (Requirement Discussion).
**Task**:
1. Recommend specific algorithms or tech stacks (e.g., Collaborative Filtering, specific DBs).
2. Outline Data Sources and Processing flow.
3. Define Performance and Real-time requirements.
4. Estimate Development Workload.

**Output Format (Markdown)**:
### 🛠️ Technical Implementation / 技术方案建议
(Algorithm types, Tech stack recommendations)

### 🔄 Data Flow / 数据来源与处理
(Data sources, processing logic, storage)

### ⚡ Performance / 性能与实时性要求
(QPS, Latency, Concurrency)

### ⏱️ Workload Estimate / 预估开发工作量
(T-shirt sizing, Complexity analysis)

### ❓ Missing Information / 待确认疑问
(Crucial questions to ask for clarification)
""",
    "DEV_TO_PM": """
You are a savvy Product Owner who understands technology but cares strictly about User Value and Business ROI.
Your goal is to translate **Developer** technical jargon into **Product/Business** value.

**Context**: A Developer is reporting technical work (Technical Solution).
**Task**:
1. Explain the actual impact on User Experience.
2. Identify Business Growth opportunities unlocked by this.
3. Highlight Cost Reductions or Commercial Value.

**Output Format (Markdown)**:
### 🚀 User Experience Impact / 用户体验影响
(Actual changes users will feel: Speed, Stability, New Features)

### 📈 Business Growth Space / 业务增长空间
(New capabilities, scalability for future growth)

### 💰 Cost & Value / 降本与商业价值
(Infrastructure savings, Efficiency gains, ROI)
""",
    "ANY_TO_MGMT": """
You are a Management Consultant translating team updates for the **CEO/Board**.
Your goal is to strip away detail and focus on **ROI, Timeline, and Strategic Alignment**.

**Task**:
1. Summarize the input in 1 sentence (High-level Status).
2. Explain the impact on Company Goals (Revenue, Growth, Efficiency).
3. Estimate Timeline or Budget impact if applicable.

**Output Format (Markdown)**:
### 📊 Executive Summary / 高层摘要
(1-2 sentences)

### 💰 Strategic ROI / 战略回报
(Commercial impact)

### 🗓️ Timeline & Risks / 进度与风险
(High-level schedule/blockers)
"""
}

def detect_role_logic(text, client):
    # This is a bit of a hack: we use the generator but just take the full text
    full_resp = ""
    stream = client.generate(AUTO_DETECT_PROMPT, text)
    for chunk in stream:
        full_resp += chunk
    
    clean_resp = full_resp.strip().upper()
    if "PM" in clean_resp: return "PM"
    if "DEV" in clean_resp: return "DEV"
    if "MGMT" in clean_resp: return "MGMT"
    return "PM" # Default

def translate_content(text, source_role, target_role, model_name, auto_detect=False, target_language="English"):
    client = get_client(model_name)
    
    # Role Maps
    ROLE_MAP = {
        "English": {
            "PM": "Product Manager", 
            "DEV": "Developer", 
            "MGMT": "Management",
            "label": "👉 **Detected Role**",
            "analyzing": "🔍 *Analyzing input style...*"
        },
        "中文": {
            "PM": "产品经理", 
            "DEV": "开发人员", 
            "MGMT": "管理层",
            "label": "👉 **识别角色**",
            "analyzing": "🔍 *正在分析输入风格...*"
        }
    }
    # Fallback to English if unknown language
    lang_map = ROLE_MAP.get(target_language, ROLE_MAP["English"])

    detected_source = source_role
    if auto_detect:
        # We need a quick non-streaming call or just capture the stream
        # To avoid UI blocking, we can yield a "Detecting..." status first? 
        # For simplicity in this function, we'll just accept that the first part of the stream might be the detection if we wanted to show it,
        # but here we'll do two calls. Detection is fast.
        yield lang_map["analyzing"]
        detected_code = detect_role_logic(text, client)
        
        # Map code to full name
        detected_name = lang_map.get(detected_code, detected_code)
        
        yield f"\n\n{lang_map['label']}: {detected_name}\n\n---\n\n"
        
        # Determine target based on source (Logic uses the CODE)
        detected_source = detected_code # Update for logic flow below
        
        if detected_source == "PM":
            target_role = "DEV" # Default PM -> DEV
        elif detected_source == "DEV":
            target_role = "PM" # Default DEV -> PM
        elif detected_source == "MGMT":
            target_role = "DEV" # Assume MGMT talks to DEV/Team
        
    # Select Prompt
    prompt_key = ""
    if target_role == "MGMT":
        prompt_key = "ANY_TO_MGMT"
    elif detected_source == "PM" and target_role == "DEV":
        prompt_key = "PM_TO_DEV"
    elif detected_source == "DEV" and target_role == "PM":
        prompt_key = "DEV_TO_PM"
    else:
        # Fallback for weird combos
        prompt_key = "PM_TO_DEV" 

    base_prompt = TRANSLATION_PROMPTS.get(prompt_key, TRANSLATION_PROMPTS["PM_TO_DEV"])
    
    # Inject Language Constraint
    lang_instruction = f"\n\n**IMPORTANT**: The output response MUST be written in **{target_language}**. Keep specific technical terms in English where standard."
    system_prompt = base_prompt + lang_instruction
    
    # Generate Translation
    stream = client.generate(system_prompt, text)
    for chunk in stream:
        yield chunk
