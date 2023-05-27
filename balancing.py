from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    Sort the list in a way that make the tree to be balanced when inserting the sorted list

    Args:
        my_coordinate_list: A list of coordinates which will then be inserted into a threedeebeetree
        result: An empty list which will be used to store the sorted version of my_coordinate_list which can meet the requirement given

    Returns:
        A list which consists of sorted version of my_coordinate_list which can meet the requirement given

    Complexity:
        Best Case = Worst Case : O(nlogn), n is the number of elements in my_coordinate_list
        ( At here we assume the time complexity always O(1) )

    Explanation:
        First a variable named result, which is initialised with an empty list ( Time Complexity : O(1) )
        Then balancing aux function is called to sort the points in my_coordinate_list ( Time Complexity : O(nlog(n))
        Finally result which is filled with sorted version of my_coordinate_list is returned ( Time Complexity : O(1) )
    """
    result = []
    balancing(my_coordinate_list, result)
    return result


def balancing(my_coordinate_list: list[Point], result: list[Point]) -> None:
    """
       Find the subroot for a particular octant and append it to result which is the list that stores the sorted version of my_coordinate_list

        Args:
            my_coordinate_list: A list of coordinates which will then be inserted into a threedeebeetree
            result: An empty list which will be used to store the sorted version of my_coordinate_list which can meet the requirement given
            x: Point which its x-coordinates sits between 12.5% to 87.5% in the list.
            y: Point which its y-coordinates sits between 12.5% to 87.5% in the list.
            z: Point which its z-coordinates sits between 12.5% to 87.5% in the list.
            point : A point which will be used as subroot

        Returns:
            None

        Complexity:
            Best Case = Worst Case : O(nlogn), n is the number of elements in my_coordinate_list
            ( At here we assume the time complexity always O(1) )

        Explanation:
            First we check if the length of my_coordinate_list is smaller than 18 ( base case ) ( Time Complexity : O(1) )
            If yes, the list result will use extend function to append remaining points into its list ( Time Complexity : O(n), n as the length of the my_coordinate_list )
            And the return ( Time Complexity : O(1) )
            If not , 3 variables, x,y,z will be initialised with   points which the correspond coordinates(x,y,z) is in the 12.5% to 87.5% of the current_list which is the result from percentile_xyz ( Time Complexity : O(nlog(n)) )
            Variable point is then initialised with the result of calling search_points function with x, (y[0],y[-1]), (z[0],z[-1]) as parameter.
            ( Time Complexity : Best Case : O(1) , Worst Case : O(n) ( Detailed Explanation at search_points )
            Then result will append the point into its list.
            space function will then be exceuted to allocate the points in my_coordinate_list ( Time Complexity : O(n) )
            Until now, the complexity will be O(nlogn + n) for the best case and O(nlogn + n + n) for the worst case,
            which the overall complexity is O(nlogn)
            Finally, a for loop will be used to recursively call this method by inserting the list allocated just now. As we can see, the number of points will be reduce to roughly 1/8.
            So the n from above will change by each recursion call
            Through computation, the overall complexity of this recursive method is O(nlog(n))
    """
    if len(my_coordinate_list) < 18:
        result.extend(my_coordinate_list)
        return
    x, y, z = percentile_xyz(my_coordinate_list)
    point = search_points(x, (y[0], y[-1]), (z[0], z[-1]))
    result.append(point)
    for child in space(my_coordinate_list, point):
        balancing(child, result)


def search_points(x_list: list[Point], y_bound: tuple, z_bound: tuple) -> Point:
    """
    Search for a point which fulfils the requirement

    Args:
        x_list: Point which its x-coordinates sits between 12.5% to 87.5% in the list.
        y_bound : A tuple where 1st position stores the smallest point of y-coordinate can be and 2nd position stores the largest point of y-coordinate can be
        z_bound: A tuple where 1st position stores the smallest point of z-coordinate can be and 2nd position stores the largest point of z-coordinate can be

    Returns:
        A point which fulfil requirement

    Complexity:
       Best Case : O(1), where the first point in x_list fulfils the requirement
       Worst Case : O(n), where the last point is x_list only fulfil the requirement or no point fulfil the requirement.
                    n as the number of elements in x_list.
       At here, we assume the time complexity for comparing as O(1).

    Explanation:
        A for loop is used to check which point in x_list meets the requirement
        Then if statement to check whether the points in x_list meets the requirement
        If yes, return the point else continue to iterate the loop until a point is found or no point is found and loop is exited.

        Time Complexity :
            Best Case : O(1), the first point in x_list fulfils the requirement, it will only iterate for loop once and its point will then be returned
            Worst Case : O(n), the last point in x_list only fulfils the requirement or no point fulfil the requirement at at all. n as the number of elements in x_list
            Complexity of comparing assume as O(1)
    """
    for index in range(len(x_list)):
        if y_bound[0] <= x_list[index][1] <= y_bound[-1] and z_bound[0] <= x_list[index][2] <= z_bound[-1]:
            return x_list[index]


def space(remaining_list: list[Point], cur_point: Point) -> list[list]:
    """
    To sort the point from remaining_list to the octant of point

    Args:
        remaining_list : The remaining list of points which yet to be sorted
        cur_point : Subroot of a particular octant
        child : A list of lists, where there are 8 empty lists in a list
        index : An integer which is used to determine where should the point be added

    Returns:
        A list of lists which store 8 octants

    Complexity:
        Best Case = Worst Case : O(n), n as the number of elements in remaining_list
        ( Assume time complexity of comparing as O(1) )

    Explanation:
        First, a variable child is initialised with list of lists of 8 empty list in a list ( Time Complexity : O(1) )
        Then, for loop is used to iterate all remaining points ( Time Complexity : O(n), n as the number of elements in remaining list )
        if the point is equal to cur_point continue to the next point ( Time Complexity : O(1) )
        Else, a variable name index is initialised with the result from calc_index function ( Time Complexity : O(1) )
        child will then append the point in the position of index ( Time Complexity : O(1) )
        After iterating the loop, return child which is a list of lists which store 8 octants ( Time Complexity : O(1) )
    """
    child = [[], [], [], [], [], [], [], []]
    for i in remaining_list:
        if i == cur_point:
            continue
        index = calc_index(i, cur_point)
        child[index].append(i)
    return child


def percentile_xyz(my_coordinate_list: list[Point]) -> tuple[list[Point], list[Point], list[Point]]:
    """
    Create Percentile class for each x,y,z coordinate and add the point respectively

    Args:
        my_coordinate_list : The remaining list to be appended to each Percentile class of x,y,z coordinate
        x1 : A percentile to store points
        y1 : A percentile to store points
        z1 : A percentile to store points
        x : The point which its x-coordinate is in the 12.5% to 87.5% of the my_coordinate_list
        y : The point which its y-coordinate is in the 12.5% to 87.5% of the my_coordinate_list
        z : The point which its z-coordinate is in the 12.5% to 87.5% of the my_coordinate_list

    Returns:
        A tuple where 1st position is the list of points for x-coordinate, 2nd position is the list of points for y-coordinate,
        3rd position is the list of points for z-coordinate

    Complexity:
        Best Case = Worst Case : O ( nlog(n) + n ), since we consider about the dominant term , O(nlog(n)) will be the complexity.
                                 n as the number of points in my_coordinate_list
        At here, we assume the time complexity of comparing as O(1)

    Explanation:
        First 3 variables x1,y1,z1 is initialised with Percentiles()
        Then a for loop is used to iterate all points in my_coordinate_list ( Time Complexity : O(n) )
        add_point() function to add points into x1,y1,z1 (Time Complexity : O(log(n)) )
        After that, 3 variables x,y,z is initialised with the reult of calling ratio ()
        ratio() has a complexity of O(logN + O), but since we called ratio(12.5,12.5) each time,
        O can be converted into (3/4)*N as removing the front 12.5% and back 12.5% removes 25% of my_coordinate_list in total.
        Hence the complexity here O(logN + (3/4)*N),
        since we are considering dominant term the complexity here will be O(N) (Best Case = Worst Case )
    """
    x1, y1, z1 = Percentiles(), Percentiles(), Percentiles()
    for i in my_coordinate_list:
        x1.add_point(i)
        y1.add_point(i[1])
        z1.add_point(i[2])
    x = x1.ratio(12.5, 12.5)
    y = y1.ratio(12.5, 12.5)
    z = z1.ratio(12.5, 12.5)
    return x, y, z

def calc_index(current: Point, other: Point) -> int:
    """
    To calculate the position of point to be added in a list

    Args:
        current : Point to be compared with other
        other : Point to be compared with current
        sum : The position of point current will be added into the list

   Returns:
       An interger which indicates the position of a point to be added in a list

   Complexity:
        Best Case = Worst Case : O(1) ( At here, we assume the complexity of comparing as O(1) )

   Explanation:
        First, a variable sum is initialised with value 0 ( Time Complexity : O(1) )
        Then check if the point of x-coordinate of current is larger than or equal to point other or not. ( Time Complexity : O(1) )
        If yes sum += 4 ( Time Complexity : O(1) )
        Then check if the point of y-coordinate of current is larger than or equal to point other or not. ( Time Complexity : O(1) )
        If yes sum += 2 ( Time Complexity : O(1) )
        Then check if the point of x-coordinate of current is larger than or equal to point other or not. ( Time Complexity : O(1) )
        If yes sum += 1 ( Time Complexity : O(1) )
        Finally, return the sum ( Time Complexity : O(1) )
    """

    sum = 0
    if current[0] >= other[0]:
        sum += 4
    if current[1] >= other[1]:
        sum += 2
    if current[2] >= other[2]:
        sum += 1
    return sum
