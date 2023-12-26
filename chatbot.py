import openai

openai.api_key = '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'

def generate_custom_question(user_info):
    # Example rule-based logic to generate a custom question
    if user_info.get('target_job'):
        return f"What skills or experiences do you have that align with your target job as a {user_info['target_job']}?"
    else:
        return "What are your key strengths and experiences relevant to the position you are applying for?"

messages = [
    {"role": "system", "content": "You are a job interviewer."},
]

# Assume user_info is a dictionary containing user information
user_info = {
    'name': 'John Doe',
    'target_job': 'Software Engineer',
    # Add more user information fields as needed
}

while True:
    message = input("User : ")
    
    if message:
        messages.append({"role": "user", "content": message})
        
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
