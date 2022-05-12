from heuristic import gen_links, get_best_class, get_utility, LemmaTokenizer, text_from_html
from threading import Thread
from urllib import request
import time

link_texts = []


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_text(link):
    html = request.urlopen(link).read()
    text = [text_from_html(html)]
    link_texts.append((link, text))
    print(f"Fetched webpage {len(link_texts)}")
    

def gen_link_texts(links):
    for link in links:
        get_text(link)


def search(source, target):
    target_class = get_best_class(target)

    current_page = source
    unexplored_pages = []

    visited_pages = set()

    while True:
        print(f"At page {current_page[current_page.rindex('/') : ]}")
        links = [link for link in gen_links(current_page) if link not in visited_pages]
        print(f"Number of links: {len(links)}")
        if target in links:
            print("Reached target")
            break
        
        link_texts.clear()
        threads = []
        for chunk in chunks(links, 30):
            t = Thread(target=gen_link_texts, args=(chunk,))
            t.start()
            threads.append(t)
        
        print(f"Started {len(threads)} threads")
        t = time.time()

        for thread in threads:
            thread.join()
        
        print("Threads done")
        print(time.time() - t)

        link_utilities = [(link, get_utility(text, target_class)) for link, text in link_texts]
        unexplored_pages.extend(link_utilities)
        unexplored_pages.sort(key=lambda x: x[1], reverse=True)

        print(f"{len(unexplored_pages)} unexplored pages")
        print(unexplored_pages[:5])
        visited_pages.add(current_page)
        current_page, _ = unexplored_pages.pop(0)
        
    
        

if __name__ == "__main__":
    SOURCE = "https://en.wikipedia.org/wiki/Metal"
    TARGET = "https://en.wikipedia.org/wiki/Microsoft"

    print(len(gen_links(SOURCE)))

    search(SOURCE, TARGET)