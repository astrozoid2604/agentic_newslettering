# 🧠 Agentic Newsletter Generator

A multi-agent AI application that generates research-driven newsletter using [CrewAI](https://github.com/joaomdmoura/crewai), [Streamlit](https://streamlit.io/), and Cohere’s `command-r` language model. Built for writers, marketers, and researchers who want quick, accurate, and well-structured content generation from a simple web interface.

<p align="center">
  <img src="./github_thumbnail.png" alt="Project Thumbnail" width="600"/>
</p>

---

## 🚀 Features

- 🧠 Multi-agent architecture using CrewAI
- 🔍 Automated research via web search APIs
- ✍️ Markdown-based newsletter writing by AI
- 🎛️ Streamlit UI with adjustable creativity (temperature)
- 📎 Inline citations and reference management
- 💾 Exportable content in `.md` format

---

## 🧰 Tech Stack

- **[CrewAI](https://github.com/joaomdmoura/crewai)** – Agent orchestration framework  
- **[Cohere](https://cohere.com/)** – Language model backend (`command-r`)  
- **[Serper.dev](https://serper.dev/)** – Google Search API for real-time research  
- **[Streamlit](https://streamlit.io/)** – Lightweight web UI  
- **Python 3.10**

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone git@github.com:astrozoid2604/agentic_newslettering.git
cd agentic_newslettering
```

### 2. Set up the Conda environment

```bash
conda create -n aiagent python=3.10 -y
conda activate aiagent
pip install -r requirements.xt
```

### 3. Configure your environment variables
Create a `.env` file in the root directory:

```bash
COHERE_API_KEY=your-cohere-api-key
SERPER_API_KEY=your-serper-api-key
```

You can get your personal API keys here:
- [Serper API](https://serper.dev/)
- [Cohere API](https://dashboard.cohere.com/api-keys)

### 4. Launch the app

```bash
streamlit run app.py
```

### 5. Live-Demo Video

[![Watch the video](https://img.youtube.com/vi/huVbfgQ5yPw/0.jpg)](https://www.youtube.com/watch?v=huVbfgQ5yPw)

