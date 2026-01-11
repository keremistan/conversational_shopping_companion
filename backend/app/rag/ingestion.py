
def store_products_in_nosql_db(products: list[dict]) -> list[str]:
    # Store the json documents into a Nosql db. 
    # return the ids of the stored documents

    pass


def store_products_in_vector_db(product_ids: list[str]):
    # Utilise primiarily product description to generate embedding. But use price, brand, etc. as well. To have at least some reference 'feeling' for the product on those dimensions.

    pass


def ingest(products: list[dict]):
    # store the documents first in db
    # then in vector db

    pass
