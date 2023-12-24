import pymongo 
from dotenv import load_dotenv, find_dotenv
import os
import requests
load_dotenv(find_dotenv())

MONGO_URI=os.environ.get("MONGO_URI")
hf_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN")

client = pymongo.MongoClient(MONGO_URI)
db = client.sample_mflix
collection = db.movies

# Not using 

embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

# Generate embedding with Hugging face sentence transformer
def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text},
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed with code {response.status_code}, {response.text}")
    return response.json()
    


# Storing embedding into oiriginal collection
for doc in collection.find({'plot':{'$exists': True}}).limit(10):
    doc['plot_embedding'] = generate_embedding(doc['plot'])
    collection.replace_one({'_id': doc['_id']}, doc)
    

    