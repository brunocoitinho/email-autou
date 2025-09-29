import nltk
import os

# Define the target directory relative to this script
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'nltk_data')

# Create the directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Download the 'punkt' package to our local directory
nltk.download('punkt', download_dir=DOWNLOAD_DIR)

print(f"NLTK 'punkt' package downloaded to {DOWNLOAD_DIR}")
