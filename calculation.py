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
        # Calculate average orient angle.
        za = math.atan2(sz, cz)
        while za<0:
            za = za + math.pi * 2
        
        return Angle(za)

    @staticmethod
    def polarpoint(st, obs):
        """
            Calculate coordinates of a point measured by an independent radial measurement
            :param st: station (Station)
            :param obs: observation from station to the unknown point (PolarObservation)
            :return the polar point with new coordinates (Point)
        """
        # Calculate the bearing angle between the station and new point.
        b = st.o.hz.get_angle() + obs.hz.get_angle()
        # Calculate the coordinates of the new point.
        e = st.p.e + obs.horiz_dist() * math.sin(b)
        n = st.p.n + obs.horiz_dist() * math.cos(b)
        return Point(obs.target, e, n)

    @staticmethod
    def intersection(s1, obs1, s2, obs2):
        """
            Calculate intersection
            :param s1: station 1 (Station)
            :param obs1: observation from station 1 (PolarObservation)
            :param s2: station 2 (Station)
            :param obs2: observation from station 2 (PolarObservation)
        """
        # If the two observation are the same.
        if obs1.target != obs2.target:
            return None
        # Calculate the two bearing angles of two observations.
        b1 = s1.o.hz.get_angle() + obs1.hz.get_angle()
        b2 = s2.o.hz.get_angle() + obs2.hz.get_angle()
        # Calculate an intersection point of two lines. If the two lines are parallels the function returns None object
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
        try:
            # Calculate angle between obs1 and obs2 and between obs2 and obs3.
            angle1 = Angle(obs2.hz.get_angle() - obs1.hz.get_angle())
            angle2 = Angle(obs3.hz.get_angle() - obs2.hz.get_angle())
        
            # Create a circle on points p1 and p2 and angle1.
            circ1 = Circle(p1, p2, angle1)
            print circ1.p.e, circ1.p.n, circ1.r
            # Create a circle on points p2 and p3 and angle2.
            circ2 = Circle(p2, p3, angle2)
            print circ2.p.e, circ2.p.n, circ2.r
            # Calculate the intersection of two circles.
            points = intersecCC(circ1, circ2)

            # IntersectCC functions can return with zero or two intersection points.
            # If the number of intersection point is zero the resection method return None object.
            if len(points) == 2:
                #  Select the right one from the two intersection points.
                if math.fabs(p2.e - points[0].e) < 0.1 and math.fabs(p2.n - points[0].n) < 0.1:
                    return Point(st.p.id, points[1].e, points[1].n, None, st.p.pc)
                else :
                    return Point(st.p.id, points[0].e, points[0].n, None, st.p.pc)
                return None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def traverse(trav_obs, forceFree=False):
        """
            Calculate traverse line. This method can compute the following types of travesres>
            1. open traverse (free): originates at a known position with known bearings and ends at an unknown position
            2. closed traverse at both ends and the start point has known bearings
            3. closed traverse at both ends and both endpoints has known bearings
            4. inserted traverse: closed at both ends but no bearings
            :param trav_obs a list of sublists consists of a Point and two PolarObservations
            If the station member is not None the point is a station.
            Start point must have coordinates in case of type 1-4 and 
            end points must have coordinates in case of type 2-4.
            Two observations are needed at the angle points. At the start point the second observation 
            is required in case of type 1-3. At the end point the first observation is required in case of type 3.
            :param forceFree force free traverse calculation (for node)
            :return a list of points which's coordinates has been computed.
        """
        n = len(trav_obs)
        # at least 3 points must be
        if n<3:
            return None
        # start point and end point
        startp = trav_obs[0][0]
        endp = trav_obs[n-1][0]
        # no coord for startpoint
        if startp is None or startp.p is None or startp.p.e is None or startp.p.n is None:
            return None
        
        free = False
        if forceFree is True:
            # force to calculate free traverse (for node)
            free = True
            endp.p.e = None
            endp.p.n = None
        elif endp is None or endp.p is None or endp.p.e is None or endp.p.n is None:
            # no coordinate for endpoint            
            #TODO messagebox for free traverse accepted 
            free = True # free traverse
            
        #collect measurements in traverse
        beta = [None]*n
        t = [None]*n
        t1 = [None]*n
        t2 = [None]*n
        
        for i in range(0,n):
            st = trav_obs[i][0]
            obsprev = trav_obs[i][1]
            obsnext = trav_obs[i][2]
            if i==0:
                beta[0] = st.o.hz
                if beta[0] is None:
                    # no orientation on start
                    #TODO messagebox
                    print "No orientation on start - inserted traverse"
                    pass
                
            if i==n-1:
                beta[i] = st.o.hz
                if beta[i] is None:
                    # no orientation on end
                    #TODO messagebox
                    print "No orientation on end"
                    pass
            
            if i!=0 and i!=n-1 and (obsprev is None or obsnext is None or obsprev.hz is None or obsnext.hz is None):
                # no angle at angle point
                #TODO messagebox
                return None

            if i == 0:
                # there was orientation on first
                if beta[0] is not None and obsnext is not None and obsnext.hz is not None:
                    beta[0].set_angle( beta[0].get_angle() + obsnext.hz.get_angle() )
                else:
                    beta[0] = None
            elif i==n-1:
                if beta[i] is not None and beta[0] is not None and obsprev is not None and obsprev.hz is not None:
                # there was orientation on last and first
                    beta[i].set_angle( math.pi * 2 - (beta[i].get_angle() + obsprev.hz.get_angle()) )
                else:
                    beta[i] = None
            else:
                beta[i] = Angle( obsnext.hz.get_angle() - obsprev.hz.get_angle() )
                
            if beta[i] is not None:
                while beta[i].get_angle() > math.pi * 2:
                    beta[i].set_angle( beta[i].get_angle() - math.pi * 2 ) 
                while beta[i].get_angle() < 0:
                    beta[i].set_angle( beta[i].get_angle() + math.pi * 2 )
                    
            if obsprev is not None and obsprev.d is not None:
                if t[i] is not None:
                    # save distance for output
                    t1[i] = Distance(obsprev.horiz_dist(), "HD")
                    t2[i] = t[i]
                    t[i]  = Distance((t[i].horiz_dist() + obsprev.horiz_dist()) / 2.0, "HD")
                else:
                    t[i] = Distance(obsprev.horiz_dist(),"HD")
            elif i>1 and t[i-1] is None:
                # no distance between points
                #TODO messagebox
                return None
            
            if obsnext is not None and obsnext.d is not None:
                t[i+1] = Distance(obsnext.horiz_dist(),"HD")

        if forceFree is True:
            beta[n-1] = None

        # calculate sum of betas if we have both orientation
        if beta[0] is not None and beta[n-1]is not None:
            sumbeta = 0 # in seconds
            for i in range(0,n):
                sumbeta = sumbeta + beta[i].get_angle("SEC")
            # calculate angle error
            dbeta = (n-1) * PISEC - sumbeta # in seconds
            while dbeta > PISEC:
                dbeta = dbeta - 2*PISEC
            while dbeta < -PISEC:
                dbeta = dbeta + 2*PISEC
        else:
            sumbeta = 0
            dbeta = 0

        # angle corrections
        w = 0   # in seconds
        vbeta = []  # in seconds
        for i in range(0,n):
            vbeta[i] = math.round(dbeta / n)
            w = w + vbeta[i]

        # forced rounding
        i = 0
        dbeta = math.round(dbeta)
        while w < dbeta:
            vbeta[i] = vbeta[i] + 1 
            i = i + 1
            w = w + 1
            if i >= n:
                i = 0
        while w > dbeta:
            vbeta[i] = vbeta[i] - 1
            i = i + 1
            w = w - 1
            if i >= n:
                i = 0

        #    calculate bearings and de & dn for sides
        delta = [0] # in seconds
        sumde = 0
        sumdn = 0
        sumt = 0
        de = []
        dn = []
        for i in range(1,n):

            j = i - 1
            if j==0:
                if beta[j] is not None:
                    d = delta[j] + beta[j].get_angle("SEC") + vbeta[j]
                else:
                    # find orientation for first side "beillesztett"
                    d = 0
                    sumde = 0
                    sumdn = 0
                    for k in range(1,n):
                        de[k] = t[k] * math.sin(d / RO)
                        dn[k] = t[k] * math.cos(d / RO)
                        sumde = sumde + de[k]
                        sumdn = sumdn + dn[k]
                        if k < n-1:
                            d = d + beta[k] - PISEC
                    
                    d = Bearing( Point("@",endp.p.e, endp.p.n), Point("@",startp.p.e,startp.p.n)).get_angle("SEC") - \
                            Bearing (Point("@",sumde,sumdn),Point("@",0, 0)).get_angle("SEC")
                    sumde = 0
                    sumdn = 0
            else:
                d = delta[j] + beta[j].get_angle("SEC") + vbeta[j] - PISEC
            
            while d < 0:
                d = d + PISEC*2
            while d > PISEC*2:
                d = d - PISEC*2
            delta[i] = d
            de[i] = t[i] * math.sin(d / RO)
            dn[i] = t[i] * math.cos(d / RO)
            sumde = sumde + de[i]
            sumdn = sumdn + dn[i]
            sumt = sumt + t[i]
            
        #    calculate de & dn error
        if free is True:
            dde = 0 # free traverse
            ddn = 0
            ddist = 0
        else:
            dde = endp.p.e - startp.p.e - sumde
            ddn = endp.p.n - startp.p.n - sumdn
            ddist = math.hypot(dde, ddn)    # linear error

        #    calculate final coords
        we = dde / sumt
        wn = ddn / sumt
        for i in range(1,n):
            ve[i] = t[i] * we
            vn[i] = t[i] * wn
            e[i] = e[i-1] + de[i] + ve[i]
            n[i] = n[i-1] + dn[i] + vn[i]
        
        plist = []  # list of calculated points
        if free is True:
            last = n
        else:
            last = n-1
        for i in range(1,last):
            
            if trav_obs[i][0] is not None and trav_obs[i][0].p is not None:
                plist[i] = trav_obs[i][0].p
            else:
                plist[i] = Point("@")
            plist[i].e = e[i]
            plist[i].n = n[i]

        return plist
    
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
    
    #traverse1
    # open traverse
    p5241otra = Point("5241",646414.44,211712.77)
    p5245otra = Point("5245",646938.71,212635.92)
    p5246otra = Point("5246",646380.61,212793.97)
    p5247otra = Point("5247",646381.14,212476.49)
    o5247otra = PolarObservation("station_5247")
    s5247otra = Station( p5247otra, o5247otra )
    o5241otra = PolarObservation( "5241", Angle("245-23-41", "DMS") )
    o5245otra = PolarObservation( "5245", Angle("141-56-11", "DMS") )
    o5246otra = PolarObservation( "5246", Angle("67-47-14", "DMS") )
    s5247otra.o.hz = Calculation.orientation(s5247otra, [[p5241otra,o5241otra], [p5245otra,o5245otra], [p5246otra,o5246otra]])
    print s5247otra.o.hz.get_angle('DMS');  #292-06-34
    
    o5247_111otra = PolarObservation("111", Angle("241-26-57","DMS"), None, Distance(123.42,"HD")) 
    s111otra = Station( None, PolarObservation("station_111") )
    o111_5247otra = PolarObservation("5247", Angle("225-39-00","DMS")) 
    o111_112otra = PolarObservation("112", Angle("92-38-43","DMS"), None, Distance(142.81,"HD")) 
    s112otra = Station( None, PolarObservation("station_112") )
    o112_111otra = PolarObservation("111", Angle("227-16-34","DMS")) 
    o112_113otra = PolarObservation("113", Angle("69-16-28","DMS"), None, Distance(253.25,"HD")) 
    s113otra = Station( None, PolarObservation("station_113") )
    o113_112otra = PolarObservation("112", Angle("102-56-44","DMS")) 
    o113_114otra = PolarObservation("114", Angle("205-46-21","DMS"), None, Distance(214.53,"HD")) 
    s114otra = Station( None, PolarObservation("station_114") )
    o114_113otra = PolarObservation("113", Angle("104-23-11","DMS")) 
    o114_115otra = PolarObservation("115", Angle("305-54-29","DMS"), None, Distance(234.23,"HD")) 
    #Calculation.traverse( [ [s5247otra,None,o5247_111otra], [s111otra,o111_5247otra,o111_112otra],
    #                       [s112otra,o112_111otra,o112_113otra],[s113otra,o113_112otra,o113_114otra],
    #                       [s114otra,o114_113otra,o114_115otra] ] )
    
