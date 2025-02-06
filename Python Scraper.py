import time
import requests
import os
import re
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions  # Import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

def setup_webdriver_headless():
    """Sets up the Edge WebDriver in headless mode."""
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")  # Headless argument
    driver = webdriver.Edge(service=service, options=options)
    return driver

def navigate_to_url(driver, url):
    """Navigates the WebDriver to the specified URL."""
    driver.get(url)
    time.sleep(1)  # Allow page to load

def download_raw_metadata(driver):
    """Downloads the raw metadata and saves it to full_content.txt."""
    try:
        base_element = driver.find_element(By.XPATH, "/html/body/div/main/div[2]")  # Keep original XPath
        full_content = base_element.get_attribute('outerHTML')
        with open("full_content.txt", "w", encoding="utf-8") as file:
            file.write(full_content)
        print("Raw metadata downloaded.")
    except Exception as e:
        print("Error downloading raw metadata:", e)
        return None  # Indicate failure
    return True  # Indicate success

def write_markdown(metadata, filename="metadata.md"):
    """Writes metadata to a Markdown file."""
    try:
        with open(filename, "w", encoding="utf-8") as md_file:
            md_file.write(f"# {metadata.get('Title', 'N/A')}\n\n")  # Title as Heading 1

            cover_image_url = metadata.get('Cover Image URL')
            if cover_image_url:
                md_file.write(f"![Cover Image]({cover_image_url})\n\n")  # Cover Image

            md_file.write(f"**Author:** {metadata.get('Author', 'N/A')}\n\n")
            md_file.write(f"**Genres:** {metadata.get('Genres', 'N/A')}\n\n")
            md_file.write(f"**Status:** {metadata.get('Status', 'N/A')}\n\n")
            md_file.write(f"**Publisher:** {metadata.get('Publisher', 'N/A')}\n\n")
            md_file.write(f"**Tags:** {metadata.get('Tags', 'N/A')}\n\n")
            md_file.write(f"**Year of Publishing:** {metadata.get('Year of Publishing', 'N/A')}\n\n")
            md_file.write(f"**Rating:** {metadata.get('Rating', 'N/A')}\n\n")

            md_file.write(f"## Synopsis\n\n{metadata.get('Synopsis', 'N/A')}\n") #Synopsis as Heading 2

        print(f"Metadata saved to {filename}")
    except Exception as e:
        print(f"Error writing Markdown file: {e}")

def process_metadata(driver):
    """Processes the raw metadata and saves it to metadata.md (Markdown)."""
    metadata = {}
    try:
        # ... (Your existing metadata extraction XPaths) ...
        metadata["Title"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/h3").text
        metadata["Cover Image URL"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[2]/div/div[2]/img").get_attribute("src")
        metadata["Rating"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/div/div[2]").text
        metadata["Author"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[1]").text
        metadata["Genres"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[2]").text
        metadata["Status"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[3]").text
        metadata["Publisher"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[4]").text
        metadata["Tags"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[5]").text
        metadata["Year of Publishing"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[6]").text
        metadata["Synopsis"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[4]/div/div[1]/div").text

        write_markdown(metadata)  # Call the function to write Markdown

    except Exception as e:
        print("Error processing metadata:", e)

def navigate_to_chapter_list(driver):
    """Navigates to the chapter list and clicks the button."""
    try:
        chapter_list_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[4]/ul/li[2]")
        chapter_list_button.click()
        time.sleep(1)  # Allow time for chapter list to load
        print("Navigated to chapter list.")
    except Exception as e:
        print("Error navigating to chapter list:", e)

def download_raw_chapter_content(driver):
    """Downloads the raw chapter content and saves it to chapter_content.txt."""
    try:
        chapter_content_element = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[4]/div/div[2]/div/div/div")
        chapter_content = chapter_content_element.get_attribute('outerHTML')
        with open("chapter_content.txt", "w", encoding="utf-8") as file:
            file.write(chapter_content)
        print("Raw chapter content downloaded.")
    except Exception as e:
        print("Error downloading raw chapter content:", e)

def process_chapter_content(driver):
    """Processes the raw chapter content and saves it to chapters.json."""
    try:
      with open("chapter_content.txt", "r", encoding="utf-8") as file:
        chapter_data = file.read()

      chapters = re.findall(r'<a href="([^"]+)"[^>]*title="([^"]+)"', chapter_data)
      chapter_dict = {title: url for url, title in chapters}

      with open("chapters.json", "w", encoding="utf-8") as json_file:
          json.dump(chapter_dict, json_file, indent=4)

      print("Chapter content processed and saved to chapters.json.")
    except Exception as e:
      print("Error processing chapter content", e)

def get_chapter_range(chapter_data):
    """Gets the chapter range from the user, with validation."""
    while True:
        chapter_range_input = input("Enter chapter range to scrape (e.g., 1-5, or press Enter to scrape all): ")
        if not chapter_range_input:
            start_chapter = 1
            end_chapter = len(chapter_data)
            print(f"Scraping all chapters ({start_chapter}-{end_chapter}).")
            return start_chapter, end_chapter  # Return the range

        try:
            start_chapter, end_chapter = map(int, chapter_range_input.split("-"))
            if 1 <= start_chapter <= end_chapter <= len(chapter_data):
                print(f"Scraping chapters {start_chapter}-{end_chapter}.")
                return start_chapter, end_chapter  # Return the range
            else:
                print("Invalid chapter range. Please enter a valid range within the number of chapters.")
        except ValueError:
            print("Invalid input. Please enter a range in the format 'start-end'.")

def scrape_and_save(url, file):
    """Scrapes content from a URL and saves it to a file."""
    try:  # Add try-except block for requests
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = '\n\n'.join([p.get_text(strip=True) for p in soup.find_all('p')])
        file.write(page_text)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {url}: {e}")
    except Exception as e: # Catch other potential errors (e.g., BeautifulSoup errors)
        print(f"Error processing {url}: {e}")

def main():
    novel_url = input("Enter the novel URL: ")
    driver = setup_webdriver_headless()
    current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        navigate_to_url(driver, novel_url)

        if download_raw_metadata(driver):
            process_metadata(driver)

        navigate_to_chapter_list(driver)
        download_raw_chapter_content(driver)
        process_chapter_content(driver)

        with open(os.path.join(current_dir, "chapters.json"), "r", encoding="utf-8") as json_file:
            chapter_data = json.load(json_file)

        start_chapter, end_chapter = get_chapter_range(chapter_data)

        chapter_titles = list(chapter_data.keys())
        selected_chapters = {}
        for i in range(start_chapter - 1, end_chapter):
            title = chapter_titles[i]
            url = chapter_data[title]
            selected_chapters[title] = url

        # Now you have selected_chapters, which is a dictionary of title:url pairs
        # for the chapters the user wants to scrape.

        all_chapter_file_path = os.path.join(current_dir, "all_chapters.txt") #correct path for all_chapters.txt

        with open(all_chapter_file_path, 'w', encoding='utf-8') as file:
            progress = 1
            for title, url in selected_chapters.items():  # Iterate through selected chapters
                file.write(f'\n###\n{title}\n') #write the title instead of chapter count

                scrape_and_save(url, file)
                print(f"Progress: {progress}/{len(selected_chapters)}")

                progress += 1
                time.sleep(1)  # Rate limit

    except Exception as e:
        print("Error during scraping:", e)

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
