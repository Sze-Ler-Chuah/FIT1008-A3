from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field
from referential_array import ArrayR

I = TypeVar('I')
Point = Tuple[int, int, int]


@dataclass
class BeeNode:
    """
    Node class which is use to represent BST nodes

    Args :
        key : The key which is used to store the coordinates of BeeNode
        item : To store the value stored in Node
        subtree_size : An integer which is used to store the size of subtree where the current node is subroot
        node_lst : An ArrayR to store the pointer to 8 different directions, each direction will have BeeNode or None

    Complexity :
        Best Case = Worst Case : O(1)

    Explanation :
        The complexity of initailsing ArrayR is usually O(n) where, n is the size of ArrayR but since we already know that we neede
        to initialise it with size of 8, thhus the complexity will be O(1)
    """
    key: Point
    item: I
    subtree_size: int = 1
    node_lst: ArrayR = field(default_factory=lambda: ArrayR(8))

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        """
        Return one of the node's children which can be a BeeNode or None depending on the key and which octant does the point pointing to.

        Args:
            point: The coordinates which indicates its child will be searched later ( Point can be not stored in node )

        Returns:
            The Node stored in the octant or None

        Complexity:
            Best Case = Worst Case : O(comp), comp is the complexity of comparing 2 integer(comparing coordinates)

        Explanation:
            At here we just call insert_index() method to determine the position which will be used to access self.node_lst
            ( Time Complexity : O(comp) )
            Then, use the result from insert_index() to access self.node_lst ( Time Complexity : O(1) )

        """
        return self.node_lst[insert_index(self, point)]


