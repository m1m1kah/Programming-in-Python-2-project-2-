import pytest
from BinarySearchTree import BinarySearchTree
from TreeNode import TreeNode
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
def bst():
    """Creates a new Binary Search Tree for testing."""
    tree = BinarySearchTree()
    return tree

@pytest.fixture
def bst_15():
    b = BinarySearchTree()
    b.root = TreeNode(6, "Six")
    b.root.left = TreeNode(5, "Five")
    b.root.left.left = TreeNode(2, "Two")
    b.root.left.left.left = TreeNode(1, "One")
    b.root.left.left.right = TreeNode(3, "Three")
    b.root.left.left.right.right = TreeNode(4, "Four")
    b.root.right = TreeNode(8, "Eight")
    b.root.right.left = TreeNode(7, "Seven")
    b.root.right.right = TreeNode(14, "Fourteen")    
    b.root.right.right.left = TreeNode(13, "Thirteen")    
    b.root.right.right.left.left = TreeNode(9, "Nine")    
    b.root.right.right.left.left.right = TreeNode(11, "Eleven")    
    b.root.right.right.left.left.right.left = TreeNode(10, "Ten")    
    b.root.right.right.left.left.right.right = TreeNode(12, "Twelve")    
    b.root.right.right.right = TreeNode(15, "Fifteen")    
    return b

def test_insert(bst):
    """Test inserting values into the BST."""
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)
    
    assert bst.root.key == 10
    assert bst.root.left.key == 5
    assert bst.root.right.key == 15

def test_search(bst):
    """Test searching for values in the BST."""
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)
    
    assert bst.search(10) is not None
    assert bst.search(5) is not None
    assert bst.search(15) is not None
    with pytest.raises(KeyError): 
        bst.search(20) 

@pytest.mark.parametrize("d", [4,3,5,2,8,6])
def test_delete(bst_15, d):
    """Test deleting a leaf node (key 4) from the BST."""
    bst_15.delete(d)
    assert has_been_deleted(bst_15, d)
    assert satisfies_bst_property(bst_15)
    assert len(__inorder(bst_15.root)) == 14

def test_delete_root_1(bst):
    """Test deleting a node from the BST."""
    n3 = TreeNode(3, "Three")
    n1 = TreeNode(1, "One")
    n2 = TreeNode(2, "Two")
    bst.root = n3
    bst.root.left = n1
    bst.root.left.right = n2
    bst.delete(3)
    assert bst.root is n1
    assert bst.root.right is n2
    assert bst.root.left is None

def test_delete_root_2(bst):
    """Test deleting a node from the BST."""
    n3 = TreeNode(3, "Three")
    n1 = TreeNode(1, "One")
    n2 = TreeNode(2, "Two")
    bst.root = n1
    bst.root.right = n2
    bst.root.right.right = n3
    bst.delete(1)
    assert bst.root is n2
    assert bst.root.right is n3
    assert bst.root.left is None

def test_range_query_mid(bst_15):
    """Test range query in the BST."""
    
    result = range_query(bst_15,5, 7)
    assert result == [(5, "Five"), (6, "Six"), (7, "Seven")]

def test_range_query_low(bst_15):
    """Test range query in the BST."""
    
    result = range_query(bst_15,-3, 4)
    assert result == [(1, "One"), (2, "Two"), (3, "Three"), (4, "Four")]

def test_range_query_high(bst_15):
    """Test range query in the BST."""
    
    result = range_query(bst_15,12, 20)
    assert result == [(12, "Twelve"), (13, "Thirteen"), (14, "Fourteen"), (15, "Fifteen")]

def test_range_query_empty_tree(bst):
    assert range_query(bst,1, 10) == []

def test_range_query_empty_result(bst):
    bst.root = TreeNode(1, "Foo")
    bst.root.right = TreeNode(10, "Bar")
    bst.root.left = TreeNode(-1, "Hello")
    bst.root.right.right = TreeNode(11, "World")
    assert range_query(bst,3, 7) == []

def test_get_value(bst_15):
    """Test retrieving a value associated with a key."""
    
    assert bst_15.get_value(10) == "Ten"
    assert bst_15.get_value(5) == "Five"
    assert bst_15.get_value(15) == "Fifteen"
    with pytest.raises(KeyError):
        bst_15.get_value(20)
