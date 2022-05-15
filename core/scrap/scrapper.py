import concurrent.futures
from typing import List
from config import Config
import requests

import time
import cchardet

class Scrapper:
    requests_session = requests.Session()
    @staticmethod
    def load_page(page_link: str, timeout: int = 10):
        resp = Scrapper.requests_session.get(page_link, timeout=timeout)
        return resp.text

    
    # @staticmethod
    # def load_page_parse(page_link: str, timeout: int = 10):
    #     resp = Scrapper.requests_session.get(page_link, timeout=timeout)
    #     from .parser import Parser
    #     return Parser.parse_html_text(resp.text)


class ConcurrentScrapper:
    @staticmethod
    def load_pages_concurrent(page_links: List[str]):

        html_results = [None] * len(page_links)

        t = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=Config.THREAD_COUNT) as executor:
            future_index_dict = {}
            
            for index, page_link in enumerate(page_links):
                execute_future = executor.submit(Scrapper.load_page, page_link, Config.URL_LOAD_TIMEOUT) 
                # execute_future = executor.submit(Scrapper.load_page_parse, page_link, Config.URL_LOAD_TIMEOUT) 

                future_index_dict[execute_future] = index

            count = 0
            for future in concurrent.futures.as_completed(future_index_dict):
                print(f"Loaded {count}")
                count += 1
                index = future_index_dict[future]
                try:
                    data = future.result()
                    html_results[index] = data
                except Exception as exc:
                    print(f'{index} generated an exception: {exc}')
    

        print(f"{len(html_results)} pages loaded in {time.time() - t} seconds")

        return html_results