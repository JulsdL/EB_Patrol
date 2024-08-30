import os
from dotenv import load_dotenv
from .crew import crew  # Ensure the import is correct

# Load environment variables from .env file
load_dotenv()

def main():
    # Define the number of iterations for training
    n_iterations = 1
    filename = 'zooniverse_scraper_train'
    inputs = {
        'inputs': {
            'website_url': 'https://www.zooniverse.org/projects/vbkostov/eclipsing-binary-patrol/talk/6324/3355091',
            'css_element': {
                'message': '.talk-comment-body',  # Adjust this selector to the actual class or tag for message content
                'author': '.talk-comment-author'  # Adjust this selector to the actual class or tag for author names
            }
        }
    }

    try:
        # Ensure crew is properly initialized and the train method is called correctly
        crew.train(n_iterations=n_iterations, inputs=inputs, filename=filename)
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")

# Ensure this script runs the main function when executed
if __name__ == "__main__":
    main()
