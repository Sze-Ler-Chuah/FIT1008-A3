from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        Args :
            self.bsearch : Initialised with a BST which is used to stored the nodes to be added

        Returns :
            None

        Complexity :
            Best Case = Worst Case : O(1)

        Explanation :
            At here, we just initialised self.bsearch as a BST ( Time Complexity : O(1) )
        """
        self.bsearch = BinarySearchTree()
    def add_point(self, item: T) -> None:
        """
        Args :
            item : Item to be added into BST, self.bsearch

        Returns :
            None

        Complexity :
            Best Case = O(CompK), where item to be added at the root , CompK is the complexity of comparing 2 keys
            Worst Case = O(log(n)*CompK), where the item to be added is at the bottom of BST, n as the number of elements in BST,
                                        CompK as the complexity of comparing 2 keys
            To achieve worst case above, we need to assume that is a balanced tree.

        Explanation :
            At here, we just use _set_item_ method of BST ( from bst.py ) to insert item into BST
            ( Time Complexity : Best Case : O(CompK), Worst Case : O(D*CompK) )
        """
        self.bsearch[item] = item

    def remove_point(self, item: T) -> None:
        """
        Args :
            item : Item to be deleted from BST, self.bsearch

        Returns :
            None

        Complexity :
            Best Case = O(CompK), where item to be deleted at the root , CompK is the complexity of comparing 2 keys
            Worst Case = O(log(n)*CompK), where the item to be deleted is at the bottom of BST, n as the number of elements in BST,
                                          CompK as the complexity of comparing 2 keys
            To achieve worst case above, we need to assume the tree is a balanced tree

        Explanation :
            At here, we just use _del_item_ method of BST ( from bst.py ) to delete item from BST
            ( Time Complexity : Best Case : O(CompK), Worst Case : O(D*CompK) )
        """
        del self.bsearch[item]

    def ratio(self, x:float, y:float) -> list:
        """
        Args :
            x : The starting range where all elements in bound will be at least larger than x% of elements in BST, self.bsearch
            y : The starting range where all elements in bound will be at least smaller than y% of elemehnts in BST, self.bsearch
            ans : The list which is used to store the elements in bound of [x,y] which is arranged in inorder ( ascending order )
            lower_bound_value : An interger which is later used in kth smallest to find the smallest key value can be added into ans
            upper_bound_value : An integer which is later used in kth smallest to find the largest key value can be added into ans
            lower_bound : An integer which acts a lower bound to ensure all elements returned are larger than it
            upper_bound : An integer which acts a upper bound to ensure all elements returned are smaller than it

        Returns :
            A list of elements which sits in bound of x and y and arranged in ascending order due to inorder traversal

        Complexity :
            Best Case = Worst Case : O(log(n) + O) assuming that it is a balanced tree,
            where O is the number of points which fulfill the requirement, n is the number of elements in the tree


        Explanation :
            At first, variable ans is initialised with an empty list. ( Time Complexity : O(1) )
            Then variable lower_bound_value,upper_bound_value are then initialised with an integer which is obtained from computation.
            ( Time Complexity : O(1) )
            lower_bound is then initialised with key of the smallest node which meets the requirement above by using kth_smallest
            ( Time Complexity : O(log(n)) )
            upper_bound is then initialised with key of the largest node which meets the requirement above by using kth_smallest
            ( Time Complexity : O(log(n)) )
            Then ratio_aux function is called to return append elements into ans in inorder
            ( Time Complexity : O(O) )
            And finally ans which stores a list of elements which are added in ascending order ( Time Complexity : O(1) )
        """
        ans = []
        lower_bound_value = ceil(self.bsearch.length*x/100) + 1
        upper_bound_value = self.bsearch.length - ceil(self.bsearch.length*y/100)
        lower_bound = self.bsearch.kth_smallest(lower_bound_value, self.bsearch.root).key
        upper_bound = self.bsearch.kth_smallest(upper_bound_value, self.bsearch.root).key
        self.ratio_aux(self.bsearch.root, lower_bound, upper_bound,ans)
        return ans

    def ratio_aux(self, current: TreeNode, lb: int, ub: int,lst:list) -> None:
        """
        Args :
            current : A treenode and is the root node where user want to compute the list from
            lb : The key value of the minimum boundary node
            ub : The key value of the maximum boundary node
            lst : A list of elements which is arranged in ascending order due to inorder traversal

        Returns :
            None

        Complexity :
            Best Case = Worst Case : O(O), where O is the number of elements appended into lst

        Explanation :
            First we will check whether current is None. ( Time Complexity : O(1) )
            If current is None, return ( Time Complexity : O(1) )
            Else, add elements into lst.
            If current.key is smaller than ub and larger than lb, call itself with left subtree of current and lb, ub,lst as parameters
            ( Assume Time Complexity of comparing as O(1) )
            lst will then append current's key ( Time Complexity : O(1) )
            Then it will call itself with right subtree of current and lb, ub, lst as parameters
            ( Assume Time Complexity of comparing as O(1) )
            Else if current.key is larger than ub and larger than lb, call itself with left subtree of current and lb,ub,lst as paramters
            ( Assume Time Complexity of comparing as O(1) )
            Else if current.key is smaller than or equal to lb, check if current.key is equal to lb.
            If current.key is equal to lb, lst append current.key ( Time Complexity : O(1) )
            If current.key is smaller than lb, call itself with right subtree of current and lb,ub,lst as parameters
            ( Assume Time Complexity of comparing as O(1) )
            Else if current.key is equal to ub, call itsellf with left subtree of current and lb,ub,ls as parameters
            ( Assume Tim Complexity of comparing as O(1) )
            lst will then append current.key ( Time Complexity : O(1) )

            The recursion depth will be as long as O, where O is the number of points appended into lst, so the complexity
            of the operation will always be O(O)

        """
        if current is not None:
            if lb < current.key < ub:
                self.ratio_aux(current.left,lb,ub,lst)
                lst.append(current.key)
                self.ratio_aux(current.right,lb,ub,lst)
            elif lb < current.key > ub:
                self.ratio_aux(current.left,lb,ub,lst)
            elif current.key <= lb:
                if current.key == lb:
                    lst.append(current.key)
                self.ratio_aux(current.right,lb,ub,lst)
            elif current.key == ub:
                self.ratio_aux(current.left,lb,ub,lst)
                lst.append(current.key)
        return

if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))