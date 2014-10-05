#!/usr/bin/env python
"""
    Surveying calculation for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

import math
from base_classes import *

class SurveyingCalculation(object):
    """ container class for all calculations """

    def __init__(self):
        pass

    def distance(self, p1, p2):
        try:
            d = math.sqrt((p2.e - p1.e) ** 2 + (p2.n - p1.n) ** 2)
        except (TypeError, ValueError):
            d = None
        return Distance(d, 'HD')

    def distance3d(self, p1, p2):
        try:
            d = math.sqrt((p2.e - p1.e) ** 2 + (p2.n - p1.n) ** 2 + (p2.z - p1.z) ** 2)
        except (ValueError, TypeError):
            d = None
        return Distance(d, 'SD')

    def bearing(self, p1, p2):
        """
            Calculate whole circle bearing
        """
        # TODO exception handling
        try:
            wcb = math.atan2(p2.e - p1.e, p2.n - p1.n)
            while wcb < 0:
                wcb = wcb + PI2
        except TypeError:
            wcb = None
        return Angle(wcb)
    
    def intersection(self, s1, obs1, s2, obs2):
        """
            Calculate intersection
            :param s1: station 1 (Station)
            :param obs1: observation from station 1 (Observation)
            :param s2: station 2 (Station)
            :param obs2: observation from station 2 (Observation)
        """
        if obs1.target != obs2.target:
            return None
        try:
            b1 = s1.o.get_angle() + obs1.hz.get_angle()
            sb1 = math.sin(b1)
            cb1 = math.cos(b1)
            b2 = s2.o.get_angle() + obs2.hz.get_angle()
            sb2 = math.sin(b2)
            cb2 = math.cos(b2)
            det = sb1 * cb2 - sb2 * cb1
            t1 = (s2.p.e - s1.p.e) * cb2 - (s2.p.n - s1.p.n) * sb2 / det
            e = s1.p.e + t1 * sb1
            n = s1.p.n + t1 * cb1
            if obs1.pc is None:
                pc = obs2.pc
            else:
                pc = obs1.pc
            return Point(obs1.target, e, n, None, pc)
        except (ValueError, TypeError):
            return None
        

if __name__ == "__main__":
    """
        unit test
    """
    sc = SurveyingCalculation()
    #p1 = Point("1", 100, 200, 10)
    p1 = Point("1", 100, 200)
    p2 = Point("2", 150, 250, 30)
    d = sc.distance(p1, p2)
    print d.d
    d = sc.distance3d(p1, p2)
    print d.d
    b = sc.bearing(p1, p2)
    print b.get_angle('DMS');
    s1 = Station(p1, Angle(0))
    s2 = Station(p2, Angle(0))
    o1 = PolarObservation("p", Angle(25, "DEG"))
    o2 = PolarObservation("p", Angle(310, "DEG"))
    p3 = sc.intersection(s1, o1, s2, o2)
    print p3.e, p3.n
