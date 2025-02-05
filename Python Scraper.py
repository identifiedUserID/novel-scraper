import time
import re
import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def main():
    novel_url = input("Enter the novel URL: ")

    # Setup Edge WebDriver
    service = EdgeService(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    options.use_chromium = True

    driver = webdriver.Edge(service=service, options=options)

    try:
        driver.get(novel_url)
        time.sleep(2)  # Allow the page to load fully

        # Scrape and save entire content from base XPath
        base_element = driver.find_element(By.XPATH, "/html/body/div/main/div[2]")
        full_content = base_element.get_attribute('outerHTML')
        with open("full_content.txt", "w", encoding="utf-8") as file:
            file.write(full_content)

        # Extract metadata using specific XPaths
        metadata = {}
        try:
            metadata["Title"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]").text
            metadata["Cover Image URL"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[2]/div/div[2]").get_attribute("src")
            metadata["Rating"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/div/div[2]").text
            metadata["Author"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[1]").text
            metadata["Genres"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[2]").text
            metadata["Status"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[3]").text
            metadata["Publisher"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[4]").text
            metadata["Tags"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[5]").text
            metadata["Year of Publishing"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[3]/ul/li[6]").text
            metadata["Synopsis"] = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[4]/div/div[1]/div").text

        except Exception as e:
            print("Error extracting metadata:", e)

        # Save metadata to a file
        with open("metadata.txt", "w", encoding="utf-8") as meta_file:
            for key, value in metadata.items():
                meta_file.write(f"{key}: {value}\n")

        print("Metadata extraction completed successfully.")

        # Navigate to Chapter List and click the button
        chapter_list_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[4]/ul/li[2]")
        chapter_list_button.click()
        time.sleep(3)  # Allow time for chapter list to load

        # Scrape chapter list content
        chapter_content_element = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/div[4]/div/div[2]/div/div/div")
        chapter_content = chapter_content_element.get_attribute('outerHTML')

        # Save chapter content to file
        with open("all_chapters.txt", "w", encoding="utf-8") as file:
            file.write(chapter_content)

        print("Chapter content saved. Processing chapter links...")

        # Process and extract chapter links from the file
        with open("all_chapters.txt", "r", encoding="utf-8") as file:
            chapter_data = file.read()

        # Regex to find chapter URLs and titles
        chapters = re.findall(r'<a href="([^"]+)"[^>]*title="([^"]+)"', chapter_data)

        # Convert to dictionary
        chapter_dict = {title: url for url, title in chapters}

        # Save as JSON
        with open("chapters.json", "w", encoding="utf-8") as json_file:
            json.dump(chapter_dict, json_file, indent=4)

        print("Chapters successfully saved to chapters.json.")

    except Exception as e:
        print("Error during scraping:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()



