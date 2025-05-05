from scrapper.scrapper import scrape_article
from scrapper.save_to_db import save_article

def main():
    print("🔍 Entrez l'URL d’un article du Blog du Modérateur à scraper :")
    url = "https://www.blogdumoderateur.com/duolingo-ia-concurrence-google/"

    try:
        print("\n⏳ Récupération des données en cours...")
        article_data = scrape_article(url)
        print("📄 Article extrait avec succès :")
        print(f"  - Titre : {article_data['titre']}")
        print(f"  - Auteur : {article_data['auteur']}")
        print(f"  - Date de publication : {article_data['date_publication']}")
        print(f"  - Catégorie : {article_data['categorie']}")
        print(f"  - Nb images : {len(article_data['images'])}")
        print(f"  - Résumé : {article_data['resume']}")
        print(f"  - URL : {article_data['url']}")   
        print(f"  - Thumbnail : {article_data['thumbnail']}")
        print(f"  - Sous-catégories : {', '.join(article_data['sous_categories'])}")

        save_article(article_data)

    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()
