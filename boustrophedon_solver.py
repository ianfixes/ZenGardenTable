
from sensor import DisplacementSensor, DisplacementError
from ida_star import IDAStar

DEBUG = False


class BoustrophedonSolver(object):

    def __init__(self, table, ball_radius):
        self.table = table
        self.rockpoint = table.get_rockpoint()
        self.canvas = table.drawing_area
        self.radius = ball_radius
        self.sensor = DisplacementSensor(self.radius, DEBUG)
        self.covered = None
        self.visited = None
        self.path = None


    def reset(self):
        self.covered_first_point = False
        self.covered = [[False for y in col] for col in self.rockpoint]
        self.visited = [[False for y in col] for col in self.rockpoint]
        self.path = []


    def is_covered(self, point):
        x, y = point
        return self.covered[x][y]

    def is_visited(self, point):
        x, y = point
        return self.visited[x][y]

    def get_visited_list(self):
        ret = []
        for x, row in enumerate(self.visited):
            for y, is_visited in enumerate(row):
                if is_visited:
                    ret.append((x, y))
        return ret


    def visit_point(self, x, y):
        try:
            d = self.sensor.displacement(x, y, self.is_rockpoint) #, coverage)
            if (0, 0) != d:
                # we have detected a rock
                return False

            # else no rock exists at this location
            self.visited[x][y] = True

            # update info on where we "went"
            self.path.append((x, y, True))

            # mark points underneath ball as covered
            # use full coverage the first time, but all other times we can just cover the shell
            if self.covered_first_point:
                coverage = self.sensor.ball_shell(x, y)
            else:
                self.covered_first_point = True
                coverage = self.sensor.ball_coverage(x, y)

            for xc, yc in coverage:
                self.covered[xc][yc] = True
        except DisplacementError:
            print "DISPLACEMENT ERROR"
            return False
        except IndexError:
            print "failed", xc, yc
            raise
        except:
            raise

        return True


    def is_ball_contained(self, x, y):
        lo = self.radius - 1
        hi = len(self.rockpoint) - self.radius
        if x < lo: return False
        if x > hi: return False
        if y < lo: return False
        if y > hi: return False
        return True

    # use fake omnipotent algorithm to exercise coverage algorithm
    def cover_bogo(self):
        for x, row in enumerate(self.rockpoint):
            print "testing col", x
            for y, is_rock in enumerate(row):
                if not self.is_ball_contained(x, y): continue
                #print "testing ", x, y
                # test coverage and verify no displacement
                self.visit_point(x, y)


    # where position is (x, y)
    def cover_floodfill(self):

        flood_covered = [[False for y in col] for col in self.rockpoint]

        # return all manhattan neighbors
        def get_neighbors(xx, yy):
            return filter(self.is_in_bounds, [
                    (xx - 1, yy),
                    (xx, yy - 1),
                    (xx + 1, yy),
                    (xx, yy + 1),
                    ])

        S = [(self.radius + 1, self.radius + 1)] # start at 10,10 for funsies
        while 0 < len(S):
            (x, y) = S.pop()
            #print "Covering", x, y
            # only get neighbors of points with no displacement... otherwise dead end
            if not flood_covered[x][y]:
                flood_covered[x][y] = True
                if not self.visit_point(x, y): continue

            for neighbor in get_neighbors(x, y):
                xx, yy = neighbor
                if not flood_covered[xx][yy]:
                    if self.is_ball_contained(xx, yy):
                        S.append(neighbor)



    # where position is (x, y)
    def cover_xytable(self):
        total_distance = 0

        flood_covered = [[False for y in col] for col in self.rockpoint]

        # return all manhattan neighbors
        def get_neighbors(loc):
            xx, yy = loc
            return filter(self.is_in_bounds, [
                    (xx - 1, yy),
                    (xx, yy - 1),
                    (xx + 1, yy),
                    (xx, yy + 1),
                    ])


        S = [(self.radius + 1, self.radius + 1)] # start at 10,10 for funsies
        self.visited[self.radius + 1][self.radius + 1] = True
        current_location = S[0]
        while 0 < len(S):
            new_loc = S.pop()
            (x, y) = new_loc
            (x0, y0) = current_location

            # don't do all this twice
            if flood_covered[x][y]: continue
            flood_covered[x][y] = True

            print current_location, "to", new_loc

            # set up the path planner, from the new point back to the current point
            # IDAStar(cost_fn, is_goal_fn, h_fn, successors_fn)
            cost_fn = lambda _, __  : 1
            h_fn = lambda path : abs(path[0][0] - x0) + abs(path[0][1] - y0) # manhattan distance
            is_goal_fn = lambda path : path[0] == current_location
            successors_fn = lambda path : [[n] + path
                                           for n in get_neighbors(path[0])
                                           if n not in path and (self.is_visited(n)
                                                                 or n == current_location
                                                                 or n == new_loc)]
            is_goal_fn = lambda path : path[-1] == current_location
            successors_fn = lambda path : [path + [n]
                                           for n in get_neighbors(path[-1])
                                           if n not in path and (self.is_visited(n)
                                                                 or n == current_location
                                                                 or n == new_loc)]
            path_planner = IDAStar(cost_fn, is_goal_fn, h_fn, successors_fn, self.hack_draw_planned_path)

            # steps to get us to new location
            current_to_new_location = path_planner.solve([new_loc])
            if current_to_new_location is None:
                self.draw_pathplan_failure(current_location, new_loc)
                raise AssertionError("Couldn't go from " + str(current_location) + " to " + str(new_loc))

            print "path plan complete", len(current_to_new_location)

            # now pretend we've arrived
            current_location = new_loc

            # actually  visit points
            total_distance += len(current_to_new_location) - 1
            self.path += [(xx, yy, False) for (xx, yy) in current_to_new_location[1:-1]]


            # only get neighbors of points with no displacement... otherwise dead end
            if not self.visit_point(x, y): continue

            # add new neighbors to the list of places we need to check
            for neighbor in get_neighbors(new_loc):
                xx, yy = neighbor
                if not flood_covered[xx][yy]:
                    if self.is_ball_contained(xx, yy):
                        S.append(neighbor)

        print "Total distance is", total_distance,
        print "which has % efficiency", round(100.0 * (len(self.rockpoint) ** 2) / total_distance, 1)


    def solve(self):

        self.reset()

        #self.cover_bogo()
        #self.cover_floodfill()
        self.cover_xytable()

        self.animate_path(self.path)



    # whether a point is in the bounds of the table
    def is_in_bounds(self, point):
        x, y = point
        return 0 <= x < len(self.rockpoint) and 0 <= y < len(self.rockpoint)

    # whether a point is a rock
    def is_rockpoint(self, point):
        x, y = point
        col = self.rockpoint[x]
        if y >= len(col): return True
        return col[y]


    def draw_point(self, x, y, color="black"):
        self.table.draw_point(x, y, color)


    # show point a, point b, and the visited places
    def draw_pathplan_failure(self, p1, p2):
        for p in self.get_visited_list():
            self.draw_point(p[0], p[1], "black")

        self.draw_point(p1[0], p1[1], "yellow")
        self.draw_point(p2[0], p2[1], "yellow")



    def animate_path(self, path):
        self.path_to_animate = path[:]
        self.draw_ball_path()

    def draw_ball_path(self):
        if 0 == len(self.path_to_animate): return

        (x, y, exploratory) = self.path_to_animate.pop(0)
        coverage = self.sensor.ball_shell(x, y)

        for xc, yc in coverage:
            self.draw_point(xc, yc, "yellow")

        if exploratory:
            self.draw_point(x, y, "green")
        else:
            self.draw_point(x, y, "black")

        self.canvas.after(1, self.draw_ball_path)


    def hack_draw_planned_path(self, p1, p2, plan):
        print "drawing visited list...",
        for (x, y) in self.get_visited_list():
            self.draw_point(x, y, "black")
        print "done"

        for (x, y) in plan:
            self.draw_point(x, y, "blue")

        for (x, y) in [p1, p2]:
            self.draw_point(x, y, "green")

        print "updateing idletasks...",
        self.canvas.update_idletasks()
        print "done"


    def example_animate(self):
        self.animation_steps = 100
        self.example_draw_frame()
        print "Animate is done"


    def example_draw_frame(self):
        if 0 >= self.animation_steps:
            print "DONE"
        else:
            print "example_draw_frame"
            p  = self.animation_steps
            np = p - 1

            self.canvas.create_line(p, p, np, np, smooth=False, fill="blue")
            self.animation_steps = np

            #self.update_idletasks()

            self.canvas.after(100, self.example_draw_frame)
