class Node:
    def __init__(self, domain, i, j):
        self.domain = domain  # List of integers representing the domain
        self.original_domain = domain.copy()
        self.i = i  # Row index
        self.j = j  # Column index

    def __repr__(self):
        return f"Node(i={self.i}, j={self.j}), domain={self.domain}"