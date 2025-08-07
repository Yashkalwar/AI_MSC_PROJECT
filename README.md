# A-Level History Study Assistant

This is a personal AI-powered study tool designed to help A-Level History students enhance their learning experience. The system adapts to your individual learning pace and style, making it an effective study companion for exam preparation and historical understanding.

## Key Features

- **Adaptive Learning**: The system intelligently adjusts question difficulty based on your performance, providing a personalized learning experience
- **Interactive Quizzes**: Test your knowledge with dynamically generated questions
- **Comprehensive Feedback**: Receive detailed explanations and insights for each answer
- **Topic-Focused Practice**: Target specific historical periods or subjects for focused study
- **Progress Monitoring**: Track your improvement and knowledge growth over time

## Getting Started

### Prerequisites
Before getting started, ensure you have the following:
- Python 3.10 or higher installed, but you might have to check the dependencies since some are compatible with some versions of other libraries. It is recommended to check on CLI as here you will be able to see the actual ZPD update.
- A valid OpenAI API key (available at [OpenAI's website](https://platform.openai.com/))
- Basic familiarity with command line/terminal operations

### Step 1: Clone the Repository
To get started, clone this repository to your local machine:
```bash
git clone https://github.com/Yashkalwar/AI_MSC_PROJECT.git
```

### Step 2: Configure Your Environment

1. **Set up a virtual environment** to manage dependencies:
   ```bash
   # Windows:
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**:
   - Create a new `.env` file in the project directory
   - Add your OpenAI API key in the following format:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

### Step 3: Launch the Application

#### Command Line Interface (Basic Usage)
```bash
python main.py
```

#### Web Interface (Recommended)

1. **Initialize the Database** (one-time setup):
   ```bash
   python create_sample_data.py
   ```
   This creates the initial database with sample content that you can modify as needed. You can check the student ID from here which you will need to login in the web interface or the command line interface.

2. **Start the Backend Server**:
   ```bash
   uvicorn quiz_api:app --reload
   ```
   This launches the FastAPI backend with auto-reload functionality.

3. **Launch the Web Interface**:
   ```bash
   streamlit run streamlit_frontend.py
   ```
   The application will open automatically in your default web browser at `http://localhost:8501`

**Note**: For full functionality, ensure both the backend server and frontend interface are running simultaneously. The web interface requires the backend API to be active for proper operation.

---

## Table of Contents

- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Project File Structure](#project-file-structure)
- [Usage](#step-3-launch-the-application)

## Project File Structure

Below is an overview of the main files and directories in this repository:

```
AI_MSC_PROJECT/
├── .env                  # Environment variables (not tracked in git)
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation (this file)
├── requirements.txt      # Python dependencies
├── main.py               # Main entry point for CLI usage
├── streamlit_frontend.py # Streamlit web interface
├── frontend_style.css    # Custom CSS styling for Streamlit frontend
├── quiz_api.py           # FastAPI backend API
├── create_sample_data.py # Script to initialize the database with sample data
├── student_db.py         # Student database operations
├── student_manager.py    # Student management logic
├── models.py             # Data models and schemas
├── zpd_api.py            # API for Zone of Proximal Development calculations
├── ZPD_calculator.py     # Core logic for adaptive learning and ZPD
├── data/                 # Data directory (PDFs, indexes, and more)
│   ├── raw/                  # Raw source files (PDFs, JSON)
│   └── faiss_index_optimized/ # Precomputed FAISS index files
└── .git/                 # Git version control files
```

### File & Directory Descriptions

- **main.py**: Command-line interface for running quizzes and interacting with the assistant.
- **streamlit_frontend.py**: Provides a user-friendly web interface for students.
- **frontend_style.css**: Custom CSS file for modern, visually enhanced Streamlit UI/UX.
- **quiz_api.py**: Backend API using FastAPI to serve quiz data and logic.
- **create_sample_data.py**: Script to populate the database with initial/sample data.
- **student_db.py**: Handles database operations related to students.
- **student_manager.py**: Contains logic for managing student progress and profiles.
- **models.py**: Defines data structures and models used throughout the project.
- **zpd_api.py**: Implements API endpoints for ZPD (adaptive learning) calculations.
- **ZPD_calculator.py**: Core algorithms for adaptive learning and question adjustment.
- **requirements.txt**: Lists all required Python packages.
- **data/**: Contains raw data files (PDFs, JSON) and FAISS index files for search/embedding.
- **.env**: Store your OpenAI API key and other environment variables here (not tracked by git).
- **.gitignore**: Specifies files and directories ignored by git.
- **.git/**: Git version control directory (not relevant for usage).

For more details about each component, see the comments in the respective files.
