
class SearchError(Exception):
    pass


class IDAStar:
    # cost_fn(node, successor) is the path cost function from node to successor
    # is_goal_fn(node) returns boolean
    # h_fn(node) is the heuritic function
    def __init__(self, cost_fn, is_goal_fn, h_fn, successors_fn):
        self.cost       = cost_fn
        self.is_goal    = is_goal_fn
        self.h          = h_fn
        self.successors = successors_fn

    
    # solve, given a root.  return solution or None
    def solve(self, root):

        bound = self.h(root)

        while(True):
            (next_bound, solution) = self.search(root, 0, bound)
            # return solution or deepen search
            if solution is not None: return solution
            if next_bound is None:   return None
            bound = next_bound
        

    # returns (next_bound, solution) 
    #          "next_bound is None" means dead end node
    #            "solution is None" means dead end branch
    def search(self, node, g, bound):
        f = g + self.h(node)
        if f > bound:          return (f, None)
        if self.is_goal(node): return (f, node)
        min_bound = None
        for succ in self.successors(node):
            (next_bound, solution) = self.search(succ, g + self.cost(node, succ), bound)
            # return solution or set next search depth
            if solution is not None:     return (f, solution)
            elif min_bound is None:      min_bound = next_bound
            elif min_bound > next_bound: min_bound = next_bound

        return (min_bound, None)
                            