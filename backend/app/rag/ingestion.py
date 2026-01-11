import os
import json
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_CONNECTION_STRING = os.environ["MONGO_DB_CONNECTION_STRING"]

def store_products_in_nosql_db(products: list[dict]) -> list[str]:
    # Upsert the json documents into a Nosql db. 
    # return the ids of the stored documents
    mongo_client = pymongo.MongoClient(MONGO_DB_CONNECTION_STRING)

    products_db = mongo_client.products

    all_colls = products_db.list_collection_names()
    print("all_colls: {}".format(all_colls))
    if "products" not in all_colls:
        products_coll = products_db.create_collection("products")
    else:
        products_coll = products_db.get_collection("products")

    products_count_from_coll = products_coll.count_documents({})

    if products_count_from_coll == 0:
        products_coll.insert_many(products)

    products_from_coll = products_coll.find()

    for p in products_from_coll:
        print("product from the db: {}".format(p))


def store_products_in_vector_db(product_ids: list[str]):
    # Utilise primarily product description to generate embedding. But use price, brand, etc. as well. To have at least some reference 'feeling' for the product on those dimensions.
    
    # 1. generate embeddings using => name + description + brand + price
    # 2. store the product_id in the metafield of this document

    pass


def ingest():
    # store the documents first in db
    # then in vector db

    with open("tools/synthetic_shopping_data_xs.jsonl", 'r') as products_f:
        # products = json.load(products_f)
        products = []
        for i, p in enumerate(products_f):
            p_dict = json.loads(p)
            print(p_dict)
            products.append(p_dict)

            if i > 2:
                break

    store_products_in_nosql_db(products)


if __name__ == "__main__":
    ingest()
