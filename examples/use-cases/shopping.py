from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Browser

load_dotenv()

import asyncio
import os

task = """
   ### Prompt for Shopping Agent – Noon.com Women's Fashion Order

**Objective:**
Visit [Noon.com](https://www.noon.com), search for women's fashion items, add them to the cart, and complete the checkout process.

**Important:**
- Make sure to select the correct size and color for each item.
- After your search, click the "Add to Cart" button to add items to your basket.
- You can view your cart by clicking the cart icon in the top right corner.
- Check product reviews and ratings before adding to cart.
---

### Step 1: Navigate to the Website
- Open [Noon.com](https://www.noon.com)
- Navigate to the Women's Fashion section
- You should be logged in as a guest user

---

### Step 2: Add Items to the Basket

#### Shopping List:

**Dresses:**
- 1 Casual summer dress (size M, any color)
- 1 Formal evening dress (black or navy, size M)

**Tops:**
- 2 Basic white t-shirts (size M)
- 1 Blouse for office wear (size M, light colors)
- 1 Statement top for parties (size M)

**Bottoms:**
- 1 Pair of black formal trousers (size M)
- 1 Pair of blue jeans (size M)
- 1 Skirt (size M, any style)

**Outerwear:**
- 1 Light jacket or cardigan (size M)
- 1 Formal blazer (size M, black or navy)

**Accessories:**
- 1 Handbag (medium size, neutral color)
- 1 Pair of sunglasses
- 1 Scarf (any color/pattern)
- 1 Statement necklace

**Shoes:**
- 1 Pair of comfortable flats (size 38)
- 1 Pair of heels (size 38, black or nude)
- 1 Pair of casual sneakers (size 38)

At this stage, check the cart icon in the top right (indicates the number of items) and verify you've added the correct items with proper sizes.

---

### Step 3: Handling Unavailable Items
- If an item is **out of stock** in your size or preferred color:
  - Look for similar items from other brands
  - Check different color options
  - Consider alternative styles that serve the same purpose
- For shoes, if size 38 is not available:
  - Check if the brand runs large/small and adjust size accordingly
  - Look for similar styles from other brands

---

### Step 4: Adjusting for Minimum Order Requirement
- If the total order **is below AED 200**, add more accessories or basic items
- At this step, check if you have bought MORE items than needed. If the price is more than AED 2000, you MUST remove items.
- If an item is not available, choose an alternative.

---

### Step 5: Checkout
- Proceed to checkout by clicking the cart icon and then "Proceed to Checkout"
- Select delivery address (use default if available)
- Choose delivery time slot (preferably within the next 2 days)
- Select payment method (use default if available)
- Complete the checkout process

---

### Step 6: Confirm Order & Output Summary
- Once the order is placed, output a summary including:
  - **Final list of items purchased** (including any substitutions)
  - **Total cost in AED**
  - **Chosen delivery time**
  - **Size and color details for each item**

**Important:** 
- Ensure all items are in the correct size
- Check return policies for each item
- Verify color accuracy from product images
- Ensure efficiency and accuracy throughout the process."""

browser = Browser()

model = ChatGoogleGenerativeAI(
	model="gemini-2.0-flash",
	google_api_key=os.getenv("GEMINI_API_KEY"),
	temperature=0.0,
)

# agent = Agent(
# 	task=task,
# 	llm=model,
# 	browser=browser,
# )


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
