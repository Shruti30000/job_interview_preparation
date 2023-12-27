import openai
import dotenv

openai.api_key = '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'

dotenv.load_dotenv()

from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryMemory

# Initialize the database
db = SQLDatabase.from_uri("sqlite:///job.db")

# Initialize the OpenAI language model
llm = OpenAI(temperature=0, verbose=True)

# Create a database chain with the language model
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def generate_custom_question(user_info):
    # Example rule-based logic to generate a custom question
    if user_info.get('target_job'):
        return f"What skills or experiences do you have that align with your target job as a {user_info['target_job']}?"
    else:
        return "What are your key strengths and experiences relevant to the position you are applying for?"

def fetch_user_info_from_database(user_id):
    # Example function to fetch user information from the database
    # Modify this function based on your database schema
    user_info = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return user_info

messages = [
    {"role": "system", "content": "You are a job interviewer."},
]

# Assume user_id is the ID of the user in the database
user_id = 1

# Fetch user information from the database
user_info = fetch_user_info_from_database(user_id)

# Add user information to the conversation
messages_with_user_info = messages.copy()
messages_with_user_info.append({"role": "user_info", "content": user_info})

# Use the conversation with user information for generating questions
chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=messages_with_user_info
)

reply = chat.choices[0].message.content
print(f"ChatGPT: {reply}")
messages.append({"role": "assistant", "content": reply})

# Generate and ask a custom question based on user information
custom_question = generate_custom_question(user_info)
print(f"Custom Question: {custom_question}")
messages.append({"role": "assistant", "content": custom_question})
