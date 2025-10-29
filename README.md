⌨️ Instant Autocomplete Typing Tool (Flask & Datamuse)

A personalized, real-time writing assistant featuring intelligent autocompletion, context-aware suggestions, custom snippets, and user-controlled spellcheck integrated with a persistent personal dictionary.

✨ Features

This tool blends ultra-fast client-side lookups with robust server-side processing to deliver an uninterrupted typing experience.

Real-Time Autocomplete: Suggests completions based on prefixes (str -> string, structure).

Context-Aware Prediction: After typing a space, the tool suggests the next most relevant word based on the preceding context word.

User-Controlled Spellcheck: Right-click any misspelled or unrecognized word (red underline) to instantly bring up a custom menu showing spelling corrections.

Personalized Learned Dictionary:

Includes a "Add to Dictionary (Force Learn)" option on the spellcheck menu. Words are only added when explicitly instructed by the user, ensuring a clean, technical dictionary.

Learned words are prioritized and appear at the top of the suggestion list.

Custom Snippets: Expands common acronyms instantly (e.g., typing brb suggests be right back).

Customizable UI: Control the maximum number of suggestions and change the editor/suggestion font size, with preferences saved locally.

Asynchronous Performance: Uses AbortController to cancel slow network requests, ensuring only the latest, most relevant suggestions are displayed instantly.

💻 Tech Stack

Component

Technology

Role

Backend API

Python (Flask)

Handles dynamic requests, routes logic, and communicates with the external Datamuse API.

Data Source

Datamuse API

Provides network-based word suggestions, related words, and spelling corrections.

Frontend

HTML5 / JavaScript (ES6+)

Manages UI, handles all input/keyboard events, implements local cache logic, and manages the dictionary.

Styling

Tailwind CSS (CDN)

Provides a clean, modern, and fully responsive interface.

Data Persistence

localStorage

Stores the user's custom learned dictionary and UI preferences.

⚙️ Setup and Installation

Follow these steps to get the application running locally.

1. Backend Setup (app.py)

Clone the Repository:

git clone [https://github.com/YourUsername/typing-tool.git](https://github.com/YourUsername/typing-tool.git)
cd typing-tool/


Create and Activate a Virtual Environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate


Install Requirements: (Requires flask and requests)

pip install flask requests


Run the Flask Server:

python app.py


The console will show the local IP address where the server is running (e.g., http://10.2.0.2:5000). Make a note of this IP.

2. Frontend Configuration (template/index.html)

The JavaScript file uses a hardcoded IP to connect to the Flask server.

Open template/index.html.

Find the FLASK_BASE_URL constant inside the <script> tag (around line 230).

Update the value to match the IP shown in your Flask console output (e.g., http://10.2.0.2:5000).

// In template/index.html
const FLASK_BASE_URL = 'http://YOUR_FLASK_IP:5000'; 


3. Launch the Application

Open the template/index.html file directly in your web browser. The front end will now connect to your running Flask server for suggestions.

💡 Usage

Typing Suggestions: Start typing any word. Suggestions will appear below the cursor.

Accepting Suggestions: Press TAB or ENTER to accept the actively highlighted (blue) suggestion.

Next Word Prediction: Press the SPACE key after a complete word to see contextually related words.

Spellcheck & Learning:

Type a misspelled word (e.g., teh). The browser will underline it in red.

Right-click on the misspelled word.

A custom suggestions menu will appear with corrections and the "Add to Dictionary (Force Learn)" option.

Click the option to add the word to your private dictionary immediately.

Manage Dictionary: Click "Manage Learned Words" to manually inspect, add, or delete words from your personalized list.
