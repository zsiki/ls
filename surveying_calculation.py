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

    def __intersecLL(self, pa, pb, dap,dbp):
        """
            Calculate intersection of two lines solving
                xa + t1 * sin dap = xb + t2 * sin dbp
                ya + t1 * cos dap = yb + t2 * cos dbp
            :param pa first point
            :param pb  second point
            :param dap direction (bearing) from first point to new point
            :param dbp direction (bearing) from second point to new point
            :return xp yp as a list or an empty list if lines are near paralel
        """
        
        try:
            sdap = math.sin(dap)
            cdap = math.cos(dap)
            sdbp = math.sin(dbp)
            cdbp = math.cos(dbp)
            det = sdap*cdbp - sdbp*cdap
            
            if det==0:  # paralel lines
                return None;
            t1 = ((pb.e - pa.e) * cdbp - (pb.n - pa.n) * sdbp) / det
        
            e = pa.e + t1 * sdap
            n = pa.n + t1 * cdap
            return Point("",e,n)
        except (ValueError, TypeError):
            return None


    class __Circle(object):
        """
            circle: center easting, center northing, radius
        """
        def __init__(self, e, n, r):
            """
                :param e center easting (float)
                :param n center northing (float)
                :param r radius (float)
            """
            self.e = e
            self.n = n
            self.r = r

    def __circle3P(self, p1, p2, p3):
        """
            Calculate circle parameters defined by three points
            center is the intersection of orthogonals at the midpoints
            @param p1: first point
            @param p2: second point
            @param p3: third point
            @return center x y and radius (Circle) or None in case of error
            e.g infinit radius, two points are the same
        """

        try:
            # midpoints
            midp12 = Point( "", (p1.e + p2.e) / 2.0,  (p1.n + p2.n) / 2.0 )
            midp23 = Point( "", (p2.e + p3.e) / 2.0,  (p2.n + p3.n) / 2.0 )
            d12 = self.bearing( p1, p2 ).get_angle() + math.pi / 2.0
            d23 = self.bearing( p2, p3 ).get_angle() + math.pi / 2.0

            pcenter = self.__intersecLL( midp12, midp23, d12, d23 )
            
            if pcenter is not None:
                r = self.distance( pcenter, p1 ).d
                return self.__Circle( pcenter.e, pcenter.n, r)

            return None
        except (ValueError, TypeError):
            return None

    def __circle2P(self, p1, p2, alpha):
        """
            Calculate circle parameters defined by two points and included angle
            :param p1: first point (Point)
            :param p2: second point (Point)
            :param alpha: included angle (radian) (Angle)

            @return center x y and radius (Circle) or None in case of error
            e.g infinit radius, two points are the same
        """
        try:
            t2 = self.distance( p1, p2 ).d / 2.0
            d = t2 / math.tan( alpha / 2.0 )
            dab = self.bearing( p1, p2 )
            e3 = p1.e + t2 * math.sin(dab.get_angle()) + d * math.cos(dab.get_angle())
            n3 = p1.n + t2 * math.cos(dab.get_angle()) - d * math.sin(dab.get_angle())
            p3 = Point( "", e3, n3 )
            return self.__circle3P( p1, p2, p3 )
        except (ValueError, TypeError):
            return None

    def __intersecCC(self, circle1, circle2):
        """
            Calculate intersection of two circles solving 
                (x - x01)^2 + (y - y01)^2 = r1^2
                (x - x02)^2 + (y - y02)^2 = r2^2
            :param circle1: center coordinates and radius of first circle (Circle)
            :param circle2: center coordinates and radius of first circle (Circle)

            :return two, one or none intersection as a list
        """
        try:
            swap = 0
            if math.fabs( circle2.e - circle1.e ) < 0.001:
                w = circle1.e
                circle1.e = circle1.n
                circle1.n = w
                w = circle2.e
                circle2.e = circle2.n
                circle2.n = w
                swap = 1

            t = ( circle1.r ** 2 - circle1.e ** 2 - circle2.r ** 2 + \
                  circle2.e ** 2 + circle2.n ** 2 - circle1.n ** 2 ) / 2.0
            de = circle2.e - circle1.e
            dn = circle2.n - circle1.n

            if math.fabs(de) > 0.001:
                a = 1.0 + dn * dn / de / de
                b = 2.0 * (circle1.e * dn / de - circle1.n - t * dn / de / de )
                c = t * t / de / de - 2 * circle1.e * t / de - circle1.r ** 2 + \
                    circle1.e ** 2 + circle1.n ** 2
                d = b * b - 4 * a * c
                if d < 0:
                    return None

                np1 = (-b + math.sqrt(d)) / 2.0 / a
                np2 = (-b - math.sqrt(d)) / 2.0 / a
                ep1 = (t - dn * np1) / de
                ep2 = (t - dn * np2) / de
                if swap == 0:
                    return [ Point("",ep1,np1), Point("",ep2,np2) ]
                else:
                    return [ Point("",np1,ep1), Point("",np2,ep2) ]

            return None
        except (ValueError, TypeError):
            return None

    def resection(self, st, p1, p2, p3, obs1, obs2, obs3):
        """
            Calculate resection
            :param st: station (Station)
            :param p1: first control point (Point)
            :param p2: second control point (Point)
            :param p3: third control point (Point)
            :param obs1: observation from st to p1 (PolarObservation)
            :param obs2: observation from st to p2 (PolarObservation)
            :param obs3: observation from st to p3 (PolarObservation)
            :return coordinates of the resection point (st) if it can be calculated; otherwise None
        """
        if p1 == p2 or p1 == p3 or p2 == p3:
            return
        if obs1.target == obs2.target or obs1.target == obs3.target or obs2.target == obs3.target:
            return
        if obs1.hz is None or obs2.hz is None or obs3.hz is None:
            return
        # TODO this has to be considered
        
        try:
            angle1 = obs2.hz.get_angle() - obs1.hz.get_angle()
            angle2 = obs3.hz.get_angle() - obs2.hz.get_angle()

            circ1 = self.__circle2P( p1, p2, angle1 )
            circ2 = self.__circle2P( p2, p3, angle2 )
            points = self.__intersecCC( circ1, circ2 )
    
            if len(points) == 2:
                #    select the right one from the two intersection points
                if math.fabs(p2.e - points[0].e) < 0.1 and math.fabs(p2.n - points[0].n) < 0.1:
                    return Point(st.p.id, points[1].e, points[1].n, None, st.p.pc)
                else :
                    return Point(st.p.id, points[0].e, points[0].n, None, st.p.pc)
            return None

        except (ValueError, TypeError):
            return None

