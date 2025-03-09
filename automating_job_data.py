from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Keep browser open

driver = webdriver.Chrome(options=chrome_options)

driver.get('WEBSITE') #enter the site you want to run this script on

# Login
enter_email = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@type="email"]'))
)
enter_email.send_keys('EMAIL LOGIN TO SITE') #enter your login name or email for site
enter_email.send_keys(Keys.ENTER)

enter_password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))
)
enter_password.send_keys('PASSWORD LOGIN TO SITE') #enter your login password for site
enter_password.send_keys(Keys.ENTER)

# Search for jobs
search_bar = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@type="text"]'))
)
search_bar.send_keys('AWS Cloud Engineer')
search_bar.send_keys(Keys.ENTER)

# Apply filters
filters = [
    '//*[@id="facets"]/dhi-accordion[1]/div[2]/div/js-single-select-filter/div/div/button[4]',  # Posted Date
    '//*[@id="facets"]/dhi-accordion[2]/div[2]/div/js-multi-select-filter/div/ul/li[1]/span/button/i',  # Employment Type
    '//*[@id="facets"]/dhi-accordion[4]/div[2]/div/js-multi-select-filter/div/ul/li[1]/span/button/i',  # Employer Type
    '//*[@id="facets"]/dhi-accordion[5]/div[2]/div/js-multi-select-filter/div/ul/li[2]/span/button/i'  # Work Setting
]

for xpath in filters:
    try:
        filter_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        filter_element.click()
    except Exception as e:
        print(f"⚠️ Skipping filter: {xpath} due to error: {e}")

# Navigate to jobs page
url = "https://www.dice.com/jobs?q=AWS%20Cloud%20Engineer&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=10&filters.postedDate=SEVEN&filters.workplaceTypes=Remote&filters.employmentType=FULLTIME&filters.employerType=Direct%20Hire&language=en"
driver.get(url)

# Extract jobs
jobs = {}

# Wait for job cards to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[@data-cy='card-title-link']"))
)

job_cards = driver.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")

for i, job in enumerate(job_cards):
    try:
        title = job.text.strip() if job.text else "❌ No title found"
        
        # Click the job link
        job.click()
        
        # Switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        
        # Wait for job details to load
        time.sleep(3)  # Adjust as needed

        # Extract job summary
        try:
            summary_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'job-description')]"))
            )
            summary = summary_element.text.strip() if summary_element.text else "❌ No summary found"
        except:
            summary = "❌ No summary found"

        # Store in dictionary
        jobs[title] = summary

        # Close job tab and switch back
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"⚠️ Error extracting job {i + 1}: {e}")
        continue

# Print results
print(f"\n✅ Total Jobs Extracted: {len(jobs)}")
for title, summary in jobs.items():
    print(f"\n📝 Job Title: {title}\n📌 Summary: {summary}\n" + "-" * 60)
