#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Basic classes for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

import re
import math

RO = 180 * 60 * 60 / math.pi
PISEC = 180 * 60 * 60

class Angle(object):
    """
        Angle class, value stored in radian internally
    """
    def __init__(self, value, unit='RAD'):
        """
            Create 
            :param value: angle value
            :param unit: angle unit (RAD/DMS/DEG/GON/NMEA/PDEG/SEC)
        """
        self.set_angle(value, unit)

    def get_angle(self, out='RAD'):
        """
            Get angle value in diffferent units
            :param out: output unit (RAD/DMS/DEG/GON/NMEA/PDEG/SEC)
            :returns float or string 
        """
        if out == 'RAD':
            output = self.value
        elif out == 'DMS':
            output = self.__dms()
        elif out == 'DEG':
            output = self.__rad2deg()
        elif out == 'GON':
            output = self.__rad2gon()
        elif out == 'NMEA':
            output = self.__rad2dm()
        elif out == 'PDEG':
            # pseudo decimal DMS ddd.mmss
            output = self.__rad2pdeg()
        elif out == 'SEC':
            output = self.__rad2sec()
        else:
            output = None
        return output

    def set_angle(self, value, unit='RAD'):
        """
            Change value of angle
            :param value: new value for angle
            :param unit: unit for the new value
            :return: none
        """
        if unit == 'RAD':
            self.value = value
        elif unit == 'DMS':
            self.value = self.__dms2rad(value)
        elif unit == 'DEG':
            self.value = self.__deg2rad(value)
        elif unit == 'GON':
            self.value = self.__gon2rad(value)
        elif unit == 'NMEA':
            self.value = self.__dm2rad(value)
        elif unit == 'PDEG':
            self.value = self.__pdeg2rad(value)
        elif unit == 'SEC':
            self.value = self.__sec2rad(value)
        else:
            # unknown unit
            self.value = None

    def __deg2rad(self, angle):
        try:
            a = math.radians(angle)
        except (ValueError, TypeError):
            a = None
        return a

    def __gon2rad(self, angle):
        try:
            a = angle / 200.0 * math.pi
        except (ValueError, TypeError):
            a = None
        return a

    def __dms2rad(self, dms):
        try:
            items = [float(item) for item in dms.split('-')]
            div = 1.0
            a = 0.0
            for i, val in enumerate(items):
                a += val / div
                div *= 60.0
            a = math.radians(a)
            #a = math.radians(items[0] + items[1] / 60.0 + items[2] / 3600.0)
        except (ValueError, TypeError):
            a = None
        return a

    def __dm2rad(self, angle):
        "DDMM.nnnnnn NMEA angle to radian"
        try:
            w = angle / 100.0
            d = int(w)
            a = math.radians(d + (w - d) * 100.0 / 60.0)
        except (ValueError, TypeError):
            a = None
        return a

    def __pdeg2rad(slf, angle):
        "dd.mmss to radian"
        try:
            d = math.floor(angle)
            angle = (angle - d) * 100
            m = math.floor(angle)
            s = (angle - m) * 100
            a = math.radians(d + m / 60.0 + s / 3600.0)
        except (ValueError, TypeError):
            a = None
        return a

    def __sec2rad(self, angle):
        try:
            a = angle / RO
        except (ValueError, TypeError):
            a = None
        return a

    def __rad2gon(self):
        try:
            a = self.value / math.pi * 200.0
        except (ValueError, TypeError):
            a = None
        return a

    def __rad2sec(self):
        try:
            a = self.value * RO
        except (ValueError, TypeError):
            a = None
        return a

    def __rad2deg(self):
        try:
            a = math.degrees(self.value)
        except (ValueError, TypeError):
            a = None
        return a

    def __dms(self):
        try:
            secs = round(self.__rad2sec())
            min, sec = divmod(secs, 60)
            deg, min = divmod(min, 60)
            deg = int(deg)
            dms = "%d-%02d-%02d" % (deg, min, sec)
        except (ValueError, TypeError):
            dms = None
        return dms

    def __rad2dm(self):
        try:
            w = self.value / math.pi * 180.0
            d = int(w)
            a = d * 100 + (w - d) * 60
        except (ValuError, TypeError):
            a = None
        return a

    def __rad2pdeg(self):
        try:
            secs = round(self.__rad2sec())
            min, sec = divmod(secs, 60)
            deg, min = divmod(min, 60)
            deg = int(deg)
            pdeg = deg + min / 100.0 + sec / 10000.0
        except (ValueError, TypeError):
            pdeg = None
        return pdeg

