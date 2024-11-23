import pickle
from itertools import chain
from functools import reduce
import json

class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.values = []
        self.children = []

class BTree:
    def __init__(self, degree):
        self.root = Node(is_leaf=True)
        self.degree = degree
    
    @classmethod
    def load(cls, file_path):
        with open(file_path, 'rb') as file:
            btree = cls.__new__(cls)
            btree.root = pickle.load(file)
        return btree
    
    def search(self, key):
        return self._search(self.root, key)
    
    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        elif node.is_leaf:
            return None
        else:
            return self._search(node.children[i], key)

    def search_prefix(self, prefix):
        results = []
        self._search_prefix(self.root, prefix, results)
        return results

    def _search_prefix(self, node, prefix, results):
        i = 0
        while i < len(node.keys):
            if node.keys[i].startswith(prefix):
                results.append((node.keys[i], node.values[i]))
            if node.keys[i] > prefix and not node.is_leaf:
                self._search_prefix(node.children[i], prefix, results)
            i += 1
        if not node.is_leaf:
            self._search_prefix(node.children[i], prefix, results)

    def search_suffix(self, suffix):
        reversed_suffix = suffix[::-1]
        results = []
        self._search_prefix(self.root, reversed_suffix, results)
        return [(key[::-1], values) for key, values in results]

def intersect(lists):
    if not lists:
        return []
    
    sorted_lists = sorted(lists, key=len)    
    return list(reduce(set.intersection, map(set, sorted_lists)))

def union(lists):
    return list(set(chain.from_iterable(lists)))

def parse_query(query):
    if ' AND ' in query:
        return 'AND', query.split(' AND ')
    elif ' OR ' in query:
        return 'OR', query.split(' OR ')
    else:
        return 'SINGLE', [query]

def combine_results(operation, posting_lists):
    if operation == 'AND':
        return intersect(posting_lists)
    elif operation == 'OR':
        return union(posting_lists)
    elif operation == 'SINGLE':
        return posting_lists[0] if posting_lists else []

def handle_wildcard(query, btree, inverted_btree):
    if '*' in query:
        parts = query.split('*')
        if len(parts) == 2:
            prefix, suffix = parts[0], parts[1]
            prefix_results = btree.search_prefix(prefix)
            suffix_results = inverted_btree.search_suffix(suffix)
            matching_words = [key for key, _ in prefix_results if key.endswith(suffix)]
            prefix_postings = union([values for key, values in prefix_results if key.endswith(suffix)])
            suffix_postings = union([values for key, values in suffix_results if key.startswith(prefix)])
            return intersect([prefix_postings, suffix_postings]), matching_words
    return [], []

def load_document_data(file_path):
    with open(file_path, "rb") as file:
        document_data = pickle.load(file)
    return document_data

def main():
    btree_file = 'btree.pkl'
    inverted_btree_file = 'inverted_btree.pkl'
    document_pickle_file_path = 'document_data.pkl'
    
    btree = BTree.load(btree_file)
    inverted_btree = BTree.load(inverted_btree_file)
    document_data = load_document_data(document_pickle_file_path)

    while True:
        print("""Possible queries:
        - Single word query: word
        - Conjunctive query: word1 AND word2
        - Disjunctive query: word1 OR word2
        - Prefix query: prefix*
        - Suffix query: *suffix
        - Wildcard query: prefix*suffix
              """)
        try:
            query = input("Enter a query or press 'Ctrl+C' to quit: ").strip()
        except KeyboardInterrupt:
            break

        operation, words = parse_query(query)

        posting_lists = []
        matching_words = []
        prefix_results = []
        suffix_results = []

        for word in words:
            if word.endswith('*'):
                prefix = word[:-1]
                postings = btree.search_prefix(prefix)
                prefix_results.extend(postings)
                posting_lists.append(union([value for _, value in postings]))
            elif word.startswith('*'):
                suffix = word[1:]
                postings = inverted_btree.search_suffix(suffix)
                suffix_results.extend(postings)
                posting_lists.append(union([value for _, value in postings]))
            elif '*' in word:
                postings, words = handle_wildcard(word, btree, inverted_btree)
                if postings:
                    posting_lists.append(postings)
                matching_words.extend(words)
            else:
                postings = btree.search(word)
                if postings is not None:
                    posting_lists.append(postings)

        try:
            final_result = combine_results(operation, posting_lists)
        except Exception as e:
            final_result = None

        if final_result:
            print(f"Number of documents retrieved for '{query}': {len(final_result)}")
            if prefix_results:
                print(f"Words starting with the prefix:")
                for key, _ in prefix_results:
                    print(f"{key}")
            if suffix_results:
                print(f"Words ending with the suffix:")
                for key, _ in suffix_results:
                    print(f"{key}")
            if matching_words:
                print(f"Words matching the wildcard:")
                for word in matching_words:
                    print(f"{word}")

            print("\nDocuments matching the IDs:")
            for doc_id in final_result:
                if doc_id in document_data:
                    print(f"Document ID: {doc_id}")
                    print(json.dumps(document_data[doc_id], indent=4))
                    print("\n")
        else:
            print(f"No results found for '{query}'.")

if __name__ == "__main__":
    main()
