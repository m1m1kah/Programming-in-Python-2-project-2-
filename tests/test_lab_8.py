import pytest
from Heap import MinHeap
from TreeNode import TreeNode
from TreePrinter import print_tree
from collections import deque
import random


# Build a dictionary of current keys in heap,
# starting at node
def build_key_dict(h):
    key_dict = {}

    def build_key_dict_rec(node):
        if node is None:
            return
        key_dict[node] = node.key
        build_key_dict_rec(node.right)
        build_key_dict_rec(node.left)

    build_key_dict_rec(h.root)
    return key_dict


# Check if node keys have changed:
def check_keys(h, key_dict):
    def check_keys_rec(node):
        if node is None:
            return
        assert key_dict[node] == node.key
        check_keys_rec(node.right)
        check_keys_rec(node.left)
    check_keys_rec(h.root)

def check_heap(h):
    # Check if parent/child links in the heap are consistent
    def check_heap_links(node):
        if node is None:
            return True
        result = True
        if node.left is not None:
            result = result and (node.left.parent is node) and check_heap_links(node.left)
        if node.right is not None:
            result = result and (node.right.parent is node) and check_heap_links(node.right)
        return result

    # Check if each parent's key is at least those of its children
    def check_heap_property(h):
        if h.root is None:
            return True
        def check_heap_property_rec(node):
            result = True
            if node.left is not None:
                result = result and (node.left.key >= node.key) and check_heap_property_rec(node.left)
            if node.right is not None:
                result = result and (node.right.key >= node.key) and check_heap_property_rec(node.right)
            return result
        return check_heap_property_rec(h.root)

    # Check if the size matches the number of elements in the heap
    def check_heap_size(h):
        if h.root is None:
            return len(h) == 0
        def compute_size(node):
            if node is None:
                return 0
            return 1 + compute_size(node.left) + compute_size(node.right)
        return len(h) == compute_size(h.root)

    # Check if the heap is a complete binary tree
    def check_heap_complete(h):
        if h.root is None:
            return True
        q = deque([h.root])
        end = False
        while 0 < len(q):
            cur = q.popleft()
            if cur.left:
                if end:
                    return False
                q.append(cur.left)
            else:
                end = True
            if cur.right:
                if end:
                    return False
                q.append(cur.right)
            else:
                end = True
        return True

    # Run each of the above tests, and assert the result
    assert(check_heap_links(h.root))
    assert(check_heap_size(h))
    assert(check_heap_complete(h))
    assert(check_heap_property(h))

@pytest.fixture
def h():
    h = MinHeap()
    h.root = TreeNode(1,1)
    h.root.left = TreeNode(4,4)
    h.root.right = TreeNode(10,10)
    h.root.left.right = TreeNode(6,6)
    h.root.left.left = TreeNode(8,8)
    h.root.right.left = TreeNode(15,15)
    h.root.right.right = TreeNode(12,12)
    h.root.left.left.left = TreeNode(9,9)
    h.root.left.left.right = TreeNode(13,13)
    h._size = 9
    return h

def test_sift_down_1(h):
    h.root.key = 19
    h.root.value = 19
    d = build_key_dict(h)
    r = h.root
    print("Before")
    print_tree(h.root)
    h._sift_down(h.root)
    print("After")
    print_tree(h.root)
    # Make sure the heap is valid
    check_heap(h)
    # Make sure n has been sifted to correct position
    assert r is h.root.left.right
    # Make sure keys and value have not changed
    check_keys(h, d)

def test_sift_down_2(h):
    h.root.left.key = 3
    h.root.left.value = 3
    d = build_key_dict(h)
    print("Before")
    print_tree(h.root)
    r = h.root
    h._sift_down(h.root)
    print("After")
    print_tree(h.root)
    # Make sure the heap is valid
    check_heap(h)
    # Make sure the root has not been moved
    assert r is h.root
    # Make sure keys have not changed
    check_keys(h, d)

def test_sift_down_3(h):
    h.root.left.key = 7
    h.root.left.value = 7
    d = build_key_dict(h)
    print("Before")
    print_tree(h.root)
    n = h.root.left
    h._sift_down(n)
    print("After")
    print_tree(h.root)
    # Make sure the heap is valid
    check_heap(h)
    # Make sure n has moved to correct position
    assert n is h.root.left.right
    # Make sure keys have not changed
    check_keys(h, d)

def test_sift_down_4(h):
    n = h.root.right.left
    d = build_key_dict(h)
    h._sift_down(n)
    print("Before")
    print_tree(h.root)
    print("After")
    print_tree(h.root)
    check_heap(h)
    # Make sure n has not moved
    assert n is h.root.right.left
    # Make sure keys have not changed
    check_keys(h, d)

def test_sift_down_5(h):
    n = h.root.right
    n.key = 16
    n.value = 16
    d = build_key_dict(h)
    h._sift_down(n)
    print("Before")
    print_tree(h.root)
    print("After")
    print_tree(h.root)
    check_heap(h)
    # Make sure n has moved to correct position
    assert n is h.root.right.right
    # Make sure keys have not changed
    check_keys(h, d)

