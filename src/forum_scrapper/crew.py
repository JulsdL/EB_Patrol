import os
import yaml
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai_tools import SeleniumScrapingTool
from src.forum_scrapper.tools.markdown_writer import MarkdownWriterTool

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# Load agents and tasks from YAML files
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

agents_config = load_yaml('src/forum_scrapper/config/agents.yaml')
tasks_config = load_yaml('src/forum_scrapper/config/tasks.yaml')

# Initialize the tools
selenium_scraper_tool = SeleniumScrapingTool()
markdown_writer_tool = MarkdownWriterTool()

# Scraper Agent
scraper = Agent(
    role=agents_config['scraper_agent']['role'],
    goal=agents_config['scraper_agent']['goal'],
    backstory=agents_config['scraper_agent']['backstory'],
    tools=[selenium_scraper_tool],
    memory=True,
    verbose=True
)

# Formatter Agent
formatter = Agent(
    role=agents_config['formatter_agent']['role'],
    goal=agents_config['formatter_agent']['goal'],
    backstory=agents_config['formatter_agent']['backstory'],
    tools=[markdown_writer_tool],
    memory=True,
    verbose=True
)

# Scrape Discussions Task
scrape_task = Task(
    description=tasks_config['scrape_discussions_task']['description'],
    expected_output=tasks_config['scrape_discussions_task']['expected_output'],
    agent=scraper
)

# Format to Markdown Task
format_task = Task(
    description=tasks_config['format_to_markdown_task']['description'],
    expected_output=tasks_config['format_to_markdown_task']['expected_output'],
    agent=formatter
)

# Crew Configuration
crew = Crew(
    agents=[scraper, formatter],
    tasks=[scrape_task, format_task],
    process=Process.sequential
)
