from db.mongo_client import get_database

def save_article(article_data):
    db = get_database()
    collection = db["articles"]
    existing = collection.find_one({"url": article_data["url"]})
    if existing:
        print("ℹ️ L'article existe déjà dans la base.")
    else:
        collection.insert_one(article_data)
        print("✅ Article enregistré avec succès.")
