import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent

load_dotenv()

# Initialize the model
llm = ChatGoogleGenerativeAI(
	model="gemini-2.0-flash",
	google_api_key=os.getenv("GEMINI_API_KEY"),
	temperature=0.0,
)
task = 'go to devmatesolutions.com.'

# agent = Agent(task=task, llm=llm)  # Moved inside main()


async def main():
	agent = Agent(task=task, llm=llm)
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
