# 🤖 AI Agent System with CrewAI

> 🚀 A powerful AI agent system built with CrewAI framework, featuring multimodal capabilities, memory integration, and diverse knowledge sources.

[![Python 3.11+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/joaomdmoura/crewAI)

## ✨ Features

### 🎯 Core Capabilities
- **🖼️ Multimodal Agents**
  - Image analysis using GPT-4 and Gemini models
  
- **🧠 Memory Integration**
  - Short-term memory 
  - Long-term memory
  - Entity-term memory
  - mem0

  
- **📚 Knowledge Sources**
  - 📝 String-based documents
  - 📄 Text files
  - 📑 PDF documents
  - 📊 CSV files
  - 🔄 JSON files
  - 🌐 Custom API integrations (e.g., Weather API)


### 👥 Human Collaboration
- Human validation and feedback integration
- Interactive decision-making processes

## 🛠️ Prerequisites

- 🐍 Python 3.11+
- 🔑 API Keys:
  - OpenAI (GPT-4)
  - Google Gemini
  - Serper
  - mem0

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/sourangshupal/crewai-advanced.git
cd your-repo-name
```

2. **Create a virtual environment**
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

## 📁 Project Structure

```
📦 AI-Agent-System
 ┣ 📓 crewai_advanced.ipynb    # CrewAI Advanced implementations
 ┣ 📓 knowledge.ipynb          # CrewAI Knowledge source demos
 ┣ 📓 memory.ipynb            # CrewAI Memory system examples
 ┣ 📜 multimodal-*.py         # Multimodal agent code
 ┣ 📜 memtest.py              # MemO test
 ┗ 📂 knowledge/
    ┗ 📄 company_info.json    # Sample data
```


## 🔐 Environment Variables

Required in `.env`:
```env
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
MEM0_API_KEY=your_key_here
```

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌱 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔍 Open a Pull Request

## 📝 License

[MIT License](LICENSE) - feel free to use this project for your own purposes!

## 🌟 Show your support

Give a ⭐️ if this project helped you!

---

<div align="center">
Made with ❤️ by Satish Tiwari
</div>
