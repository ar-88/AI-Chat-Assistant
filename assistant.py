import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import db_utils
import datetime
import subprocess
import sys
import os
import platform
import requests

import warnings
warnings.filterwarnings("ignore", category=User Warning, module='sklearn')

# Download NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')

# Replace with your actual OpenWeatherMap API key or leave None to disable weather
OPENWEATHER_API_KEY = None

class AIChatAssistant:
    def __init__(self, knowledge_base):
        self.questions = [item['question'] for item in knowledge_base]
        self.answers = [item['answer'] for item in knowledge_base]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        filtered_tokens = [w for w in tokens if w.isalpha() and w not in self.stop_words]
        return " ".join(filtered_tokens)

    def get_response(self, user_input):
        # First check for system commands
        cmd_response = self.handle_system_commands(user_input)
        if cmd_response is not None:
            return cmd_response

        # Otherwise fallback to knowledge base
        user_input_processed = self.preprocess(user_input)
        user_vec = self.vectorizer.transform([user_input_processed])
        similarities = cosine_similarity(user_vec, self.question_vectors).flatten()
        max_sim_index = np.argmax(similarities)
        max_sim_score = similarities[max_sim_index]

        if max_sim_score < 0.2:
            return "Sorry, I don't understand your question. Can you please rephrase?"
        else:
            return self.answers[max_sim_index]

    def handle_system_commands(self, text):
        text_lower = text.lower()

        # Exit commands
        if any(phrase in text_lower for phrase in ['exit', 'quit', 'close app', 'close application', 'stop']):
            print("Assistant: Closing the application. Goodbye!")
            sys.exit(0)

        # Date and time
        if 'date' in text_lower or 'time' in text_lower:
            now = datetime.datetime.now()
            return f"The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}."

        # Lock screen
        if 'lock screen' in text_lower or 'lock the screen' in text_lower:
            return self.lock_screen()

        # Open app (Windows example)
        if text_lower.startswith('open '):
            app_name = text_lower.replace('open ', '').strip()
            return self.open_application(app_name)

        # Close app (Windows example)
        if text_lower.startswith('close '):
            app_name = text_lower.replace('close ', '').strip()
            return self.close_application(app_name)

        # Weather info
        if 'weather' in text_lower:
            return self.get_weather()

        return None

    def lock_screen(self):
        os_name = platform.system()
        try:
            if os_name == 'Windows':
                subprocess.run('rundll32.exe user32.dll,LockWorkStation')
            elif os_name == 'Darwin':  # macOS
                subprocess.run(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'])
            elif os_name == 'Linux':
                subprocess.run(['gnome-screensaver-command', '-l'])
            else:
                return "Sorry, locking screen is not supported on your OS."
            return "Screen locked."
        except Exception as e:
            return f"Failed to lock screen: {e}"

    def open_application(self, app_name):
        os_name = platform.system()
        try:
            if os_name == 'Windows':
                # Map common app names to executable paths or commands
                apps = {
                    'notepad': 'notepad.exe',
                    'calculator': 'calc.exe',
                    'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
                }
                exe = apps.get(app_name)
                if exe:
                    subprocess.Popen(exe)
                    return f"Opening {app_name}."
                else:
                    return f"Sorry, I don't know how to open {app_name}."
            elif os_name == 'Darwin':
                subprocess.Popen(['open', '-a', app_name])
                return f"Opening {app_name}."
            elif os_name == 'Linux':
                subprocess.Popen([app_name])
                return f"Opening {app_name}."
            else:
                return "Unsupported OS for opening applications."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"

    def close_application(self, app_name):
        os_name = platform.system()
        try:
            if os_name == 'Windows':
                # Use taskkill to close by process name
                subprocess.run(['taskkill', '/IM', f'{app_name}.exe', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"Closed {app_name} if it was running."
            elif os_name == 'Darwin' or os_name == 'Linux':
                subprocess.run(['pkill', app_name])
                return f"Closed {app_name} if it was running."
            else:
                return "Unsupported OS for closing applications."
        except Exception as e:
            return f"Failed to close {app_name}: {e}"

    def get_weather(self):
        if OPENWEATHER_API_KEY is None:
            return "Weather feature is not configured. Please set your API key."

        # For demo, use a fixed location (e.g., London)
        city = "London"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('cod') != 200:
                return f"Failed to get weather data: {data.get('message', '')}"
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"The current weather in {city} is {weather_desc} with a temperature of {temp}°C."
        except Exception as e:
            return f"Failed to get weather data: {e}"

def main():
    connection = db_utils.create_connection('localhost', 'root', 'your_password', 'your_database_name')
    if not connection:
        print("Failed to connect to database. Exiting.")
        return

    knowledge_base = db_utils.fetch_knowledge_base(connection)
    assistant = AIChatAssistant(knowledge_base)

    print("Welcome to AI Chat Assistant! Type 'exit' or 'quit' to close.")
    while True:
        user_input = input("You: ")
        response = assistant.get_response(user_input)
        print(f"Assistant: {response}")

    connection.close()

if __name__ == "__main__":
    main()
