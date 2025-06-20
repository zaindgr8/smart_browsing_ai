# Goal: Implements a multi-agent system for online code editors, with separate agents for coding and execution.

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Browser

# Load environment variables
load_dotenv()
if not os.getenv('GEMINI_API_KEY'):
	raise ValueError('GEMINI_API_KEY is not set. Please add it to your environment variables.')


async def main():
	browser = Browser()
	async with await browser.new_context() as context:
		model = ChatGoogleGenerativeAI(
			model="gemini-2.0-flash",
			google_api_key=os.getenv('GEMINI_API_KEY'),
			convert_system_message_to_human=True
		)

		# Initialize browser agent
		agent1 = Agent(
			task='Open an online code editor programiz.',
			llm=model,
			browser_context=context,
		)
		executor = Agent(
			task='Executor. Execute the code written by the coder and suggest some updates if there are errors.',
			llm=model,
			browser_context=context,
		)

		coder = Agent(
			task='Coder. Your job is to write and complete code. You are an expert coder. Code a simple calculator. Write the code on the coding interface after agent1 has opened the link.',
			llm=model,
			browser_context=context,
		)
		await agent1.run()
		await executor.run()
		await coder.run()


if __name__ == '__main__':
	asyncio.run(main())