def test_sift_up_1(h):
    n = h.root.right.left
    n.key = 0
    n.value = 0
    d = build_key_dict(h)
    r = h.root
    n2 = h.root.right
    print("Before")
    print_tree(h.root)
    h._sift_up(n)
    print("After")
    print_tree(h.root)
    check_heap(h)
    # Make sure nodes have been swapped into correct
    # positions
    assert n is h.root
    assert r is n.right
    assert n2 is r.left
    # Make sure keys have not changed
    check_keys(h, d)

def test_sift_up_2(h):
    n = h.root.right.left
    n.key = 15
    n.value = 15
    d = build_key_dict(h)
    print("Before")
    print_tree(h.root)
    h._sift_up(n)
    print("After")
    print_tree(h.root)
    check_heap(h)
    # Make sure n has not moved
    assert n is h.root.right.left
    # Make sure keys have not changed
    check_keys(h, d)

def test_sift_up_3(h):
    n = h.root.left.left
    r = h.root
    n2 = h.root.left
    n.key = 2
    n.value = 2
    d = build_key_dict(h)
    print("Before")
    print_tree(h.root)
    h._sift_up(n)
    print("After")
    print_tree(h.root)
    check_heap(h)
    # Make sure all nodes have swapped correctly
    assert r is h.root
    assert n is h.root.left
    assert n2 is h.root.left.left
    # Make sure keys have not changed
    check_keys(h, d)


def test_sift_up_4(h):
    r = h.root
    d = build_key_dict(h)
    print("Before")
    print_tree(h.root)
    h._sift_up(h.root)
    check_heap(h)
    print("After")
    print_tree(h.root)
    # Make sure root has not moved
    assert r is h.root
    # Make sure keys have not changed
    check_keys(h, d)

def test_get_node_at_1(h):
    print("Heap is:")
    print_tree(h.root)
    print("Getting Node at 4")
    assert h._get_node_at(4) is h.root.left.left

def test_get_node_at_2(h):
    print("Heap is:")
    print_tree(h.root)
    print("Getting Node at 9")
    assert h._get_node_at(9) is h.root.left.left.right

def test_get_node_at_3(h):
    print("Heap is:")
    print_tree(h.root)
    print("Getting Node at 6")
    assert h._get_node_at(6) is h.root.right.left

def test_get_node_at_4(h):
    print("Heap is:")
    print_tree(h.root)
    print("Getting Node at 1")
    assert h._get_node_at(1) is h.root

def test_get_node_at_err1(h):
    print("Heap is:")
    print_tree(h.root)
    print("Getting Node at 0")
    with pytest.raises(KeyError):
        h._get_node_at(0)

def test_get_node_at_err2(h):
    print("Heap is:")
    print_tree(h.root)
    print("Getting Node at 10")
    with pytest.raises(KeyError):
        h._get_node_at(10) 

def test_add_leaf_1(h):
    n = TreeNode(100,100)
    print("Before:")
    print_tree(h.root)
    print("Adding leaf with key 100")
    h._add_leaf(n)
    print("After:")
    print_tree(h.root)
    assert h.root.left.right.left is n

def test_add_leaf_2():
    h = MinHeap()
    n = TreeNode(100,100)
    print("Before: (Empty Heap)")
    print("Adding leaf with key 100")
    h._add_leaf(n)
    print("After:")
    print_tree(h.root)
    assert h.root is n

def test_insert_node_1():
    h = MinHeap()
    d = build_key_dict(h)
    n = TreeNode(10,10)
    d[n] = 10
    print("Before: (Empty Heap)")
    new_node = h.insert_node(n)
    print("After:")
    print_tree(h.root)
    assert len(h) == 1
    assert h.root is n
    assert new_node is n
    # Make sure keys have not changed
    check_keys(h, d)

def test_insert_node_2(h):
    s = len(h)
    print("Before:")
    print_tree(h.root)
    n = TreeNode(11,11)
    d = build_key_dict(h)
    d[n] = 11
    new_node = h.insert_node(n)
    print("After inserting 11:")
    print_tree(h.root)
    assert new_node is n
    assert n is h.root.left.right.left
    assert len(h) == s+1
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_insert_node_3(h):
    s = len(h)
    print("Before:")
    print_tree(h.root)
    n = TreeNode(3,3)
    d = build_key_dict(h)
    d[n] = 3
    new_node = h.insert_node(n)
    print("After inserting 3:")
    print_tree(h.root)
    assert len(h) == s+1
    assert new_node is n
    # Make sure heap is still valid
    check_heap(h)
    # Make sure new node has been sifted into position
    assert n is h.root.left
    # Make sure keys have not changed
    check_keys(h, d)