class Point(object):
    """
        Point class
    """

    def __init__(self, id, e=None, n=None, z=None, pc=None, pt=None):
        """
            initialize new Point object
            :param id: point name (string), use '@' for temporary points
            :param e: easting coordinate (float)
            :param n: northing coordinate (float)
            :param z: elevation (float)
            :param pc: point code (string)
            :param pt: point type (string, e.g. controll/detail)
        """
        self.id = id
        self.n = n
        self.e = e
        self.z = z
        self.pc = pc
        self.pt = pt

class Distance(object):
    """
        Distance observation
    """

    def __init__(self, d, m='SD'):
        """
            :param d: distance value
            :param m: slope/horizontal/vertical distance SD/HD/VD
        """
        self.d = d
        self.mode = m

class PolarObservation(object):
    """
        Polar observation classs
    """

    def __init__(self, tp, hz=None, v=None, d=None, th=None, pc=None):
        """
            initialize new Polar observation object
            stations are marked in name 'station_<id>',
            instrument height is stored in th field
            :param tp: target point id/station point id (string)
            :param hz: horizontal angle/orientation angle (Angle)
            :param v: zenith angle (Angle)
            :param d: slope distance (Distance)
            :param th: target height/instrument height (float)
            :param pc: point code (string)
        """
        if re.match('^station_', tp):
            # remove distance and zenith
            v = None
            d = None
        self.target = tp
        self.hz = hz
        self.v = v
        self.d = d
        self.th = th
        self.pc = pc

    def horiz_dist(self):
        if self.d is None:
            return None
        if self.d.mode == 'HD':
            return self.d.d
        elif self.d.mode == 'SD':
            return self.d.d * math.sin(self.v.get_angle())
        elif self.d.mode == 'VD':
            return 0.0
        return None

class Station(object):
    """
        station data
    """
    def __init__(self, p, o):
        """
            :param p point data (Point)
            :param o observation data (PolarObservation)
            orientation angle in hz field, instrument height in th field
        """
        self.p = p
        self.o = o

class Circle(object):
    """
        circle object
    """
    def __init__(self, p1, p2, p3=None):
        """
            Multiple initialize signatures
            1. Center and radius given
            :param p1 center point (Point)
            :param p2 radius (float)
            :param p3 None

            2. Calculate circle parameters from three points
            center is the intersection of orthogonals at the midpoints
            :param p1: first point (Point)
            :param p2: second point (Point)
            :param p3: third point (Point)

            3 Calculate circle parameters defined by two points and included angle
            :param p1: first point (Point)
            :param p2: second point (Point)
            :param p3: included angle (radian) (Angle)

        """
        if isinstance(p1, Point) and isinstance(p2, float):
            self.p = p1
            self.r = p2
        elif isinstance(p1, Point) and isinstance(p2, Point) and isinstance(p3, Point):
            self.p = self.__center(p1, p2, p3)
            self.r = distance2d(self.p, p1).d
        elif isinstance(p1, Point) and isinstance(p2, Point) and isinstance(p3,  Angle):
            t2 = distance2d(p1, p2).d / 2.0
            d = t2 / math.tan(p3.get_angle() / 2.0)
            dab = bearing(p1, p2)
            e3 = p1.e + t2 * math.sin(dab.get_angle()) + d * math.cos(dab.get_angle())
            n3 = p1.n + t2 * math.cos(dab.get_angle()) - d * math.sin(dab.get_angle())
            p4 = Point( "@", e3, n3 )
            self.p = self.__center(p1, p2, p4)
            self.r = distance2d(self.p, p1).d
        else:
            self.p = None
            self.r = None

    def __center(self, p1, p2, p3):
        # midpoints
        midp12 = Point("@", (p1.e + p2.e) / 2.0,  (p1.n + p2.n) / 2.0)
        midp23 = Point("@", (p2.e + p3.e) / 2.0,  (p2.n + p3.n) / 2.0)
        d12 = bearing(p1, p2).get_angle() + math.pi / 2.0
        d23 = bearing(p2, p3).get_angle() + math.pi / 2.0
        return intersecLL( midp12, midp23, d12, d23 )


