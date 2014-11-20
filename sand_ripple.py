import numpy
import math
import random


# adapted from http://temp.1060research.com/2013/03/SandRipple.java
#  (Tony Butterfield - tab@1060.org)
#  Simulation of sand ripples, code adapted from work by
#  Peter Lamb, Jordan Kwan and Sam Ahn May 1, 2002
#  www.math.hmc.edu/~hosoi/M164/sanddunes.doc

class SandRipple(object):

    def __init__(self):
        pass

    # @w: width in pixels
    # @h: height in pixels
    def generateOutput(self, w, h):
        data = self.generateInitial(w, h, 1.0, 10.0, 0)
        data = self.ripples2(data, 20.0, 0.5, 0.0, 0.0, 0.1, 0.8, 0, 200)
        self.normalize(data, 255.0)


    # @aArray: float[][] - the 2D array to be normalized
    # @z: float          - the normalization factor
    def normalize(self, aArray, z):
        v_min = None
        v_max = None

        for col in aArray:
            for v in col:
                if v_min is None or v < v_min:
                    v_min = v
                if v_max is None or v_max < v:
                    v_max = v

        f = z / (v_max - v_min)

        for i, col in enumerate(aArray):
            for j, v in enumerate(col):
                aArray[i][j] = (v - v_min) * f



    # return 2d height map with v
    def generateInitial(self, w, h, aHeightVariation, aHeightOffset, aSeed):
        random.seed(aSeed)
        return [[random.gauss(aHeightOffset, aHeightVariation) for _ in range(h)] for __ in range(w)]


    """
    * @param H 2d float array containing initial random heights to seed algorithm
    * @param hopX the distance that sand will hop when blown by wind
    * @param windX strength of wind
    * @param hopY the distance that sand will hop when blown by wind
    * @param windY strength of wind
    * @param grain size of grains moved
    * @param gravity strength of gravity (used to smooth sand)
    * @param critAng (unused as of yet)
    * @param numsteps number of iterations of algorithm
    * @return 2d float array containing sand ripples as heightmap hopefully
    """
    def ripples2(self, H, hopX, windX, hopY, windY, grain, gravity, critAng, numsteps):

        # surprisingly, python doesn't build this in
        def sign(x):
            if x < 0: return -1
            if 0 < x: return 1
            return 0

        cols = len(H)
        rows = len(H[0])

        Hodd = [col[:] for col in H]

        for currstep in range(numsteps):
            # blow Hodd to Heven
            Heven = [col[:] for col in Hodd]

            for x in range(rows):
                for y in range(cols):

                    # here we define the coordinates for all surrounding neighbors of a point
                    xU = (x - 1) % rows
                    xD = (x + 1) % rows
                    yL = (y - 1) % cols
                    yR = (y + 1) % cols

                    # positions of the neighbors
                    hLU = Hodd[xU][yL]; hU  = Hodd[xU][y]; hRU = Hodd[xU][yR]
                    hL  = Hodd[x][yL];  h   = Hodd[x][y];  hR  = Hodd[x][yR]
                    hLD = Hodd[xD][yL]; hD  = Hodd[xD][y]; hRD = Hodd[xD][yR]

                    # SALTATION

                    # define the gradient of the cliff
                    delHx = hD - h
                    delHy = hR - h
                    delH  = sign(delHx) * math.hypot(delHx, delHy)

                    # hop length depends on height and slope
                    hopLengthX = (hopX + windX * h) * (1 - math.tanh(delHx))
                    hopLengthY = (hopY + windY * h) * (1 - math.tanh(delHy))

                    # the amount of grains transported depends on the slope, delH
                    grainAmt = -1.0 * grain * (1 + math.tanh(delH))

                    # this is where the grains blow
                    blowToX = int(round(x + hopLengthX)) % cols
                    blowToY = int(round(y + hopLengthY)) % rows

                    Heven[x][y] = Heven[x][y] - grainAmt
                    Heven[blowToX][blowToY] = Heven[blowToX][blowToY] + grainAmt;

                    # CREEP due to gravity
                    firstNbrSum = 0.16666 * ( hU + hD + hL + hR )       # here we're taking a weighted sum of the 4 immediate neighbors
                    secondNbrSum = 0.083333 * ( hLU + hRU + hLD + hRD)  # we take a less-weighted sum of the four "corner neighbors"
                    Heven[x][y] = Heven[x][y] + gravity * (firstNbrSum + secondNbrSum - h);
                    # TODO: this looks wrong because we are not transferring sand...

                    #  AVALANCHE if the slope gets too big

                    sandIndex = []
                    b = []

                    # TODO: integer 1,2,3,4 represent enum values
                    if ((h - hR) > math.tan(critAng)):
                        sandIndex.append(1)
                        b.append(math.tan(critAng) + hR - h)

                    if (h - hRD) / (math.sqrt(2)) > math.tan(critAng):
                        sandIndex.append(2)
                        b.append(math.sqrt(2) * math.tan(critAng) + hRD - h)

                    if (h - hD) > math.tan(critAng):
                        sandIndex.append(3)
                        b.append(math.tan(critAng) + hD - h)

                    if (h - hLD) / (math.sqrt(2)) > math.tan(critAng):
                        sandIndex.append(4)
                        b.append(math.sqrt(2) * math.tan(critAng) + hLD - h)

                    # create matrix of -1s with -2s on the diagonal
                    n = len(b)
                    if 0 < n:
                        A = [[-2 if i == j else -1 for i in range(n)] for j in range(n)]

                        sandShift = numpy.linalg.solve(numpy.array(A), numpy.array(b))

                        for i, o in enumerate(sandIndex):
                            shift = sandShift[i]
                            if o == 1:
                                Heven[x][yR] = hR + shift
                            elif o == 2:
                                Heven[xD][yR] = hRD + shift
                            elif o == 3:
                                Heven[xD][y] = hD + shift
                            elif o == 4:
                                Heven[xD][yL] = hLD + shift

                        Heven[x][y] -= sum(sandShift)

            Hodd = [col[:] for col in Heven]

        return Hodd;
