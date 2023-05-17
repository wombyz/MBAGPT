import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
from utils import intent_classifier, semantic_search, ensure_fit_tokens, get_page_contents
from prompts import human_template, system_message
from render import user_msg_container_html_template, bot_msg_container_html_template
import openai

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.header("MBAGPT: Chatting with Multiple Data Sources")

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Load the Buffett and Branson databases
buffettDB = Chroma(persist_directory=os.path.join('db', 'buffett'), embedding_function=embeddings)
buffett_retriever = buffettDB.as_retriever(search_kwargs={"k": 3})

bransonDB = Chroma(persist_directory=os.path.join('db', 'branson'), embedding_function=embeddings)
branson_retriever = bransonDB.as_retriever(search_kwargs={"k": 3})


# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Construct messages from chat history
def construct_messages(history):
    messages = [{"role": "system", "content": system_message}]
    
    for entry in history:
        role = "user" if entry["is_user"] else "assistant"
        messages.append({"role": role, "content": entry["message"]})
    
    # Ensure total tokens do not exceed model's limit
    messages = ensure_fit_tokens(messages)
    
    return messages


# Define handler functions for each category
def hormozi_handler(query):
    print("Using Hormozi handler...")
    # Perform semantic search and format results
    search_results = semantic_search(query, top_k=3)
    context = ""
    for i, (title, snippet) in enumerate(search_results):
        context += f"Snippet from: {title}\n {snippet}\n\n"

    # Generate human prompt template and convert to API message format
    query_with_context = human_template.format(query=query, context=context)

    # Return formatted message
    return {"role": "user", "content": query_with_context}


def buffett_handler(query):
    print("Using Buffett handler...")
    # Get relevant documents from Buffett's database
    relevant_docs = buffett_retriever.get_relevant_documents(query)

    # Use the provided function to prepare the context
    context = get_page_contents(relevant_docs)

    # Prepare the prompt for GPT-3.5-turbo with the context
    query_with_context = human_template.format(query=query, context=context)

    return {"role": "user", "content": query_with_context}


def branson_handler(query):
    print("Using Branson handler...")
    # Get relevant documents from Branson's database
    relevant_docs = branson_retriever.get_relevant_documents(query)

    # Use the provided function to prepare the context
    context = get_page_contents(relevant_docs)

    # Prepare the prompt for GPT-3.5-turbo with the context
    query_with_context = human_template.format(query=query, context=context)

    return {"role": "user", "content": query_with_context}


def other_handler(query):
    print("Using other handler...")
    # Return the query in the appropriate message format
    return {"role": "user", "content": query}


# Function to route query to correct handler based on category
def route_by_category(query, category):
    if category == "0":
        return hormozi_handler(query)
    elif category == "1":
        return buffet_handler(query)
    elif category == "2":
        return branson_handler(query)
    elif category == "3":
        return other_handler(query)
    else:
        raise ValueError("Invalid category")

# Function to generate response
def generate_response():
    # Append user's query to history
    st.session_state.history.append({
        "message": st.session_state.prompt,
        "is_user": True
    })
    
    # Classify the intent
    category = intent_classifier(st.session_state.prompt)
    
    # Route the query based on category
    new_message = route_by_category(st.session_state.prompt, category)
    
    # Construct messages from chat history
    messages = construct_messages(st.session_state.history)
    
    # Add the new_message to the list of messages before sending it to the API
    messages.append(new_message)
    
    # Ensure total tokens do not exceed model's limit
    messages = ensure_fit_tokens(messages)
    
    # Call the Chat Completions API with the messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the assistant's message from the response
    assistant_message = response['choices'][0]['message']['content']
    
    # Append assistant's message to history
    st.session_state.history.append({
        "message": assistant_message,
        "is_user": False
    })


# Take user input
st.text_input("Enter your prompt:",
              key="prompt",
              placeholder="e.g. 'How can I diversify my portfolio?'",
              on_change=generate_response
              )

# Display chat history
for message in st.session_state.history:
    if message["is_user"]:
        st.write(user_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
    else:
        st.write(bot_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
