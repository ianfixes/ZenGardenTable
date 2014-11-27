
import ball

class ProximityMap(object):

    def __init__(self, width, height, covered_list, visited_list):
        self.width        = width
        self.height       = height
        self.covered_list = covered_list
        self.visited_list = visited_list



    def solve(radius, weight_fn):
        prox = [[None for y in range(self.height)] for x in range(self.width)]

        # for each point in radius of influence, if point is covered then add prox to total prox
        # find a path within min/max proximity in either direction
        

        return prox
