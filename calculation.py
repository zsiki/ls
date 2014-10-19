#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Surveying calculation for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

import math
from base_classes import *

class Calculation(object):
    """ container class for all calculations """

    def __init__(self):
        pass

    @staticmethod
    def orientation(st, ref_list):
        """
            Orientation calculation for a station
            reference angles are added to geo data set with    code 100/102 
            the station gets the average of reference angles with code 101/103
            :param st: station (Station)
            :param ref_list list of [Point, PolarObservation] lists
            :return average orient angle in radians or
                -2 if no reference direction at all or
                -1 in case of error
        """
        sz = 0
        cz = 0
        sd = 0
        for ref in ref_list:
            pt = ref[0]
            obs = ref[1]
            b = bearing(st.p, pt).get_angle()
            z = b - obs.hz.get_angle()
            if z<0:
                z = z + math.pi * 2
            d = distance2d(st.p, pt).d
            sd = sd + d
            sz = sz + math.sin(z) * d
            cz = cz + math.cos(z) * d
 
        if sd==0:
            return None
        
        sz = sz / sd
        cz = cz / sd
        za = math.atan2(sz, cz)                    ;# average orient angle
        while za<0:
            za = za + math.pi * 2
        
        return Angle(za)

    @staticmethod
    def intersection(s1, obs1, s2, obs2):
        """
            Calculate intersection
            :param s1: station 1 (Station)
            :param obs1: observation from station 1 (PolarObservation)
            :param s2: station 2 (Station)
            :param obs2: observation from station 2 (PolarObservation)
        """
        if obs1.target != obs2.target:
            return None
        b1 = s1.o.hz.get_angle() + obs1.hz.get_angle()
        b2 = s2.o.hz.get_angle() + obs2.hz.get_angle()
        pp = Calculation.intersecLL(s1.p, s2.p, b1, b2)
        if obs1.pc is None:
            pc = obs2.pc
        else:
            pc = obs1.pc
        pp.id = obs1.target
        pp.pc = pc
        return pp

    @staticmethod
    def intersecLL(pa, pb, dap, dbp):
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
        from base_classes import Point
        
        try:
            sdap = math.sin(dap)
            cdap = math.cos(dap)
            sdbp = math.sin(dbp)
            cdbp = math.cos(dbp)
            det = sdap*cdbp - sdbp*cdap
            
            t1 = ((pb.e - pa.e) * cdbp - (pb.n - pa.n) * sdbp) / det
        
            e = pa.e + t1 * sdap
            n = pa.n + t1 * cdap
            return Point("@",e,n)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def __intersecCC(circle1, circle2):
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
            if math.fabs( circle2.p.e - circle1.p.e ) < 0.001:
                w = circle1.p.e
                circle1.p.e = circle1.p.n
                circle1.p.n = w
                w = circle2.p.e
                circle2.p.e = circle2.p.n
                circle2.p.n = w
                swap = 1

            t = ( circle1.r ** 2 - circle1.p.e ** 2 - circle2.r ** 2 + \
                  circle2.p.e ** 2 + circle2.p.n ** 2 - circle1.p.n ** 2 ) / 2.0
            de = circle2.p.e - circle1.p.e
            dn = circle2.p.n - circle1.p.n

            if math.fabs(de) > 0.001:
                a = 1.0 + dn * dn / de / de
                b = 2.0 * (circle1.p.e * dn / de - circle1.p.n - t * dn / de / de )
                c = t * t / de / de - 2 * circle1.p.e * t / de - circle1.r ** 2 + \
                    circle1.p.e ** 2 + circle1.p.n ** 2
                d = b * b - 4 * a * c
                if d < 0:
                    return None

                np1 = (-b + math.sqrt(d)) / 2.0 / a
                np2 = (-b - math.sqrt(d)) / 2.0 / a
                ep1 = (t - dn * np1) / de
                ep2 = (t - dn * np2) / de
                if swap == 0:
                    return [ Point("@",ep1,np1), Point("@",ep2,np2) ]
                else:
                    return [ Point("@",np1,ep1), Point("@",np2,ep2) ]

            return None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def resection(st, p1, p2, p3, obs1, obs2, obs3):
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
        #try:
        angle1 = Angle(obs2.hz.get_angle() - obs1.hz.get_angle())
        angle2 = Angle(obs3.hz.get_angle() - obs2.hz.get_angle())
        
        circ1 = Circle(p1, p2, angle1)
        print circ1.p.e, circ1.p.n, circ1.r
        circ2 = Circle(p2, p3, angle2)
        print circ2.p.e, circ2.p.n, circ2.r
        points = Calculation.__intersecCC(circ1, circ2)

        if len(points) == 2:
            #    select the right one from the two intersection points
            if math.fabs(p2.e - points[0].e) < 0.1 and math.fabs(p2.n - points[0].n) < 0.1:
                return Point(st.p.id, points[1].e, points[1].n, None, st.p.pc)
            else :
                return Point(st.p.id, points[0].e, points[0].n, None, st.p.pc)
        return None

        #except (ValueError, TypeError):
        #    return None

