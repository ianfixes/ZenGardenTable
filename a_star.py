import operator
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
        
    def empty(self):
        return len(self.elements) == 0
   
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
   
    def get(self):
        return heapq.heappop(self.elements)[1]



class AStar:
    # cost_fn(node, successor) is the path cost function from node to successor
    # is_goal_fn(node) returns boolean
    # h_fn(node) is the heuritic function
    def __init__(self, cost_fn, is_goal_fn, h_fn, successors_fn, debug_fn = None):
        self.cost       = cost_fn
        self.is_goal    = is_goal_fn
        self.h          = h_fn
        self.successors = successors_fn
        self.debug      = debug_fn


    def hash(self, obj):
        #return str(obj)
        return obj

    # solve, given a root.  return solution or None
    def solve(self, root):
        
        frontier = PriorityQueue()
        frontier.put(root, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self.hash(root)] = None
        cost_so_far[self.hash(root)] = 0

        while not frontier.empty():
            current = frontier.get()

            if self.is_goal(current):
                return self.reconstruct_path(came_from, root, current)

            for succ in self.successors(current):
                if succ in cost_so_far: continue

                new_g = cost_so_far[self.hash(current)] + self.cost(current, succ)
                if succ not in cost_so_far or new_g < cost_so_far[self.hash(succ)]:
                    
                    cost_so_far[self.hash(succ)] = new_g
                    f = new_g + self.h(succ)
                    frontier.put(succ, f)
                    came_from[self.hash(succ)] = current
                    
        return None

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[self.hash(current)]
            path.append(current)
        return path
