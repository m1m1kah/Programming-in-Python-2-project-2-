import pytest
from AVLTree import AVLTree, AVLNode 
from BST import range_query

def __inorder(n):
    l = [] if n.left is None else __inorder(n.left)
    r = [] if n.right is None else __inorder(n.right)
    return l + [(n.key, n.value)] + r

def satisfies_bst_property(t):
    l = __inorder(t.root)
    return sorted(l) == l

def has_been_deleted(t, k):
    return k not in [v[0] for v in __inorder(t.root)]

@pytest.fixture
def avl():
    """Creates a new Binary Search Tree for testing."""
    tree = AVLTree()
    return tree

@pytest.fixture
def avl_15():
    b = AVLTree()
    b.root = AVLNode(6, "Six")
    b.root.left = AVLNode(5, "Five")
    b.root.left.left = AVLNode(2, "Two")
    b.root.left.left.left = AVLNode(1, "One")
    b.root.left.left.right = AVLNode(3, "Three")
    b.root.left.left.right.right = AVLNode(4, "Four")
    b.root.right = AVLNode(8, "Eight")
    b.root.right.left = AVLNode(7, "Seven")
    b.root.right.right = AVLNode(14, "Fourteen")    
    b.root.right.right.left = AVLNode(13, "Thirteen")    
    b.root.right.right.left.left = AVLNode(9, "Nine")    
    b.root.right.right.left.left.right = AVLNode(11, "Eleven")    
    b.root.right.right.left.left.right.left = AVLNode(10, "Ten")    
    b.root.right.right.left.left.right.right = AVLNode(12, "Twelve")    
    b.root.right.right.right = AVLNode(15, "Fifteen")    
    return b



def test_range_query_mid(avl_15):
    """Test range query in the BST."""
    
    result = range_query(avl_15,5, 7)
    assert result == [(5, "Five"), (6, "Six"), (7, "Seven")]

def test_range_query_low(avl_15):
    """Test range query in the BST."""
    
    result = range_query(avl_15,-3, 4)
    assert result == [(1, "One"), (2, "Two"), (3, "Three"), (4, "Four")]

def test_range_query_high(avl_15):
    """Test range query in the BST."""
    
    result = range_query(avl_15,12, 20)
    assert result == [(12, "Twelve"), (13, "Thirteen"), (14, "Fourteen"), (15, "Fifteen")]

def test_range_query_empty_tree(avl):
    assert range_query(avl,1, 10) == []

def test_range_query_empty_result(avl):
    avl.root = AVLNode(1, "Foo")
    avl.root.right = AVLNode(10, "Bar")
    avl.root.left = AVLNode(-1, "Hello")
    avl.root.right.right = AVLNode(11, "World")
    assert range_query(avl,3, 7) == []
