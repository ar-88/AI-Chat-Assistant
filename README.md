# AI Chat Assistant

An AI-powered chat assistant that answers user questions based on a knowledge base.  
Supports natural language queries and can be extended with additional features like weather info.

---

## Live Demo

Try the AI Chat Assistant online without any setup:  
[https://ai-chat-assistant-rathodamruta888.replit.app](https://ai-chat-assistant-rathodamruta888.replit.app)

---

## Features

- Responds to user questions using a knowledge base.
- Uses NLP techniques with `nltk` and `scikit-learn`.
- Can be connected to a MySQL database for dynamic knowledge base (optional).
- Easily extendable for additional commands and APIs.

---

## Project Structure
ai_assistant/ │ ├── assistant.py # Main program ├── db_utils.py # Database utility functions (optional) ├── requirements.txt # Python dependencies └── README.md # This file



## Getting Started (Local Setup)

### Prerequisites

- Python 3.7 or higher
- MySQL server (optional, if using database)
- An OpenWeatherMap API key (optional, for weather features)

### Installation

1. Clone the repository:


git clone https://github.com/yourusername/ai_assistant.git
cd ai_assistant

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
 Set up your MySQL database and update connection details in assistant.py or db_utils.py.

() Set your OpenWeatherMap API key as an environment variable:


export OPENWEATHER_API_KEY="f1293b006c4520783604f930e5f4138e"  # On Windows use set instead of export
Running the Assistant

python assistant.py
Type your questions and get responses. Type exit or quit to close.

Using the Online Demo
No setup required! Just visit the live demo link:
https://ai-chat-assistant-rathodamruta888.replit.app


The online demo uses an in-memory knowledge base for simplicity.
For production or advanced use, connect to a MySQL database and update the code accordingly.
Feel free to extend the knowledge base and add new features.
Contributing
Contributions are welcome! Please open issues or pull requests for improvements.

License
This project is licensed under the MIT License.

