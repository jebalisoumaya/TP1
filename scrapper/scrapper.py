import requests
from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup

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
        author_img = soup.select_one('div.meta-picture img')
        auteur = author_img['alt'].strip() if author_img and author_img.has_attr('alt') else "Auteur inconnu"
        print(f"Auteur trouvé: {auteur}")
    except Exception as e:
        auteur = "Auteur inconnu"
        print(f"Erreur lors de l'extraction de l'auteur: {e}")

    # Images
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            alt = img.get('alt') or img.get('title') or ''
            images.append({
                "url": src,
                "legende": alt
            })

    return {
        "titre": titre,
        "thumbnail": thumbnail_url,
        "categorie": categorie,
        "sous_categories": sous_categories,
        "resume": resume,
        "date_publication": date_publication,
        "auteur": auteur,
        "images": images,
        "url": url
    }

