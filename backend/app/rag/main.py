
def process_user_query(query: str):
    """
    Accept the query from user and handle routing logic, product search, vector search, response generation and returning the most relevant response

    """

    # Optional for now (11.01.26): route the query (this step can be done later as well)

    pass


def search_products(query: str):
    # create an embedding from query using bedrock
    # extract keywords through an LLM

    # how to combine the products-matched-with-query-embedding and products-matched-with-hard-filters?
    '''
    vector matched products: these might not be within budget, brand, etc. So, maybe apply these hard-filters on them.
        Actually, these filters would be implicitly applied when retrieving these products from the DB.

    keyword matched products: these might not be desirable for user (such undesired products would be filtered out in cross-encoding step)
    '''
    # use mongodb to get the complete info about the products

    # apply cross encoding upon user query and (both) lists
    #   If latency becomes a bottleneck, apply only to the keyword-matched-products.

    # apply RRF to merge the both lists

    pass


def generate_advice(query: str, products: list[dict]):
    # convert the products to a concise format before inserting it to the prompt
    # write a prompt for the consultive LLM so that it advises the user
    # connect to an LLM
    # parse response and stream it back to the user
    pass


if __name__ == '__main__':
    # sample call
    process_user_query("I want a computer that i can use to build ai platorfms") # typo intended.

