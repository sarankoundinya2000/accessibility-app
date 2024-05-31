import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from axe_selenium_python import Axe
import time

# Configure headless Chrome
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Function to perform accessibility analysis using Selenium and Axe
def analyze_accessibility(url):
    driver = get_driver()
    try:
        # Load the web page in the browser
        driver.get(url)
        time.sleep(2)  # Wait for the page to fully load

        # Inject Axe accessibility testing script and run checks
        axe = Axe(driver)
        axe.inject()
        results = axe.run()

        # Check if any violations are found
        if results['violations']:
            # Display detected accessibility issues to the user
            st.write("Accessibility issues detected:")
            for violation in results['violations']:
                st.write(f"- {violation['description']}")
                st.write("  Tags with issues:")
                for node in violation['nodes']:
                    st.write(f"    - HTML Tag: {node['html']}")

        else:
            # No accessibility issues found
            st.write("No accessibility issues detected.")

    except Exception as e:
        st.write(f"Error analyzing accessibility: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Streamlit UI
st.title('Accessibility Issue Detector')

prompt = st.text_input('Enter prompt:')
url = st.text_input('Enter URL:', 'http://example.com')
if st.button('Check Accessibility'):
    if url:
        st.write(f"Prompt: {prompt}")
        st.write(f"Analyzing accessibility issues for URL: {url}")
        analyze_accessibility(url)
    else:
        st.write("Please enter a valid URL.")
