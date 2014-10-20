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
            :param st: station (Station)
            :param ref_list list of [Point, PolarObservation] lists
            :return average orient angle in radians or
                None if no reference direction at all or in case of error
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
    def polarpoint(st, obs):
        b = st.o.hz.get_angle() + obs.hz.get_angle()
        e = st.p.e + obs.horiz_dist() * math.sin(b)
        n = st.p.n + obs.horiz_dist() * math.cos(b)
        return Point("@",e,n)

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
        pp = intersecLL(s1.p, s2.p, b1, b2)
        if obs1.pc is None:
            pc = obs2.pc
        else:
            pc = obs1.pc
        pp.id = obs1.target
        pp.pc = pc
        return pp


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
        points = intersecCC(circ1, circ2)

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
    o101ori = PolarObservation("station_101")
    s101ori = Station( p101ori, o101ori )
    o102ori = PolarObservation( "102", Angle("268-14-13", "DMS") )
    o103ori = PolarObservation( "103", Angle("80-57-34", "DMS") )
    o104ori = PolarObservation( "104", Angle("105-53-19", "DMS") )
    z101ori = Calculation.orientation(s101ori, [[p102ori,o102ori], [p103ori,o103ori], [p104ori,o104ori]])
    print z101ori.get_angle('DMS');
    o201ori = PolarObservation("station_201")
    s201ori = Station( p201ori, o201ori )
    o202ori = PolarObservation( "202", Angle("316-40-57", "DMS") )
    o203ori = PolarObservation( "203", Angle("258-22-09", "DMS") )
    o204ori = PolarObservation( "204", Angle("357-19-49", "DMS") )
    z201ori = Calculation.orientation(s201ori, [[p202ori,o202ori], [p203ori,o203ori], [p204ori,o204ori]])
    print z201ori.get_angle('DMS');
    o301ori = PolarObservation("station_301")
    s301ori = Station( p301ori, o301ori )
    o302ori = PolarObservation( "302", Angle("166-10-30", "DMS") )
    o303ori = PolarObservation( "303", Angle("281-13-55", "DMS") )
    z301ori = Calculation.orientation(s301ori, [[p302ori,o302ori], [p303ori,o303ori]])
    print z301ori.get_angle('DMS');
    o401ori = PolarObservation("station_401")
    s401ori = Station( p401ori, o401ori )
    o402ori = PolarObservation( "402", Angle("101-37-23", "DMS") )
    o403ori = PolarObservation( "403", Angle("103-53-37", "DMS") )
    z401ori = Calculation.orientation(s401ori, [[p402ori,o402ori], [p403ori,o403ori]])
    print z401ori.get_angle('DMS');

    # polar points
    p101pol = Point("101", 13456.25, 12569.75)
    p201pol = Point("201", 13102.13, 11990.13)
    p202pol = Point("202", 13569.11, 12788.66)
    p203pol = Point("203", 13861.23, 12001.54)
    o101pol = PolarObservation("station_101")
    s101pol = Station( p101pol, o101pol )
    o201pol = PolarObservation("201", Angle("112-15-15", "DMS"))
    o202pol = PolarObservation("202", Angle("288-06-30", "DMS"))
    o203pol = PolarObservation("203", Angle("45-21-12", "DMS"))
    o9pol = PolarObservation("9", Angle("145-10-16", "DMS"), None, Distance(206.17,"HD") )
    o10pol = PolarObservation("10", Angle("201-30-47", "DMS"), None, Distance(219.38,"HD") )
    z101pol = Calculation.orientation(s101pol, [[p201pol,o201pol], [p202pol,o202pol], [p203pol,o203pol]])
    print z101pol.get_angle('DMS');
    s101pol.o.hz = z101pol
    p9pol = Calculation.polarpoint(s101pol, o9pol)
    p10pol = Calculation.polarpoint(s101pol, o10pol)
    print p9pol.id, p9pol.e, p9pol.n
    print p10pol.id, p10pol.e, p10pol.n

   
