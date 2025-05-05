import asyncio
import os
from dataclasses import dataclass
from typing import List, Optional

import gradio as gr
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Load environment variables
load_dotenv()

@dataclass
class ActionResult:
    is_done: bool
    extracted_content: Optional[str]
    error: Optional[str]
    include_in_memory: bool

@dataclass
class AgentHistoryList:
    all_results: List[ActionResult]
    all_model_outputs: List[dict]

def parse_agent_history(history_str: str) -> None:
    console = Console()
    sections = history_str.split('ActionResult(')
    
    for i, section in enumerate(sections[1:], 1):
        content = ''
        if 'extracted_content=' in section:
            content = section.split('extracted_content=')[1].split(',')[0].strip("'")
        
        if content:
            header = Text(f'Step {i}', style='bold blue')
            panel = Panel(content, title=header, border_style='blue')
            console.print(panel)
            console.print()

async def run_browser_task(
    task: str,
    api_key: str,
    model: str = 'gemini-pro',
    headless: bool = True,
) -> str:
    if not api_key.strip():
        return 'Please provide a Gemini API key'

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize the selected model
        model = genai.GenerativeModel(model)
        
        # Create a prompt that includes the task
        prompt = f"""Task: {task}
        Please analyze this task and provide a detailed step-by-step plan to accomplish it.
        Include any relevant web browsing steps, data extraction methods, and potential challenges.
        Format the response in a clear, structured way with numbered steps.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f'Error: {str(e)}'

def create_ui():
    with gr.Blocks(title='Browser Use GUI') as interface:
        gr.Markdown('# AI Task Assistant (Powered by Gemini)')
        gr.Markdown('Enter your task and let Gemini help you plan and execute it!')

        with gr.Row():
            with gr.Column():
                api_key = gr.Textbox(
                    label='Gemini API Key', 
                    placeholder='Enter your Gemini API key...', 
                    type='password'
                )
                task = gr.Textbox(
                    label='Task Description',
                    placeholder='E.g., Find flights from New York to London for next week',
                    lines=3
                )
                model = gr.Dropdown(
                    choices=[
                        'gemini-pro',
                        'gemini-pro-vision',
                        'gemini-1.0-pro',
                        'gemini-1.0-pro-vision',
                    ], 
                    label='Model', 
                    value='gemini-pro'
                )
                headless = gr.Checkbox(
                    label='Run Headless', 
                    value=True, 
                    info="Run browser in background"
                )
                submit_btn = gr.Button('Analyze Task')

            with gr.Column():
                output = gr.Textbox(
                    label='Analysis Results', 
                    lines=10, 
                    interactive=False
                )

        gr.Markdown("""
        ### Notes:
        - You need a Gemini API key to use this tool
        - Get your API key from: https://makersuite.google.com/app/apikey
        - The tool uses Gemini's advanced models for task analysis
        """)

        submit_btn.click(
            fn=lambda *args: asyncio.run(run_browser_task(*args)),
            inputs=[task, api_key, model, headless],
            outputs=output,
        )

    return interface

if __name__ == '__main__':
    demo = create_ui()
    demo.launch(share=True) 