import streamlit as st
from selenium import webdriver
from axe_selenium_python import Axe
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Function to perform accessibility analysis using Selenium and Axe
def analyze_accessibility(url):
    try:
        # Load the web page in the browser
        driver.get(url)
        time.sleep(2)  # Wait for the page to fully load

        # Inject Axe accessibility testing script and run checks
        axe = Axe(driver)
        axe.inject()
        results = axe.run()

        # Check if any violations are found
        violations = results.get('violations', [])
        if violations:
            # Display detected accessibility issues and corresponding HTML tags to the user
            st.write("Accessibility issues detected:")
            for violation in violations:
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
