from time import perf_counter

class maze_solver():
    def __init__(self, maze_file_path, search_method):
        self.explored = []
        self.frontier_class = stackfrontier()
        with open(maze_file_path, "r") as maze:
            self.layout = maze.read()
            maze.close()
        self.maze_length = self.layout.find("\n") + 1
        self.starting_point = self.coordinate(self.layout.find("S"))
        self.ending_point = self.coordinate(self.layout.find("E"))
        self.search_method = search_method
        self.solution = []

    def check_explored(self, state):
        return state in self.explored

    def coordinate(self,point):
        if point < self.maze_length:
            return (point, 0)
        else:
            row = int(point / self.maze_length)
            column = point - row * self.maze_length
            return (column, row)

    def point(self,coordinate):
        column = coordinate[0]
        row = coordinate[1]
        point = row * self.maze_length + column
        return point

    def find_moves(self,current_location):
        moves = []
        for location in (0,1):
           for move in (-1, 1):
                location_buffer = list(current_location)
                location_buffer[location] += move
                possible_moves = tuple(location_buffer)
                if self.layout[self.point(possible_moves)] in (" ", "E"):
                    moves.append(possible_moves)
        return moves

    def print_solution(self, print_explored_states = False):
        solution_map = list(self.layout)

        if print_explored_states:
            for explored_state in self.explored:
                solution_map[self.point(explored_state)] = "◇"

        for move in self.solution:
            solution_map[move] = "◆"


        print("".join(solution_map).replace("#", "█"))

    def find_heristic_value(self, target_coordinate):
        x_dist = abs(self.ending_point[0] - target_coordinate[0])
        y_dist = abs(self.ending_point[1] - target_coordinate[1])
        return x_dist + y_dist

    def solve(self):
        for action in self.find_moves(self.starting_point):
            child_node = Node(self.starting_point,None,action,self.find_heristic_value(action),1)
            self.frontier_class.add(child_node)

        while True:
            if len(self.frontier_class.frontier) == 0:
                print("No Solution!")
                return

            current_node = getattr(self.frontier_class,self.search_method)()

            if self.layout[(self.point(current_node.action))] == "E":
                print("Found path!")

                while current_node.parent != None:
                    self.solution.append(self.point(current_node.state))
                    current_node = current_node.parent
                return

            self.explored.append(current_node.action)

            for action in self.find_moves(current_node.action):
                if self.check_explored(action):
                    continue

                child_node = Node(current_node.action,current_node,action,self.find_heristic_value(action),current_node.cost + 1)
                self.frontier_class.add(child_node)



class Node():
    def __init__(self,state,parent,action,heuristic,cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic = heuristic
        self.cost = cost

class stackfrontier():
    def __init__(self):
        self.frontier = []

    def add(self,node):
        self.frontier.append(node)

    def BFS(self):
        return self.frontier.pop(0)

    def DFS(self):
        return self.frontier.pop(-1)

    def GBFS(self):
        greedy_node = min(self.frontier,key = lambda node: node.heuristic)
        self.frontier.remove(greedy_node)
        return greedy_node

    def A_star(self):
        A_star_node = min(self.frontier,key = lambda node: node.cost + node.heuristic)
        self.frontier.remove(A_star_node)
        return A_star_node

solver = maze_solver("Maze/Maze_2.txt", "GBFS")
start = perf_counter()
solver.solve()
print("Time Taken: ", perf_counter() - start, "seconds")
solver.print_solution(print_explred_states=True)
print("Explored State: ", len(solver.explored))