if __name__ == "__main__":
    """
        unit test
    """
    sc = SurveyingCalculation()
    #p1 = Point("1", 100, 200, 10)
    p1 = Point("1", 100, 200, 20)
    p2 = Point("2", 150, 250, 30)
    d = sc.distance(p1, p2)
    print d.d
    d = sc.distance3d(p1, p2)
    print d.d
    b = sc.bearing(p1, p2)
    print b.get_angle('DMS');
    
    # intersection test
    s1o = PolarObservation('station_1', Angle(0))
    s2o = PolarObservation('station_2', Angle(0))
    s1 = Station(p1, s1o)
    s2 = Station(p2, s1o)
    o1 = PolarObservation("p", Angle(25, "DEG"))
    o2 = PolarObservation("p", Angle(310, "DEG"))
    p3 = sc.intersection(s1, o1, s2, o2)
    print p3.id, p3.e, p3.n
    
    # resection test
    p1res = Point("3")
    o1res = PolarObservation( "station_3", Angle(0) )
    s1res = Station( p1res, o1res )
    p101res = Point( "101", 658031.813, 247985.580 )
    p102res = Point( "102", 657638.800, 247759.380 )
    p103res = Point( "103", 658077.700, 247431.381 )
    o101res = PolarObservation( "101", Angle("22-45-56", "DMS") )
    o102res = PolarObservation( "102", Angle("164-38-59", "DMS") )
    o103res = PolarObservation( "103", Angle("96-23-12", "DMS") )
    p1res = sc.resection( s1res, p101res, p102res, p103res, o101res, o102res, o103res )
    print p1res.id, p1res.e, p1res.n
    # so657871.95 247973.24
