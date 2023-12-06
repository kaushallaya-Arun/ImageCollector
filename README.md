# Image Downloader Script

## Description
This Python script allows you to download images from a given URL, filter them by extensions, and save them to a local directory. It supports concurrent downloading and provides options for customization.

## Features
- Fetches HTML content from a specified URL
- Parses the HTML to extract image URLs
- Filters images based on specified extensions
- Downloads images concurrently using threads
- Supports custom User-Agent for each request
- Option to overwrite existing files
- Supports http proxy configurations


## Usage
1. Run the script.
2. Enter the URL when prompted.
3. Customize the output folder, image extensions, and other options as needed.

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/image-downloader.git
   cd image-downloader ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the script:
   ```bash
   python image_downloader.py

## Configuration
- `output_folder`: Set the desired output folder for downloaded images.
- `extensions`: Specify image extensions to filter (comma-separated, e.g., jpg,png,gif).
- `overwrite`: Set to True to overwrite existing files, or False to skip them.
- `max_workers`: Set the maximum number of concurrent downloads.

## Using Tor for Anonymity
To access .onion URLs anonymously, follow these steps:

1. Install Tor: Download and install Tor from [https://www.torproject.org/](https://www.torproject.org/).

2. Run Tor as a SOCKS Proxy:
   - Open Tor Browser and go to `Settings`.
   - Under `Advanced`, find `Network` and note the SOCKS port (default is 9050).

3. Configure the Script:
   - When running the script, enter 'y' when prompted to use a proxy.
   - Enter the SOCKS proxy details (e.g., `socks5h://127.0.0.1:9050`).

## Contributing
Feel free to contribute by opening issues or submitting pull requests. Your contributions are welcome and appreciated!

## Disclaimer
This script is for educational purposes only. Use it responsibly and comply with the terms of service of the websites you interact with. The author is not responsible for any misuse of this script.
