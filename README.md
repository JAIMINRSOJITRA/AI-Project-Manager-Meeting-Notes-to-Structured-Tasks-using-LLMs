# 🚀 AI Project Manager — Meeting Notes to Structured Tasks

Turn messy meeting notes into a clean, trackable task list using LLMs.

## 📌 Overview

After a meeting, action items are usually buried in free-form notes. This app reads meeting notes (typed text, PDF, DOCX, email, or a Slack export), uses an LLM to extract structured tasks, and gives you an editable task board you can visualize and export.

It helps project managers, team leads, and students keep follow-ups from slipping through the cracks.

## ✨ Features

* Multiple input formats: plain text, PDF, DOCX, email, and Slack exports
* LLM extraction of tasks with assignee, priority (High / Medium / Low), deadline, description, and status
* Choice of Groq (cloud) or a local model via Ollama
* Interactive task table with filters and inline editing
* Kanban board and Gantt timeline views
* Export to CSV and Markdown
* SQLite persistence with meeting history
* 71-test Pytest suite

## 🛠️ Tech Stack

* Language: Python
* AI / LLM: Groq API, Ollama (local LLMs)
* Libraries: Streamlit, SQLAlchemy (SQLite), Pandas, Plotly, Pydantic, pypdf, python-docx
* Tools: Git, GitHub, Pytest

## 📂 Project Structure

```
AI-Project-Manager-Meeting-Notes-to-Structured-Tasks-using-LLMs/
├── app.py                # Streamlit app (4 tabs)
├── config.py             # Settings loaded from .env
├── database/             # connection, models, CRUD
├── input_processors/     # text, PDF, DOCX, email, Slack
├── llm/                  # prompt, extractor, parser
├── services/             # task service, export service
├── tests/                # 71 Pytest tests
└── requirements.txt
```

## ⚙️ Installation

1. Clone the repository:

```
git clone https://github.com/JAIMINRSOJITRA/AI-Project-Manager-Meeting-Notes-to-Structured-Tasks-using-LLMs.git
```

2. Navigate to the project:

```
cd AI-Project-Manager-Meeting-Notes-to-Structured-Tasks-using-LLMs
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your own settings (never commit it):

```
GROQ_API_KEY=your_key_here
# optional
GROQ_MODEL=llama-3.3-70b-versatile
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

## ▶️ Usage

```
streamlit run app.py
```

Then use the four tabs: **Process Notes** (input + extraction), **Tasks** (edit and filter), **Visualize** (Kanban + Gantt), and **Export** (CSV / Markdown). To run fully offline, install [Ollama](https://ollama.com), pull a model, and choose the local provider in the sidebar.

Run the tests:

```
pytest
```

## 📊 Results / Demo

* All 71 tests pass and the app launches cleanly.
* Paste meeting notes into the first tab, run extraction, and the resulting tasks appear in an editable table, a Kanban board, and a Gantt timeline.

## 🧠 What I Learned

* Getting reliable structured JSON out of an LLM, then validating and repairing it before it reaches the database
* A layered architecture (input → LLM → services → database) that keeps each part independently testable
* Normalizing many input formats into one pipeline
* Testing LLM-dependent code by isolating the model call

## 🔮 Future Improvements

* Push tasks to tools like Jira, Trello, or Notion
* Detect and merge duplicate tasks across meetings
* Send deadline reminders

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Jaimin Sojitra

* GitHub: https://github.com/JAIMINRSOJITRA
* LinkedIn: https://www.linkedin.com/in/jaimin-sojitra-4683a1277/
