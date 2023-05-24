from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None  :
        self.bsearch = BinarySearchTree()
    def add_point(self, item: T) -> None:
        self.bsearch[item] = item

    def remove_point(self, item: T) -> None:
        del self.bsearch[item]

    def ratio(self, x, y) -> list:
        ans = []
        lower_bound_value = ceil(self.bsearch.length*x/100) + 1
        upper_bound_value = self.bsearch.length - ceil(self.bsearch.length*y/100)
        lower_bound = self.bsearch.kth_smallest(lower_bound_value, self.bsearch.root).key # O(log(n))
        upper_bound = self.bsearch.kth_smallest(upper_bound_value, self.bsearch.root).key # O(log(n))
        self.inorder(self.bsearch.root, lower_bound, upper_bound,ans)
        return ans

    def inorder(self, current, lb: int, ub: int,lst:list) -> None:
        if current is not None:
            if lb < current.key < ub:
                self.inorder(current.left,lb,ub,lst)
                lst.append(current.key)
                self.inorder(current.right,lb,ub,lst)
            elif lb < current.key > ub:
                self.inorder(current.left,lb,ub,lst)
            elif current.key <= lb:
                if current.key == lb:
                    lst.append(current.key)
                self.inorder(current.right,lb,ub,lst)
            elif current.key == ub:
                self.inorder(current.left,lb,ub,lst)
                lst.append(current.key)

if __name__ == "__main__":
    final = 0
    for i in range(100):
        points = list(range(50))
        import random
        random.shuffle(points)
        print(points)
        p = Percentiles()
        for point in points:
            p.add_point(point)
        # Numbers from 8 to 16.
        print(p.ratio(15, 66))

        if p.ratio(15,66) == [8,9,10,11,12,13,14,15,16]:
            final += 1
    print(final)
