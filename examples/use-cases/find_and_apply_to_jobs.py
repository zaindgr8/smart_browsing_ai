"""
Goal: Searches for job listings, evaluates relevance based on a CV, and applies

@dev You need to add GEMINI_API_KEY to your environment variables.
Also you have to install PyPDF2 to read pdf files: pip install PyPDF2
"""

import asyncio
import csv
import logging
import os
import sys
from pathlib import Path
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, SecretStr
from PyPDF2 import PdfReader

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Validate required environment variables
load_dotenv()
if not os.getenv('GEMINI_API_KEY'):
	raise ValueError('GEMINI_API_KEY is not set. Please add it to your environment variables.')

logger = logging.getLogger(__name__)
# full screen mode
controller = Controller()

# NOTE: This is the path to your cv file
CV = Path.cwd() / 'mycv.pdf'

if not CV.exists():
	raise FileNotFoundError(f'You need to set the path to your cv file in the CV variable. CV file not found at {CV}')


class Job(BaseModel):
	title: str
	link: str
	company: str
	fit_score: float
	location: Optional[str] = None
	salary: Optional[str] = None


@controller.action('Save jobs to file - with a score how well it fits to my profile', param_model=Job)
def save_jobs(job: Job):
	with open('jobs.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow([job.title, job.company, job.link, job.salary, job.location])

	return 'Saved job to file'


@controller.action('Read jobs from file')
def read_jobs():
	with open('mycv.pdf', 'r') as f:
		return f.read()


@controller.action('Read my cv for context to fill forms')
def read_cv():
	pdf = PdfReader(CV)
	text = ''
	for page in pdf.pages:
		text += page.extract_text() or ''
	logger.info(f'Read cv with {len(text)} characters')
	return ActionResult(extracted_content=text, include_in_memory=True)


@controller.action(
	'Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element',
)
async def upload_cv(index: int, browser: BrowserContext):
	path = str(CV.absolute())
	dom_el = await browser.get_dom_element_by_index(index)

	if dom_el is None:
		return ActionResult(error=f'No element found at index {index}')

	file_upload_dom_el = dom_el.get_file_upload_element()

	if file_upload_dom_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	file_upload_el = await browser.get_locate_element(file_upload_dom_el)

	if file_upload_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file "{path}" to index {index}'
		logger.info(msg)
		return ActionResult(extracted_content=msg)
	except Exception as e:
		logger.debug(f'Error in set_input_files: {str(e)}')
		return ActionResult(error=f'Failed to upload file to index {index}')


browser = Browser(
	config=BrowserConfig(
		browser_binary_path=None,  # Let Playwright use its bundled browser
		disable_security=False,    # Disable security features that might interfere
	)
)


async def main():
	ground_task = (
		'You are a professional job finder. '
		'1. Read my cv with read_cv'
		'find web developer jobs and save them to a file'
		'search jobs at linked in'
		"If it asks you to verify as a human, click on the checkbox and then click on the button that says 'Continue'"
		"Sign in as email and My Email for linked in is: //"
		"my password for linked in is: //"
		"Search for web developer jobs"
		"Job Location should be United States"
		"Only Apply for the jobs with option of Easy Apply"
		"Apply on all the jobs in this category but do not apply same job twice"
		"If you find a job that you have already applied to, do not apply again"
		"After clicking Easy Apply mentioned in the job. Slelect first cv option and fill all the options and click on submit application"
		"Than close any pop up and continue with next job"
	)
	tasks = [
		ground_task + '\n' + 'Google',
	]
	
	model = ChatGoogleGenerativeAI(
		model="gemini-2.0-flash",
		google_api_key=os.getenv("GEMINI_API_KEY"),
		temperature=0.0,
	)

	agents = []
	for task in tasks:
		agent = Agent(task=task, llm=model, controller=controller, browser=browser)
		agents.append(agent)

	await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == '__main__':
	asyncio.run(main())
