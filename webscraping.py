import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
driver = webdriver.Chrome()
csv_file = "onepiece_episodes.csv"
cookies_accepted = False

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(["Episode Number", "Episode Title", "Air Date", "Short Summary", "Long Summary", "Characters", "Fruits"])

    
    for episode_num in range(1, 1121):
        url = f"https://onepiece.fandom.com/wiki/Episode_{episode_num}"
        driver.get(url)
        
        try:
            
            if not cookies_accepted:
                try:
                    accept_cookies_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "NN0_TB_DIsNmMHgJWgT7U"))
                    )
                    accept_cookies_button.click()
                    cookies_accepted = True  
                except Exception:
                    pass  

            # Episode Number
            ep_num = driver.find_element(By.ID, "firstHeading").text

            # Episode Title
            ep_title = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/h2').text

            # Episode Air Date
            ep_air_date = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/section[2]/div[3]/div').text

            # Episode Short Summary
            before_short_sum = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/h2[1]')
            ep_short_sum_start = before_short_sum.find_element(By.XPATH, 'following-sibling::*[1]' )
            end_header_short = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/h2[2]')

            paragraphsShort = []
            current_element_short = ep_short_sum_start
      
            while current_element_short is not None and current_element_short != end_header_short:
                if current_element_short.tag_name == 'p':
                    paragraphsShort.append(current_element_short.text)

                try:
                    current_element_short = current_element_short.find_element(By.XPATH, 'following-sibling::*[1]')
                except Exception:
                    break

            ep_short_sum = "\n".join(paragraphsShort)

            # Episode Long Summary
            before_long_sum = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/h2[2]')
            ep_long_sum_start = before_long_sum.find_element(By.XPATH, 'following-sibling::*[1]')
            end_header = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/h2[3]')

            paragraphs = []
            ep_fruits = []
            current_element = ep_long_sum_start

            # Regex pattern to match "*blank* *blank* no Mi" and "*blank* *blank* no Mi, Model: *blank*"
            fruit_pattern = r'(\w+\s\w+\sno\sMi(?:,\sModel:\s\w+)?)'

            # Collect paragraphs until end_header is reached
            while current_element is not None and current_element != end_header:
                if current_element.tag_name == 'p':
                    paragraph_text = current_element.text
                    paragraphs.append(paragraph_text)

                    # Find all matching fruits in the paragraph
                    fruits_in_paragraph = re.findall(fruit_pattern, paragraph_text)
                    fruits_in_paragraph = [fruit.replace(",", "") for fruit in fruits_in_paragraph]
                    ep_fruits.extend(fruits_in_paragraph)

                    # teste
                    if fruits_in_paragraph:
                        print(f"Fruits found in paragraph: {fruits_in_paragraph}")

                try:
                    current_element = current_element.find_element(By.XPATH, 'following-sibling::*[1]')
                except Exception:
                    break

            ep_long_sum = "\n".join(paragraphs)

            # Skip the <h2> (end_header) and move to the next sibling element para ir para os characters
            next_element_after_h2 = end_header.find_element(By.XPATH, 'following-sibling::*[1]')

            # Now we need to handle the characters list starting from the next element after <h2>
            try:
                if next_element_after_h2.tag_name == 'div':  # Case 1: <div> contains a <ul>
                    ul_element = next_element_after_h2.find_element(By.XPATH, './ul')
                elif next_element_after_h2.tag_name == 'ul':  # Case 2: It's directly a <ul>
                    ul_element = next_element_after_h2
                else:
                    ul_element = None

                if ul_element:
                    # Extract characters list
                    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
                    ep_characters = [li.text for li in li_elements]

            except Exception as e:
                print(f"Error extracting characters: {str(e)}")


            # Write the extracted data to the CSV file
            writer.writerow([ep_num, ep_title, ep_air_date, ep_short_sum, ep_long_sum, ", ".join(ep_characters), ", ".join(ep_fruits)])

            print(f"Episode {episode_num} data written to CSV")

        except Exception as e:
            print(f"Error extracting data for Episode {episode_num}: {str(e)}")


driver.quit()
"""
# Initialize the WebDriver
driver = webdriver.Chrome()

# CSV file to save the ratings
all_ratings = []

# Loop through pages with offsets in increments of 100 (until offset 1100)
for offset in range(0, 1200, 100):
    # Navigate to the target URL with the current offset
    url = f'https://myanimelist.net/anime/21/One_Piece/episode?offset={offset}'
    print(f"Scraping {url}")
    driver.get(url)
    
    try:
        # Wait until the table is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table'))
        )

        # Find all `td` elements with class `episode-poll ac nowrap scored`
        rating_elements = driver.find_elements(By.XPATH, '//td[contains(@class, "episode-poll")]//div[@class="average"]//span[@class="value"]')
        
       
        # Loop through all the ratings and extract the text
        for index, rating_element in enumerate(rating_elements, start=offset+1):
            rating = rating_element.text
            all_ratings.append((index, rating))
            print(f"Episode {index}: Rating {rating}")
            
        # Small sleep to avoid overwhelming the server
        time.sleep(2)
        
    except Exception as e:
        print(f"Error while extracting ratings for offset {offset}: {e}")

# Close the WebDriver
driver.quit()


print(all_ratings)

csv_file = "onepiece_allepisodes.csv"
updated_csv_file = "onepiece_allepisodes_with_ratings.csv"
# Print all the ratings
with open(csv_file, mode='r', encoding='utf-8') as infile, open(updated_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Read and write the header with the new "Rating" column
    header = next(reader)
    header.append("Rating")
    writer.writerow(header)
    
    # Write the rest of the data along with the ratings
    for i, row in enumerate(reader):
        if i < len(all_ratings):
            row.append(all_ratings[i][1])  # Append the rating to the row
        else:
            row.append("")  # In case there are more rows than ratings
        writer.writerow(row)
