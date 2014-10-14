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
            return None
        return Distance(d, 'HD')

    def distance3d(self, p1, p2):
        try:
            d = math.sqrt((p2.e - p1.e) ** 2 + (p2.n - p1.n) ** 2 + (p2.z - p1.z) ** 2)
        except (ValueError, TypeError):
            return None
        return Distance(d, 'SD')

    def bearing(self, p1, p2):
        """
            Calculate whole circle bearing
        """
        # TODO exception handling
        try:
            wcb = math.atan2(p2.e - p1.e, p2.n - p1.n)
            while wcb < 0:
                wcb = wcb + 2.0 * math.pi
        except TypeError:
            return None
        return Angle(wcb)


    def zenithangle(self, st, obs):
        """
            Calculate zenith angle between a station and an observation point
            :param st station (Station)
            :param obs: observation from the station (PolarObservation)
            :return zenith angle in radian
        """
#        try:
#            d = self.distance( st.p, obs.tp )
#            dz = (obs.tp.z + obs.th) - (st.p.z + st.ih)
#            if math.abs(dz) > 0.0:
#                z = math.atan( d / dz)
#                if dz < 0.0:
#                    z = math.pi + z
#            else:
#                z = math.pi / 2.0   # 90 degree zenith
#        except (ValueError, TypeError):
#            return None
#        return Angle(z)

    def zenithangle(self, p1, p2, ih=0, th=0):
        """
            Calculate zenith angle between two points
            :param p1 coordinates of station
            :param p2 coordinates of reference point
            :param ih instrument height (optional, default 0)
            :param th target height (optional, default 0)
            :return zenith angle in radian
        """
        try:
            d = self.distance( p1, p2 )
            dz = (p2.z + th) - (p1.z + ih)
            if math.abs(dz) > 0.0:
                z = math.atan( d / dz)
                if dz < 0.0:
                    z = math.pi + z
            else:
                z = math.pi / 2.0   # 90 degree zenith
        except (ValueError, TypeError):
            return None
        return Angle(z)
    
    def intersection(self, s1, obs1, s2, obs2):
        """
            Calculate intersection
            :param s1: station 1 (Station)
            :param obs1: observation from station 1 (PolarObservation)
            :param s2: station 2 (Station)
            :param obs2: observation from station 2 (PolarObservation)
        """
        if obs1.target != obs2.target:
            return None
        try:
            b1 = s1.o.hz.get_angle() + obs1.hz.get_angle()
            sb1 = math.sin(b1)
            cb1 = math.cos(b1)
            b2 = s2.o.hz.get_angle() + obs2.hz.get_angle()
            sb2 = math.sin(b2)
            cb2 = math.cos(b2)
            det = sb1 * cb2 - sb2 * cb1
            t1 = ((s2.p.e - s1.p.e) * cb2 - (s2.p.n - s1.p.n) * sb2) / det
            e = s1.p.e + t1 * sb1
            n = s1.p.n + t1 * cb1
            if obs1.pc is None:
                pc = obs2.pc
            else:
                pc = obs1.pc
            return Point(obs1.target, e, n, None, pc)
        except (ValueError, TypeError):
            return None
        
    def circle2P(self, p1, p2, alpha):
        """
            Calculate circle parameters defined by two points and included angle
            :param p1 first point (Point)
            :param p2 second point (Point)
            :param alpha included angle (radian) (Angle)

            Returns center x y and radius as a list or empty list in case of error
            e.g infinit radius, two points are the same
        """
        try:
            t2 = self.distance( p1, p2 ) / 2.0
            d = t2 / math.tan( alpha / 2.0 )
            dab = self.bearing( p1, p2 )
            x3 = p1.n + t2 * math.sin(dab) + d * math.cos(dab)
            y3 = p1.e + t2 * math.cos(dab) - d * math.sin(dab)
        except (ValueError, TypeError):
            return None
#        return __circle3P(p1.y,p1.x,p2.y,p2.x,y3,x3)
        return None
        
    def resection(self, st, obs1, obs2, obs3):
        """
            Calculate resection
            :param st: station (Station)
            :param obs1: observation from station 1 (PolarObservation)
            :param obs2: observation from station 2 (PolarObservation)
            :param obs3: observation from station 3 (PolarObservation)
        """
        if obs1 == obs2 or obs1 == obs3 or obs2 == obs3:
            return
        if obs1.hz is None or obs2.hz is None or obs3.hz is None:
            return
        angle1 = obs2.hz - obs1.hz
        angle2 = obs3.hz - obs2.hz

        circ1 = __circle2P( obs1.tp, obs2.tp, angle1)
        circ2 = __circle2P( obs2.tp, obs3.tp, angle2)
        #res = __intersecCC( circ1, circ2 )
    
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
    s1o = PolarObservation('station_1', Angle(0))
    s2o = PolarObservation('station_2', Angle(0))
    s1 = Station(p1, s1o)
    s2 = Station(p2, s1o)
    o1 = PolarObservation("p", Angle(25, "DEG"))
    o2 = PolarObservation("p", Angle(310, "DEG"))
    p3 = sc.intersection(s1, o1, s2, o2)
    print p3.e, p3.n
