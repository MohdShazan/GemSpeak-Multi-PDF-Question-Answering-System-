import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Utility functions
def inject_custom_css(css_path):
    """Inject custom CSS into Streamlit."""
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    """Split extracted text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)


def get_vector_store(text_chunks):
    """Generate and save vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    """Create a question-answering chain."""
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the context, respond with: "Answer is not available in the context."
    
    Context:
    {context}

    Question: {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)


def user_input(user_question):
    """Handle user input for Q&A."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("**Reply:**", response["output_text"])


# Main app
def main():
    st.set_page_config(page_title="GemSpeak - Chat PDF", page_icon="📜", layout="wide")

    # Inject custom CSS
    inject_custom_css("style.css")

    # App header
    st.markdown("<h1 style='text-align: center;'>GemSpeak 📜💡</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your go-to tool for analyzing multiple PDFs effortlessly!</p>", unsafe_allow_html=True)

    # User question input
    user_question = st.text_input("**Ask a Question from the PDF Files**", placeholder="Type your question here...")

    if user_question:
        user_input(user_question)

    # Sidebar
    with st.sidebar:
        st.title("📂 Dashboard")
        pdf_docs = st.file_uploader("Drop your PDF files here for analysis", accept_multiple_files=True)

        # Analyze Files Button
        if st.button("Analyze Files"):
            with st.spinner("Analyzing your files..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Analysis complete! Ready for questions.")


if __name__ == "__main__":
    main()

