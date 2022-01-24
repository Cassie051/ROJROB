import math
import heapq
import matplotlib.pyplot as plt
from scene.map import Map


class Node:
    """A node class for A* pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def __str__(self):
        return str(self.position[0]) + ", " + str(self.position[1])

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


class Astar:
    def __init__(self):
        self.states_ = []

    def solve(self, start, goal, occupancy_map):
        solution = None
        start_state = start
        goal_state = goal
        start_node = Node(None, start_state)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, goal_state)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []
        heapq.heapify(open_list)
        # adjacent_squares = ((1, 0, 0), (1, 1, 45), (0, 1, 90), (-1, 1, 135),
        #                     (-1, 0, 0), (-1, -1, -135), (0, -1, -90), (1, -1, -45))
        adjacent_squares = ((1, 0, 0), (0, 1, 90), (-1, 0, 0), (0, -1, -90))

        heapq.heappush(open_list, start_node)
        while len(open_list) > 0:
            current_node = heapq.heappop(open_list)
            if current_node == end_node:  # if we hit the goal
                current = current_node
                path = []
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                for i in range(1, len(path)):
                    self.states_.append(path[len(path) - i - 1])
                solution = len(self.states_)
                break
            closed_list.append(current_node)

            children = []
            for new_position in adjacent_squares:
                current_node_x = current_node.position[0]
                current_node_y = current_node.position[1]
                node_position = list((0, 0))
                node_position[0], node_position[1] = current_node_x + new_position[0], current_node_y + new_position[1]

                # check if node is reachable
                if 0 > node_position[0] or node_position[0] > occupancy_map.get_x_size()-1:
                    continue
                if 0 > node_position[1] or node_position[1] > occupancy_map.get_y_size()-1:
                    continue
                if occupancy_map.is_occupacy(node_position[0], node_position[1]):
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                if child in closed_list:
                    continue
                child.g = current_node.g + 1
                child.h = math.hypot(goal[0] - child.position[0], goal[1] - child.position[1])
                child.f = child.g + child.h
                if len([i for i in open_list if child == i and child.g >= i.g]) > 0:
                    continue
                heapq.heappush(open_list, child)

        if not solution:
            return []
        else:
            path = [start]
            for s in self.states_[:solution]:
                path.append(s)
            return path

    def clear(self):
        self.states_ = []


def plan():
    n = 10
    start = 5, 4
    goal = 2, 3
    result = Astar().solve(start, goal, Map(n, n))
    if result:
        print(result)
        plt.axis([0, n, 0, n])
        x = []
        y = []
        for i in result:
            x.append(i[0])
            y.append(i[1])
        plt.plot(x, y, 'ro-')
        plt.show()


if __name__ == "__main__":
    plan()
