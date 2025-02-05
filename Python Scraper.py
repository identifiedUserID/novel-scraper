import time
import re
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions  # Import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

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


def main():
    novel_url = input("Enter the novel URL: ")
    driver = setup_webdriver_headless()

    try:
        navigate_to_url(driver, novel_url)

        if download_raw_metadata(driver): # Check if raw metadata download was successful
            process_metadata(driver)

        navigate_to_chapter_list(driver)
        download_raw_chapter_content(driver)
        process_chapter_content(driver)

    except Exception as e:
        print("Error during scraping:", e)

    finally:
        if 'driver' in locals(): # Check if driver was initialized
            driver.quit()

if __name__ == "__main__":
    main()