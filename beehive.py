from dataclasses import dataclass, field
from heap import MaxHeap


@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0
    emerald: int = 0

    def money(self):
        return min(self.capacity, self.volume) * self.nutrient_factor

    def __gt__(self, other):
        return self.emerald > other.emerald

    def __le__(self, other):
        return self.emerald <= other.emerald

class BeehiveSelector:

    def __init__(self, max_beehives: int):
        self.honey_store = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]):
        for i in hive_list:
            i.emerald = i.money()
        self.honey_store.length += len(hive_list)
        self.honey_store.heapify(hive_list)
    def add_beehive(self, hive: Beehive):
        hive.emerald = hive.money()
        self.honey_store.add(hive)

    def harvest_best_beehive(self):
        temp = self.honey_store.get_max()
        temp.volume -= temp.capacity
        if temp.volume >= temp.capacity:
            self.add_beehive(temp)
        elif temp.capacity > temp.volume >= 0:
            self.honey_store.add(Beehive(temp.x, temp.y, temp.z, temp.capacity, temp.nutrient_factor, temp.volume, temp.money()))
        return temp.emerald
