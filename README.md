# 🤖 AI Project Manager
### Transform Meeting Notes into Structured Tasks using LLMs

A production-ready Streamlit application that leverages **Google Gemini** or **local Ollama models** to automatically extract, structure, and manage project tasks from unstructured meeting content.

> **Problem Statement**: Project managers spend hours manually reviewing meeting notes, emails, and chat threads to identify action items, assign owners, set priorities, and track deadlines. This tool eliminates that manual work entirely.

---

## 🎯 What This Application Does

**INPUT** → Meeting notes (Text, PDF, DOCX, Email, Slack)  
**PROCESS** → AI extracts tasks with assignees, priorities, and deadlines  
**OUTPUT** → Structured task list with Kanban board, Gantt chart, and export

### Core Capabilities

✅ **5 Input Sources** — Text, PDF, DOCX, Email threads, Slack conversations  
✅ **Dual LLM Support** — Cloud (Gemini) or Local (Ollama) for privacy  
✅ **Intelligent Extraction** — Identifies action items, infers priority, resolves relative dates  
✅ **Full CRUD Interface** — Add, edit, delete, filter, and search tasks  
✅ **Visual Project Management** — Kanban board + Gantt timeline  
✅ **Export Options** — CSV and Markdown report generation  
✅ **Persistent Storage** — SQLite database with meeting history  
✅ **Production Quality** — 71 passing unit tests, error handling, validation

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)               │
│  ┌──────────┬──────────┬──────────┬──────────┐             │
│  │ Process  │  Tasks   │ Visualize│  Export  │             │
│  │  Notes   │ & Editor │  Board   │  Data    │             │
│  └──────────┴──────────┴──────────┴──────────┘             │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│               INPUT PROCESSORS LAYER                        │
│  ┌────────┬────────┬────────┬────────┬────────┐            │
│  │  Text  │  PDF   │  DOCX  │ Email  │ Slack  │            │
│  └────────┴────────┴────────┴────────┴────────┘            │
│  (pypdf, python-docx, regex cleaning)                       │
└──────────────────┬──────────────────────────────────────────┘
                   │ Clean Plain Text
