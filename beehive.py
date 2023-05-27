from dataclasses import dataclass, field
from heap import MaxHeap


@dataclass
class Beehive:
    """
    A beehive has a position in 3d space, and some stats.

    Args :
        x : An integer which indicates the x-coordinate of the position of beehive in 3d space
        y : An integer which indicates the y-coordinate of the position of beehive in 3d space
        z : An integer which indicates the z-coordinate of the position of beehive in 3d space
        capacity : An integer which indicates the amount of money we can take from single sitting before the bee attacks
        nutrient_factor : An integer which indicates how nutritious the honey is
        volume : An integer which indicates the total amount of honey in this hive
    """

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

    def money(self) -> int:
        """
        Used to calculate the amount of emerald that can be obtained from beehive in a single sitting before the bee attacks

        Returns :
            An integer which indicate the amount of emerald can be obtained from beehive in a single sitting before the bee attacks

        Complexity :
            Best Case = Worst Case : O(1)

        Explanation :
            At here we just return the minimum between capacity and volume multiply by nutrient factor which is the amount of
            emerald can be obtained ( Time Complexity : O(1) )
        """
        return min(self.capacity, self.volume) * self.nutrient_factor

    def __gt__(self, other) -> bool:
        """
        A magic method to check if the Beehive object is greater than another Beehive object according to the amount of emerald which is the result of money() function

        Complexity :
            Best Case = Worst Case : O(comp), comp is the complexity of comparing 2 integers

        Explanation:
            At here, we return a boolean which is True when self.money() > other money and False when other.money() > self.money
            ( Time Complexity : O(comp) )
        """
        return self.money() > other.money()

    def __le__(self, other) -> bool:
        """
        A magic method to check if the Beehive object is less than or equal to another Beehive object according to the amount of emerald which is the result of money() function

        Complexity :
            Best Case = Worst Case : O(comp), comp is the complexity of comparing 2 integers

        Explanation:
            At here, we return a boolean which is True when self.money() <= other money and False when other.money() > self.money
            ( Time Complexity : O(comp) )
        """
        return self.money() <= other.money()


class BeehiveSelector:

    def __init__(self, max_beehives: int):
        """
        Args:
            max_beehives : An integer which indicated the maximum amount of beehives that can be placd in BeehiveSelector
            self.honey_store : A MaxHeap object used to store all behives according to their value of emerald which is the result from money() function

        Complexity:
            Best Case = Worst Case : O(n), n as the number of max beehives

        Explanation:
            At here, we just initialise variable honey_store with a MaxHeap object which includes max_beehives as its parameter
            ( Time Complexity : O(n) )
        """

        self.honey_store = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]) -> None:
        """
        Args:
            hive_list: A list which is used to store Beehive objects
            self.honey_store : A MaxHeap object used to store all behives according to their value of emerald which is the result from money() function

        Complexity:
            Best Case = Worst Case : O(k), k is the length of hive_list

        Explanation:
            First self.honey_store.length will be added the length of hive_list ( Time Complexity : O(1) )
            Then self.honey_store call heapify() method from MaxHeap with hive_list as input ( Time Complexity : O(k) )
        """
        self.honey_store.length += len(hive_list)
        self.honey_store.heapify(hive_list)

    def add_beehive(self, hive: Beehive):
        """
        Args:
            hive : The beehive that will be added to self.honey_store
            self.honey_store : A MaxHeap object used to store all behives according to their value of emerald which is the result from money() function

        Complexity:
            Best Case : O(1), when no rising is required
            Worst Case : O(n), when rising is required and n as the length of self.honey_store currently

            At here, we assume the complexity of comparing as O(1)

        Explanation:
            Call the add() method from MaxHeap to add hive into self.honey_store
            ( Time Complexity : Best Case : O(1), Worst Case : O(n) )
        """
        self.honey_store.add(hive)

    def harvest_best_beehive(self) -> float:
        """
        Args:
            temp: The Beehive with the highest amount of emerald can be obtained in a single sitting before bee attacks
            large: The amount of emerald of the best Beehive

        Complexity:
            Best Case = Worst Case : O(log(n)), n is the number of Beehive currently in self.honey_store
            At here, we assume the complexity of comparing as O(1)

        Returns:
            A float that represents the amount of emerald of Beehive in the BeehiveSelector

        Explanation:
            First, variable temp is initialised with the Beehive which can extract the most emerald by calling get_max() function from MaxHeap
            ( Time Complexity : O(log(n) )
            Then , variable large is initialised with the amount of emerald extracted from temp by calling money() method
            ( Time Complexity :  O(1) )
            Subtraction occurs by subtracting temp capacity from temp volum ( Time Complexity : O(1) )
            After that, if statement is used to check whether temp.volume is smaller than 0 ( Time Complexity : O(1) )
            If yes, set the temp.volume to 0 which means no more emerald can be obtained from this Beehive anymore ( Time Complexity : O(1) )
            Then, use add_beehive() method to add back temp which is a Beehive into self.honey_store
            ( Time Complexity : Best Case : O(1), Worst Case : O(n) )
            Finally, return the amount of emerald obtained from this sitting ( Time Complexity : O(1) )

            Hence, the overall complexity is O(log(n)) for best case and O(log(n) + log(n) ) for worst case
            which is then simplified to O(log(n). Therefore, the overall complexity of best case and worst case is the same
            which is O(log(n)).
        """
        temp = self.honey_store.get_max()
        large = temp.money()
        temp.volume -= temp.capacity
        if temp.volume < 0:
            temp.volume = 0
        self.add_beehive(temp)
        return large
