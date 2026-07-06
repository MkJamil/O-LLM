import ollama
from ollama import Client

client = Client(host='http://localhost:11434')

saved_context = None

print("--- Chat Started (Type 'exit' to quit) ---")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        break

    response = client.generate(
        model='llama3',
        prompt=user_input,
        context=saved_context,
        options={
            'temperature': 0.6,
            'top_p': 1.0,
            'top_k': 100,
            'num_ctx': 4096
        }
    )

    print(f"\nAI: {response['response']}")


    saved_context = response['context']

#Tested prompt engineering with 5 different prompts with different paramateres