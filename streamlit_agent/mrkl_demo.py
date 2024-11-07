from pathlib import Path

import streamlit as st

from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.chains import LLMMathChain
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, SQLDatabase
from langchain_core.runnables import RunnableConfig
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI
from sqlalchemy import create_engine
import sqlite3

# openai_api_key = st.secrets.openai_api_key
WEAVIATE_API_KEY = st.secrets.WEAVIATE_API_KEY
UNSTRUCTURED_API_KEY = st.secrets.UNSTRUCTURED_API_KEY
UNSTRUCTURED_API_URL = st.secrets.UNSTRUCTURED_API_KEY
WEAVIATE_URL = st.secrets.WEAVIATE_URL

from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container

DB_PATH = (Path(__file__).parent / "Chinook.db").absolute()

SAVED_SESSIONS = {
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?": "leo.pickle",
    "What is the full name of the female artist who recently released an album called "
    "'The Storm Before the Calm' and are they in the FooBar database? If so, what albums of theirs "
    "are in the FooBar database?": "alanis.pickle",
}

st.set_page_config(
    page_title="Mind Matrix", page_icon="📓", layout="wide", initial_sidebar_state="collapsed"
)


"# ꡌꡙꡚ Labrynth Learning"

st.subheader("Empower Your Knowledge and Skill Acquisition Journey")


# Setup credentials in Streamlit
user_openai_api_key = st.sidebar.text_input(
    "OpenAI API Key", type="password", help="Set this to run your own custom questions."
)

if user_openai_api_key:
    openai_api_key = user_openai_api_key
    enable_custom = True
else:
    openai_api_key = "not_supplied"
    enable_custom = False

# Tools setup
llm = OpenAI(temperature=0, openai_api_key=openai_api_key, streaming=True)
search = DuckDuckGoSearchAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm)

# Make the DB connection read-only to reduce risk of injection attacks
# See: https://python.langchain.com/docs/security
creator = lambda: sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
db = SQLDatabase(create_engine("sqlite:///", creator=creator))

db_chain = SQLDatabaseChain.from_llm(llm, db)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="FooBar DB",
        func=db_chain.run,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
]

# Initialize agent
react_agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
mrkl = AgentExecutor(agent=react_agent, tools=tools)



# with st.form(key="form"):
#     if not enable_custom:
#         "Ask one of the sample questions, or enter your API Key in the sidebar to ask your own custom questions."
#     prefilled = st.selectbox("Sample questions", sorted(SAVED_SESSIONS.keys())) or ""
#     user_input = ""
#
#     if enable_custom:
#         user_input = st.text_input("Or, ask your own question")
#     if not user_input:
#         user_input = prefilled
#     submit_clicked = st.form_submit_button("Submit Question")
#
# output_container = st.empty()
# if with_clear_container(submit_clicked):
#     output_container = output_container.container()
#     output_container.chat_message("user").write(user_input)
#
#     answer_container = output_container.chat_message("assistant", avatar="🦜")
#     st_callback = StreamlitCallbackHandler(answer_container)
#     cfg = RunnableConfig()
#     cfg["callbacks"] = [st_callback]
#
#     # If we've saved this question, play it back instead of actually running LangChain
#     # (so that we don't exhaust our API calls unnecessarily)
#     if user_input in SAVED_SESSIONS:
#         session_name = SAVED_SESSIONS[user_input]
#         session_path = Path(__file__).parent / "runs" / session_name
#         print(f"Playing saved session: {session_path}")
#         answer = playback_callbacks([st_callback], str(session_path), max_pause_time=2)
#     else:
#         answer = mrkl.invoke({"input": user_input}, cfg)
#
#     answer_container.write(answer["output"])

st.divider()  # Adds a horizontal rule
st.header("✎ Your Use Case")
st.write("Generate lessons to build a plan to learn the concepts you need to make your idea into a reality")

# Text input with session state
user_input = st.text_input(
    label="Enter your use case here",
    key="use_case"  # This automatically stores the value in session state
)

# Access the input value anywhere using:
st.write("You entered:", st.session_state.use_case)

st.divider()  # Adds a horizontal rule
st.header("💬 Verbal Review")
st.write("Time for a verbal review of your lessons. We have three options for you to choose from.")

# Create three columns
col1, col2, col3, col4 = st.columns(4)

# Add a button to each column
with col1:
    if st.button("Practice Basic Concepts"):
        st.write("Let's practice basic concepts!")

with col2:
    if st.button("Practice Study Cards"):
        st.write("Lets practice study cards!")

with col3:
    if st.button("Interview Me"):
        st.write("Time to practice interview questions!")

# # Button in a specific color
# if st.button("Delete", type="primary"):  # primary gives it emphasis
#     st.write("Delete button clicked!")
st.divider()  # Adds a horizontal rule
st.header("👩‍🎓Study Cards")
st.write("Spaced Repetition Cards, based on your lessons")
if st.button("Review Study Cards"):
    st.write("Time to review!")

st.divider()  # Adds a horizontal rule
st.header("🗄️Add to your Knowledge Base")
st.write("Upload text, documentation or pdf to your knowledge base")
# Specify allowed file types
uploaded_file = st.file_uploader(
    "Upload a file",
    type=['csv', 'txt', 'pdf'],  # List of allowed file types
    accept_multiple_files=False,  # Allow multiple files
    help="Upload your file here"  # Tooltip text
)

import weaviate


# documents = client.collections.get(os.getenv("WEAVIATE_COLLECTION_CLASS_NAME"))
#
# response = documents.query.hybrid(
#     query="How would you Design a URL Shortener?",
#     alpha=0.5, # equal weighting of BM25 and vector search
#     return_properties=['text'],
#     auto_limit=2  # autocut after 2 jumps
# )
#
# for obj in response.objects:
#     print(json.dumps(obj.properties, indent=2))