# Novel Scraper

## **Project Overview**
Novel Scraper is a robust, automated web scraping tool designed for novel enthusiasts who wish to collect metadata and chapter information from online novel pages effortlessly. This project utilizes Selenium, WebDriver Manager, and Python’s standard libraries to navigate dynamic web pages and scrape detailed information.

The scraper is structured to capture and store key data points, including novel titles, metadata, and chapter links, making it an essential tool for archiving, analysis, or personal reading projects.

---

## **Key Features**
- **Metadata Extraction:**
  - Scrapes and saves critical details such as:
    - Title
    - Cover Image URL
    - Rating
    - Author
    - Genres
    - Status
    - Publisher
    - Tags
    - Year of Publishing
    - Synopsis

- **Chapter List Extraction:**
  - Automatically navigates to and clicks the "Chapter List" button on the target website.
  - Captures chapter list content and saves it as a structured JSON file.
  - Extracts chapter URLs and titles.

- **Full Page Content Capture:**
  - Saves the entire main section of the webpage as raw HTML content for further processing.

- **Flexible and Extendable:**
  - Built with clean and modular code.
  - Easily extendable to handle other scraping requirements.

---

## **Code Flow Breakdown**

1. **User Input:**
   - The script prompts the user for the target novel’s URL.

2. **WebDriver Setup:**
   - The tool initializes the Microsoft Edge WebDriver using the `webdriver-manager` library to manage driver installations.

3. **Metadata Scraping:**
   - Navigates the page using defined XPath selectors to extract key metadata.
   - Metadata is saved in a structured text file (`metadata.txt`).

4. **Chapter List Navigation:**
   - Automatically clicks the "Chapter List" button to load the full list of available chapters.

5. **Chapter Extraction:**
   - Captures all chapter links and titles.
   - Stores chapter information in `chapters.json` as a dictionary of titles and URLs.

6. **Data Persistence:**
   - Saves data in plain text and JSON formats for user access.

7. **Error Handling:**
   - Built-in exception handling to manage errors during scraping.

---

## **Dependencies and Installation**

### **Requirements:**
- **Python 3.x**
- **Microsoft Edge (Chromium-based)**
- **Edge WebDriver (Automatically managed)**

### **Installation Instructions:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/identifiedUserID/novel-scraper.git
   cd novel-scraper
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```
   
   Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install selenium webdriver-manager
   ```

4. **Ensure Edge is Installed:**
   The script uses `webdriver-manager` to automatically manage the Edge WebDriver. Ensure you have Microsoft Edge (Chromium-based) installed.

---

## **How to Use**

1. **Run the Script:**
   ```bash
   python scraper.py
   ```

2. **Enter the Novel URL:**
   Input the URL of the target novel page when prompted.

3. **Data Output:**
   - `full_content.txt`: Raw HTML content of the main section of the novel page.
   - `metadata.txt`: Text file containing novel metadata.
   - `all_chapters.txt`: Full chapter list as raw HTML.
   - `chapters.json`: JSON dictionary containing chapter titles and URLs.

---

## **Sample Output Files**

### **Metadata (`metadata.txt`) Example:**
```
Title: Master of None
Author: John Doe
Genres: Action, Adventure, Fantasy
Status: Ongoing
Publisher: XYZ Publications
Tags: Strong MC, Magic
Year of Publishing: 2022
Rating: 4.8/5
Synopsis: A gripping tale of...
```

### **Chapter JSON (`chapters.json`) Example:**
```json
{
  "Chapter 1 - Awakening": "https://novelbin.com/b/master-of-none/chapter-1-awakening",
  "Chapter 2 - The Journey Begins": "https://novelbin.com/b/master-of-none/chapter-2-the-journey-begins"
}
```

---

## **Error Handling and Troubleshooting**
- **EdgeDriver Not Found:**
  Ensure Edge is installed, and `pip install webdriver-manager` has been run.
- **Timeout Errors:**
  Increase `time.sleep()` intervals to allow slow-loading pages more time.
- **Invalid XPaths:**
  XPaths may need adjustment if the website structure changes.

---

## **Potential Enhancements**
- Improved error handling with detailed logging.
- Support for additional browsers.
- Multi-threaded chapter scraping for faster performance.
- GUI interface for user-friendly operations.

---

## **License**
This project is licensed under the Apache 2.0 License.

---

## **Contributions**
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

## **Acknowledgements**
- [Selenium](https://www.selenium.dev/) for browser automation.
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) for easy driver management.
- Novelbin for novel content to scrape from.
- The developers and contributors of novel scraping resources.

Happy scraping! 📰

