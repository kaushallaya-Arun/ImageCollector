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
- Creates a zip file containing all downloaded images

## Usage
1. Run the script.
2. Enter the URL when prompted.
3. Customize the output folder, image extensions, and other options as needed.

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/image-downloader.git
   cd image-downloader ```

2.Install dependencies:
   ```pip install -r requirements.txt```

Usage Example:
   ```python image_downloader.py```

Configuration:
~output_folder: Set the desired output folder for downloaded images.
~extensions: Specify image extensions to filter (comma-separated, e.g., jpg,png,gif).
~overwrite: Set to True to overwrite existing files, or False to skip them.
~max_workers: Set the maximum number of concurrent downloads.

**Contributing:- Feel free to contribute by opening issues or submitting pull requests.
