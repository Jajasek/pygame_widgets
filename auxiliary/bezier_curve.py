class Bezier:
    class SmoothnessError(Exception):
        pass

    class CurveError(Exception):
        pass

    def __init__(self):
        """
        A Python class for generating bezier curves

        An implementation of an algorithm presented by Nils Pipenbrinck
        http://www.cubic.org/docs/bezier.htm
        """

    def __lerp(self, ptA, ptB, t):
        """
        Returns the linear interp between two points as a list
        ptA and ptB are a list of xy coords, t is the point on the curve
        """
        dest = []
        dest.append(ptA[0] + float(ptB[0] - ptA[0]) * t)
        dest.append(ptA[1] + float(ptB[1] - ptA[1]) * t)
        return dest

    def bezierPt(self, ctrlPts, t):
        """A recursive function for finding point t along a bezier curve"""
        if len(ctrlPts) == 1:
            # print "Len is 1", ctrlPts
            return ctrlPts[0]
        lerpList = []
        for i in range(len(ctrlPts) - 1):
            ptA = [ctrlPts[i][0], ctrlPts[i][1]]
            ptB = [ctrlPts[i + 1][0], ctrlPts[i + 1][1]]
            lerpList.append(self.__lerp(ptA, ptB, t))
        # print len(lerpList)
        return self.bezierPt(lerpList, t)

    def makeBezier(self, ctrlPts, smoothness):
        """
        Returns a list of points on a bezier curve

        ctrlPts is a list of 2d Points that define the curve, in most cases these
        consist of control point locations and their handles, except in a 3 point
        curve where it's just defined by the three control points.

        smoothness is the number of points on the curve that should be generated.
        This should always be more than two points or generating the bezier curve is
        pointless and the script dies in a fire (or throws an exception)
        """

        if len(ctrlPts) < 2:
            raise self.CurveError("Curve list must contain more than one point")
        if smoothness < 3:
            raise self.SmoothnessError("Smoothness must be more than two")
        iteration = smoothness
        bezierList = []
        subtract = 1.0 / smoothness
        for i in range(0, iteration):
            t = 1.0 - (subtract * i)
            if t < subtract:
                t = 0
            bPt = self.bezierPt(ctrlPts, t)
            # print bPt
            bezierList.append(bPt)
        return bezierList


## Class ends

###################
# An example of how to use the class with pygame


## Pygame Example
import math, pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    b = Bezier()
    """
	A bezier curve definition, a list of 2d poins, simple innit
	It's basically control points with control handle locations before or
	after the control point.

    Read http://www.cubic.org/docs/bezier.htm for more info
    """
    bezierPts = [[40, 100], [80, 20], [150, 180], [260, 100]]
    bLine = b.makeBezier(bezierPts, 10)
    screen.fill((255, 255, 255))
    pygame.draw.aalines(screen, (1, 1, 1), False, bLine, 1)
    pygame.display.flip()
    bounce = False

    while True:
        clock.tick(60)
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == QUIT:
            return
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return
        setTo = pygame.time.get_ticks() / 20
        bezierPts[1][1] = setTo
        bLine = b.makeBezier(bezierPts, 20)
        screen.fill((255, 255, 255))
        pygame.draw.aalines(screen, (1, 1, 1), False, bLine, 1)
        pygame.display.flip()


if __name__ == "__main__":
    main()
