def wiki_page_filter(url: str) -> bool:
    return url.startswith('/wiki')

def special_link_filter(url: str) -> bool:
    return ':' not in url

def intra_link_filter(url: str) -> bool:
    return '#' not in url

def main_page_filter(url: str) -> bool:
    return url != '/wiki/Main_Page'

link_filters = [
    wiki_page_filter,
    special_link_filter,
    intra_link_filter,
    main_page_filter
]