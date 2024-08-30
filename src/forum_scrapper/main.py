from src.forum_scrapper.crew import crew

# Define the inputs for the scraping task
inputs = {'inputs': {
    'website_url': 'https://www.zooniverse.org/projects/vbkostov/eclipsing-binary-patrol/talk/6324/3355091',
    'css_element': {
        'message': '.talk-comment-body',  # Adjust this selector to the actual class or tag for message content
        'author': '.talk-comment-author'  # Adjust this selector to the actual class or tag for author names
    }
}}

# Print inputs to verify correctness before passing to crew.kickoff
print(f"Kicking off crew with inputs: {inputs}")

# Start the crew with the correct inputs structure
result = crew.kickoff(inputs=inputs)

# Print the result or handle the markdown output
print(result)
