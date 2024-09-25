from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://onepiece.fandom.com/wiki/Episode_93")

try:
    # Wait for the "ACCEPT COOKIES" button to be clickable and click it
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "NN0_TB_DIsNmMHgJWgT7U"))
    )
    accept_cookies_button.click()

    # Episode Num
    ep_num = driver.find_element(By.ID,"firstHeading")
   
    print("Episode number:", ep_num.text)

    #Episode title

    ep_title = driver.find_element(By.XPATH,'//*[@id="mw-content-text"]/div/aside/h2')

    print("Episode title:", ep_title.text)

    #Episode air date
    ep_air_date = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/section[2]/div[3]/div')

    print("Air date:", ep_air_date.text)

    #Episode short summ

    ep_short_sum = driver.find_element(By.XPATH,'//*[@id="mw-content-text"]/div/p[4]')

    print("Short Sum:",ep_short_sum.text)

    #Episode long summ

    ep_long_sum_start = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/p[5]')

    end_header = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/h2[3]')

    paragraphs = []
    current_element = ep_long_sum_start

    while current_element is not None and current_element != end_header:
        
        if current_element.tag_name == 'p':
            paragraphs.append(current_element.text)

        
        try:
            current_element = current_element.find_element(By.XPATH, 'following-sibling::*[1]')
        except Exception as e:
            break

    
    ep_long_sum = "\n".join(paragraphs)  

    
    print("All Paragraphs Text:")
    print(ep_long_sum) 

    #Episode characters

    ep_characters_start = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/div[2]/ul')

    
    li_elements = ep_characters_start.find_elements(By.TAG_NAME, 'li')

    # Extract text from each <li> and store it in the list
    ep_characters = [li.text for li in li_elements]

    # Print the list of characters to verify
    print("Episode Characters:")
    for character in ep_characters:
        print(character)
    



finally:
    driver.quit()
