
import math
import ball

pythag = lambda x1, y1, x2, y2: math.hypot(x1 - x2, y1 - y2)

class DisplacementError(Exception):
    pass


class RockSensor(object):

    def __init__(self, ball, do_debug):
        self.ball = ball
        self.DEBUG = do_debug
        self.is_rockpoint = None

    def set_debug(self, enabled):
        self.DEBUG = enabled

    def set_rockpoint_fn(self, is_rockpoint_fn):
        self.is_rockpoint = is_rockpoint_fn




class DisplacementSensor(RockSensor):
    

    def displacement(self, ctr_x, ctr_y):
        """
        calculate the displacement of the ball from its desired center

        work from the inside out.  stop on the first rock point; the displacement is
        ((r + k) - x, (r + k) - y) where r is the overall radius 
                                     and k is a fudge factor that i may not need
        """
        
        if self.is_rockpoint((ctr_x, ctr_y)): 
            raise DisplacementError("No allowed coverage for %d, %d" % (ctr_x, ctr_y))

        k = 1
        for (x, y) in self.ball.coverage_sorted(ctr_x, ctr_y, True):
            if self.is_rockpoint((x, y)):
                r = pythag(ctr_x, ctr_y, x, y) + k
                return (r - x, r - y)
            
        return (0, 0)



class ProximitySensor(RockSensor):
    """ 
    this class uses the "ball" argument to indicate how far around each point should be checked for rocks
    """

    def proximity(self, ctr_x, ctr_y, whitelist_hash=None):
        """
        find the distance of the closest rock point
        """

        for (x, y) in self.ball.coverage_sorted(ctr_x, ctr_y, True):
            #if whitelist_hash is not None and (x, y) not in whitelist_hash: continue
            #if self.is_rockpoint((x, y)):
            if (x, y) not in whitelist_hash:
                return pythag(ctr_x, ctr_y, x, y)

        return None
