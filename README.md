# ꡌꡙꡚ Labrynth Learning


This repository contains reference implementations of various LangChain agents as Streamlit apps including:

## Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```shell
# Install poetry
brew install pipx
pipx ensurepath
pipx install poetry
```

```shell
# Use a newer python version
poetry env use python3.10
python --version  # Should show 3.10.x or higher
```


```shell
# Install dependecies
$ poetry install

# Activate the new environment
poetry shell
```

## Running

```shell
# Run mrkl_demo.py or another app the same way
$ streamlit run streamlit_agent/mrkl_demo.py
```

## Where did this code come from?
This is a branch from: 
* ([Streamlit Langchain: Chat with Search Demo](https://langchain-chat-search.streamlit.app/))
* ([Streamlit-Agent Github](https://github.com/langchain-ai/streamlit-agent))

This repository contains reference implementations of various LangChain agents as Streamlit apps including:

- `basic_streaming.py`: Simple streaming app with `langchain.chat_models.ChatOpenAI` ([View the app](https://langchain-streaming-example.streamlit.app/))
- `basic_memory.py`: Simple app using `StreamlitChatMessageHistory` for LLM conversation memory ([View the app](https://langchain-st-memory.streamlit.app/))
- `mrkl_demo.py`: An agent that replicates the [MRKL demo](https://python.langchain.com/docs/modules/agents/how_to/mrkl) ([View the app](https://langchain-mrkl.streamlit.app))
- `minimal_agent.py`: A minimal agent with search (requires setting `OPENAI_API_KEY` env to run)
- `search_and_chat.py`: A search-enabled chatbot that remembers chat history ([View the app](https://langchain-chat-search.streamlit.app/))
- `simple_feedback.py`: A chat app that allows the user to add feedback on responses using [streamlit-feedback](https://github.com/trubrics/streamlit-feedback), and link to the traces in [LangSmith](https://docs.smith.langchain.com/) ([View the app](https://langsmith-simple-feedback.streamlit.app/))
- `chat_with_documents.py`: Chatbot capable of answering queries by referring custom documents ([View the app](https://langchain-document-chat.streamlit.app/))
- `chat_with_sql_db.py`: Chatbot which can communicate with your database ([View the app](https://langchain-chat-sql.streamlit.app/))
- `chat_pandas_df.py`: Chatbot to ask questions about a pandas DF (Note: uses `PythonAstREPLTool` which is vulnerable to arbitrary code execution,
  see [langchain #7700](https://github.com/langchain-ai/langchain/issues/7700))


## Contributing

We plan to add more agent and chain examples over time and improve the existing ones - PRs welcome! 🚀
