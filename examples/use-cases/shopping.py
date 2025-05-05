from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser
import asyncio
import os

load_dotenv()

task = """
Visit [Noon.com](https://www.noon.com) and shop for women's clothing items with a total budget of 200 AED.

Shopping List:
- 1 Basic t-shirt (size M)
- 1 Casual top (size M)
- 1 Pair of basic pants (size M)

Instructions:
1. Navigate to noon.com
2. Search for each item
3. Make sure the total cost stays under 200 AED
4. Add items to cart
5. Proceed to checkout
6. Output a summary of:
   - Items purchased
   - Total cost in AED
"""

browser = Browser()

model = ChatGoogleGenerativeAI(
	model="gemini-2.0-flash",
	google_api_key=os.getenv("GEMINI_API_KEY"),
	temperature=0.0,
)

async def main():
	agent = Agent(
		task=task,
		llm=model,
		browser=browser,
	)
	await agent.run()
	input('Press Enter to close the browser...')
	await browser.close()

if __name__ == '__main__':
	asyncio.run(main())
