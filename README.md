## Live Demo
Check out the live demo of the app here: [GemSpeak - Live Demo](https://ask-gemspeak.streamlit.app/)


![Chat PDF - Google Chrome 25-12-2024 00_00_38](https://github.com/user-attachments/assets/b60cd8f6-532d-4efe-a566-c241dde79e40)

GemSpeak – Multi-PDF Question Answering System
GemSpeak is a web application built using Streamlit that allows users to ask questions based on the content of multiple uploaded PDF documents. It leverages Google Generative AI and Langchain to provide detailed answers by extracting and processing the text from PDFs.

Features
Upload and analyze multiple PDF files.
Automatically extracts and processes text from PDFs.
Splits text into chunks for better search and question-answering.
Uses Google Generative AI for question answering based on the document's content.
User-friendly interface built with Streamlit.
Prerequisites
To run this project locally, you need to have the following installed:

Python 3.x
Streamlit
PyPDF2
Langchain
Google Generative AI API (API key)
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/username/repository-name.git
Navigate to the project directory:

bash
Copy code
cd repository-name
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Make sure you have a .env file with your Google API key for Google Generative AI.

Running the Application
To start the app, run the following command:

bash
Copy code

streamlit run app.py

The app will launch in your browser, and you can start uploading your PDF files and asking questions.

Contributing
Feel free to fork this repository, submit issues, or create pull requests to contribute to the project.

License
This project is licensed under the MIT License – see the LICENSE file for details.
