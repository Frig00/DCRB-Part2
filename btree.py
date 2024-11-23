import pickle

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
    
    def build_from_file(self, file_path, inverted=False):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                key, values_str = line.strip().split(': ')
                values = list(map(int, values_str.strip('[]').split(', ')))
                if inverted:
                    key = key[::-1]
                self.insert(key, values)
    
    def insert(self, key, values):
        if len(self.root.keys) == (2 * self.degree) - 1:
            new_root = Node()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key, values)
    
    def _insert_non_full(self, node, key, values):
        i = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = values
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.degree) - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, values)
    
    def _split_child(self, parent, i):
        degree = self.degree
        child = parent.children[i]
        new_child = Node(is_leaf=child.is_leaf)

        parent.keys.insert(i, child.keys[degree - 1])
        parent.values.insert(i, child.values[degree - 1])
        parent.children.insert(i + 1, new_child)

        new_child.keys = child.keys[degree:]
        new_child.values = child.values[degree:]
        child.keys = child.keys[:degree - 1]
        child.values = child.values[:degree - 1]

        if not child.is_leaf:
            new_child.children = child.children[degree:]
            child.children = child.children[:degree]

    def save(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.root, file)
        print(f"B-tree saved to {file_path}")


def main():
    file_path = 'inverted_index.txt'  
    degree = 5 

    btree = BTree(degree)
    btree.build_from_file(file_path)
    btree.save('btree.pkl')  

    inverted_btree = BTree(degree)
    inverted_btree.build_from_file(file_path, inverted=True)
    inverted_btree.save('inverted_btree.pkl') 

if __name__ == "__main__":
    main()
