from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pymongo import MongoClient
from flask import Flask, jsonify, render_template
import uuid
from datetime import datetime
import time

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["stir_tech"]
collection = db["twitter_trends_db"]

PROXY = "in.proxymesh.com:31280"
# us-ca.proxymesh.com:31280

# Twitter credentials
TWITTER_USERNAME =  "your_twitter_username" # Replace with your Twitter username/email
TWITTER_EMAIL = "your_twitter_email" # Replace with your Twitter username/email
TWITTER_PASSWORD = "your_twitter_password" # "your_password"  # Replace with your Twitter password


def get_trending_topics():
    options = webdriver.ChromeOptions()
    
    options.add_argument("--start-maximized")
    options.add_argument(f"--proxy-server=http://{PROXY}")

    # Launch Selenium browser
    driver = webdriver.Chrome(options=options)

    driver.get("https://twitter.com/login")

    time.sleep(20)

    try:
        # Log in to Twitter
        driver.find_element(By.NAME, "text").send_keys(TWITTER_USERNAME)
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()
        time.sleep(10)  # Wait for next page to load

        driver.find_element(By.NAME, "text").send_keys(TWITTER_EMAIL)
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()
        time.sleep(10)  # Wait for next page to load

        driver.find_element(By.NAME, "password").send_keys(TWITTER_PASSWORD)
        driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
        time.sleep(25)  # Wait for login to complete

        xpaths = [
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div[4]/div/div/div/div[2]/span",
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div[5]/div/div/div/div[2]/span",
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div[6]/div/div/div/div[2]/span",
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div[7]/div/div/div/div[2]/span",
        ]

        # Initialize an empty list to store all the elements
        trending = []
        trending_text = []

        # Loop through each XPath and find elements
        for xpath in xpaths:
            elements = driver.find_elements(By.XPATH, xpath)
            trending.extend(elements)  # Add the found elements to the list

        for element in trending:
            trending_text.append(element.text)


        print(trending_text)

        # Fetch the proxy IP
        driver.get("https://api.ipify.org/")
        time.sleep(5)

        ip_element = driver.find_element(By.TAG_NAME, "pre")
        proxy_ip = ip_element.text

    except Exception as e:
        print(f"Error fetching trends: {e}")
        driver.quit()
        return None

    driver.quit()

    # Save to MongoDB
    record = {
        "_id": str(uuid.uuid4()),
        "nameoftrend1": trending_text[0] if len(trending_text) > 0 else None,
        "nameoftrend2": trending_text[1] if len(trending_text) > 1 else None,
        "nameoftrend3": trending_text[2] if len(trending_text) > 2 else None,
        "nameoftrend4": trending_text[3] if len(trending_text) > 3 else None,
        # "trend5": trends[4] if len(trends) > 4 else None,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": proxy_ip,
    }
    collection.insert_one(record)
    return record


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run_script", methods=["GET"])
def run_script():
    record = get_trending_topics()
    if record:
        return jsonify(record)
    return jsonify({"error": "Failed to fetch trends please try again"})


if __name__ == "__main__":
    app.run(debug=True)
