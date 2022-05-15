from os import stat
from bs4 import BeautifulSoup
from bs4.element import Comment
from typing import List
import concurrent.futures
from config import Config
import time
import lxml
import cchardet

WIKIPEDIA_PREFIX = "https://en.wikipedia.org"

class Parser:
    @staticmethod
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    @staticmethod
    def parse_html_text(html):
        soup = BeautifulSoup(html, 'lxml')
        texts = soup.findAll(text=True)
        visible_texts = filter(Parser.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    
    @staticmethod
    def parse_html_list_text_concurrent(html_list):
        text_results = [None] * len(html_list)

        t = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=Config.THREAD_COUNT) as executor:
            future_index_dict = {}
            
            print("Before loop")
            for index, html in enumerate(html_list):
                execute_future = executor.submit(Parser.parse_html_text, html) 
                future_index_dict[execute_future] = index

            count = 0
            print("Initialized parsers")
            for future in concurrent.futures.as_completed(future_index_dict):
                print(f"Parsed {count}")
                count += 1
                index = future_index_dict[future]
                try:
                    data = future.result()
                    text_results[index] = data
                except Exception as exc:
                    print(f'{index} generated an exception: {exc}')

        
        print(f"{len(text_results)} pages parsed in {time.time() - t} seconds")

        return text_results

    
    @staticmethod
    def parse_html_links(html, link_filters: List[callable]) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        link_results = set()

        for link_element in links:
            if not link_element.has_attr('href'):
                continue
            
            link = link_element['href']
            
            valid_link = True
            for link_filter in link_filters:
                if not link_filter(link):
                    valid_link = False
                    break
            
            if valid_link and link not in link_results:
                link_results.add(WIKIPEDIA_PREFIX + link)

        return list(link_results)
