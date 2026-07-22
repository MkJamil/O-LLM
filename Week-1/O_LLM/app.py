import os
from ollama import Client
from fpdf import FPDF
import re

client = Client(host='http://127.0.0.1:11434')

saved_context = None

print("--- Chatbot Started (Type 'exit' to quit) ---")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        break

    match = re.search(r"save it as a (pdf|txt|text)", user_input.lower())
    
    # Set the flags based on what was matched inside the parentheses
    is_pdf = match is not None and match.group(1) == "pdf"
    is_txt = match is not None and match.group(1) in ["txt", "text"]

    # Clean the prompt for the LLM if it's a file request, instructing it to ONLY return the summary text
    llm_prompt = user_input
    if is_pdf or is_txt:
        llm_prompt = f"{user_input} \n\nCRITICAL INSTRUCTION: Provide ONLY the summary text. Do not include any meta-text, introductions, markdown formatting for file creation, or file explanations."

    # Call the model (Updated to llama3.2)
    response = client.generate(
        model='llama3.2',
        prompt=llm_prompt,
        context=saved_context,
        options={
            'temperature': 0.6,
            'top_p': 1.0,
            'top_k': 100,
            'num_ctx': 1024,
            'num_thread': 8,
            'low_vram': True,
        }
    )

    summary_output = response['response']
    print(f"\nAI: {summary_output}")

    saved_context = response['context']

    # --- File Generation ---
    if is_pdf or is_txt:
        os.makedirs("outputs", exist_ok=True)

    if is_pdf:
        print("\n[System: Generating A4 PDF Summary sustainably using Python...]")
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        # multi_cell automatically wraps text beautifully
        pdf.multi_cell(0, 10, txt=summary_output.encode('latin-1', 'replace').decode('latin-1'))
        

        pdf.output("outputs/summary.pdf") 
        print("[System: 'outputs/summary.pdf' has been successfully saved!]")

    elif is_txt:
        print("\n[System: Generating TXT Summary sustainably using Python...]")

        with open("outputs/summarize.txt", "w", encoding="utf-8") as f:
            f.write(summary_output)
        print("[System: 'outputs/summarize.txt' has been successfully saved!]")


#Tested prompt engineering with 5 different prompts with different paramateres