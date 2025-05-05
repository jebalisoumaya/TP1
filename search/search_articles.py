from db.mongo_client import get_database

def rechercher_par_categorie(categorie):
    db = get_database()
    collection = db["articles"]
    results = collection.find({"categorie": categorie})
    for art in results:
        print(f"[{art['date_publication']}] {art['titre']} par {art['auteur']}")

if __name__ == "__main__":
    cat = input("Catégorie ou sous-catégorie : ")
    rechercher_par_categorie(cat)
