#!/usr/bin/env python
"""
    Basic classes for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

import math
RO = 180 * 60 * 60 / math.pi

class Angle(object):
    """
        Angle class, value stored in radian internally
    """
    def __init__(self, value=None, unit='RAD'):
        """
            Create 
            :param value: angle value
            :param unit: angle unit (RAD/DMS/DEG/GON/NMEA/PDEG)
        """
        self.set_angle(value, unit)

    def get_angle(self, out='RAD'):
        """
            Get angle value in diffferent units
            :param out: output unit (RAD/DMS/DEG/GON/NMEA)
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
            a = math.radians(items[0] + items[1] / 60.0 + items[2] / 3600.0)
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

class Station(object):
    """
        Station data from observations
    """

    def __init__(self, p, o=None, ih=None):
        """
            :param p: station id & coordinates (Point)
            :param o: orientation angle (Angle)
            :param ih: instrument height (float)
        """
        self.p = p
        self.o = o
        self.ih = ih

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
            :param tp: target point id (string)
            :param hz: horizontal angle (Angle)
            :param v: zenith angle (Angle)
            :param d: distance (Distance)
            :param th: target height (float)
            :param pc: point code (string)
        """
        self.target = tp
        self.hz = hz
        self.v = v
        self.d = d
        self.th = th
        self.pc = pc

    def horiz_dist(self):
        if self.mode == 'HD':
            return self.d
        elif self.mode == 'SD':
            return self.d * sin(self.hz.get_angle())
        elif self.mode == 'VD':
            return 0.0
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
