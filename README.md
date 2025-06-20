📚 SMART DICTIONARY–WORD WISE

A student-friendly offline dictionary desktop application built using Python and CustomTkinter, designed to provide a clean, intuitive, and interactive vocabulary learning experience — even without an internet connection.


🚀 Features

- 🔍 Word Meaning Lookup – Definitions fetched from WordNet
- 🔈 Text-to-Speech – Pronounce the word using pyttsx3
- 🔖 Bookmark System – Save important words for later
- 🌗 Dark/Light Mode Toggle – Customize your interface
- 🌟 Motivational Word of the Day – Daily flashcard-style popup with a quote
- 📚 Synonyms, Antonyms, Examples – For better context and vocabulary building

💡 Why I Built This

As a student, I wanted to create a *fully offline dictionary* that could:
- Help learners understand words with examples
- Be accessible without internet
- Be simple to use with a modern GUI
- Include motivational features to encourage learning


## 🛠 Tech Stack

| Component         | Description                              |
|------------------ |------------------------------------------|
| Python            | Core programming language                |
| CustomTkinter     | Modern, styled GUI library for Python    |
| NLTK              | Natural Language Toolkit for NLP         |
| WordNet           | Offline lexical database (via NLTK)      |
| pyttsx3           | Offline text-to-speech engine            |


![App Screenshot](![Screenshot (10)](https://github.com/user-attachments/assets/cf11104f-a825-432d-9901-a7b16d2de7df)
)

## ⚙ How to Run the Project

1. *Clone the repository* or download the .py file
   ```bash
   git clone https://github.com/yourusername/Smart-Dictionary.git 
2. *install required packages*: 
   pip install nltk customtkinter pyttsx3 
3. *Run the script*:
   python smart_dictionary.py
4. *First time only* - Download WordNet data
   import nltk 
   nltk.download('wordnet')
