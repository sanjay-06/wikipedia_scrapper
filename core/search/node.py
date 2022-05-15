from __future__ import annotations

class Node:
    def __init__(self, link: str, parent: Node):
        self.link = link
        self.parent = parent
    
    def __hash__(self):
        return hash(self.link)
    
    def __eq__(self, other):
        return self.link == other.link