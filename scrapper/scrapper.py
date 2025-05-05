import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_categories(base_url):
    print(f"🔗 Scraping categories from: {base_url}")
    response = requests.get(base_url)
    if response.status_code != 200:
        raise Exception(f"Erreur de requête : {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all big categories
    categories = []
    category_links = soup.select('ul#primary-menu a.nostyle.t-menu')  # Updated selector
    print(f"Found {len(category_links)} category links.")  # Debugging log
    for link in category_links:
        category_name = link.get_text(strip=True)
        category_url = urljoin(base_url, link['href'])
        print(f"Category: {category_name}, URL: {category_url}")  # Debugging log
        categories.append({"name": category_name, "url": category_url})

    return categories

def scrape_articles_from_category(category_url):
    print(f"🔗 Scraping articles from category: {category_url}")
    response = requests.get(category_url)
    if response.status_code != 200:
        raise Exception(f"Erreur de requête : {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article links in the category
    articles = []
    article_links = soup.select('article a')  # Adjust selector based on the site's structure
    for link in article_links:
        article_url = urljoin(category_url, link['href'])
        articles.append(article_url)

    return articles

def scrape_article(url):
    print(f"🔗 Scraping URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erreur de requête : {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Titre
    titre_tag = soup.find('h1', class_='entry-title')  
    titre = titre_tag.get_text(strip=True) if titre_tag else None

    # Image principale
    thumbnail = soup.find('meta', property='og:image')
    thumbnail_url = thumbnail['content'] if thumbnail else None

    # Catégorie
    categorie_tag = soup.find('a', class_='nostyle t-menu')  
    categorie = categorie_tag.get_text(strip=True) if categorie_tag else "Catégorie inconnue"

    # Sous-catégories
    sous_categories = [div.get_text(strip=True) for div in soup.find_all('div', class_='favtag mb-1')]
    sous_categories = list(set(sous_categories))  # Remove duplicates

    # Résumé
    resume_elem = soup.find('div', class_='article-hat t-quote pb-md-8 pb-5')
    resume = resume_elem.get_text(strip=True) if resume_elem else None

    # Date
    date_tag = soup.find('time')
    date_publication = date_tag['datetime'][:10] if date_tag and 'datetime' in date_tag.attrs else None

    # Auteur
    try:
        author_section = soup.find('div', class_='article-social-content pb-md-7 pb-5 d-md-flex justify-content-md-between align-items-center text-start')
        if author_section:
            # Extract author's profile picture
            author_img_tag = author_section.find('div', class_='meta-picture').find('img')
            author_profile_pic = author_img_tag['src'] if author_img_tag else None

            # Extract author's name
            author_name_tag = author_section.find('span', class_='byline').find('a')
            auteur = author_name_tag.get_text(strip=True) if author_name_tag else "Auteur inconnu"
        else:
            auteur = "Auteur inconnu"
            author_profile_pic = None

        print(f"Auteur trouvé: {auteur}, Profile Picture: {author_profile_pic}")
    except Exception as e:
        auteur = "Auteur inconnu"
        author_profile_pic = None
        print(f"Erreur lors de l'extraction de l'auteur: {e}")

    # Images
    images = []
    article_tag = soup.find('article')  # Locate the <article> tag
    if article_tag:
        for img in article_tag.find_all('img'):  # Find all <img> tags within the article
            src = img.get('src') or img.get('data-src')
            if src:
                alt = img.get('alt') or img.get('title') or ''
                images.append({
                    "url": src,
                    "legende": alt
                })

    body_content = ""
    body_div = soup.find('div', class_='entry-content row justify-content-center')
    if body_div:
        paragraphs = body_div.find_all(['p', 'h2', 'blockquote', 'ol', 'ul'])
        body_content = "\n".join([p.get_text(strip=True) for p in paragraphs])

    return {
        "titre": titre,
        "thumbnail": thumbnail_url,
        "categorie": categorie,
        "sous_categories": sous_categories,
        "resume": resume,
        "date_publication": date_publication,
        "auteur": auteur,
        "images": images,
         "body_content": body_content,

        "url": url
    }