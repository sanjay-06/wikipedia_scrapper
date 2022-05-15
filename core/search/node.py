from __future__ import annotations

class Node:
    def __init__(self, link: str, parent: Node):
        self.link = link
        self.parent = parent