# Twitter Trends Scraper

This project is a Flask web application that scrapes trending topics from Twitter using Selenium, stores the results in MongoDB, and displays them on a web page.

## Features

- Scrape trending topics from Twitter.
- Store the scraped data in a MongoDB database.
- Display the trending topics along with the query's proxy IP address on a web page.

## Prerequisites

- Python 3.8+
- Google Chrome browser
- ChromeDriver compatible with your Chrome version
- MongoDB server running locally or remotely
- Proxy Mesh account:
  - Ensure your local system IP is whitelisted in Proxy Mesh settings.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-trends-scraper.git
cd twitter-trends-scraper
```

### 2. Install Dependencies

Use the `requirements.txt` file to install the required Python libraries:

```bash
pip install -r requirements.txt
```

### 3. Set Up MongoDB

Ensure MongoDB is running locally or update the connection string in the code if using a remote server.

### 4. Set Up ChromeDriver

- Download ChromeDriver for your Chrome version.
- Place the ChromeDriver executable in a directory included in your system's PATH or update the `webdriver.Chrome()` call to include the executable's path.

### 5. Update Twitter Credentials

Replace `your_twitter_username`, `your_twitter_email`, and `your_twitter_password` in the script with your actual Twitter credentials.

### 6. Update Proxy

- Replace `PROXY` with a working proxy address.
- Ensure your local system IP is whitelisted in Proxy Mesh settings.

## Usage

### 1. Run the Flask Application

Start the Flask app by running:

```bash
python app.py
```

The application will run on `http://127.0.0.1:5000`.

### 2. Access the Web Application

- Open a browser and navigate to `http://127.0.0.1:5000`.
- Click the "Click here to run the script" button to scrape Twitter trends.

### 3. View the Results

- The trending topics and proxy IP address will be displayed on the web page.
- Data is also stored in the `twitter_trends_db` collection in MongoDB.

## File Structure

```
├── app.py                # Main application script
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Web page template
├── README.md             # Project documentation
```

## Dependencies

The following Python libraries are required:

- `selenium`: For browser automation.
- `pymongo`: To connect and interact with MongoDB.
- `Flask`: For building the web application.