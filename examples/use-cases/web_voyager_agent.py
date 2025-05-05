# Goal: A general-purpose web navigation agent for tasks like flight booking and course searching.

import asyncio
import os
import sys

# Adjust Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from browser_use.browser.context import BrowserContextWindowSize

# Load environment variables
load_dotenv()

# Configure Gemini API
gemini_api_key = os.getenv('GEMINI_API_KEY')
if not gemini_api_key:
	raise ValueError('No GEMINI_API_KEY found. Please set GEMINI_API_KEY in your .env file.')

llm = ChatGoogleGenerativeAI(
	model="gemini-2.0-flash",
	google_api_key=gemini_api_key,
	convert_system_message_to_human=True
)

browser = Browser(
	config=BrowserConfig(
		headless=False,  # This is True in production
		disable_security=True,
		new_context_config=BrowserContextConfig(
			disable_security=True,
			minimum_wait_page_load_time=1,  # 3 on prod
			maximum_wait_page_load_time=10,  # 20 on prod
			browser_window_size=BrowserContextWindowSize(width=1280, height=1100),
		),
	)
)

TASK = """
Search for the best priced resort in Bali on booking.com with the following requirements:
- 1 bedroom accommodation
- 2 nights stay
- Sort by price (lowest first)
- Select dates from 10th May 2025 to 12th May 2025
- Chose 1 rooms and 2 adults option
- use your reasoning to find the best resort
- reserve the best resort
- use your creativity from searching to finding to reserving the best resort in Bali , but in the end best room should be reserved. In any complex situation you must use your ultimate intelligence to go through.
"""

async def main():
	agent = Agent(
		task=TASK,
		llm=llm,
		browser=browser,
		validate_output=True,
		enable_memory=False,
	)
	history = await agent.run(max_steps=50)
	history.save_to_file('./tmp/history.json')

if __name__ == '__main__':
	asyncio.run(main())
