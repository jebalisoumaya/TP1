from scrapper.scrapper import scrape_categories, scrape_articles_from_category, scrape_article
from scrapper.save_to_db import save_article

def main():
    base_url = "https://www.blogdumoderateur.com/"
    print("⏳ Scraping categories...")
    categories = scrape_categories(base_url)

    for category in categories:
        print(f"\n📂 Category: {category['name']}")
        try:
            articles = scrape_articles_from_category(category['url'])
            for article_url in articles:
                print(f"  🔗 Scraping article: {article_url}")
                try:
                    article_data = scrape_article(article_url)
                    save_article(article_data)
                except Exception as e:
                    print(f"    ❌ Failed to scrape article: {e}")
        except Exception as e:
            print(f"❌ Failed to scrape category: {e}")

if __name__ == "__main__":
    main()