if __name__ == "__main__":
    """
        unit test
    """
    #p1 = Point("1", 100, 200, 10)
    p1 = Point("1", 100, 200, 20)
    p2 = Point("2", 150, 250, 30)
    d = distance2d(p1, p2)
    print d.d
    d = distance3d(p1, p2)
    print d.d
    b = bearing(p1, p2)
    print b.get_angle('DMS');
    
    # intersection test
    s1o = PolarObservation('station_1', Angle(0))
    s2o = PolarObservation('station_2', Angle(0))
    s1 = Station(p1, s1o)
    s2 = Station(p2, s1o)
    o1 = PolarObservation("p", Angle(25, "DEG"))
    o2 = PolarObservation("p", Angle(310, "DEG"))
    p3 = Calculation.intersection(s1, o1, s2, o2)
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
    p1res = Calculation.resection( s1res, p101res, p102res, p103res, o101res, o102res, o103res )
    print p1res.id, p1res.e, p1res.n
    # so657871.95 247973.24
    
    #orientation
    p101ori = Point( "101", 5693.45, 328.81 )
    p102ori = Point( "102", 6002.13, 1001.13 )
    p103ori = Point( "103", 5511.25, -253.16 )
    p104ori = Point( "104", 5033.45, -396.15 )
    p201ori = Point( "201", -4396.15, -561.13 )
    p202ori = Point( "202", -4000.55, 496.14 )
    p203ori = Point( "203", -5115.33, 366.11 )
    p204ori = Point( "204", -3863.96, -268.15 )
    p301ori = Point( "301", 4512.35, -496.29 )
    p302ori = Point( "302", 4073.16, -986.32 )
    p303ori = Point( "303", 3952.25, 818.66 )
    p401ori = Point( "401", -3516.22, 156.25 )
    p402ori = Point( "402", -3986.35, 460.18 )
    p403ori = Point( "403", -4019.28, 510.54 )
    o101ori = PolarObservation( "station_101", Angle(0) )
    s101ori = Station( p101ori, o101ori )
    o102ori = PolarObservation( "102", Angle("268-14-13", "DMS") )
    o103ori = PolarObservation( "103", Angle("80-57-34", "DMS") )
    o104ori = PolarObservation( "104", Angle("105-53-19", "DMS") )
    z101ori = Calculation.orientation(s101ori, [[p102ori,o102ori], [p103ori,o103ori], [p104ori,o104ori]])
    print z101ori.get_angle('DMS');
    o201ori = PolarObservation( "station_201", Angle(0) )
    s201ori = Station( p201ori, o201ori )
    o202ori = PolarObservation( "202", Angle("316-40-57", "DMS") )
    o203ori = PolarObservation( "203", Angle("258-22-09", "DMS") )
    o204ori = PolarObservation( "204", Angle("357-19-49", "DMS") )
    z201ori = Calculation.orientation(s201ori, [[p202ori,o202ori], [p203ori,o203ori], [p204ori,o204ori]])
    print z201ori.get_angle('DMS');
    o301ori = PolarObservation( "station_301", Angle(0) )
    s301ori = Station( p301ori, o301ori )
    o302ori = PolarObservation( "302", Angle("166-10-30", "DMS") )
    o303ori = PolarObservation( "303", Angle("281-13-55", "DMS") )
    z301ori = Calculation.orientation(s301ori, [[p302ori,o302ori], [p303ori,o303ori]])
    print z301ori.get_angle('DMS');
    o401ori = PolarObservation( "station_401", Angle(0) )
    s401ori = Station( p401ori, o401ori )
    o402ori = PolarObservation( "402", Angle("101-37-23", "DMS") )
    o403ori = PolarObservation( "403", Angle("103-53-37", "DMS") )
    z401ori = Calculation.orientation(s401ori, [[p402ori,o402ori], [p403ori,o403ori]])
    print z401ori.get_angle('DMS');
    
