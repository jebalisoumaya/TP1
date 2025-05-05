
# TP BeautifulSoup4 - Web Scraping Project

This project is a web scraping application that extracts articles from the Blog du Modérateur website. It uses **BeautifulSoup4** for scraping, **MongoDB** for storing the data, and **Flask** for providing a frontend to display and search the scraped articles.

## Features

1. **Web Scraping**:
   - Scrapes the homepage to extract big categories.
   - Scrapes articles from each category.
   - Extracts the following details from each article:
     - Title
     - Thumbnail image
     - Category and sub-categories
     - Summary
     - Publication date
     - Author
     - Images with captions
     - Full article content

2. **Database Integration**:
   - Saves scraped articles into a MongoDB database.
   - Prevents duplicate entries.

3. **Frontend**:
   - Displays categories and their articles.
   - Allows scraping individual articles.
   - Provides a search interface to filter articles by various criteria.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/tp-beautifulsoup4.git


2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the scraper
    ```bash
      python main.py

4. Start the Flask app:
    ```bash
   python frontend/app.py


   