def distance2d(p1, p2):
    """
        Calculate horizontal distance between two points
    """
    try:
        d = math.sqrt((p2.e - p1.e) ** 2 + (p2.n - p1.n) ** 2)
    except (TypeError, ValueError):
        return None
    return Distance(d, 'HD')

def distance3d(p1, p2):
    """
        Calculate 3D distance between two points
    """
    try:
        d = math.sqrt((p2.e - p1.e) ** 2 + (p2.n - p1.n) ** 2 + (p2.z - p1.z) ** 2)
    except (ValueError, TypeError):
        return None
    return Distance(d, 'SD')

def bearing(p1, p2):
    """
        Calculate whole circle bearing
    """
    try:
        wcb = math.atan2(p2.e - p1.e, p2.n - p1.n)
        while wcb < 0:
            wcb = wcb + 2.0 * math.pi
    except TypeError:
        return None
    return Angle(wcb)

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

def intersecCC(circle1, circle2):
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
            circle1.p.e, circle1.p.n = circle1.p.n, circle1.p.e
            circle2.p.e, circle2.p.n = circle2.p.n, circle2.p.e

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
    
def pn_to_stationpn(pn):
    if isinstance(pn, basestring):
        return "station_" + pn
    else:
        return None

def stationpn_to_pn(stpn):
    if isinstance(stpn, basestring):
        if stpn.startswith("station_"):
            return stpn[8:]
        else:
            return stpn
    else:
        return None

if __name__ == "__main__":
    """
        unit test
    """
    a = Angle('359-59-59', 'DMS')
    print a.get_angle('RAD')
    print a.get_angle('DMS')
    print a.get_angle('DEG')
    print a.get_angle('GON')
    print a.get_angle('NMEA')
    print Angle(a.get_angle('RAD'), 'RAD').get_angle('DMS')
    print Angle(a.get_angle('DMS'), 'DMS').get_angle('DMS')
    print Angle(a.get_angle('DEG'), 'DEG').get_angle('DMS')
    print Angle(a.get_angle('GON'), 'GON').get_angle('DMS')
    print Angle(a.get_angle('NMEA'), 'NMEA').get_angle('DMS')
    print Angle(a.get_angle('PDEG'), 'PDEG').get_angle('PDEG')
    print Angle('16-20', 'DMS').get_angle('DMS')
    print Angle('16', 'DMS').get_angle('DMS')
    p = [Point('1', 1000, 2000, 50), Point('2', 1500, 2000, 60)]
    o = [PolarObservation('station_1', None, None, None, 1.54),
         PolarObservation('2', Angle(60.9345, 'GON'), Angle(89.855615, 'DEG'), Distance(501.105, 'SD'), 1.80)]
    print o[1].horiz_dist()
    c = Circle(Point('3', 100, 200), 100.0)
    print c.p.e, c.p.n, c.r
    c = Circle(Point('4', 100, 100), Point('5', 0, 100), Point('6', 100, 50))
    print c.p.e, c.p.n, c.r
    c = Circle(Point('4', 100, 100), Point('5', 0, 100), Angle(60, 'DEG'))
    print c.p.e, c.p.n, c.r
