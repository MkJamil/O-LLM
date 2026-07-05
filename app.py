import ollama

user_prompt = "What is the capital?"
system_instruction = "You are a American citizen"

response = ollama.chat(
    model='llama3',
    messages=[
        {
            'role': 'system', 
            'content': system_instruction  # Your Instructions go here
        },
        {
            'role': 'user', 
            'content': user_prompt
        }
    ],
    options={
        'temperature': 0.7,
        'num_predict': 150,
    }
)

print(response['message']['content'])