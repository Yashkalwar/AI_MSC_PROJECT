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
- Python 3.8 or higher installed
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
   This creates the initial database with sample content that you can modify as needed.

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