def test_insert_node_4(h):
    s = len(h)
    print("Before:")
    print_tree(h.root)
    n = TreeNode(0,0)
    d = build_key_dict(h)
    d[n] = 0
    r = h.root
    n2 = h.root.left
    n3 = h.root.left.right
    new_node = h.insert_node(n)
    print("After inserting 0:")
    print_tree(h.root)
    assert len(h) == s+1
    assert new_node is n
    check_heap(h)
    # Make sure node has sifted to the root
    assert h.root is n
    # Make sure other nodes have been swapped correctly
    assert h.root.left is r
    assert h.root.left.right is n2
    assert h.root.left.right.left is n3
    # Make sure keys have not changed
    check_keys(h, d)

def test_insert_1(h):
    s = len(h)
    print("Before:")
    print_tree(h.root)
    d = build_key_dict(h)
    new_node = h.insert(100,"Hello")
    d[new_node] = 100
    print("After inserting 100:")
    print_tree(h.root)
    assert len(h) == s+1
    assert new_node.key == 100
    assert new_node.value == "Hello"
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_insert_2(h):
    s = len(h)
    print("Before:")
    print_tree(h.root)
    new_node = h.insert(3)
    d = build_key_dict(h)
    d[new_node] = 3
    print("After inserting 3:")
    print_tree(h.root)
    assert len(h) == s+1
    assert new_node.key == 3
    assert new_node.value is None
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_insert_3(h):
    s = len(h)
    print("Before:")
    print_tree(h.root)
    new_node = h.insert(0, "Bar")
    d = build_key_dict(h)
    d[new_node] = 0
    print("After inserting 0:")
    print_tree(h.root)
    assert len(h) == s+1
    assert new_node is h.root
    assert new_node.key == 0
    assert new_node.value == "Bar"
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_extract_1(h):
    print("Before:")
    print_tree(h.root)
    d = build_key_dict(h)
    root = h.root
    s = len(h)
    n = h.extract()
    print("After extracting:")
    print_tree(h.root)
    assert n is root
    check_heap(h)
    assert len(h) == s - 1
    root = h.root
    n = h.extract()
    print("After extracting again:")
    print_tree(h.root)
    assert n is root
    check_heap(h)
    assert len(h) == s - 2
    # Make sure keys have not changed
    check_keys(h, d)

def test_extract_2():
    h = MinHeap()
    print("Before: (Empty Heap)")
    print("Trying to extract:")
    with pytest.raises(KeyError):
        h.extract()

def test_delete_1(h):
    print("Before:")
    print_tree(h.root)
    s = len(h)
    n = h.root.left.left
    d = build_key_dict(h)
    del d[n]
    deleted_node = h.delete_node(n)
    print("After deleting: 6")
    print_tree(h.root)
    assert deleted_node == n
    assert len(h) == s-1
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_delete_2(h):
    print("Before:")
    print_tree(h.root)
    s = len(h)
    n = h.root.left.right
    d = build_key_dict(h)
    del d[n]
    deleted_node = h.delete_node(n)
    print("After deleting: 8")
    print_tree(h.root)
    assert deleted_node == n
    assert len(h) == s-1
    check_heap(h)
    d = build_key_dict(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_delete_3(h):
    print("Before:")
    print_tree(h.root)
    s = len(h)
    n = h.root.left.left.right
    d = build_key_dict(h)
    del d[n]
    deleted_node = h.delete_node(n)
    print("After deleting: 13")
    print_tree(h.root)
    assert deleted_node == n
    assert len(h) == s-1
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_delete_4(h):
    print("Before:")
    print_tree(h.root)
    s = len(h)
    n = h.root
    d = build_key_dict(h)
    del d[n]
    deleted_node = h.delete_node(n)
    print("After deleting: 1")
    print_tree(h.root)
    assert deleted_node == n
    assert len(h) == s-1
    check_heap(h)
    # Make sure keys have not changed
    check_keys(h, d)

def test_heap_insert_delete():
    h = MinHeap()
    random.seed(10)
    nodes = []
    d = {}
    for i in range(31):
        d = build_key_dict(h)
        k = random.randint(0,100)
        print(f"Inserting {k}")
        nodes.append(h.insert(k,k))
        d[nodes[-1]] = k
        check_heap(h)
        print(f"Size is {len(h)}")
        print_tree(h.root)
        # Make sure keys have not changed
        check_keys(h, d)
    random.shuffle(nodes)
    for n in nodes:
        print(f"Deleting {n.key}")
        del d[n]
        h.delete_node(n)
        print(f"Size is {len(h)}")
        if len(h) > 0:
            print_tree(h.root)
        check_heap(h)
        check_keys(h, d)

def test_heap_insert_extract():
    h = MinHeap()
    random.seed(10)
    nodes = []
    d = {}
    for i in range(31):
        d = build_key_dict(h)
        k = random.randint(0,100)
        print(f"Inserting {k}")
        nodes.append(h.insert(k,k))
        d[nodes[-1]] = k
        check_heap(h)
        print(f"Size is {len(h)}")
        print_tree(h.root)
        check_keys(h, d)
    results = []
    while len(h) > 0:
        n = h.extract()
        print(f"Extracted {n}")
        del d[n]
        results.append(n.key)
        print_tree(h.root)
        print(f"Size is {len(h)}")
        check_keys(h, d)
    assert results == sorted([n.key for n in nodes])
