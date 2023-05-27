""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from node import TreeNode
import sys

# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item=item)
            self.length += 1
        elif key < current.key:
            current.set_subtree_size(current.subtree_size + 1)
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.set_subtree_size(current.subtree_size + 1)
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)
        current.set_subtree_size(current.subtree_size - 1)
        return current

    def get_successor(self, current: TreeNode) -> TreeNode | None:
        """
        Get successor of the current node. It should be a child node having the smallest key among all the larger keys.

        Args:
            current: The node where its successor will be found throughout this method

        Returns:
            The child node from the current node which have the smallest key among other nodes but greater than key of current node

        Complexity:
            Best case: O(1), current is the leaf of the tree
            Worst case: O(Depth), current is the root of the tree, Depth is the height of the tree

        Explanation:
            First, check whether current.right is None ( Time Complexity : O(1) )
            If yes, return None ( Time Complexity : O(1) )

            Best Case Scenario:
                Current is the leaf node of tree, so it does not have any child nodes. Thus, it will return None,
                hence the complexity of best case is O(1)

            Then, smallest key which is larger than key of current will be found from the right subtree of current by using get_minimal method

            Worst case scenario:
                When current is at the root of the tree, we will need to traverse to the edge of the tree in order to obtain the
                smallest key which is larger than key of current node, which has the complexity of O(Depth), Depth as the height of the tree.

                Thre are 2 situations when talking about worst case scenario.

                First one is the tree is unbalanced. Depth of tree will be n-1, n as the number of elements of the tree,
                hence the complexity will be O(n),n as the number of elements of the tree

                Second one is the tree is balanced. Depth of the tree will be log(n), n as the number of elements of the tree,
                hence the complexity will be O(log(n)), n as the number of elements of the tree.
        """
        if current.right is None:
            return None
        return self.get_minimal(current.right)

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
        Get a node having the smallest key in the current sub-tree.

        Args:
            current: The node where its successor will be found throughout this method

        Returns:
            The child node from the current node which have the smallest key among other nodes but greater than key of current node

        Complexity:
            Best case: O(1), current is the leaf of the tree
            Worst case: O(Depth), current is the root of the tree, Depth is the height of the tree

        Explanation:
            First, check whether current.left is None ( Time Complexity : O(1) )
            If yes, return current ( Time Complexity : O(1) )

            Best Case Scenario:
                Current is the leaf node of tree, so it does not have any child nodes. Thus, it will return current,
                hence the complexity of best case is O(1)

            Else, it wil call itself with current.left as parameter until the smallest key is found

            Worst case scenario:
                When current is at the root of the tree, we will need to traverse to the edge of the tree in order to obtain the
                smallest key which is larger than key of current node, which has the complexity of O(Depth), Depth as the height of the tree.

                Thre are 2 situations when talking about worst case scenario.

                First one is the tree is unbalanced. Depth of tree will be n-1, n as the number of elements of the tree,
                hence the complexity will be O(n),n as the number of elements of the tree

                Second one is the tree is balanced. Depth of the tree will be log(n), n as the number of elements of the tree,
                hence the complexity will be O(log(n)), n as the number of elements of the tree.
        """
        if current.left is None:
            return current
        else:
            return self.get_minimal(current.left)

    def is_leaf(self, current: TreeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """

        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left, prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: TreeNode) -> TreeNode:
        """
        Finds the kth smallest value by key in the subtree rooted at current.

        Args :
           k : It is used to search for the node with the kth smallest key
           current : The current node which is used for comparison to find the node we wanted

        Returns :
            The node with the kth smallest key among all the nodes in BST

        Complexity :
            Best Case : O(1), when the kth smallest is the current node in the first comparison
            Worst Case : (Occurs when the k value is equal to the number of nodes in the BST, as it has to go into the last level of the BST)
                        - Balanced Tree O(logn), where n is the number of nodes in the BST
                        - Unbalanced Tree O(n), where n is the number of nodes in the BST

        Explanation :
            At here we just return the TreeNode which is computed from kth_smallest_aux ( Time Complexity : O(D) )

        """
        return self.kth_smallest_aux(current, k)

    def kth_smallest_aux(self, current: TreeNode, k: int, nodes_travelled: int = 0) -> TreeNode:
        """
               A helper function to find the kth smallest value by key in the subtree rooted at current.

               Complexity:
                   Best Case - O(1), occurs when the kth smallest is the current node in the first comparison
                   Worst Case (Occurs when the k value is equal to the number of nodes in the BST, as it has to go into the last level of the BST)
                       - Balanced Tree O(logn), where n is the number of nodes in the BST
                       - Unbalanced Tree O(n), where n is the number of nodes in the BST

               Explanation:
                   There are several conditions to check before we find the kth smallest value by key in the subtree rooted at current:
                       (i) If k value is smaller than (nodes_travelled + left_subtree_elem) and current node has a left child, means that the kth smallest element will surely be in the current left-subtree
                           Recursively calls the kth_smallest_aux and pass the current left child as argument
                       (ii) If nodes_travelled + left_subtree_elem + 1 equals to k, the reason we +1 is we have to count the current node itself, means we found the kth smallest element
                       (iii) If k value is bigger than (nodes_travelled + left_subtree_elem) and current node has a right child, means that the kth smallest element will surely be in the current right-subtree
                           Recursively calls the kth_smallest_aux and pass the current right child as argument
               """
        if current.left is None:  # O(1)
            left_subtree_elem = 0  # O(1)
        else:
            left_subtree_elem = current.left.subtree_size  # O(1)

        # If k value is smaller than (nodes_travelled + left_subtree_elem) and current node has a left child, means that the kth smallest element will surely be in the current left-subtree
        if nodes_travelled + left_subtree_elem >= k and current.left is not None:  # O(1)
            return self.kth_smallest_aux(current.left, k, nodes_travelled)

        # In this condition, the reason we +1 is we have to count the current node itself
        elif nodes_travelled + left_subtree_elem + 1 == k:  # O(1)
            return current  # O(1)

        # If k value is bigger than (nodes_travelled + left_subtree_elem) and current node has a right child, means that the kth smallest element will surely be in the current right-subtree
        elif nodes_travelled + left_subtree_elem + 1 < k and current.right is not None:
            return self.kth_smallest_aux(current.right, k, nodes_travelled + left_subtree_elem + 1)

