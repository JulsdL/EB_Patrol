from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from crewai_tools import BaseTool
import time

class SeleniumScraperTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="SeleniumScraperTool",
            description="Tool to scrape forum discussions using Selenium."
        )

    def _run(self, inputs):
        # Log inputs to verify correctness
        print(f"Inputs received: {inputs}")

        # Extract the actual inputs from the nested 'inputs' dictionary
        actual_inputs = inputs.get('inputs', {})
        url = actual_inputs.get('url')
        message_selector = actual_inputs.get('selectors', {}).get('message')
        author_selector = actual_inputs.get('selectors', {}).get('author')

        if not url or not message_selector or not author_selector:
            raise ValueError("URL, message selector, and author selector are required for scraping.")

        # Set up Selenium with ChromeDriver
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        service = Service(executable_path='/home/julien/.wdm/drivers/chromedriver/linux64/128.0.6613.86/chromedriver-linux64/chromedriver')


        # Launch the browser
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(5)  # Allow time for page to load

        data = []

        # Locate messages and authors using provided selectors
        messages = driver.find_elements(By.CSS_SELECTOR, message_selector)
        for message in messages:
            message_text = message.text
            try:
                author = message.find_element(By.CSS_SELECTOR, author_selector)
                author_text = author.text
            except:
                author_text = "Unknown author"

            data.append({'author': author_text, 'message': message_text})

        # Clean up
        driver.quit()
        return data

if __name__ == "__main__":
    # Example input to test the tool
    inputs = {
        'url': 'https://www.zooniverse.org/projects/vbkostov/eclipsing-binary-patrol/talk/6324/3355091',
        'selectors': {
            'message': '.talk-comment-body',  # Adjust this selector to the actual class or tag for message content
            'author': '.talk-comment-author'   # Adjust this selector to the actual class or tag for author names
        }
    }

    scraper = SeleniumScraperTool()
    results = scraper._run(inputs)
    print(results)
