from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup

# Browser options
options = Options()
# options.add_argument("--headless")  # Browser works in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
options.add_argument("accept-language=en-US,en;q=0.9")


# Start Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250&lang=en-US"  #top 250 movies url
# url = "https://www.imdb.com/chart/moviemeter/?ref_=tt_ov_pop"  #popular movies url

#  Open the URL
driver.get(url)


# Parsing the source to Beautifulsoup for scraping
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find the UL list  (UL is for finding the list of movies)
metadata_list = soup.find("ul", class_="ipc-metadata-list")

# Find the LI list (LI is for finding the movie)
movieUrls = metadata_list.find_all("a", class_="ipc-title-link-wrapper")


# To go to the review page we need base url
baseUrl = "https://www.imdb.com"

# If there is a movie list
if metadata_list:
    # For each movie add the review page to the url
    for url in movieUrls:
        urlSplit = url.get("href").split("/")
        reviewUrl = "/".join(urlSplit[0:3]) + "/reviews"

        driver.get(baseUrl + reviewUrl)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Click the see all button to see all reviews, we put sleep for waiting the page to load
        seeAllButton = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "chained-see-more-button")))
        sleep(2)
        seeAllButton[0].click()
        
        # Scroll down to load more comments 
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)

        print("Scrolling is done")

        # Get the comments
        sleep(5)
        commentDiv = driver.page_source
        commentSoup = BeautifulSoup(commentDiv, "html.parser")
        commentList = commentSoup.find_all("div", class_="ipc-html-content-inner-div")[:500] # (max 500 comments allowed)
        print("Count of th comments: " + str(len(commentList)))
      

        # Print the comments (we add new comment and * for seperation)
        for review in commentList:
            print("new comment")

            print("*" * 50)
            print(review.text.strip())
            print("*" * 50)
            print("\n")

# Controll for no movie list
else:
    print("There is no Movie list element in the page")

# stopping the driver after finishing the process
driver.quit()
