import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor
import random

# Function to generate a random User-Agent
def get_random_user_agent():
    user_agents = [
        # Add more user agents as needed
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    return random.choice(user_agents)

def download_image(img_url, output_folder, overwrite=False):
    img_filename = os.path.join(output_folder, os.path.basename(img_url))
    if not overwrite and os.path.exists(img_filename):
        print(f"Skipped: {img_filename} (already exists)")
        return

    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(img_url, headers=headers)
        response.raise_for_status()

        with open(img_filename, 'wb') as img_file:
            img_file.write(response.content)

        print(f"Downloaded: {img_filename}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def download_images(url, output_folder='downloaded_images', extensions=None, overwrite=False, max_workers=10):
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Fetch HTML content
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract image URLs
        img_urls = [urljoin(url, img['src']) for img in soup.find_all('img') if 'src' in img.attrs]

        if not img_urls:
            print("No images found on the webpage.")
            return

        # Filter images based on extensions
        if extensions:
            img_urls = [img_url for img_url in img_urls if any(img_url.lower().endswith(ext.lower()) for ext in extensions)]

        if not img_urls:
            print("No images found with the specified extensions.")
            return

        # Download images concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda img_url: download_image(img_url, output_folder, overwrite), img_urls)

        # Create a zip file
        zip_filename = os.path.join(output_folder, 'images.zip')
        with ZipFile(zip_filename, 'w') as zipf:
            for img_url in img_urls:
                img_filename = os.path.basename(img_url)
                img_path = os.path.join(output_folder, img_filename)
                if os.path.exists(img_path):
                    zipf.write(img_path, img_filename)

        print(f"\nImages downloaded and saved in '{output_folder}'.")
        print(f"Zip file created: {zip_filename}")

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Get the URL from the user
    url = input("Enter the URL: ").strip()

    # Specify output folder
    output_folder = input("Enter the output folder (press Enter for 'downloaded_images'): ").strip() or 'downloaded_images'

    # Specify image extensions (comma-separated, e.g., jpg,png,gif)
    extensions_input = input("Enter image extensions to filter (press Enter for all): ").strip()
    extensions = extensions_input.split(',') if extensions_input else None

    # Specify whether to overwrite existing files
    overwrite = input("Do you want to overwrite existing files? (y/n): ").strip().lower() == 'y'

    # Specify the maximum number of concurrent downloads
    max_workers = int(input("Enter the maximum number of concurrent downloads (press Enter for 10): ").strip()) or 10

    # Download and save images
    download_images(url, output_folder, extensions, overwrite, max_workers)
