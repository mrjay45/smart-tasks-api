<div align="center">

# 🎯 Smart Task Management API

### _Intelligent Task Organization with Classification_

[![FastAPI](https://img.shields.io/badge/FastAPI-0.125.0-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge)](https://pydantic.dev/)

---

**A powerful API that automatically categorizes, prioritizes, and extracts insights from your tasks using word based classification .**

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-endpoints) • [Architecture](#-architecture) • [Testing](#-testing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Smart Classification](#-smart-classification)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

The **Smart Task Management API** is an task management system that goes beyond basic CRUD operations. It used keyword-based classification to automatically:

- 🏷️ **Categorize** tasks into domains (Scheduling, Finance, Technical, Safety)
- ⚡ **Prioritize** tasks based on urgency indicators
- 🔍 **Extract** key entities (dates, times, people, locations, actions)
- 💡 **Suggest** contextual actions based on task category
- 📊 **Track** complete task history with audit logs


---

## ✨ Features

### 🤖 Classification

| Feature                 | Description                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------- |
| **Auto-Categorization** | Classifies tasks into `scheduling`, `finance`, `technical`, `safety`, or `general` |
| **Priority Detection**  | Assigns `high`, `medium`, or `low` priority based on urgency keywords              |
| **Entity Extraction**   | Extracts dates, times, people, locations, and action verbs                         |
| **Action Suggestions**  | Provides relevant next steps based on task category                                |

### 🔧 Core Functionality

- ✅ **CRUD Operations** - Create, Read, Update, Delete tasks
- 📜 **History Tracking** - Complete audit trail of all task changes
- 🔎 **Advanced Filtering** - Filter by status, category, priority
- 📄 **Pagination Support** - Efficient handling of large datasets
- 🛡️ **Error Handling** - Comprehensive exception management
- ✔️ **Data Validation** - Pydantic schemas for request validation

---

## 🛠️ Technology Stack


**Core Technologies:**

- **FastAPI** - Modern, fast web framework
- **Supabase** - Open-source Firebase alternative (PostgreSQL)
- **Pydantic** - Data validation using Python type hints
- **Python-dotenv** - Environment variable management
- **Pytest** - Testing framework

---

## 📁 Project Structure

```
assignment/
│
├── 📄 main.py                      # FastAPI application & endpoints
├── 🧠 classification_service.py   # ML/NLP classification logic
├── 📋 schemas.py                   # Pydantic models for validation
├── 🗄️ supabase_client.py          # Database connection setup
├── 🧪 test_main.py                 # Unit and integration tests
├── ⚙️ pytest.ini                   # Pytest configuration
├── 📦 requirements.txt             # Python dependencies (if exists)
├── 🔐 .env                         # Environment variables (not tracked)
└── 📁 env/                         # Virtual environment
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Supabase account ([Sign up here](https://supabase.com))
- Git (optional)

### Step-by-Step Setup

1️⃣ **Clone the repository**

```bash
git clone <repository-url>
cd assignment
```

2️⃣ **Create a virtual environment**

```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

3️⃣ **Install dependencies**

```bash
pip install fastapi uvicorn supabase python-dotenv pydantic pytest pytest-mock httpx
```

4️⃣ **Set up environment variables**

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

5️⃣ **Set up Supabase tables**

Execute the following SQL in your Supabase SQL Editor:

```sql
-- Tasks Table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    priority TEXT,
    status TEXT DEFAULT 'pending',
    assigned_to TEXT,
    due_date TIMESTAMPTZ,
    extracted_entities JSONB,
    suggested_actions JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Task History Table
CREATE TABLE task_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    old_value JSONB,
    new_value JSONB,
    changed_by TEXT,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);


```

6️⃣ **Run the application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` 🎉

---

## ⚙️ Configuration

### Environment Variables

| Variable       | Description                 | Example                     |
| -------------- | --------------------------- | --------------------------- |
| `SUPABASE_URL` | Your Supabase project URL   | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | Your Supabase anonymous key | `eyJhbGciOiJIUzI1NiIs...`   |

### Category Keywords

Customize classification in `classification_service.py`:

```python
CATEGORY_KEYWORDS = {
    "scheduling": ['meeting', 'schedule', 'call', 'appointment', 'deadline'],
    "finance": ['payment', 'invoice', 'bill', 'budget', 'cost', 'expense'],
    "technical": ['bug', 'fix', 'error', 'install', 'repair', 'maintain'],
    "safety": ['safety', 'hazard', 'inspection', 'compliance', 'PPE']
}
```

---

## 📡 API Endpoints

### Base URL

```
http://localhost:8000
```

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

### Endpoints Overview

| Method   | Endpoint          | Description                  |
| -------- | ----------------- | ---------------------------- |
| `GET`    | `/`               | Health check                 |
| `POST`   | `/api/tasks`      | Create a new task            |
| `GET`    | `/api/tasks`      | Get all tasks (with filters) |
| `GET`    | `/api/tasks/{id}` | Get task by ID with history  |
| `PATCH`  | `/api/task/{id}`  | Update a task                |
| `DELETE` | `/api/task/{id}`  | Delete a task                |

---

### 1️⃣ Create Task

**Endpoint:** `POST /api/tasks`

**Request Body:**

```json
{
  "title": "Fix urgent payment bug in production",
  "description": "Critical bug affecting payment processing. Need to fix ASAP by tomorrow at 5pm with John",
  "status": "pending",
  "assigned_to": "Engineering Team",
  "due_date": "2025-12-25T17:00:00Z"
}
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Fix urgent payment bug in production",
  "description": "Critical bug affecting payment processing...",
  "category": "technical",
  "priority": "high",
  "status": "pending",
  "assigned_to": "Engineering Team",
  "due_date": "2025-12-25T17:00:00Z",
  "extracted_entities": {
    "date": "tomorrow",
    "time": "5pm",
    "person": "John",
    "action": "fix"
  },
  "suggested_actions": [
    "Diagnose issue",
    "Check resources",
    "Assign technician",
    "Document fix"
  ],
  "created_at": "2025-12-24T10:30:00Z",
  "updated_at": "2025-12-24T10:30:00Z"
}
```

---

### 2️⃣ Get All Tasks

**Endpoint:** `GET /api/tasks`

**Query Parameters:**

- `status` (optional): Filter by status
- `category` (optional): Filter by category
- `priority` (optional): Filter by priority
- `limit` (optional, default: 10): Number of results
- `offset` (optional, default: 0): Pagination offset

**Example Request:**

```
GET /api/tasks?status=pending&priority=high&limit=5
```

**Response:**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Fix urgent payment bug in production",
    "category": "technical",
    "priority": "high",
    "status": "pending",
    ...
  }
]
```

---

### 3️⃣ Get Task by ID

**Endpoint:** `GET /api/tasks/{id}`

**Response:**

```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Fix urgent payment bug in production",
    ...
  },
  "history": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "task_id": "550e8400-e29b-41d4-a716-446655440000",
      "action": "created",
      "old_value": null,
      "new_value": { "task_id": "550e8400...", "status": "pending" },
      "changed_by": "system",
      "changed_at": "2025-12-24T10:30:00Z"
    }
  ]
}
```

---

### 4️⃣ Update Task

**Endpoint:** `PATCH /api/task/{id}`

**Request Body:**

```json
{
  "status": "completed",
  "assigned_to": "John Doe"
}
```

**Response:**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "assigned_to": "John Doe"
}
```

---

### 5️⃣ Delete Task

**Endpoint:** `DELETE /api/task/{id}`

**Response:**

```json
{
  "detail": "Task Deleted successfully"
}
```

---

## 🧠 Smart Classification

### Category Classification

The system automatically categorizes tasks based on keyword matching:

```python
Category Detection Rules:
┌──────────────┬────────────────────────────────────────┐
│ Category     │ Keywords                               │
├──────────────┼────────────────────────────────────────┤
│ Scheduling   │ meeting, schedule, call, appointment   │
│ Finance      │ payment, invoice, bill, budget, cost   │
│ Technical    │ bug, fix, error, install, repair       │
│ Safety       │ safety, hazard, inspection, compliance │
│ General      │ (default for unmatched tasks)          │
└──────────────┴────────────────────────────────────────┘
```

### Priority Detection

Urgency-based priority assignment:

```python
Priority Rules:
┌──────────┬────────────────────────────────────────┐
│ Priority │ Keywords                               │
├──────────┼────────────────────────────────────────┤
│ High     │ urgent, asap, immediately, critical    │
│ Medium   │ soon, this week, important             │
│ Low      │ (default)                              │
└──────────┴────────────────────────────────────────┘
```

### Entity Extraction

Extracts structured data using regex patterns:

| Entity Type  | Pattern                                   | Example                  |
| ------------ | ----------------------------------------- | ------------------------ |
| **Date**     | `today`, `tomorrow`, `week`, `DD-MM-YYYY` | "tomorrow" → next day    |
| **Time**     | `HH:MM am/pm`, `H pm/am`                  | "5pm" → "5pm"            |
| **Person**   | `with/by/assign to [Name]`                | "with John" → "John"     |
| **Location** | `at/in [Place]`                           | "at office" → "office"   |
| **Action**   | Action verbs                              | "fix", "schedule", "pay" |

### Suggested Actions

Context-aware action recommendations:

```python
Suggested Actions by Category:
┌──────────────┬──────────────────────────────────────┐
│ Category     │ Suggested Actions                    │
├──────────────┼──────────────────────────────────────┤
│ Scheduling   │ Block calendar, Send invite, ...     │
│ Finance      │ Check budget, Get approval, ...      │
│ Technical    │ Diagnose issue, Assign technician    │
│ Safety       │ Conduct inspection, File report      │
└──────────────┴──────────────────────────────────────┘
```
---

## 🧪 Testing

The project includes comprehensive unit and integration tests using Pytest.

### Run All Tests

```bash
# Activate virtual environment first
pytest
```

### Run Specific Tests

```bash
# Test task creation
pytest test_main.py::test_create_task -v