┌──────────────────┴──────────────────────────────────────────┐
│                    LLM EXTRACTION LAYER                     │
│  ┌────────────────────────────────────────────┐             │
│  │  Prompt Engineering (llm/prompt.py)        │             │
│  │  • System prompt (role, rules, checklist)  │             │
│  │  • User prompt (notes + today's date)      │             │
│  └────────────────┬───────────────────────────┘             │
│                   │                                          │
│  ┌────────────────┴───────────────────────────┐             │
│  │  LLM Client (llm/extractor.py)             │             │
│  │  • Gemini API (google-genai)               │             │
│  │  • Ollama API (ollama Python SDK)          │             │
│  └────────────────┬───────────────────────────┘             │
└──────────────────┬──────────────────────────────────────────┘
                   │ Raw JSON Response
┌──────────────────┴──────────────────────────────────────────┐
│              VALIDATION LAYER (Pydantic)                    │
│  ┌────────────────────────────────────────────┐             │
│  │  llm/parser.py                             │             │
│  │  • TaskOutput schema                       │             │
│  │  • MeetingOutput schema                    │             │
│  │  • Field validators + defaults             │             │
│  └────────────────┬───────────────────────────┘             │
└──────────────────┬──────────────────────────────────────────┘
                   │ Validated Python Objects
┌──────────────────┴──────────────────────────────────────────┐
│             BUSINESS LOGIC LAYER (Services)                 │
│  ┌────────────────────────────────────────────┐             │
│  │  services/task_service.py                  │             │
│  │  • Orchestrates LLM → Validation → DB      │             │
│  │  • Atomic transactions with rollback       │             │
│  └────────────────┬───────────────────────────┘             │
│  ┌────────────────┴───────────────────────────┐             │
│  │  services/export_service.py                │             │
│  │  • CSV generation                          │             │
│  │  • Markdown report formatting              │             │
│  └────────────────┬───────────────────────────┘             │
└──────────────────┬──────────────────────────────────────────┘
                   │ CRUD Operations
┌──────────────────┴──────────────────────────────────────────┐
│           DATABASE LAYER (SQLAlchemy ORM)                   │
│  ┌────────────────────────────────────────────┐             │
│  │  database/connection.py                    │             │
│  │  • Engine + SessionLocal factory           │             │
│  │  • init_db() table creation                │             │
│  └────────────────┬───────────────────────────┘             │
│  ┌────────────────┴───────────────────────────┐             │
│  │  database/models.py                        │             │
│  │  • Meeting ORM model                       │             │
│  │  • Task ORM model (FK → Meeting)           │             │
│  │  • Cascade delete relationship             │             │
│  └────────────────┬───────────────────────────┘             │
│  ┌────────────────┴───────────────────────────┐             │
│  │  database/crud.py                          │             │
│  │  • create_meeting() / create_task()        │             │
│  │  • get_all_meetings() / get_tasks()        │             │
│  │  • update_task_field() / bulk_update()     │             │
│  │  • delete_meeting() / delete_task()        │             │
│  │  • tasks_to_dataframe() converter          │             │
│  └────────────────┬───────────────────────────┘             │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴────────────┐
        │  project_manager.db   │
        │  (SQLite Database)    │
        └───────────────────────┘
```

---

## 🔄 Complete Application Flow

### 📝 Step 1: Input Selection
**User Action:** Opens the **Process Notes** tab in Streamlit

**Available Options:**
1. **📝 Text** — Paste raw meeting transcript or notes
2. **📄 PDF** — Upload scanned/digital meeting documents
3. **📃 DOCX** — Upload Microsoft Word files
4. **📧 Email** — Paste email thread copy
5. **💬 Slack** — Paste channel/thread messages

**What Happens:**
- Streamlit displays the appropriate input widget (text area or file uploader)
- User provides content via paste or upload
- `st.file_uploader` reads bytes for PDFs/DOCX

### 📋 Step 2: Input Processing
**Module:** `input_processors/` (5 specialized processors)

**Text Processor** (`text_processor.py`):
- Strips leading/trailing whitespace per line
- Collapses multiple consecutive blank lines
- Returns normalized plain text

**PDF Processor** (`pdf_processor.py`):
- Uses `pypdf.PdfReader` to extract text from each page
- Adds page markers (`--- Page X ---`)
- Handles text-based PDFs only (no OCR for scanned images)

**DOCX Processor** (`docx_processor.py`):
- Uses `python-docx` Document API
- Extracts all paragraph text
- Flattens table cells with `|` separators

**Email Processor** (`email_processor.py`):
- Strips standard headers: `From:`, `To:`, `Subject:`, `Date:`
- Removes quoted reply lines (starting with `>`)
- Removes signature separators (`--`, `___`)

**Slack Processor** (`slack_processor.py`):
- Filters system messages: `joined the channel`, `left the channel`, `pinned a message`
- Preserves conversational format: `John Doe 10:30 AM\nMessage text`
- Adds context header for LLM understanding

**Output:** Clean, normalized plain text ready for LLM analysis

### 🤖 Step 3: LLM Extraction
**Module:** `llm/extractor.py`

**Provider Selection:**
- **Gemini (Google)** — Cloud API via `google-genai` SDK
- **Ollama (Local)** — On-premise via `ollama` Python SDK

**Prompt Construction** (`llm/prompt.py`):

**System Prompt** (1,500+ words):
- **Role Definition:** Expert AI Project Manager with 10+ years experience
- **Task Identification Rules:** Must start with verb, no greetings/opinions
- **Assignee Rules:** Use explicit names or "Unassigned", never guess
- **Priority Detection:** High (urgent/blocker), Medium (planned), Low (backlog)
- **Date Resolution:** Convert "next Monday" to `YYYY-MM-DD` using supplied date
- **Quality Checklist:** 11-point validation before returning JSON
- **JSON Schema:** Exact structure with field types and constraints

**User Prompt:**
```
Today's Date: 2026-07-07

Analyze the following meeting notes and extract structured project management
data according to the rules in your system instructions.
Return ONLY valid JSON. No extra text.

=== MEETING NOTES START ===
[Clean plain text from input processor]
=== MEETING NOTES END ===
```

**API Call:**
```python
# Gemini
client.models.generate_content(
    model="gemini-2.5-flash",
    contents=full_prompt
)

# Ollama
ollama.chat(
    model="llama3",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
```

**LLM Response Example:**
```json
{
  "title": "Sprint Planning - Q3 Roadmap",
  "summary": "Team discussed Q3 priorities, agreed to focus on...",
  "decisions": [
    "Move beta release to August 15th",
    "Hire two frontend developers by month-end"
  ],
  "tasks": [
    {
      "name": "Fix login authentication bug",
      "assignee": "Rahul",
      "priority": "High",
      "due_date": "2026-07-10",
      "description": "Users cannot log in with SSO. Critical blocker.",
      "status": "Todo"
    },
    ...
  ]
}
```

### ✅ Step 4: Validation
**Module:** `llm/parser.py` (Pydantic schemas)

**TaskOutput Model:**
```python
class TaskOutput(BaseModel):
    name: str                      # Required
    assignee: str = "Unassigned"   # Default if missing
    priority: str = "Medium"       # Default if missing/invalid
    due_date: Optional[str] = None # YYYY-MM-DD or null
    description: Optional[str] = ""
    status: str = "Todo"           # Always Todo for new
```

**Field Validators:**
- `validate_priority()` — Ensures only High/Medium/Low, fallback to Medium
- `validate_assignee()` — Replaces empty string with "Unassigned"
- `validate_due_date()` — Accepts only `YYYY-MM-DD` or null, discards invalid

**MeetingOutput Model:**
```python
class MeetingOutput(BaseModel):
    title: str                           # Required
    summary: str                         # Required
    decisions: List[str] = []            # Optional
    tasks: List[TaskOutput] = []         # Optional
```

**Parsing Function:**
```python
def parse_llm_response(raw_response: str) -> MeetingOutput:
    # Strip markdown code fences (```json ... ```)
    # Parse JSON string → Python dict
    # Validate against MeetingOutput schema
    # Return validated object or raise ValueError
```

**Error Handling:**
- **Invalid JSON** → `ValueError: LLM returned invalid JSON`
- **Missing required field** → `ValueError: JSON does not match schema`
- **Type mismatch** → Pydantic auto-converts or raises validation error

### 💾 Step 5: Database Storage
**Module:** `services/task_service.py` + `database/crud.py`

**Orchestration Function:**
```python
def process_meeting(db, meeting_notes, provider, model):
    # 1. Extract data via LLM
    meeting_output = extract_meeting_data(...)
    
    # 2. Create Meeting record
    meeting = crud.create_meeting(db, title, summary, decisions)
    db.flush()  # Get meeting.id
    
    # 3. Create Task records (loop)
    for task in meeting_output.tasks:
        crud.create_task(db, meeting.id, task_data)
    
    # 4. Commit transaction (atomic)
    db.commit()
    return meeting.id
```

**Database Tables:**

**meetings:**
```sql
id          INTEGER PRIMARY KEY AUTOINCREMENT
title       VARCHAR(255) NOT NULL
summary     TEXT
decisions   TEXT
created_at  DATETIME(timezone=True) DEFAULT CURRENT_TIMESTAMP
```

**tasks:**
```sql
id          INTEGER PRIMARY KEY AUTOINCREMENT
meeting_id  INTEGER NOT NULL REFERENCES meetings(id) ON DELETE CASCADE
name        VARCHAR(512) NOT NULL
assignee    VARCHAR(255) DEFAULT 'Unassigned'
priority    VARCHAR(50) DEFAULT 'Medium'
due_date    VARCHAR(20) NULL
description TEXT
status      VARCHAR(50) DEFAULT 'Todo'
created_at  DATETIME(timezone=True) DEFAULT CURRENT_TIMESTAMP
```

**Relationship:** Meeting (1) ← (Many) Task with CASCADE DELETE

**CRUD Operations:**
- `create_meeting()` — Insert + flush to get ID
- `create_task()` — Insert with FK to meeting
- `get_all_meetings()` — Fetch ordered by created_at DESC
- `get_tasks_by_meeting()` — Fetch by meeting_id FK
- `update_task_field()` — Single field update
- `bulk_update_tasks()` — Sync edited DataFrame
- `delete_meeting()` — Delete + auto-cascade to tasks
- `delete_task()` — Delete single task
- `tasks_to_dataframe()` — ORM → Pandas conversion

### 🎨 Step 6: UI Display
**Tab 1: Process Notes**

**After Extraction:**
1. **Meeting Header** — AI-generated title
2. **Summary Card** — Styled `<div>` with gradient background
3. **Key Decisions** — Markdown bullet list
4. **Metric Cards** — 4 clickable buttons:
   - 📋 Total Tasks
   - 🔥 High Priority
   - ⏳ Todo
   - ✅ Done
5. **Filtered Task Table** — Updates when metric card clicked
   - Active filter highlighted with ⭐
   - Read-only `st.dataframe()` with custom column config

**Custom CSS Styling:**
- Google Fonts (Inter)
- Dark gradient backgrounds (`linear-gradient(135deg, ...)`)
- Hover effects (`transform: translateY(-2px)`)
- Border animations on metric cards
- Priority badges (colored pills)

### ✏️ Step 7: Task Management
**Tab 2: Tasks & Editor**

**Section 1: Task List**
**Filters (4 columns):**
- 🔎 **Search** — Free text across name/assignee/description
- **Status** — Multi-select from STATUS_OPTIONS
- **Priority** — Multi-select from PRIORITY_OPTIONS
- **Assignee** — Multi-select from unique assignees in current meeting

**Applied Logic:**
```python
filtered_df = df.copy()
if search_q:
    mask = (df['name'].str.contains(search_q, case=False) | ...)
    filtered_df = filtered_df[mask]
if filter_status:
    filtered_df = filtered_df[filtered_df['status'].isin(filter_status)]
# ... similar for priority and assignee
```

**Display:**
- Shows `X of Y tasks` counter
- Read-only `st.dataframe()` with no ID column
- Custom column widths (name and description are "large")

**Section 2: Add New Task Form**
```python
with st.form("add_task_form", clear_on_submit=True):
    new_name = st.text_input("Task Name*", ...)
    new_assignee = st.text_input("Assignee", ...)
    new_priority = st.selectbox("Priority", PRIORITY_OPTIONS)
    new_due_date = st.text_input("Due Date (YYYY-MM-DD)", ...)
    new_desc = st.text_area("Description", ...)
    submit_add = st.form_submit_button("➕ Add Task & Save")
```

**On Submit:**
- Validates `new_name.strip()` not empty
- Creates "Manual Tasks" meeting if no active meeting
- Calls `crud.create_task()` + `db.commit()`
- Refreshes `st.session_state.tasks_df`
- Triggers `st.rerun()` to update UI

**Section 3: Edit/Delete Task Form**
```python
task_options = {f"{row['name']} ({row['assignee']})": index for ...}
selected_task_label = st.selectbox("Choose task...", task_options)

with st.form("edit_task_form"):
    edit_name = st.text_input("Task Name*", value=task_row['name'])
    # ... all editable fields pre-filled
    
    c_save, c_delete = st.columns(2)
    submit_edit = st.form_submit_button("💾 Save Edits")
    submit_delete = st.form_submit_button("🗑️ Delete Task")
```

**On Save:**
- Fetches task by `task_id` from DB
- Updates all fields
- Commits + refreshes + rerun

**On Delete:**
- Calls `crud.delete_task(task_id)`
- Removes from `st.session_state.tasks_df`
- Commits + refreshes + rerun

### 📊 Step 8: Visualization
**Tab 3: Visualize**

**Kanban Board:**
```html
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr;">
  <div class="kanban-col">
    <div class="kanban-col-header" style="background: #dc2626;">
      📋 Todo (X tasks)
    </div>
    <!-- Task cards -->
  </div>
  <div class="kanban-col">
    <div class="kanban-col-header" style="background: #ea580c;">
      ⏳ In Progress (Y tasks)
    </div>
  </div>
  <div class="kanban-col">
    <div class="kanban-col-header" style="background: #16a34a;">
      ✅ Done (Z tasks)
    </div>
  </div>
</div>
```

**Task Card HTML:**
```html
<div class="task-card">
  <h4>Fix login bug</h4>
  <p>👤 Rahul | 🔥 High | 📅 2026-07-10</p>
</div>
```

**Gantt Chart (Plotly):**
```python
fig = px.timeline(
    gantt_df,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Status",
    hover_data=["Assignee", "Priority"]
)
fig.update_layout(
    xaxis_title="Timeline",
    yaxis_title="Tasks",
    height=500,
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)
```

**Gantt Data Preparation:**
- Filters tasks with valid `due_date`
- Creates `Start` = today, `Finish` = due_date
- Groups by Status for color coding

### 📥 Step 9: Export
**Tab 4: Export**

**CSV Export:**
```python
def export_to_csv(tasks_df):
    # Drop 'id' column
    # Rename columns to Title Case
    # Convert to CSV bytes
    return df.to_csv(index=False).encode('utf-8')
```

**Download Button:**
```python
st.download_button(
    label="📥 Download CSV",
    data=csv_bytes,
    file_name=f"tasks_{timestamp}.csv",
    mime="text/csv"
)
```

**Markdown Export:**
```python
def export_to_markdown(title, summary, decisions, tasks_df):
    md_lines = [
        f"# 📋 {title}",
        f"> Generated on {timestamp}",
        "## 📝 Meeting Summary",
        summary,
        "## ✅ Key Decisions",
        decisions,
        "## 📌 Extracted Tasks",
        "| Task | Assignee | Priority | Due Date | Status | Description |",
        "| --- | --- | --- | --- | --- | --- |",
        # ... task rows
    ]
    return "\n".join(md_lines).encode('utf-8')
```

**Features:**
- Replaces empty due_date with "TBD"
- Escapes `|` characters in descriptions
- Formats as GitHub-compatible Markdown table
- Includes generation timestamp

---

## 📂 Detailed File Structure

```
project_root/
│
├── app.py                          # Streamlit UI entry point (800+ lines)
│   ├── Page config + custom CSS
│   ├── Session state initialization
│   ├── Sidebar (LLM settings + meeting history)
│   ├── Tab 1: Process Notes (input + extraction)
│   ├── Tab 2: Tasks & Editor (CRUD operations)
│   ├── Tab 3: Visualize (Kanban + Gantt)
│   └── Tab 4: Export (CSV + Markdown)
│
├── config.py                       # Environment configuration
│   ├── load_dotenv() loader
│   ├── GEMINI_API_KEY
│   ├── GEMINI_MODEL (gemini-2.5-flash)
│   ├── OLLAMA_BASE_URL (localhost:11434)
│   ├── OLLAMA_MODEL (llama3)
│   ├── DATABASE_URL
│   ├── APP_TITLE / APP_SUBTITLE
│   ├── LLM_PROVIDERS list
│   ├── PRIORITY_OPTIONS (High/Medium/Low)
│   ├── STATUS_OPTIONS (Todo/In Progress/Done)
│   └── INPUT_SOURCES (5 types)
│
├── requirements.txt                # Python dependencies
│   ├── streamlit >= 1.35.0
│   ├── google-genai >= 1.0.0      # Gemini SDK
│   ├── ollama >= 0.2.0            # Local LLM SDK
│   ├── sqlalchemy >= 2.0.0        # ORM
│   ├── pandas >= 2.0.0
│   ├── plotly >= 5.20.0           # Charts
│   ├── python-dotenv >= 1.0.0
│   ├── pydantic >= 2.0.0          # Validation
│   ├── pypdf >= 4.0.0             # PDF parsing
│   └── python-docx >= 1.1.0       # Word parsing
│
├── .env                            # API keys (NEVER commit!)
│   ├── GEMINI_API_KEY=your_key
│   ├── GEMINI_MODEL=gemini-2.5-flash
│   ├── OLLAMA_BASE_URL=http://localhost:11434
│   ├── OLLAMA_MODEL=llama3
│   └── DATABASE_URL=sqlite:///project_manager.db
│
├── .gitignore                      # Git exclusions
│   ├── .env
│   ├── *.db
│   ├── __pycache__/
│   └── .pytest_cache/
│
├── README.md                       # This documentation
│
├── project_manager.db              # SQLite database (auto-created)
│
├── input_processors/                # Input format converters
│   ├── __init__.py
│   ├── text_processor.py           # Plain text cleaner
│   │   └── process_text() → strips whitespace, collapses blanks
│   ├── pdf_processor.py            # PDF extractor (pypdf)
│   │   └── process_pdf() → extracts text per page, adds markers
│   ├── docx_processor.py           # Word document parser
│   │   └── process_docx() → paragraphs + tables → plain text
│   ├── email_processor.py          # Email thread cleaner
│   │   └── process_email() → strips headers, quoted replies, signatures
│   └── slack_processor.py          # Slack thread formatter
│       └── process_slack() → removes system messages, preserves conversation
│
├── llm/                            # AI extraction layer
│   ├── __init__.py
│   ├── prompt.py                   # Prompt engineering
│   │   ├── get_system_prompt() → 1500+ word instruction set
│   │   │   • Role definition (expert PM)
│   │   │   • Task identification rules
│   │   │   • Priority detection logic
│   │   │   • Date resolution instructions
│   │   │   • Quality checklist (11 points)
│   │   │   • JSON schema definition
│   │   └── get_user_prompt(notes) → injects notes + today's date
│   ├── extractor.py                # LLM API clients
│   │   ├── call_gemini() → google.genai.Client.generate_content()
│   │   ├── call_ollama() → ollama.chat() with system/user messages
│   │   └── extract_meeting_data() → orchestrator, returns MeetingOutput
│   └── parser.py                   # Pydantic validation
│       ├── TaskOutput(BaseModel)
│       │   • name: str (required)
│       │   • assignee: str = "Unassigned"
│       │   • priority: str = "Medium"
│       │   • due_date: Optional[str] = None
│       │   • description: Optional[str] = ""
│       │   • status: str = "Todo"
│       │   • @field_validator for priority, assignee, due_date
│       ├── MeetingOutput(BaseModel)
│       │   • title: str
│       │   • summary: str
│       │   • decisions: List[str] = []
│       │   • tasks: List[TaskOutput] = []
│       └── parse_llm_response() → strips markdown, parses JSON, validates
│
├── database/                       # Data persistence layer
│   ├── __init__.py
│   ├── connection.py               # SQLAlchemy setup
│   │   ├── engine = create_engine(DATABASE_URL)
│   │   ├── SessionLocal = sessionmaker(bind=engine)
│   │   ├── Base = declarative_base()
│   │   ├── get_db() → yields session with auto-close
│   │   └── init_db() → creates tables if not exist
│   ├── models.py                   # ORM table definitions
│   │   ├── Meeting(Base)
│   │   │   • id: Integer PK
│   │   │   • title: String(255)
│   │   │   • summary: Text
│   │   │   • decisions: Text
│   │   │   • created_at: DateTime(timezone=True)
│   │   │   • tasks: relationship with cascade delete
│   │   └── Task(Base)
│   │       • id: Integer PK
│   │       • meeting_id: Integer FK → meetings.id CASCADE
│   │       • name: String(512)
│   │       • assignee: String(255) = "Unassigned"
│   │       • priority: String(50) = "Medium"
│   │       • due_date: String(20) nullable
│   │       • description: Text
│   │       • status: String(50) = "Todo"
│   │       • created_at: DateTime(timezone=True)
│   │       • meeting: relationship back_populates
│   └── crud.py                     # Database operations (10 functions)
│       ├── create_meeting() → insert + flush → return Meeting
│       ├── create_task() → insert Task with FK
│       ├── get_all_meetings() → query ordered by created_at DESC
│       ├── get_meeting_by_id() → single Meeting or None
│       ├── get_tasks_by_meeting() → list of Tasks for meeting_id
│       ├── tasks_to_dataframe() → ORM objects → pandas DataFrame
│       ├── update_task_field() → single field update
│       ├── bulk_update_tasks() → sync DataFrame → DB
│       ├── delete_meeting() → cascade deletes tasks
│       └── delete_task() → single task deletion
│
├── services/                        # Business logic orchestration
│   ├── __init__.py
│   ├── task_service.py             # Main processing pipeline
│   │   └── process_meeting(db, notes, provider, model)
│   │       1. extract_meeting_data() → calls LLM
│   │       2. create_meeting() → inserts Meeting record
│   │       3. Loop: create_task() → inserts each Task
│   │       4. db.commit() → atomic transaction
│   │       5. return meeting.id
│   │       • Includes rollback on failure
│   └── export_service.py           # Export generators
│       ├── export_to_csv(df) → bytes
│       │   • Drops 'id' column
│       │   • Renames columns to Title Case
│       │   • Returns UTF-8 encoded CSV
│       └── export_to_markdown(title, summary, decisions, df) → bytes
│           • Generates formatted Markdown report
│           • Includes metadata header
│           • Builds task table
│           • Returns UTF-8 encoded .md file
│
└── tests/                          # Unit test suite (71 tests, 100% pass)
    ├── __init__.py
    ├── test_database.py            # 20 tests
    │   • Test Meeting CRUD operations
    │   • Test Task CRUD operations
    │   • Test relationship cascade delete
    │   • Test tasks_to_dataframe() conversion
    │   • Test get_all_meetings() ordering
    │   • Test foreign key constraints
    ├── test_export_service.py      # 16 tests
    │   • Test CSV column names
    │   • Test CSV data encoding
    │   • Test Markdown structure
    │   • Test Markdown table formatting
    │   • Test empty DataFrame handling
    │   • Test special character escaping
    ├── test_input_processors.py    # 15 tests
    │   • Test text_processor whitespace cleaning
    │   • Test email_processor header removal
    │   • Test email_processor quote stripping
    │   • Test slack_processor system message filter
    │   • Test blank line collapse logic
    ├── test_parser.py              # 20 tests
    │   • Test TaskOutput validation
    │   • Test default value assignment
    │   • Test priority validator
    │   • Test assignee validator
    │   • Test due_date format validation
    │   • Test MeetingOutput schema
    │   • Test parse_llm_response()
    │   • Test markdown fence stripping
    │   • Test invalid JSON error handling
    └── __pycache__/                # Python bytecode cache

```

---

## ⚡ Installation & Setup

### Prerequisites

- **Python 3.10+** (Recommended: 3.11)
- **pip** package manager
- **Git** (for cloning)
- **Gemini API Key** OR **Ollama** installed locally

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd "AI Project Manager Meeting Notes to Structured Tasks using LLMs"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Installed Packages:**
- `streamlit` — Web UI framework
- `google-genai` — Gemini API client
- `ollama` — Local LLM client
- `sqlalchemy` — Database ORM
- `pandas` — Data manipulation
- `plotly` — Interactive charts
- `python-dotenv` — Environment variable loader
- `pydantic` — Data validation
- `pypdf` — PDF text extraction
- `python-docx` — Word document parsing

### Step 4: Configure Environment

Create/edit `.env` file in project root:

```env
# === LLM Provider: Gemini (Cloud) ===
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX
GEMINI_MODEL=gemini-2.5-flash

# === LLM Provider: Ollama (Local) ===
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# === Database ===
DATABASE_URL=sqlite:///project_manager.db
```

**Get Gemini API Key:**
1. Visit https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `.env`

**Setup Ollama (Optional):**
```bash
# 1. Download Ollama from https://ollama.com
# 2. Install and start the service
# 3. Pull a model (examples):

ollama pull llama3          # Meta Llama 3 (4.7 GB)
ollama pull phi3            # Microsoft Phi-3 (2.3 GB) — Recommended
ollama pull mistral         # Mistral 7B (4.1 GB)
ollama pull gemma2          # Google Gemma 2 (5.4 GB)

# 4. Verify model is available
ollama list

# 5. Update .env with model name
# OLLAMA_MODEL=phi3
```

### Step 5: Run Application

```bash
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.X:8501
```

Open browser at `http://localhost:8501`

### Step 6: First Run Initialization

On first launch:
1. SQLite database `project_manager.db` is auto-created
2. Tables `meetings` and `tasks` are created via `init_db()`
3. No manual database setup required

---

## 🎮 Usage Guide

### Basic Workflow

**1. Select LLM Provider (Sidebar)**
- Choose "Gemini (Google)" for cloud processing
- Choose "Local LLM (Ollama)" for on-premise processing

**2. Select Model (Sidebar)**
- **Gemini:** `gemini-2.5-flash` (recommended), `gemini-2.5-pro`, `gemini-2.0-flash`
- **Ollama:** Type your pulled model name (e.g., `phi3`, `llama3`)

**3. Process Meeting Notes (Tab 1)**
- Select input source type
- Paste text or upload file
- Click "✨ Generate Project Plan"
- Wait 10-30 seconds for LLM processing

**4. Review Results (Tab 1)**
- Meeting title and summary displayed
- Key decisions listed
- Click metric cards to filter tasks:
  - 📋 Total Tasks
  - 🔥 High Priority
  - ⏳ Todo
  - ✅ Done

**5. Manage Tasks (Tab 2)**
- **Filter:** Use dropdowns to filter by Status/Priority/Assignee
- **Search:** Type keywords to search task names/descriptions
- **Add:** Fill form and click "➕ Add Task & Save"
- **Edit:** Select task from dropdown, modify fields, click "💾 Save Edits"
- **Delete:** Select task and click "🗑️ Delete Task"

**6. Visualize Progress (Tab 3)**
- View **Kanban Board** with 3 columns (Todo/In Progress/Done)
- View **Gantt Timeline** showing task deadlines
- Hover over Gantt bars for details

**7. Export Data (Tab 4)**
- Click "📥 Download CSV" for spreadsheet export
- Click "📥 Download Markdown Report" for formatted document

**8. Load Past Meetings (Sidebar)**
- Select meeting from "Meeting History" dropdown
- Click "📂 Load Meeting" to restore

### Advanced Features

**Session State Persistence:**
- All data persists in `st.session_state` across tab switches
- No re-extraction when switching tabs
- Database writes are immediate (no "Save" button needed)

**Automatic Meeting Creation:**
- If you add tasks manually without processing notes first
- App auto-creates "Manual Tasks" meeting to hold them
- Ensures all tasks have a parent Meeting record

**Date Resolution:**
- LLM receives today's date in prompt
- Converts relative dates: "tomorrow", "next Monday", "end of week"
- Validates output as `YYYY-MM-DD` format
- Invalid dates become `null` (TBD)

**Priority Inference:**
- **High:** Keywords like "urgent", "critical", "blocker", "ASAP", "hotfix"
- **Medium:** Default for normal sprint work
- **Low:** Keywords like "backlog", "future", "nice to have", "eventually"

**Duplicate Task Handling:**
- LLM instructed to merge duplicate mentions
- Consolidates context into single task description

---

## 🗄️ Database Schema Details

### meetings Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique meeting identifier |
| `title` | VARCHAR(255) | NOT NULL | AI-generated meeting name |
| `summary` | TEXT | NULL | AI-written paragraph summary |
| `decisions` | TEXT | NULL | Markdown bullet list of decisions |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW | Timezone-aware UTC timestamp |

**Indexes:** Primary key auto-indexed

### tasks Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique task identifier |
| `meeting_id` | INTEGER | NOT NULL, FK → meetings.id, ON DELETE CASCADE | Parent meeting reference |
| `name` | VARCHAR(512) | NOT NULL | Actionable task title (verb-first) |
| `assignee` | VARCHAR(255) | NULL, DEFAULT 'Unassigned' | Person responsible |
| `priority` | VARCHAR(50) | NULL, DEFAULT 'Medium' | High / Medium / Low |
| `due_date` | VARCHAR(20) | NULL | YYYY-MM-DD format or null |
| `description` | TEXT | NULL | Brief context (1-2 sentences) |
| `status` | VARCHAR(50) | NULL, DEFAULT 'Todo' | Todo / In Progress / Done |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW | Timezone-aware UTC timestamp |

**Indexes:** 
- Primary key auto-indexed
- Foreign key `meeting_id` auto-indexed

**Constraints:**
- `ON DELETE CASCADE` — Deleting a meeting auto-deletes all its tasks
- Foreign key enforced by SQLAlchemy

**Relationship:**
```python
# One-to-Many: Meeting → Tasks
Meeting.tasks  # List of Task objects
Task.meeting   # Parent Meeting object
```

### Database File Location

- **Development:** `./project_manager.db` (project root)
- **Production:** Set via `DATABASE_URL` in `.env`

### Backup & Migration

**Backup:**
```bash
# Copy database file
cp project_manager.db project_manager_backup_2026-07-07.db

# Or use SQLite dump
sqlite3 project_manager.db .dump > backup.sql
```

**Restore:**
```bash
# Restore from file
cp project_manager_backup_2026-07-07.db project_manager.db

# Or restore from SQL dump
sqlite3 project_manager.db < backup.sql
```

**Reset Database:**
```bash
# Delete database file (will be recreated on next run)
rm project_manager.db  # macOS/Linux
del project_manager.db  # Windows
```

---

## 🧪 Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

**Expected Output:**
```
tests/test_database.py::test_create_meeting PASSED                    [ 1%]
tests/test_database.py::test_create_task PASSED                       [ 2%]
tests/test_database.py::test_get_all_meetings PASSED                  [ 4%]
...
tests/test_parser.py::test_validate_due_date_invalid PASSED          [100%]

========================= 71 passed in 4.83s ==========================
```

### Run Specific Test File

```bash
python -m pytest tests/test_database.py -v
python -m pytest tests/test_parser.py -v
```

### Run with Coverage Report

```bash
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

Open `htmlcov/index.html` in browser to view coverage

### Test Categories

**test_database.py (20 tests):**
- Meeting CRUD: create, read, update, delete
- Task CRUD: create, read, update, delete
- Cascade delete behavior
- DataFrame conversion
- Query ordering
- Foreign key enforcement

**test_export_service.py (16 tests):**
- CSV generation and encoding
- Markdown formatting
- Column renaming
- Empty DataFrame handling
- Special character escaping in tables
- Timestamp formatting

**test_input_processors.py (15 tests):**
- Text processor: whitespace cleaning, blank line collapse
- Email processor: header removal, quote stripping
- Slack processor: system message filtering
- Edge cases: empty input, malformed content

**test_parser.py (20 tests):**
- TaskOutput validation
- MeetingOutput validation
- Default value assignment
- Field validators (priority, assignee, due_date)
- JSON parsing with markdown fence removal
- Error handling for invalid JSON
- Schema mismatch detection

---

## 🔐 Security & Best Practices

### API Key Protection

**DO:**
✅ Store API keys in `.env` file (local development)
✅ Add `.env` to `.gitignore` (already done)
✅ Use Streamlit Secrets for cloud deployment
✅ Rotate API keys periodically

**DON'T:**
❌ Hardcode API keys in source code
❌ Commit `.env` to Git
❌ Share API keys in screenshots or logs
❌ Use production keys for development

### Streamlit Cloud Secrets

For deployment on Streamlit Cloud:

1. Go to your app dashboard
2. Click **Settings** → **Secrets**
3. Add in TOML format:

```toml
GEMINI_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXX"
GEMINI_MODEL = "gemini-2.5-flash"
DATABASE_URL = "sqlite:///project_manager.db"
```

4. Restart app to load secrets

### Database Security

**SQLite Best Practices:**
- ✅ Use parameterized queries (SQLAlchemy ORM handles this)
- ✅ Validate input via Pydantic before DB write
- ✅ Use transactions with rollback on error
- ✅ Regular backups for production data

**NOT Recommended for Production at Scale:**
- SQLite has file locking issues with high concurrency
- Consider PostgreSQL/MySQL for multi-user production

### Input Validation

**Implemented Safeguards:**
1. **Pydantic Validation** — Type checking + field validators
2. **SQL Injection Prevention** — ORM parameterized queries
3. **JSON Parsing Safety** — Try-except with error messages
4. **File Upload Limits** — Streamlit default 200MB
5. **LLM Response Sanitization** — Strip markdown fences

### Error Handling

**User-Facing Errors:**
```python
try:
    process_meeting(...)
except ValueError as e:
    st.error(f"❌ Extraction failed: {e}")
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
```

**Database Transaction Rollback:**
```python
try:
    crud.create_meeting(...)
    db.commit()
except Exception as e:
    db.rollback()
    raise ValueError(f"Database write failed: {e}")
```

---

## 🚀 Deployment Options

### Option 1: Streamlit Community Cloud (Free)

**Pros:** Free hosting, automatic SSL, GitHub integration  
**Cons:** Resource limits, public by default

**Steps:**
1. Push code to GitHub (`.env` excluded by `.gitignore`)
2. Visit https://share.streamlit.io
3. Click "New app" → Select your repo
4. Set **Main file path:** `app.py`
5. Add secrets in Settings → Secrets (TOML format)
6. Deploy

**Access Control:**
- Use Streamlit's built-in authentication
- Or add custom login via `streamlit-authenticator` package

### Option 2: Docker Container

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ai-project-manager .
docker run -p 8501:8501 --env-file .env ai-project-manager
```

### Option 3: VPS / Cloud VM

**Platforms:** AWS EC2, Google Compute, DigitalOcean, Linode

**Setup:**
```bash
# SSH into server
ssh user@your-server-ip

# Clone repo
git clone <your-repo-url>
cd project-folder

# Install dependencies
pip3 install -r requirements.txt

# Configure .env file
nano .env
# (Paste your API keys)

# Run with nohup (background process)
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

# Or use systemd service (recommended)
sudo nano /etc/systemd/system/streamlit-app.service
```

**Systemd Service File:**
```ini
[Unit]
Description=AI Project Manager Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/project-folder
ExecStart=/usr/bin/python3 -m streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app
sudo systemctl status streamlit-app
```

### Option 4: Heroku

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

Deploy:
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

---

## 🛠️ Technology Stack Deep Dive

### Frontend Layer

**Streamlit 1.35+**
- **Purpose:** Web UI framework with Python
- **Key Features:**
  - Auto-rerun on widget interaction
  - Session state for data persistence
  - Custom CSS injection via `st.markdown()`
  - File upload with `st.file_uploader()`
  - Download buttons for exports
- **Why Chosen:** Rapid prototyping, no HTML/CSS/JS needed

**Custom CSS Styling:**
- Google Fonts (Inter) for modern typography
- Dark mode color palette (slate/blue gradients)
- Hover animations (`transform: translateY()`)
- Responsive grid layouts for Kanban board
- Priority badge color coding

### Backend Layer

**Python 3.10+**
- **Features Used:**
  - Type hints for code clarity
  - F-strings for formatting
  - Context managers (`with`, `try/finally`)
  - List comprehensions for data transformation
  - Datetime with timezone awareness

**SQLAlchemy 2.0+**
- **Purpose:** ORM for database abstraction
- **Key Features:**
  - Declarative Base for model definitions
  - Relationship mapping (1-to-many)
  - Cascade delete configuration
  - Session management with context managers
  - Query builder API
- **Why Chosen:** Type-safe, prevents SQL injection, easy migrations

**Pydantic 2.0+**
- **Purpose:** Data validation and serialization
- **Key Features:**
  - BaseModel for schema definition
  - Field validators with `@field_validator`
  - Default value handling
  - Type coercion (str → int)
  - Detailed validation errors
- **Why Chosen:** Ensures LLM output matches expected structure

### AI Layer

**Google Gemini (google-genai 1.0+)**
- **Model:** `gemini-2.5-flash`
- **Performance:** ~2-3 seconds response time
- **Cost:** Free tier available (60 requests/minute)
- **API:** `client.models.generate_content()`
- **Advantages:** 
  - High accuracy for structured extraction
  - Large context window (32k tokens)
  - JSON mode support
  - Multimodal (future: image notes)

**Ollama (ollama 0.2+)**
- **Models:** Llama 3, Phi-3, Mistral, Gemma 2
- **Performance:** ~5-15 seconds (depends on hardware)
- **Cost:** Free (runs locally)
- **API:** `ollama.chat()` with messages list
- **Advantages:**
  - Complete privacy (no data sent to cloud)
  - No API costs
  - Works offline
  - Customizable models

**Prompt Engineering:**
- 1,500+ word system prompt
- Role-based instruction (expert PM)
- Rule-based extraction guidelines
- Examples for edge cases
- Quality validation checklist
- Strict JSON output requirement

### Data Processing

**Pandas 2.0+**
- **Purpose:** Tabular data manipulation
- **Usage:**
  - ORM → DataFrame conversion
  - Filtering, sorting, searching
  - CSV export generation
  - Column renaming and formatting
- **Why Chosen:** Industry standard, integrates with Streamlit

**Plotly 5.20+**
- **Purpose:** Interactive visualizations
- **Charts Used:**
  - Timeline (Gantt chart) via `px.timeline()`
  - Hover tooltips for task details
  - Dark theme integration
- **Why Chosen:** Interactive, beautiful, Streamlit-native

### File Processing

**pypdf 4.0+**
- **Purpose:** PDF text extraction
- **Method:** `PdfReader(file_stream).pages[i].extract_text()`
- **Limitation:** Text-based PDFs only (no OCR)
- **Why Chosen:** Pure Python, no system dependencies

**python-docx 1.1+**
- **Purpose:** Word document parsing
- **Method:** `Document(file_stream).paragraphs` + `tables`
- **Supports:** .docx format only (not .doc)
- **Why Chosen:** Official Microsoft format support

### Configuration Management

**python-dotenv 1.0+**
- **Purpose:** Load environment variables from `.env`
- **Method:** `load_dotenv()` at app startup
- **Security:** Excluded from Git via `.gitignore`
- **Why Chosen:** Standard for local development secrets

---

## 📊 Feature Comparison

| Feature | This App | Manual Process | Other Tools |
|---------|----------|----------------|-------------|
| **Input Sources** | 5 (Text, PDF, DOCX, Email, Slack) | N/A | Usually 1-2 |
| **LLM Options** | 2 (Cloud + Local) | N/A | Usually 1 |
| **Task Extraction** | Automated | Manual | Automated |
| **Priority Detection** | AI-inferred | Manual | Keyword-based |
| **Date Resolution** | Relative + Absolute | Manual | Absolute only |
| **Assignee Detection** | AI-extracted | Manual | Regex patterns |
| **Data Validation** | Pydantic schemas | N/A | Basic type checks |
| **Storage** | SQLite (persistent) | Notes/Spreadsheet | Varies |
| **Meeting History** | Unlimited | N/A | Often limited |
| **Task CRUD** | Full (Add/Edit/Delete) | Full | View only |
| **Visualizations** | Kanban + Gantt | Manual | Basic tables |
| **Export Options** | CSV + Markdown | Copy-paste | CSV only |
| **Cost** | Free (with API key) | Free | Varies |
| **Privacy** | Local option available | Full | Cloud-based |
| **Testing** | 71 unit tests | N/A | Usually none |
| **Setup Time** | 5 minutes | N/A | 10-30 minutes |

---

## 🎯 Use Cases & Examples

### Use Case 1: Agile Sprint Planning

**Input (Slack Thread):**
```
Alice Chen  9:00 AM
Let's plan Sprint 12. @Bob, can you handle the API gateway refactor?

Bob Kumar  9:02 AM
Yes, I can start today. Should be done by Wednesday.

Alice Chen  9:03 AM
Great. @Carol, please review the UI mockups by Friday.

Carol Lee  9:05 AM
Will do. Are we launching beta on the 15th as planned?

Alice Chen  9:06 AM
Yes, confirmed. Beta launch August 15th.
```

**Output:**
- **Title:** "Sprint 12 Planning - API Gateway & UI Review"
- **Summary:** "Team aligned on Sprint 12 priorities. Bob will refactor API gateway by Wednesday. Carol will review UI mockups by Friday. Beta launch confirmed for August 15th."
- **Decisions:**
  - Beta launch scheduled for August 15th
- **Tasks:**
  1. **Refactor API gateway** — Bob Kumar — High — 2026-07-09 (Wednesday)
  2. **Review UI mockups** — Carol Lee — Medium — 2026-07-11 (Friday)

### Use Case 2: Client Meeting (PDF)

**Input:** 5-page PDF meeting minutes with multiple action items

**Output:** 
- 12 structured tasks extracted
- 3 high-priority items flagged
- 7 team members assigned
- 8 deadlines converted to YYYY-MM-DD format

**Time Saved:** 45 minutes of manual note review

### Use Case 3: Email Thread (Long Discussion)

**Input:** 20-email thread with scattered action items

**LLM Extracts:**
- Filters out greetings, signatures, quoted replies
- Identifies 8 actual action items
- Consolidates duplicate mentions
- Infers priority from urgency keywords

**Result:** Clean 8-task list ready for sprint board

---

## 🔧 Troubleshooting

### Issue: "GEMINI_API_KEY is not set"

**Cause:** Missing or invalid API key in `.env`

**Solution:**
1. Check `.env` file exists in project root
2. Verify format: `GEMINI_API_KEY=your_key_here` (no quotes)
3. Restart Streamlit app after editing `.env`
4. Test key at https://aistudio.google.com

### Issue: "Ollama call failed. Is Ollama running?"

**Cause:** Ollama service not started or wrong URL

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If no response, start Ollama
ollama serve

# Check model is pulled
ollama list

# Pull model if missing
ollama pull phi3
```

### Issue: "LLM returned invalid JSON"

**Cause:** Model hallucinated non-JSON text

**Solution:**
1. Try different model (e.g., switch Gemini model)
2. Simplify input notes (remove special characters)
3. Check if notes are in English (multilingual support limited)
4. Re-run extraction (models are non-deterministic)

### Issue: "No tasks extracted from notes"

**Possible Causes:**
- Notes contain no actionable items
- Notes are too vague or conversational
- LLM misinterpreted content

**Solution:**
1. Review input text quality
2. Add explicit action language: "John will...", "We need to..."
3. Include deadlines: "by Friday", "next week"
4. Try more detailed notes

### Issue: Database locked error

**Cause:** Multiple Streamlit sessions accessing SQLite

**Solution:**
1. SQLite doesn't handle high concurrency well
2. Close other app instances
3. Restart Streamlit
4. For production, migrate to PostgreSQL

### Issue: PDF returns empty text

**Cause:** Scanned/image-based PDF (no text layer)

**Solution:**
- Use OCR tool first (Adobe Acrobat, Tesseract)
- Convert to text manually
- Use DOCX input instead

### Issue: Out of memory with large files

**Cause:** Very large PDF/DOCX files

**Solution:**
- Split large files into smaller chunks
- Extract text externally and paste as plain text
- Increase system memory allocation

---

## 🔄 Changelog & Version History

### Version 1.0.0 (Current)

**Features:**
- ✅ 5 input sources (Text, PDF, DOCX, Email, Slack)
- ✅ Dual LLM support (Gemini + Ollama)
- ✅ Production system prompt (1500+ words)
- ✅ Pydantic validation layer
- ✅ SQLite persistent storage
- ✅ Full CRUD interface (Add/Edit/Delete tasks)
- ✅ Clickable metric cards with filters
- ✅ Kanban board visualization
- ✅ Gantt timeline chart
- ✅ CSV + Markdown export
- ✅ Meeting history sidebar
- ✅ Custom CSS dark mode styling
- ✅ 71 passing unit tests
- ✅ Cascade delete relationships
- ✅ Timezone-aware timestamps
- ✅ Error handling with rollback

**Known Limitations:**
- No authentication/authorization
- No multi-user workspace isolation
- No real-time collaboration
- No mobile app
- No API integration (Jira, Trello, etc.)
- No email notifications
- English language only
- Text-based PDFs only (no OCR)

---

## 🚀 Roadmap & Future Enhancements

### Phase 2: Enhanced Input

- [ ] Audio/video transcript upload
- [ ] Automatic transcription (Whisper API)
- [ ] WhatsApp chat export support
- [ ] Microsoft Teams message import
- [ ] Google Meet transcript integration
- [ ] OCR for scanned PDFs (Tesseract)

### Phase 3: AI Improvements
- [ ] Multi-language support (Spanish, French, German, etc.)
- [ ] Sentiment analysis for urgency detection
- [ ] Auto-categorization (bug/feature/research)
- [ ] Task dependency detection
- [ ] Effort estimation (story points)
- [ ] Risk level assessment

### Phase 4: Collaboration
- [ ] User authentication (email/password)
- [ ] Role-based access control (PM/Developer/Viewer)
- [ ] Multi-tenant workspace isolation
- [ ] Real-time updates (WebSockets)
- [ ] Task comments and discussion threads
- [ ] @mention notifications

### Phase 5: Integrations
- [ ] Jira API sync (bidirectional)
- [ ] Trello board import/export
- [ ] Linear issues integration
- [ ] GitHub Issues sync
- [ ] Asana project import
- [ ] Slack bot for command-line task creation
- [ ] Email notifications for deadlines
- [ ] Calendar sync (Google Calendar, Outlook)

### Phase 6: Advanced Features
- [ ] Recurring tasks (daily/weekly standup notes)
- [ ] Task templates for common workflows
- [ ] Custom fields (bug severity, sprint number)
- [ ] Advanced filtering (date ranges, tag search)
- [ ] Bulk operations (assign multiple tasks)
- [ ] Task history and audit log
- [ ] Analytics dashboard (velocity, burndown)
- [ ] PDF report generation with charts
- [ ] Mobile-responsive UI
- [ ] Dark/light theme toggle

### Phase 7: Enterprise
- [ ] PostgreSQL/MySQL support
- [ ] Horizontal scaling
- [ ] Redis caching layer
- [ ] API endpoints (REST/GraphQL)
- [ ] Webhook support
- [ ] SSO integration (Okta, Auth0)
- [ ] Compliance (SOC 2, GDPR)
- [ ] On-premise deployment guides

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Setting Up Development Environment

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/ai-project-manager.git
   cd ai-project-manager
   ```
3. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Code Style Guidelines

- **Python:** Follow PEP 8 style guide
- **Docstrings:** Use Google-style docstrings
- **Type Hints:** Always use type annotations
- **Comments:** Use step-by-step explanatory comments (see existing code)
- **Naming:** Descriptive variable names (`meeting_output`, not `mo`)

### Testing Requirements

- Write unit tests for all new features
- Maintain 100% test pass rate
- Run tests before submitting PR:
  ```bash
  python -m pytest tests/ -v
  ```

### Pull Request Process

1. Update documentation in README.md
2. Add docstrings to new functions
3. Ensure all tests pass
4. Update CHANGELOG if applicable
5. Submit PR with clear description:
   - What problem does this solve?
   - What changes were made?
   - How was it tested?

### Areas Needing Contributions

- 🌐 Multi-language support (translations)
- 📱 Mobile-responsive CSS
- 🧪 Additional test coverage
- 📚 Tutorial videos/blog posts
- 🐛 Bug reports and fixes
- 💡 Feature suggestions (open an Issue first)

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 AI Project Manager

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Technologies
- **Streamlit** — Beautiful Python web apps
- **Google Gemini** — Powerful LLM for extraction
- **Ollama** — Local LLM runtime
- **SQLAlchemy** — Python ORM
- **Pydantic** — Data validation
- **Plotly** — Interactive charts

### Inspiration
- Project management pain points from Agile teams
- Manual note-taking inefficiencies
- Need for AI-powered productivity tools

### Resources
- Streamlit Documentation: https://docs.streamlit.io
- Gemini API Docs: https://ai.google.dev/docs
- Ollama Documentation: https://ollama.com/docs
- SQLAlchemy Docs: https://docs.sqlalchemy.org

---

## 📞 Support & Contact

### Get Help

- **Documentation:** This README
- **Issues:** Open a GitHub Issue for bugs
- **Discussions:** Use GitHub Discussions for questions
- **Email:** [your-email@example.com]

### Frequently Asked Questions

**Q: Is this free to use?**  
A: Yes, the application is free. You need a free Gemini API key or run Ollama locally.

**Q: Can I use this commercially?**  
A: Yes, MIT license allows commercial use.

**Q: Does it work offline?**  
A: Yes, if you use Ollama as the LLM provider.

**Q: What languages are supported?**  
A: Currently English only. Multi-language support is on the roadmap.

**Q: How secure is my data?**  
A: Data is stored locally in SQLite. For Ollama, no data leaves your machine. For Gemini, data is sent to Google's servers.

**Q: Can I integrate with Jira?**  
A: Not yet, but it's on the roadmap (Phase 5).

**Q: What's the maximum file size?**  
A: Streamlit default is 200MB. PDFs/DOCX should be under 50MB for best performance.

---

## 📊 Project Statistics

- **Total Lines of Code:** ~3,500
- **Python Files:** 20
- **Test Coverage:** 71 tests, 100% pass rate
- **Dependencies:** 10 packages
- **Documentation:** 500+ lines (this README)
- **Development Time:** [Your estimate]
- **Contributors:** [Number]

---

## 🎓 Learning Resources

If you want to understand how this project works:

1. **Start with:** `app.py` — Main UI flow
2. **Then read:** `config.py` — Configuration constants
3. **Understand:** `input_processors/` — Data cleaning
4. **Deep dive:** `llm/prompt.py` — Prompt engineering
5. **Study:** `llm/parser.py` — Pydantic validation
6. **Explore:** `database/models.py` — Database schema
7. **Learn:** `services/task_service.py` — Business logic

**Recommended Topics:**
- Streamlit session state management
- SQLAlchemy ORM relationships
- Pydantic field validators
- LLM prompt engineering
- CSS grid layouts

---

## 🎉 Thank You!

Thank you for using **AI Project Manager**! 

If this tool saves you time, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 📢 Share with your team
- 🤝 Contribute code

**Built with ❤️ using Python, AI, and a lot of coffee ☕**

---

*Last Updated: July 7, 2026*  
*Version: 1.0.0*  
*Documentation Status: Complete*
