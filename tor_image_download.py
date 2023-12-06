import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import random
import string
from requests.auth import HTTPProxyAuth

# Function to generate a random User-Agent
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    return random.choice(user_agents)

def download_image(img_url, output_folder, overwrite=False, headers=None, proxies=None, auth=None):
    try:
        if headers is None:
            headers = {'User-Agent': get_random_user_agent()}

        response = requests.get(img_url, headers=headers, proxies=proxies, auth=auth)
        response.raise_for_status()

        # Generate a short and unique filename
        short_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        img_filename = os.path.join(output_folder, f"{short_filename}.jpg")

        # Ensure the file does not exist before saving
        if not overwrite and os.path.exists(img_filename):
            return

        with open(img_filename, 'wb') as img_file:
            img_file.write(response.content)

        print(f"Downloaded: {img_filename}")

    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def download_images(url, output_folder='downloaded_images', extensions=None, overwrite=False, max_workers=10, proxies=None, auth=None):
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Fetch HTML content
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, proxies=proxies, auth=auth)
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
            executor.map(lambda img_url: download_image(img_url, output_folder, overwrite, headers, proxies, auth), img_urls)

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("##############################################")
    print("# Disclaimer:                               #")
    print("# This script is for educational purposes   #")
    print("# only. Use it responsibly and comply with  #")
    print("# the terms of service of the websites you  #")
    print("# interact with. The author is not          #")
    print("# responsible for any misuse of this script.#")
    print("##############################################\n")

    # Get the URL from the user
    url = input("Enter the .onion URL: ").strip()

    # Specify output folder
    output_folder = input("Enter the output folder (press Enter for 'downloaded_images'): ").strip() or 'downloaded_images'

    # Specify image extensions (comma-separated, e.g., jpg,png,gif)
    extensions_input = input("Enter image extensions to filter (press Enter for all): ").strip()
    extensions = extensions_input.split(',') if extensions_input else None

    # Specify whether to overwrite existing files
    overwrite = input("Do you want to overwrite existing files? (y/n): ").strip().lower() == 'y'

    # Specify the maximum number of concurrent downloads
    max_workers_input = input("Enter the maximum number of concurrent downloads (press Enter for 10): ").strip()
    max_workers = int(max_workers_input) if max_workers_input else 10

    # Specify proxy (optional, you need to configure Tor to act as a SOCKS proxy)
    use_proxy = input("Do you want to use a proxy? (y/n): ").strip().lower() == 'y'
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'} if use_proxy else None

    # Specify authentication for proxy (if needed)
    use_auth = input("Do you need authentication for the proxy? (y/n): ").strip().lower() == 'y'
    auth = None
    if use_auth:
        proxy_username = input("Enter proxy username: ").strip()
        proxy_password = input("Enter proxy password: ").strip()
        auth = HTTPProxyAuth(proxy_username, proxy_password)

    # Download and save images
    download_images(url, output_folder, extensions, overwrite, max_workers, proxies, auth)
