from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field
from referential_array import ArrayR

I = TypeVar('I')
Point = Tuple[int, int, int]


@dataclass
class BeeNode:
    key: Point
    item: I
    subtree_size: int = 1
    node_lst: ArrayR = field(default_factory=lambda: ArrayR(8))

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        return self.node_lst[insert_index(self, point)]


def insert_index(current: BeeNode, key: Point) -> int:
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
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
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
        print('end')
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current, key) -> BeeNode:
        if current is not None:
            if current.key == key:
                return current
            else:
                return self.get_tree_node_by_key_aux(current.get_child_for_key(key), key)
        raise KeyError()

    def __setitem__(self, key: Point, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
        """
        if current is None:
            current = BeeNode(key, item)
            self.length += 1
        elif key == current.key:
            raise ValueError(key)
        else:
            index = insert_index(current, key)
            current.node_lst[index] = self.insert_aux(current.node_lst[index], key, item)
            current.subtree_size += 1

        return current

    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """
        return True if current is None else False


if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root)
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size)  # 2