def insert_index(current: BeeNode, key: Point) -> int:
    """
    A function used to determine the position of current,which is a BeeNode in ArrayR

    Args :
        current : A BeeNode
        key : A point

    Returns :
        An integer which indicates the position of current in ArrayR

    Complexity :
        Best Case = Worst Case : O(comp), comp is the complexity of comparing

    Explanation :
        a,b,c each initialise with a point which represent the x,y,z coordinate of the key.
        The logic of finding position works as follows :
        If a >= current.key[0], total += 2^2
        If b >= current.key[1], total += 2^1
        If c >= current.key[2], total += 2^0

        Index 0 : a < current.key[0], b < current.key[1], c < current.key[2], the total will be 0
        Index 1 : a < current.key[0], b < current.key[1], c >= current.key[2], the total will be 1
        Index 2 : a < current.key[0], b >= current.key[1], c < current.key[2], the total will be 2
        Index 3 : a < current.key[0], b >= current.key[1], c >= current.key[2], the total will be 3
        Index 4 : a >= current.key[0], b < current.key[1], c < current.key[2], the total will be 4
        Index 5 : a >= current.key[0], b < current.key[1], c >= current.key[2], the total will be 5
        Index 6 : a >= current.key[0], b >= current.key[1], c < current.key[2], the total will be 6
        Index 7 : a >= current.key[0], b >= current.key[1], c >+ current.key[2], the total will be 7
"""
    a, b, c = key
    total = 0
    if a >= current.key[0]:
        total += 4
    if b >= current.key[1]:
        total += 2
    if c >= current.key[2]:
        total += 1
    return total


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
        Initialises an empty 3DBT

        Args:
            self.root: A pointer which points to the root node but points to None at first
            self.length: An integer which indicates the length of the threedeebeetree

        Complexity:
            Best Case = Worst Case : O(1)

        Explanation:
            At here, we just initialise self.root with None and self.length with 0 ( Time Complexity : O(1) )
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
        Checks to see if the 3DBT is empty

        Returns:
            A boolean which indicates the threedeebeetree is empty or not

        Complexity:
            Best Case = Worst Case : O(1)

        Explanation:
            At here we just return a boolean which is True when threedeebeetree is empty and False when threedeebeetree
            is not empty ( Time Complexity : O(1) )

        """
        return len(self) == 0

    def __len__(self) -> int:
        """
        Returns the number of nodes in the tree.

        Returns:
            An integer which indicates the number of nodes in the tree

        Complexity:
            Best Case = Worst Case : O(1)

        Explanation:
            At here, we just return an integer which indicates the number of nodes in the tree ( Time Complexity : O(1) )
        """
        return self.length

    def __contains__(self, key: Point) -> bool:
        """
        Checks to see if the key is in the 3DBT

        Args:
            key: A tuple with x,y,z coordinates to retrieve the BeeNode

        Returns:
            A boolean to which indicates the key is stored in the tree or not

        Complexity:
            Best Case: O(comp) when the node is at the root of the tree, comp is the complexity of comparing the coordinates
            Worst Case: O(Depth*comp) when the node is at the edge of the tree, comp is the complexity of comparing the coordinates, Depth is the height of threedeebeetree

        Explanation:
            The complexity is based on the get_tree_node_by_key function
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
        Attempts to get an item in the tree, it uses the Key to attempt to find it
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        """
        To retrieve the BeeNode based on the key given

        Raises: KeyError when key is not found

        Args:
            key: A tuple with x,y,z coordinates to retrieve the BeeNode

        Complexity:
            Best Case: O(comp) when the node is at the root of the tree, comp is the complexity of comparing the coordinates
            Worst Case: O(Depth*comp) when the node is at the edge of the tree, comp is the complexity of comparing the coordinates, Depth is the height of threedeebeetree

        Explanation:
            Complexity above is based on get_tree_node_by_key_aux method
        """
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current, key) -> BeeNode:
        """
        An auxilary function for get_tree_node_by_key_aux

        Raises: KeyError when key is not found

        Args:
            current: The node which key is used to check whether it is the key wanted
            key: The coordinate which the user want to retrieve the node

        Complexity:
            Best Case: O(comp) when the node is at the root of the tree, comp is the complexity of comparing the coordinates
            Worst Case: O(Depth*comp) when the node is at the edge of the tree, comp is the complexity of comparing the coordinates, Depth is the height of threedeebeetree

        Explanation:
            First we check if current is None ( Time Complexity : O(1) )
            If yes, raise KeyError ( Time Complexity : O(1) )
            If no, if statement is used to check if current.key is equal to key ( Time Complexity : O(comp) )
            If yes, return current ( Time Complexity : O(1) )
            If no, return itself with current.get_child_for_key(key) and key as parameter

            Best Case Scenario : The node user searching for is just located at the root of tree, thus it just need to compare
                                 the keys once and can straightly return the node, this will take the complexity of O(comp)
            Worst Case Scenario : The node user searching for is located at the edge of the tree and need to compare the keys
                                  Depth times , Depth as the height of the tree, this will take the complexity of O(Depth*comp)
                                  For Worst Case Scenario, there are 2 different situations.
                                  The first one is when the tree is unbalanced(Nodes forming a line) and the Depth will be n-1, n as the number of elements in tree,
                                  thus the complexity will be O(n*comp)
                                  The second one is when the tree is balanced(tree spread to 8 directions as required) and the Depth will be log(n), n as the number of elements in tree,
                                  thus the complexity will be O(log(n)*comp)
        """
        if current is not None:
            if current.key == key:
                return current
            else:
                return self.get_tree_node_by_key_aux(current.get_child_for_key(key), key)
        raise KeyError('Key not found: {0}'.format(key))

    def __setitem__(self, key: Point, item: I) -> None:
        """
        Use to insert a key value pair into thredeebeeetree

        Args :
            key : A key which stores a tuple of x,y,z coordinate, a point
            item : The value which pair with key

        Return :
            None

        Complexity :
            Best Case : O(comp), when the tree is unbalanced and there is one octant which is empty, comp is the complexity of comparing 2 keys
            Worst Case : O(Depth*comp), Depth is the height of tree, comp is the complexity of comparing 2 keys.

        Explanationm :
            At here, we set the value of self.root to the result of self.insert_aux()
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
        Attempts to insert an item into the tree, it uses the Key to insert it

        Args :
            current : A BeeNode which is currently pointed to
            key : The coordinate which will be inserted into the tree
            item : The value which pair with key which will be inserted into tree
            index : An integer which is the result from insert_index method and it indicates the position of key-value pair above in ArrayR

        Returns:
            A BeeNode

        Complexity :
            Best Case : O(comp), when the tree is unbalanced and there is one octant which is empty, comp is the complexity of comparing 2 keys
            Worst Case : O(Depth*comp), Depth is the height of tree, comp is the complexity of comparing 2 keys.

        Explanation:
            At first, we will check whether current is None. ( Time Complexity : O(1) )
            If yes, current will be initialised with a BeeNode object ( Time Complexity : O(1) )
            Then, self.length will be added by 1 ( Time Complexity : O(1) )
            If not None, we will check whether the key to be added is the same as the key of current node ( Time Complexity : O(comp) )
            If yes, ValueError will be raised ( Time Complexity : O(1) )
            If no, index will be initialised with the result of insert_index() method with current and key as input ( Time Complexity : O(comp) )

            Best Case Scenario:
                Assume that the tree is unbalanced and the octant which index points to is empty, it can assign node to that index (node is created during base case)
                Hence, insert_aux method will only be called once, tiem complexity will be O(comp)

            Worst Case Scenario:
                The node will be inserted at the edge of tree and key will be required to compare Depth times,
                so the complexity will be O(Depth*comp), Depth as the height of threedeebeetree and comp is the complexity of
                comparing 2 keys

                There are 2 different situations when it comes to Worst Case Scenario.

                First one will be when the tree is balanced. Since the height of a balanced tree is log(n), n as the number of elements in tree,
                the key needs to be compared log(n) times, hence the complexity will be O(log(n) * comp )

                Second One will be when the tree is unbalanced. Since the height of a unbalanced tree is n , n as the number of elements in the tree,
                the key needs to be compared n times, hence the complexity will be (n*comp)

        """
        if current is None:
            current = BeeNode(key=key, item=item)
            self.length += 1
        elif key == current.key:
            raise ValueError(key)
        else:
            index = insert_index(current, key)
            current.node_lst[index] = self.insert_aux(current.node_lst[index], key, item)
            current.subtree_size += 1

        return current

    def is_leaf(self, current: BeeNode) -> bool:
        """
        Used to check whether the node is a leaf or not.

        Args:
            current: The node that will be checked whether is a leaf or not.

        Returns:
            A boolean which indicates the node is a leaf or not.

        Complexity:
            Best Case = Worst Case : O(1)

        Explanation:
            At here, we just return a boolean which is True when current node's subtree has a size of 1 and False when
            subtree size is not 1 ( Time Complexity : O(1) )
        """
        return current.subtree_size == 1


if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size)  # 2
