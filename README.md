# Web Chapter Scraper

## Overview

This Python script is a web scraper designed to extract chapters from a website and save them into structured text files. The scraper processes each chapter, extracts the chapter title while removing numeric identifiers, and saves the content in multiple files with a maximum of 100 chapters per file. Additionally, users can specify a start and end chapter range to control which chapters are scraped.

## Features

- **Extracts Chapter Content**: Scrapes chapter text from web pages and saves them in `.txt` format.
- **Title Formatting**: Extracts chapter titles while omitting numeric prefixes (e.g., "Chapter 6: Title" → "Title").
- **Multiple Output Files**: Splits content into separate files, each containing a maximum of 100 chapters.
- **Custom Chapter Range Selection**: Allows users to specify a start and end chapter for targeted scraping.
- **Rate Limiting**: Implements a 1-second delay between requests to prevent server overload.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required dependencies:
    
    ```bash
    pip install requests beautifulsoup4
    ```
    

## Installation

1. Clone the repository:
    
    ```bash
    git clone https://github.com/yourusername/web-chapter-scraper.git
    cd web-chapter-scraper
    ```
    
2. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    

## Usage

### 1. Basic Scraping (All Chapters)

```python
scrape_and_save(urls)
```

This will scrape all available chapters and save them in multiple text files.

### 2. Scrape a Specific Range

```python
scrape_and_save(urls, start_chapter=50, end_chapter=200)
```

This extracts chapters from **Chapter 50 to Chapter 200** only.

### 3. File Naming Convention

- `ScrapedChapters_n-k.txt` (where `n` is the start chapter and `k` is the end chapter in that file).

### 4. Extracted Chapter Format

Each chapter follows this structure in the output files:

```
###
Chapter 1: Extracted Chapter Title

(Chapter content here...)
```

## Code Structure

```python
extract_chapter_title(text)  # Extracts and formats chapter titles
scrape_and_save(urls, start_chapter=None, end_chapter=None)  # Main function to scrape and save chapters
```

## Contribution

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Added feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Submit a pull request.

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for details.