from core.scrap.scrapper import ConcurrentScrapper
from core.search.classifier import Classifier
from core.scrap import Scrapper, Parser, ConcurrentScrapper
from core.scrap import link_filters
import time

def search(source, target):
    target_class = Classifier.predict_class(target)

    current_page = source
    unexplored_pages = []

    visited_pages = set()

    while True:
        print(f"At page {current_page[current_page.rindex('/') : ]}")
        current_page_html = Scrapper.load_page(current_page)
        links = [link for link in Parser.parse_html_links(current_page_html, link_filters.link_filters) if link not in visited_pages]
        print(f"Number of links: {len(links)}")
        if target in links:
            print("Reached target")
            break
        
        links_html = ConcurrentScrapper.load_pages_concurrent(links)
        print("Something")

        t = time.time()
        print("Started parsing")
        links_text = [Parser.parse_html_text(html) for html in links_html]
        print(f"Parsed {len(links_text)} pages in {time.time() - t} seconds")

        print("Parsed HTML text")
        
        links_utilities = Classifier.get_utilities(links_text, target_class)
        for link, utility in zip(links, links_utilities):
            unexplored_pages.append((link, utility))
        
        unexplored_pages.sort(key=lambda x: x[1], reverse=True)

        print(f"{len(unexplored_pages)} unexplored pages")
        print(unexplored_pages[:5])
        visited_pages.add(current_page)
        current_page, _ = unexplored_pages.pop(0)


