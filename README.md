# MBAGPT: Chatting with Multiple Data Sources

MBAGPT is a chat application that leverages the power of GPT-3.5-turbo to provide conversational responses with access to multiple data sources. It allows users to ask questions and receive answers from different knowledge bases (vectorDBs), such as Alex Hormozi, Warren Buffett and Richard Branson as well as answer general queries with the ChatGPT API as a fallback.

## Features

- Chat interface for interacting with the chatbot powered by GPT-3.5-turbo.
- Integration with Hormozi, Buffett and Branson databases for retrieving relevant documents.
- Semantic search functionality to provide informative snippets from the databases.
- Intent classification to route user queries to the appropriate database.
- HTML templates for displaying chat history and messages.
- Persistence of embeddings using the Chroma vector store.
- OpenAI API key integration for authentication.

## Installation

1. Clone the repository:

```
git clone https://github.com/wombyz/MBAGPT.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Set up your credentials:

- Sign up on the OpenAI website and obtain an API key.
- Create a new file called "secrets.toml" in the .streamlit folder.
- Set your OpenAI API key (required) and pinecone creds (optional) in the secrets.toml file or as an environment variable.
- Update the code in the app to use the correct method for accessing the API key.

4. Run the indexing script to create the vector databases:

```
python indexing.py
```

This script will create the Buffet and Branson vector databases by indexing the documents. Make sure to have the necessary PDF documents in the appropriate directories (`./docs/buffett/` and `./docs/branson/`) before running the script.

5. Run the application:

```
streamlit run app.py
```

## Usage

1. Access the application by navigating to `http://localhost:8501` in your web browser.

2. Enter your prompt in the input box and press Enter.

3. The chatbot will process your prompt and provide a response based on the available data sources.

4. The chat history will be displayed on the screen, showing both user and assistant messages.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Implement your changes and ensure that the code passes all tests.

4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License.
