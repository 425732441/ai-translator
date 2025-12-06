# AI Communication Translator (AI Talk)

A "Premium" experience translation tool designed to bridge the gap between **Product Managers (PM)**, **Developers**, and **Management**, using advanced AI models (Qwen Plus & Gemini Pro).

## 🚀 Quick Start

### 1. Installation

**Recommended: Use Conda (Python 3.10+)**

```bash
# Create and activate new environment
conda create -n ai-translator python=3.10 -y
conda activate ai-translator

# Install dependencies (using Aliyun mirror if you encounter SSL/Network errors)
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

### 2. Configuration

First, copy the example environment file to a new file named `.env`:
```bash
cp .env.example .env
# Windows PowerShell
# cp .env.example .env
```

Open `.env` and add your API keys:

```ini
DASHSCOPE_API_KEY=sk-xxxx...  # For Qwen
GEMINI_API_KEY=xxxx...        # For Gemini
```

### 3. Run the App

Launch the application with Streamlit:

```bash
streamlit run main.py
```

---

## ✨ Features

- **Multi-Model Support**: Choose between Alibaba's **Qwen Plus** or Google's **Gemini Pro**.
- **Role Translation**:
  - **PM ➡ Dev**: Converts business requirements into technical specs, RFC drafts, and risk assessments.
  - **Dev ➡ PM**: Converts technical achievements into business value, ROI, and user experience impact.
  - **➡ Management**: Summarizes technical/product updates into executive-level strategic summaries.
- **Smart Auto-Detect**: Automatically identifies who is speaking (PM/Dev/Mgmt) and translates to the appropriate target audience.
- **Proactive Intelligence**: The AI identifies **Missing Information** and suggests strategic questions to ask.
- **Premium UI**: Glassmorphism design, dark mode, and smooth animations.

---

## 🧠 Prompt Design Philosophy

This tool uses **Role-Playing** and **Chain-of-Thought** prompting:

1.  **Contextual Role Definition**: We explicitly tell the AI it is a "CTO" (for PM->Dev) or a "Product Owner" (for Dev->PM) to frame the output tone.
2.  **Structured Output**: Instead of free text, we force a Markdown structure (`### Technical Translation`, `### Missing Info`) to ensure the output is actionable.
3.  **Gap Analysis**: A key "Bonus" feature is asking the AI to find what is *missing*. A junior translator just translates; a senior partner points out gaps.

---

## 🧪 Test Cases

### Case 1: PM to Dev
**Input**:
> 我们需要一个智能推荐功能,提升用户停留时长

**Expected Output**:
- **Technical Summary**: Suggests Collaborative Filtering or DNN-based recommendation.
- **Architecture**: Redis for caching, Real-time inference service.
- **Missing Info**: "What is the QPS expectation? Do we need real-time personalization or batch updates?"

### Case 2: Dev to PM
**Input**:
> 我们优化了数据库查询，QPS提升了30%

**Expected Output**:
- **Business Value**: "System handles 30% more traffic without crashing -> Improved reliability."
- **UX Impact**: "Faster page loads -> Lower bounce rate."
- **Strategy**: "We can now support the upcoming marketing campaign without adding servers."
