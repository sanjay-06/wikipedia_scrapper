from core.search.tokenizer import LemmaTokenizer
from core.search.search import search

    
if __name__ == "__main__":

    SOURCE = "https://en.wikipedia.org/wiki/Wikipedia:Very_short_featured_articles"
    TARGET = "https://en.wikipedia.org/wiki/Google"

    print(search(SOURCE, TARGET))