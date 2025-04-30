import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Browser, BrowserConfig

dotenv.load_dotenv()

browser = Browser(
	config=BrowserConfig(
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)


async def main():
	agent = Agent(
		task='In docs.google.com write my Papa a quick letter',
		llm=ChatGoogleGenerativeAI(
			model="gemini-2.0-flash",
			google_api_key=os.getenv("GEMINI_API_KEY"),
			temperature=0.0,
		),
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
