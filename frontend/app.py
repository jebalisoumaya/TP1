from flask import Flask, render_template, request, redirect, url_for
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapper.scrapper import scrape_categories, scrape_articles_from_category, scrape_article
from scrapper.save_to_db import save_article

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # Scrape the article
            article_data = scrape_article(url)
            # Save the article to the database
            save_article(article_data)
            # Render the result page with the scraped article
            return render_template('search.html', article=article_data)
        except Exception as e:
            return f"❌ Une erreur est survenue : {e}", 400
    return render_template('scrape.html')

@app.route('/', methods=['GET'])
def scrape_categories_route():
    base_url = "https://www.blogdumoderateur.com/"
    try:
        # Scrape categories
        categories = scrape_categories(base_url)
        category_articles = {}
        for category in categories:
            articles = scrape_articles_from_category(category['url'])
            detailed_articles = []
            for article_url in articles:
                try:
                    article_data = scrape_article(article_url)
                    detailed_articles.append({
                        "title": article_data["titre"],
                        "author": article_data["auteur"],
                        "url": article_url
                    })
                except Exception as e:
                    print(f"❌ Failed to scrape article: {e}")
            category_articles[category['name']] = detailed_articles
        return render_template('categories.html', categories=categories, category_articles=category_articles)
    except Exception as e:
        return f"❌ Une erreur est survenue lors du scraping des catégories : {e}", 400

@app.route('/scrape_article', methods=['POST'])
def scrape_article_route():
    article_url = request.form.get('article_url')
    try:
        article_data = scrape_article(article_url)
        save_article(article_data)
        return render_template('search.html', article=article_data)
    except Exception as e:
        return f"❌ Une erreur est survenue lors du scraping de l'article : {e}", 400

if __name__ == '__main__':
    app.run(debug=True)