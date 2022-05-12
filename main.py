from heuristic import gen_links, get_best_class, get_utility, LemmaTokenizer

def search(source, target):
    target_class = get_best_class(target)

    current_page = source
    unexplored_pages = []
    while True:
        print(f"At page {current_page[current_page.rindex('/') : ]}")
        links = gen_links(current_page)
        if target in links:
            print("Reached target")
            break

        links = [(link, get_utility(link, target_class)) for link in links]
        unexplored_pages.extend(links)
        unexplored_pages.sort(key=lambda x: x[1], reverse=True)
        
    
        

if __name__ == "__main__":
    SOURCE = "https://en.wikipedia.org/wiki/Telecommunications"
    TARGET = "https://en.wikipedia.org/wiki/Google"

    search(SOURCE, TARGET)