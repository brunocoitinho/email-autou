import nltk
import os

# Define the target directory relative to this script
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'nltk_data')

# Create the directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# List of packages to download
packages = ['punkt', 'stopwords']

for package in packages:
    print(f"Downloading NLTK package: {package}")
    nltk.download(package, download_dir=DOWNLOAD_DIR)

print(f"\nNLTK packages downloaded to {DOWNLOAD_DIR}")