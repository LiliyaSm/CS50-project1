import requests
from settings import KEY

def goodreads(isbns):
    #get book information using goodreads API

    response = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": KEY, "isbns": isbns})

    result = response.json()["books"][0]
    print(result)
    return result
