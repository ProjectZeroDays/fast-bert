import gradio as gr
import openai
import os

# Set up OpenAI API keys
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Code Generator using AutoGPT, OpenAI Codex, and BERT")
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="Enter your prompt")
                generate_button = gr.Button("Generate Code")
            with gr.Column():
                code_output = gr.Code(label="Generated Code")
        
        generate_button.click(fn=generate_code, inputs=prompt_input, outputs=code_output)
    
    demo.launch()

if __name__ == "__main__":
    main()