# Test classification
pytest test_main.py -k "classification" -v
```

### Test Structure

```python
Tests cover:
✅ Task creation with auto-classification
✅ Task retrieval (all & by ID)
✅ Task updates with history logging
✅ Task deletion
✅ Filtering and pagination
✅ Error handling
✅ Edge cases
```

---

## 🏗️ Architecture

### System Flow

```
┌─────────────┐
│   Client    │
│  (HTTP)     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│        FastAPI Application          │
│  ┌───────────────────────────────┐  │
│  │   Route Handlers (main.py)    │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │  Classification Services      │  │
│  │  • category_classification()  │  │
│  │  • priority_detection()       │  │
│  │  • entity_extraction()        │  │
│  │  • suggested_action()         │  │
│  └───────────┬───────────────────┘  │
└──────────────┼─────────────────────┘
               │
               ▼
    ┌────────────────────┐
    │  Pydantic Schemas  │
    │   (Validation)     │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │ Supabase Client    │
    │  (PostgreSQL)      │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │   Database         │
    │  • tasks           │
    │  • task_history    │
    └────────────────────┘
```

### Key Design Patterns

- **Separation of Concerns**: Business logic separated from API routes
- **Dependency Injection**: Database client injected via module
- **Schema Validation**: Pydantic models ensure data integrity
- **History Tracking**: Audit log for all task changes
- **Error Handling**: Global exception handler with specific HTTP exceptions

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📝 License

This project is created as part of an internship assignment. All rights reserved.

---

## 🙏 Acknowledgments

- **FastAPI** - For the amazing web framework
- **Supabase** - For the excellent database platform
- **Pydantic** - For robust data validation
- **Python Community** - For the incredible ecosystem

---

<div align="center">

### 🌟 If you found this useful, give it a star! 🌟

**Made with ❤️ using FastAPI and Supabase**

---

**Questions or Issues?** Open an issue on GitHub or contact the maintainer.

</div>
