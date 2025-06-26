import pytest
import importlib

@pytest.fixture
def TreeNode():
    return importlib.import_module("TreeNode")

@pytest.fixture
def BinaryTree():
    return importlib.import_module("BinaryTree")

def test_tree_node_creation(TreeNode):
    node = TreeNode.TreeNode(10)
    assert node.key == 10
    assert node.left is None
    assert node.right is None
    assert node.parent is None  # Should be None

def test_set_get_key(TreeNode):
    node = TreeNode.TreeNode(5)
    node.key = 20
    assert node.key == 20

def test_set_valid_left_right(TreeNode):
    parent = TreeNode.TreeNode(10)
    left_child = TreeNode.TreeNode(5)
    right_child = TreeNode.TreeNode(15)
    parent.left = left_child
    parent.right = right_child
    assert parent.left is left_child
    assert parent.right is right_child
    assert left_child.parent is parent
    assert right_child.parent is parent

def test_set_new_left_right(TreeNode):
    parent = TreeNode.TreeNode(10)
    left_child = TreeNode.TreeNode(5)
    right_child = TreeNode.TreeNode(15)
    parent.left = left_child
    parent.right = right_child
    assert parent.left is left_child
    assert parent.right is right_child
    parent.right = None
    assert parent.right is None
    assert right_child.parent is None
    assert parent.left is left_child
    new_child = TreeNode.TreeNode(0)
    parent.left = new_child
    assert parent.left is new_child
    assert left_child.parent is None

def test_set_invalid_left_right(TreeNode):
    parent = TreeNode.TreeNode(10)
    with pytest.raises(TypeError):
        parent.left = "invalid"
    with pytest.raises(TypeError):
        parent.right = 123

def test_remove_leaf_left(TreeNode):
    parent = TreeNode.TreeNode(10)
    child = TreeNode.TreeNode(5)

    parent.left = child
    assert parent.left or parent.right

    parent.remove_leaf(child)
    assert parent.left is None


def test_remove_leaf_right(TreeNode):
    parent = TreeNode.TreeNode(10)
    child = TreeNode.TreeNode(5)

    parent.right = child
    assert parent.left or parent.right

    parent.remove_leaf(child)
    assert parent.right is None
    
def test_remove_child_with_children_raises(TreeNode):
    parent = TreeNode.TreeNode(10)
    child = TreeNode.TreeNode(5)
    grandchild = TreeNode.TreeNode(3)
    
    parent.left = child
    child.left = grandchild  # Child now has a child
    
    with pytest.raises(ValueError):
        parent.remove_leaf(child)
    
    
def test_tree_depth(TreeNode):
    root = TreeNode.TreeNode(10)
    child1 = TreeNode.TreeNode(5)
    child2 = TreeNode.TreeNode(15)
    child3 = TreeNode.TreeNode(20)
    child4 = TreeNode.TreeNode(25)
    
    root.left = child1
    root.right = child2
    root.right.right = child3
    root.right.right.left = child4
    
    assert root.depth == 1  # Root has depth 1
    assert child1.depth == 2
    assert child2.depth == 2
    assert child3.depth == 3
    assert child4.depth == 4
    
def test_inorder_single(TreeNode, BinaryTree):
    root = TreeNode.TreeNode(10)
    left = TreeNode.TreeNode(5)
    right = TreeNode.TreeNode(15)
    
    root.left = left
    root.right = right
    
    result = BinaryTree.inorder(root)
    assert result == [5, 10, 15]
    
    
def test_inorder(TreeNode, BinaryTree):
    root = TreeNode.TreeNode(10)
    child1 = TreeNode.TreeNode(5)
    child2 = TreeNode.TreeNode(15)
    child3 = TreeNode.TreeNode(20)
    child4 = TreeNode.TreeNode(13)
    child5 = TreeNode.TreeNode(7)
    child6 = TreeNode.TreeNode(6)
    
    root.left = child1
    root.right = child2
    root.right.right = child3
    root.right.left = child4
    root.left.right = child5
    root.left.right.left = child6
    
    result = BinaryTree.inorder(root)
    assert result == [5,6,7,10,13,15,20]

def test_preorder_single(TreeNode, BinaryTree):
    root = TreeNode.TreeNode(10)
    left = TreeNode.TreeNode(5)
    right = TreeNode.TreeNode(15)
    
    root.left = left
    root.right = right
    
    result = BinaryTree.preorder(root)
    assert result == [10, 5, 15]

def test_preorder(TreeNode, BinaryTree):
    root = TreeNode.TreeNode(10)
    child1 = TreeNode.TreeNode(5)
    child2 = TreeNode.TreeNode(15)
    child3 = TreeNode.TreeNode(20)
    child4 = TreeNode.TreeNode(13)
    child5 = TreeNode.TreeNode(7)
    child6 = TreeNode.TreeNode(6)
    
    root.left = child1
    root.right = child2
    root.right.right = child3
    root.right.left = child4
    root.left.right = child5
    root.left.right.left = child6
    
    result = BinaryTree.preorder(root)
    assert result == [10,5,7,6,15,13,20]

def test_postorder_single(TreeNode, BinaryTree):
    root = TreeNode.TreeNode(10)
    left = TreeNode.TreeNode(5)
    right = TreeNode.TreeNode(15)
    
    root.left = left
    root.right = right
    
    result = BinaryTree.postorder(root)
    assert result == [5, 15, 10]

def test_postorder(TreeNode, BinaryTree):
    root = TreeNode.TreeNode(10)
    child1 = TreeNode.TreeNode(5)
    child2 = TreeNode.TreeNode(15)
    child3 = TreeNode.TreeNode(20)
    child4 = TreeNode.TreeNode(13)
    child5 = TreeNode.TreeNode(7)
    child6 = TreeNode.TreeNode(6)
    
    root.left = child1
    root.right = child2
    root.right.right = child3
    root.right.left = child4
    root.left.right = child5
    root.left.right.left = child6
    
    result = BinaryTree.postorder(root)
    assert result == [6,7,5,13,20,15,10]

