#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module: calculation
    :platform: Linux, Windows
    :synopsis: pure calculation class

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>

"""

import math
from base_classes import *
from resultlog import *
from PyQt4.QtCore import QCoreApplication

class Calculation(object):
    """ Container class for calculations. Pure static class. """
    
    def __init__(self):
        pass

    @staticmethod
    def orientation(st, ref_list):
        """ Orientation calculation for a station

            :param st: station (Station)
            :param ref_list: list of [Point, PolarObservation] lists
            :returns: average orientation angle (Angle) None if no reference direction at all or in case of error
        """
        ResultLog.resultlog_message = ""
        try:
            sz = 0
            cz = 0
            sd = 0
            for ref in ref_list:
                pt = ref[0]
                obs = ref[1]
                b = bearing(st.p, pt).get_angle()
                r = obs.hz.get_angle()
                z = b - r
                if z<0:
                    z = z + math.pi * 2
                d = distance2d(st.p, pt).d
                sd = sd + d
                sz = sz + math.sin(z) * d
                cz = cz + math.cos(z) * d
                ref.append(d)
                ref.append(Angle(z))
                ref.append(Angle(r))
                ref.append(Angle(b))
 
            if sd==0:
                return None
        
            sz = sz / sd
            cz = cz / sd
            # Calculate average orient angle.
            za = math.atan2(sz, cz)
            while za<0:
                za = za + math.pi * 2
        except (ValueError, TypeError, AttributeError):
            return None
        
        # log results of orientation?
        for ref in ref_list:
            e = ref[3].get_angle("SEC") - Angle(za).get_angle("SEC")
            if e>PISEC:
                e = e - 2*PISEC
            if e<-PISEC:
                e = e + 2*PISEC
            E = e / RO * ref[2]
            ResultLog.resultlog_message += u"%-10s %-10s    %8.4f    %8.4f    %8.4f   %8.3f %4d %8.3f\n" % \
                (ref[1].point_id, (ref[1].pc if ref[1].pc is not None else "-"), \
                ref[4].get_angle("GON"), ref[5].get_angle("GON"), \
                ref[3].get_angle("GON"), ref[2], int(e), E)
        ResultLog.resultlog_message +=u"%-48s %8.4f\n" % (tr("Average orientation angle"), Angle(za).get_angle("GON"))
        return Angle(za)

    @staticmethod
    def polarpoint(st, obs):
        """ Calculate coordinates of a point measured by an independent radial measurement

            :param st: station (Station)
            :param obs: observation from station to the unknown point (PolarObservation)
            :returns: the polar point with new coordinates (Point)
        """
        ResultLog.resultlog_message = ""
        try:
            # Calculate the bearing angle between the station and new point.
            b = st.o.hz.get_angle() + obs.hz.get_angle()
            # Calculate the coordinates of the new point.
            e = st.p.e + obs.horiz_dist() * math.sin(b)
            n = st.p.n + obs.horiz_dist() * math.cos(b)
            if st.p.z is not None and st.o.th is not None and obs.v is not None:
                z = st.p.z + st.o.th + obs.d.d * math.cos(obs.v.get_angle())
                if obs.th is not None:
                    z = z - obs.th 
            else:
                z = None
            p = Point(obs.point_id, e, n, z, obs.pc)
            if p.z is None:
                # no z calculated
                ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f          %8.4f %8.3f" % \
                        (p.id,(p.pc if p.pc is not None else "-"),p.e,p.n,Angle(b).get_angle("GON"),obs.horiz_dist())
            else:
                ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f %8.3f %8.4f %8.3f" % \
                        (p.id,(p.pc if p.pc is not None else "-"),p.e,p.n,p.z,Angle(b).get_angle("GON"),obs.horiz_dist())
            return p
        except (ValueError, TypeError, AttributeError):
            return None

    @staticmethod
    def intersection(s1, obs1, s2, obs2):
        """ Calculate intersection

            :param s1: station 1 (Station)
            :param obs1: observation from station 1 (PolarObservation)
            :param s2: station 2 (Station)
            :param obs2: observation from station 2 (PolarObservation)
            :returns: intersection point (Point)
        """
        ResultLog.resultlog_message = ""
        # If the two observation are the same.
        if obs1.point_id != obs2.point_id:
            return None
        # Calculate the two bearing angles of two observations.
        b1 = s1.o.hz.get_angle() + obs1.hz.get_angle()
        b2 = s2.o.hz.get_angle() + obs2.hz.get_angle()
        # Calculate an intersection point of two lines. If the two lines are parallels the function returns None object
        pp = intersecLL(s1.p, s2.p, b1, b2)
        if pp is None:
            return None
        if obs1.pc is None:
            pc = obs2.pc
        else:
            pc = obs1.pc
        pp.id = obs1.point_id
        pp.pc = pc
        ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f %8.4f %8.4f" % \
                  (pp.id, (pp.pc if pp.pc is not None else "-"), pp.e, pp.n, b1, b2)
        return pp

    @staticmethod
    def resection(st, p1, p2, p3, obs1, obs2, obs3):
        """ Calculate resection

            :param st: station (Station)
            :param p1: first control point (Point)
            :param p2: second control point (Point)
            :param p3: third control point (Point)
            :param obs1: observation from st to p1 (PolarObservation)
            :param obs2: observation from st to p2 (PolarObservation)
            :param obs3: observation from st to p3 (PolarObservation)
            :returns: coordinates of the resection point (Point) if it can be calculated; otherwise None
        """
        ResultLog.resultlog_message = ""
        try:
            # Calculate angle between obs1 and obs2 and between obs2 and obs3.
            alpha = Angle(obs2.hz.get_angle() - obs1.hz.get_angle()) # alpha
            beta = Angle(obs3.hz.get_angle() - obs2.hz.get_angle()) # beta
        
            # Create a circle on points p1 and p2 and alpha.
            circ1 = Circle(p1, p2, alpha)
            # Create a circle on points p2 and p3 and beta.
            circ2 = Circle(p2, p3, beta)
            # Calculate the intersection of two circles.
            try:
                points = intersecCC(circ1, circ2)
            except(AttributeError):
                return None

            # IntersectCC functions can return with zero or two intersection points.
            # If the number of intersection point is zero the resection method return None object.
            if len(points) == 2:
                #  Select the right one from the two intersection points.
                if math.fabs(p2.e - points[0].e) < 0.1 and math.fabs(p2.n - points[0].n) < 0.1:
                    p = Point(st.p.id, points[1].e, points[1].n, st.p.z, st.p.pc, st.p.pt)
                else :
                    p = Point(st.p.id, points[0].e, points[0].n, st.p.z, st.p.pc, st.p.pt)

                ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f     %8.4f  %8.4f\n" % \
                          (obs1.point_id, (obs1.pc if obs1.pc is not None else "-"), p1.e, p1.n, \
                           obs1.hz.get_angle("GON"), alpha.get_angle("GON") )
                ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f     %8.4f  %8.4f\n" % \
                          (obs2.point_id, (obs2.pc if obs2.pc is not None else "-"), p2.e, p2.n, \
                           obs2.hz.get_angle("GON"), beta.get_angle("GON") )
                ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f     %8.4f\n" % \
                          (obs3.point_id, (obs3.pc if obs3.pc is not None else "-"), p3.e, p3.n, \
                           obs3.hz.get_angle("GON") )
                ResultLog.resultlog_message += u"%-10s %-10s %12.3f %12.3f\n" % \
                          (p.id, (p.pc if p.pc is not None else "-"), p.e, p.n)
                return p
            else:
                return None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def traverse(trav_obs, forceFree=False):
        """ Calculate traverse line. This method can compute the following types of travesres

            1. open traverse (free): originates at a known position with known bearings and ends at an unknown position
            2. closed traverse at both ends and the start point has known bearings
            3. closed traverse at both ends and both endpoints has known bearings
            4. inserted traverse: closed at both ends but no bearings

            :param trav_obs: a list of sublists consists of a Point and two PolarObservations, If the station member is not None the point is a station. Start point must have coordinates in case of type 1-4 and end points must have coordinates in case of type 2-4.  Two observations are needed at the angle points. At the start point the second observation is required in case of type 1-3. At the end point the first observation is required in case of type 3.
            :param forceFree: force free traverse calculation (Boole)
            :returns: a list of points which's coordinates has been computed.
        """
        ResultLog.resultlog_message = ""
        n = len(trav_obs)
        # at least 3 points must be
        if n<3:
            ResultLog.resultlog_message += \
                tr("Error: At least 3 points must be added to traverse line!") + "\n"
            return None
        # start point and end point
        startp = trav_obs[0][0]
        endp = trav_obs[n-1][0]
        # no coord for startpoint
        if startp is None or startp.p is None or startp.p.e is None or startp.p.n is None:
            ResultLog.resultlog_message += \
                tr("Error: No coordinates on start point!") + "\n"
            return None
        
        free = False
        if forceFree is True:
            # force to calculate free traverse (for node)
            free = True
            endp.p.e = None
            endp.p.n = None
        elif endp is None or endp.p is None or endp.p.e is None or endp.p.n is None:
            # no coordinate for endpoint            
            ResultLog.resultlog_message += \
                tr("Warning: No coordinates for end point -> Free traverse.") + "\n" 
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
                    if free is True:
                        ResultLog.resultlog_message += \
                            tr("Error: No orientation on start point and no coordinates on end point!") + "\n"
                        return None
                    else:
                        ResultLog.resultlog_message += \
                            tr("Warning: No orientation on start point - inserted traverse.") + "\n"
                
            if i==n-1:
                beta[i] = st.o.hz
                if beta[i] is None:
                    # no orientation on end
                    ResultLog.resultlog_message += \
                        tr("Warning: No orientation on end point.") + "\n"
            
            if i!=0 and i!=n-1 and (obsprev is None or obsnext is None or obsprev.hz is None or obsnext.hz is None):
                # no angle at angle point
                ResultLog.resultlog_message += \
                    tr("Error: No angle at point %s!") % trav_obs[i][0].p.id + "\n"
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
                    t[i]  = Distance((t[i].d + obsprev.horiz_dist()) / 2.0, "HD")
                else:
                    t[i] = Distance(obsprev.horiz_dist(),"HD")
            elif i>0 and t[i] is None:
                # no distance between points
                ResultLog.resultlog_message += \
                    tr("Error: No distance between points %s and %s!") % \
                    (trav_obs[i-1][0].p.id,trav_obs[i][0].p.id) + "\n"
                return None
            
            if obsnext is not None and obsnext.d is not None:
                t[i+1] = Distance(obsnext.horiz_dist(),"HD")

        if forceFree is True:
            beta[n-1] = None

        # calculate sum of betas if we have both orientation
        if beta[0] is not None and beta[n-1] is not None:
            sumbeta = 0.0 # in radians
            for i in range(0,n):
                sumbeta = sumbeta + beta[i].get_angle()
            # calculate angle error
            dbeta = (n-1) * math.pi - sumbeta # in radians
            while dbeta > math.pi:
                dbeta = dbeta - 2*math.pi
            while dbeta < -math.pi:
                dbeta = dbeta + 2*math.pi
        else:
            sumbeta = 0.0
            dbeta = 0.0

        # angle corrections
        w = 0.0   # in seconds
        vbeta = [None]*n  # in seconds
        for i in range(0,n):
            vbeta[i] = dbeta / n
            w = w + vbeta[i]

        #    calculate bearings and de & dn for sides
        delta = [0.0]*n # in radians
        sumde = 0.0
        sumdn = 0.0
        sumt = 0.0
        de = [0.0]*n
        dn = [0.0]*n
        for i in range(1,n):

            j = i - 1
            if j==0:
                if beta[j] is not None:
                    d = delta[j] + beta[j].get_angle() + vbeta[j]
                else:
                    # find orientation for first side "beillesztett"
                    d = 0
                    sumde = 0
                    sumdn = 0
                    for k in range(1,n):
                        de[k] = t[k].d * math.sin(d)
                        dn[k] = t[k].d * math.cos(d)
                        sumde = sumde + de[k]
                        sumdn = sumdn + dn[k]
                        if k < n-1:
                            d = d + beta[k].get_angle() - math.pi
                    
                    d = bearing( Point("@",endp.p.e, endp.p.n), Point("@",startp.p.e,startp.p.n)).get_angle() - \
                            bearing (Point("@",sumde,sumdn),Point("@",0, 0)).get_angle()
                    sumde = 0
                    sumdn = 0
            else:
                d = delta[j] + beta[j].get_angle() + vbeta[j] - math.pi
            
            while d < 0:
                d = d + math.pi*2
            while d > math.pi*2:
                d = d - math.pi*2
            delta[i] = d
            de[i] = t[i].d * math.sin(d)
            dn[i] = t[i].d * math.cos(d)
            sumde = sumde + de[i]
            sumdn = sumdn + dn[i]
            sumt = sumt + t[i].d
            
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
        ve = [0]*n
        vn = [0]*n
        ee = [0]*n
        nn = [0]*n
        we = dde / sumt
        wn = ddn / sumt
        ee[0] = startp.p.e
        nn[0] = startp.p.n
        for i in range(1,n):
            ve[i] = t[i].d * we
            vn[i] = t[i].d * wn
            ee[i] = ee[i-1] + de[i] + ve[i]
            nn[i] = nn[i-1] + dn[i] + vn[i]

        for i in range(0,n):
            pcode = (trav_obs[i][0].p.pc if trav_obs[i][0].p.pc is not None else "-")
            t_1 = "%8.3f" % t1[i].d if t1[i] is not None else "-"
            t_2 = "%8.3f" % t2[i].d if t2[i] is not None else "-"
            ResultLog.resultlog_message += "           %10.4f %8s\n" % (Angle(delta[i]).get_angle("GON"), t_1)

            if i > 0:
                if beta[i] is None:
                    ResultLog.resultlog_message += u"%-10s %10s %8.3f %8.3f %8.3f %10.3f %10.3f\n" % \
                             (trav_obs[i][0].p.id, "", t[i].d, \
                             de[i], dn[i], de[i]+ve[i],dn[i]+vn[i])
                else:
                    ResultLog.resultlog_message += u"%-10s %10.4f %8.3f %8.3f %8.3f %10.3f %10.3f\n" % \
                             (trav_obs[i][0].p.id, beta[i].get_angle('GON'), t[i].d, \
                             de[i], dn[i], de[i]+ve[i],dn[i]+vn[i])
            else:
                if beta[i] is None:
                    ResultLog.resultlog_message += u"%-10s %10s\n" % \
                             (trav_obs[i][0].p.id, "")
                else:
                    ResultLog.resultlog_message += u"%-10s %10.4f\n" % \
                             (trav_obs[i][0].p.id, beta[i].get_angle('GON'))
            
            if i > 0:
                if free is True:
                    w1 = "-"
                    w2 = "-"
                else:
                    w1 = "%8.3f" % ve[i]
                    w2 = "%8.3f" % vn[i]
                if beta[0] is None or beta[n-1] is None:
                    ResultLog.resultlog_message += u"%-10s %10s %8s %8s %8s %10.3f %10.3f\n" % \
                             (pcode, "", t_2, w1, w2, ee[i], nn[i])
                else:
                    ResultLog.resultlog_message += u"%-10s %10.4f %8s %8.3f %8.3f %10.3f %10.3f\n" % \
                             (pcode, Angle(vbeta[i]).get_angle('GON'), t_2, ve[i], vn[i], ee[i], nn[i])
            else:
                if beta[0] is None or beta[n-1] is None:
                    ResultLog.resultlog_message += u"%-10s %10s                           %10.3f %10.3f\n" % \
                             (pcode, "", ee[i], nn[i])
                else:
                    ResultLog.resultlog_message += u"%-10s %10.4s                           %10.3f %10.3f\n" % \
                             (pcode, Angle(vbeta[i]).get_angle('GON'), ee[i], nn[i])
            pass

        ResultLog.resultlog_message += "\n"
        if beta[0] is None or beta[n-1] is None:
            ResultLog.resultlog_message += "           %10s                            %10.3f %10.3f\n" % \
                     ("", ee[n-1]-ee[0], nn[n-1]-nn[0])
            ResultLog.resultlog_message += "           %10s %8.3f %8.3f %8.3f\n\n" % \
                     ("", sumt, sumde, sumdn)
            if not free:
                ResultLog.resultlog_message += "           %10s          %8.3f %8.3f\n" % ("",dde,ddn)
        else:
            ResultLog.resultlog_message += "           %10.4s                            %10.3f %10.3f\n" % \
                     (Angle(0).get_angle('GON'), ee[n-1]-ee[0], nn[n-1]-nn[0])
            ResultLog.resultlog_message += "           %10.4s %8.3f %8.3f %8.3f\n" % \
                     (Angle(sumbeta).get_angle('GON'),sumt,sumde,sumdn)
            ResultLog.resultlog_message += "           %10.4f\n" % \
                     (Angle((n-1) * math.pi).get_angle('GON'))
            ResultLog.resultlog_message += "           %10.4s          %8.3f %8.3f\n" % \
                     (Angle(dbeta).get_angle('GON'), dde, ddn)
        if not free:
            ResultLog.resultlog_message += "                                   %8.3f\n" % ddist
     
        if free is True:
            last = n
        else:
            last = n-1
        plist = []  # list of calculated points
        for i in range(1,last):
            
            if trav_obs[i][0] is not None and trav_obs[i][0].p is not None:
                plist.append( trav_obs[i][0].p )
            else:
                plist.append( Point( trav_obs[i][0].o.point_id) )
            plist[-1].e = ee[i]
            plist[-1].n = nn[i]

        return plist

    @staticmethod
    def gauss_elimination(a, b):
        """ Solve a linear equation system::
                a * x = b

            :param a: coefficients of the equation system (list of lists)
            :param b: list of pure term of equations
            :returns: (unknowns, inverse_matrix)
        """
        size = len(b)
        for i in range(0,size):
            q = 1.0 / a[i][i]
            for k in range(0,size):
                if i != k:
                    a[i][k] = q * a[i][k]
                else:
                    a[i][k] = q
        
            b[i] = q * b[i]
            for j in range(0,size):
                if j != i:
                    t = a[j][i]
                    for k in range(0,size):
                        if i != k :
                            a[j][k] =a[j][k] - t * a[i][k]
                        else:
                            a[j][k] = -t * q
                    b[j] = b[j] - t * b[i]
        return (b, a)
    
    @staticmethod
    def orthogonal_transformation(plist):
        """ Calculate parameters of orthogonal transformation. Four parameters scale, rotation and offset.::
            E = E0 + c * e - d * n
            N = N0 + d * e + c * n

            :param plist: a list of common points used in the transormation plist[i]==[srci,desti]
            :returns: the list of transformation parameters {E0 N0 c d}
        """
        es = 0.0    # sum of source coordinates
        ns = 0.0
        Es = 0.0    # sum of destination coordinates
        Ns = 0.0
        for p in plist:
            es = es + p[0].e
            ns = ns + p[0].n
            Es = Es + p[1].e
            Ns = Ns + p[1].n

        ew = es / float(len(plist))
        nw = ns / float(len(plist))
        Ew = Es / float(len(plist))
        Nw = Ns / float(len(plist))

        s1 = 0.0    # sum of ei*Ei+ni*Ni
        s2 = 0.0    # sum of ei*Ni-ni*Ei
        s3 = 0.0    # sum of ei*ei+ni*ni
   
        for p in plist:
            e = p[0].e - ew
            n = p[0].n - nw
            E = p[1].e - Ew
            N = p[1].n - Nw
            s1 = s1 + e * E + n * N
            s2 = s2 + e * N - n * E
            s3 = s3 + e * e + n * n

        c = s1 / s3
        d = s2 / s3
        E0 = (Es - c * es + d * ns) / float(len(plist))
        N0 = (Ns - c * ns - d * es) / float(len(plist))
        return [E0, N0, c, d]

    @staticmethod
    def orthogonal3tr(plist):
        """ Calculate parameters of orthogonal transformation. Three parameters::

            E = E0 + cos(alpha) * e - sin(alpha) * n
            N = N0 + sin(alpha) * e + cos(alpha) * n

            :param plist: a list of common points used in the transormation plist[i]==[srci,desti]
            :returns: the list of transformation parameters {E0 N0 alpha}
        """
        # approximate values from Helmert4
        appr = Calculation.orthogonal_transformation(plist)
        E0 = appr[0]
        N0 = appr[1]
        alpha = math.atan2(appr[3], appr[2])

        # calculate sums
        s1 = 0.0    # -ei*sin(alpha) - ni*cos(alpha)
        s2 = 0.0    #  ei*cos(alpha) - ni*sin(alpha)
        s3 = 0.0    # (-ei*sin(alpha) - ni*cos(alpha))^2 + \
                    # ( ei*cos(alpha) - ni*sin(alpha))^2
        s4 = 0.0    # Ei - Eei
        s5 = 0.0    # Ni - Nei
        s6 = 0.0    # (-ei*sin(alpha) - ni*cos(alpha)) * (Ei-Eei) +
                    # ( ei*cos(alpha) - ni*sin(alpha)) * (Ni-Nei)
    
        for p in plist:
            e = p[0].e
            n = p[0].n
            E = p[1].e
            N = p[1].n
            w1 = -e * math.sin(alpha) - n * math.cos(alpha)
            w2 = e * math.cos(alpha) - n * math.sin(alpha)
            s1 = s1 + w1
            s2 = s2 + w2
            s3 = s3 + w1 * w1 + w2 * w2
        
            w3 = E - (E0 + e * math.cos(alpha) - n * math.sin(alpha))
            w4 = N - (N0 + e * math.sin(alpha) + n * math.cos(alpha))
            s4 = s4 + w3
            s5 = s5 + w4
            s6 = s6 + w1 * w3 + w2 * w4

        # set matrix of normal equation
        ata = []
        ata[0][0] = len(plist)
        ata[0][1] = 0.0
        ata[0][2] = s1
        ata[1][0] = 0.0
        ata[1][1] = len(plist)
        ata[1][2] = s2
        ata[2][0] = s1
        ata[2][1] = s2
        ata[2][2] = s3
        # set A*l
        al = []
        al[0] = s4
        al[1] = s5
        al[2] = s6
        # solve the normal equation
        Calculation.gauss_elimination(ata, al)

        return [ E0 + al[0], N0 + al[1], alpha + al[2] ]

    @staticmethod
    def affine_transformation(plist):
        """ Calculate parameters of affine transformation. Six parameters::
            E = E0 + a * e + b * n
            N = N0 + c * e + d * n

            :param plist: a list of common points used in the transormation plist[i]==[srci,desti]
            :returns: the list of transformation parameters {E0 N0 a b c d}
        """
        # calculate weight point in point list
        es = 0.0    # sum of source coordinates
        ns = 0.0
        Es = 0.0    # sum of destination coordinates
        Ns = 0.0
        for p in plist:
            es = es + p[0].e
            ns = ns + p[0].n
            Es = Es + p[1].e
            Ns = Ns + p[1].n
    
        ew = es / float(len(plist))
        nw = ns / float(len(plist))
        Ew = Es / float(len(plist))
        Nw = Ns / float(len(plist))

        s1 = 0.0    # sum of ei*ei
        s2 = 0.0    # sum of ni*ni
        s3 = 0.0    # sum of ei*ni
        s4 = 0.0    # sum of ei*Ei
        s5 = 0.0    # sum of ni*Ei
        s6 = 0.0    # sum of ei*Ni
        s7 = 0.0    # sum of ni*Ni
        for p in plist:
            e = p[0].e - ew
            n = p[0].n - nw
            E = p[1].e - Ew
            N = p[1].n - Nw
            s1 = s1 + e * e
            s2 = s2 + n * n
            s3 = s3 + e * n
            s4 = s4 + e * E
            s5 = s5 + n * E
            s6 = s6 + e * N
            s7 = s7 + n * N

        w = float(s1 * s2 - s3 * s3)
        a = -(s5 * s3 - s4 * s2) / w
        b = -(s4 * s3 - s1 * s5) / w
        c = -(s7 * s3 - s6 * s2) / w
        d = -(s6 * s3 - s7 * s1) / w
        E0 = (Es - a * es - b * ns) / float(len(plist))
        N0 = (Ns - c * es - d * ns) / float(len(plist))
        return [E0, N0, a, b, c, d]

    @staticmethod
    def polynomial_transformation(plist, degree = 3):
        """ Calculate parameters of polynomial (rubber sheet) transformation.::

            X = X0 + a1 * x + a2 * y + a3 * xy + a4 * x^2 + a5 * y^2 + ...
            Y = Y0 + b1 * x + b2 * y + b3 * xy + b4 * x^2 + b5 * y^2 + ...

            :param plist: a list of common points used in the transformation plist[i]==[srci,desti]
            :param degree: degree of transformation 3/4/5
            :returns: the list of parameters X0 Y0 a1 b1 a2 b2 a3 b3 ...  and the weight point coordinates in source and target system
        """
        # set up A matrix (a1 for e, a2 for n)
        np = len(plist)     # number of points
        m = (degree + 1) * (degree + 2) // 2    # number of unknowns
        # calculate average x and y to reduce rounding errors
        s1 = 0.0
        s2 = 0.0
        S1 = 0.0
        S2 = 0.0
        for p in plist:
            e = p[0].e
            n = p[0].n
            s1 = s1 + e
            s2 = s2 + n
            E = p[1].e
            N = p[1].n
            S1 = S1 + E
            S2 = S2 + N
        avge = s1 / np
        avgn = s2 / np
        avgE = S1 / np
        avgN = S2 / n
        i = 0
        a1 = [[0 for x in range(m)] for x in range(np)]
        a2 = [[0 for x in range(m)] for x in range(np)]
        l1 = [0 for x in range(np)]
        l2 = [0 for x in range(np)]
        for p in plist:
            e = p[0].e - avge
            n = p[0].n - avgn
            E = p[1].e - avgE
            N = p[1].n - avgN
            l = 0
            for j in range(0,degree+1):
                for k in range(0,degree+1):
                    if j + k <= degree:
                        a1[i][l] = math.pow(e,k) * math.pow(n,j)
                        a2[i][l] = math.pow(e,k) * math.pow(n,j)
                        l = l + 1
            l1[i] = E
            l2[i] = N
            i = i + 1
            
        # set matrix of normal equation
        # N1 = a1T*a1, N2 = a2T * a2, n1 = a1T * l1, n2 = a2T * l2
        N1 = [[0 for x in range(m)] for x in range(m)]
        N2 = [[0 for x in range(m)] for x in range(m)]
        n1 = [0 for x in range(m)]
        n2 = [0 for x in range(m)]
        for i in range(0,m):
            for j in range(i,m):
                s1 = 0.0
                s2 = 0.0
                for k in range(0,np):
                    s1 = s1 + a1[k][i] * a1[k][j]
                    s2 = s2 + a2[k][i] * a2[k][j]
                N1[i][j] = s1
                N1[j][i] = s1
                N2[i][j] = s2
                N2[j][i] = s2
        for i in range(0,m):
            s1 = 0.0
            s2 = 0.0
            for k in range(0,np):
                s1 = s1 + a1[k][i] * l1[k]
                s2 = s2 + a2[k][i] * l2[k]
            n1[i] = s1
            n2[i] = s2

        # solve the normal equation
        (x1, inv1) = Calculation.gauss_elimination(N1, n1)
        (x2, inv2) = Calculation.gauss_elimination(N2, n2)
        return (x1, x2, [avge, avgn, avgE, avgN])

if __name__ == "__main__":
    """
        modul test
    """
    p1 = Point("1", 100, 200, 20)
    p2 = Point("2", 150, 250, 30)
    d = distance2d(p1, p2)
    if not compare(d.d, 70.7107):
        print "Distance2d test failed"
    d = distance3d(p1, p2)
    if not compare(d.d, 71.4143):
        print "Distance3d test failed"
    b = bearing(p1, p2)
    if not compare(b.get_angle('DMS'), '45-00-00'):
        print "Bearing p1-p2 test failed"
    b = bearing(p2, p1)
    if not compare(b.get_angle('DMS'), '225-00-00'):
        print "Bearing p2-p1 test failed"
    b = bearing(p1, p1)
    if not compare(b.get_angle('DMS'), '0-00-00'):
        print "Bearing p1-p1 test failed"
    
    # intersection test
    s1o = PolarObservation('1', 'station', Angle(0))
    s2o = PolarObservation('2', 'station', Angle(0))
    s1 = Station(p1, s1o)
    s2 = Station(p2, s2o)
    o1 = PolarObservation("p", None, Angle(25, "DEG"))
    o2 = PolarObservation("p", None, Angle(310, "DEG"))
    p3 = Calculation.intersection(s1, o1, s2, o2)
    if not compare(p3, Point('p', 130.8201, 266.0939)):
        print "Simple-1 intersection test failed"
    A1 = Point("A1", -150, -120)
    A2 = Point("A2", 130, 75)
    sA1o = PolarObservation('A1', 'station', Angle("76-13-23", "DMS"))
    sA2o = PolarObservation('A2', 'station', Angle("324-10-58", "DMS"))
    sA1 = Station(A1, sA1o)
    sA2 = Station(A2, sA2o)
    oA1 = PolarObservation("p3", None, Angle("308-46-36", "DMS"))
    oA2 = PolarObservation("p3", None, Angle("345-49-02", "DMS"))
    P3 = Calculation.intersection(sA1, oA1, sA2, oA2)
    if not compare(P3, Point('p3', -5.8979, 189.0319)):
        print "Simple-2 intersection test failed"
    sA1o = PolarObservation('A1', 'station', Angle("0", "DMS"))
    sA2o = PolarObservation('A2', 'station', Angle("0", "DMS"))
    sA1 = Station(A1, sA1o)
    sA2 = Station(A2, sA2o)
    oA1 = PolarObservation("p4", None, Angle("225", "DMS"))
    oA2 = PolarObservation("p4", None, Angle("45", "DMS"))
    P4 = Calculation.intersection(sA1, oA1, sA2, oA2)
    print "Result for impossible intersection:"
    print P4.id, P4.e, P4.n
    A3 = Point("A3", 0, 0)
    A4 = Point("A4", 100, 100)
    sA3o = PolarObservation('A3', 'station', Angle("0", "DMS"))
    sA4o = PolarObservation('A4', 'station', Angle("0", "DMS"))
    sA3 = Station(A3, sA3o)
    sA4 = Station(A4, sA4o)
    oA3 = PolarObservation("p5", None, Angle("45", "DMS"))
    oA4 = PolarObservation("p5", None, Angle("225", "DMS"))
    P5 = Calculation.intersection(sA3, oA3, sA4, oA4)
    print "Result for observe each other:"
    print P5.id, P5.e, P5.n #p5 100.0 100.0
    A3 = Point("A3", 0, 0)
    A4 = Point("A4", 100, 100)
    sA3o = PolarObservation('A3', 'station', Angle("0", "DMS"))
    sA4o = PolarObservation('A4', 'station', Angle("0", "DMS"))
    sA3 = Station(A3, sA3o)
    sA4 = Station(A4, sA4o)
    oA3 = PolarObservation("p5", None, Angle("45", "DMS"))
    oA4 = PolarObservation("p5", None, Angle("45", "DMS"))
    P5 = Calculation.intersection(sA3, oA3, sA4, oA4)
    if not compare(P5, None):
        print "Intersection test for parallel observation failed"
    
    # resection test
    p1res = Point("3")
    o1res = PolarObservation('3', None, "station", Angle(0) )
    s1res = Station( p1res, o1res )
    p101res = Point( "101", 658031.813, 247985.580 )
    p102res = Point( "102", 657638.800, 247759.380 )
    p103res = Point( "103", 658077.700, 247431.381 )
    o101res = PolarObservation( "101", None, Angle("22-45-56", "DMS") )
    o102res = PolarObservation( "102", None, Angle("164-38-59", "DMS") )
    o103res = PolarObservation( "103", None, Angle("96-23-12", "DMS") )
    p1res = Calculation.resection( s1res, p101res, p102res, p103res, o101res, o102res, o103res )
    if not compare( p1res, Point( "3", 657871.9494, 247973.2414 ) ):
        print "Simple-1 resection test failed"
    P4res = Point("P4")
    oP4res = PolarObservation('P4', "station", Angle(0) )
    sP4res = Station( P4res, oP4res )
    o101res = PolarObservation( "101", None, Angle("202-45-56", "DMS") )
    o102res = PolarObservation( "102", None, Angle("344-38-59", "DMS") )
    o103res = PolarObservation( "103", None, Angle("276-23-12", "DMS") )
    P4res = Calculation.resection( sP4res, p101res, p102res, p103res, o101res, o102res, o103res )
    if not compare( P4res, Point( "P4", 657871.9494, 247973.2414 ) ):
        print "Simple-2 resection test failed"
    P5res = Point("P5")
    oP5res = PolarObservation('P5', "station", Angle(0) )
    sP5res = Station( P5res, oP5res )
    o101res = PolarObservation( "101", None, Angle("88-41-35.8669", "DMS") )
    o102res = PolarObservation( "102", None, Angle("40-11-52.9394", "DMS") )
    o103res = PolarObservation( "103", None, Angle("155-23-15.1567", "DMS") )
    P5res = Calculation.resection( sP5res, p101res, p102res, p103res, o101res, o102res, o103res )
    if not compare( P5res, None ):
        print "Resection test for dangerous circle failed"
    P6res = Point("P6")
    oP6res = PolarObservation('P6', "station", Angle(0) )
    sP6res = Station( P6res, oP6res )
    p101res = Point( "101", -50, 80 )
    p102res = Point( "102", 0, 80 )
    p103res = Point( "103", 50, 80 )
    o101res = PolarObservation( "101", None, Angle("140-32-24", "DMS") )
    o102res = PolarObservation( "102", None, Angle("97-13-15", "DMS") )
    o103res = PolarObservation( "103", None, Angle("70-43-22", "DMS") )
    P6res = Calculation.resection( sP6res, p101res, p102res, p103res, o101res, o102res, o103res )
    if not compare( P6res, Point( "P6", -29.6182, 142.6576 ) ):
        print "Resection test for reference points on a line failed"
    P7res = Point("P7")
    oP7res = PolarObservation('P7', "station", Angle(0) )
    sP7res = Station( P7res, oP7res )
    p101res = Point( "101", -50, 80 )
    p102res = Point( "102", 0, 80 )
    p103res = Point( "103", 50, 80 )
    o101res = PolarObservation( "101", None, Angle("225", "DMS") )
    o102res = PolarObservation( "102", None, Angle("45", "DMS") )
    o103res = PolarObservation( "103", None, Angle("45", "DMS") )
    P7res = Calculation.resection( sP7res, p101res, p102res, p103res, o101res, o102res, o103res )
    if not compare( P7res, None ):
        print "Resection test for reference points and station point on a line failed"
    
    #orientation
    p101ori = Point( "101", 5693.45, 328.81 )
    p102ori = Point( "102", 6002.13, 1001.13 )
    p103ori = Point( "103", 5511.25, -253.16 )
    p104ori = Point( "104", 5033.45, -396.15 )
    p201ori = Point( "201", -4396.15, -561.13 )
    p202ori = Point( "202", -4000.55, 496.14 )
    p203ori = Point( "203", -5115.33, 366.11 )
    p204ori = Point( "204", -3863.96, -268.15 )
    p205ori = Point( "205", -3455.37, -959.36 )
    p206ori = Point( "206", -5500.08, -724.69 )
    p301ori = Point( "301", 4512.35, -496.29 )
    p302ori = Point( "302", 4073.16, -986.32 )
    p303ori = Point( "303", 3952.25, 818.66 )
    p401ori = Point( "401", -3516.22, 156.25 )
    p402ori = Point( "402", -3986.35, 460.18 )
    p403ori = Point( "403", -4019.28, 510.54 )
    p501ori = Point( "501", -116.94, 150.86 )
    p502ori = Point( "502", 127.03, 337.43 )
    p503ori = Point( "503", 887.64, -1068.99 )
    p504ori = Point( "504", -999.53, -896.77 )
    p505ori = Point( "505", -1150.22, 150.86 )
    o101ori = PolarObservation('101', "station")
    s101ori = Station( p101ori, o101ori )
    o102ori = PolarObservation( "102", None, Angle("268-14-13", "DMS") )
    o103ori = PolarObservation( "103", None, Angle("80-57-34", "DMS") )
    o104ori = PolarObservation( "104", None, Angle("105-53-19", "DMS") )
    z101ori = Calculation.orientation(s101ori, [[p102ori,o102ori], [p103ori,o103ori], [p104ori,o104ori]])
    if not compare( z101ori.get_angle('DMS'), '116-25-30' ):
        print "Simple-1 orientation test failed"
    o201ori = PolarObservation('201', "station")
    s201ori = Station( p201ori, o201ori )
    o202ori = PolarObservation( "202", None, Angle("316-40-57", "DMS") )
    o203ori = PolarObservation( "203", None, Angle("258-22-09", "DMS") )
    o204ori = PolarObservation( "204", None, Angle("357-19-49", "DMS") )
    o205ori = PolarObservation( "205", None, Angle("49-6-32", "DMS") )
    o206ori = PolarObservation( "206", None, Angle("197-44-22", "DMS") )
    z201ori = Calculation.orientation(s201ori, [[p202ori,o202ori], [p203ori,o203ori], [p204ori,o204ori], [p205ori,o205ori], [p206ori,o206ori]])
    if not compare( z201ori.get_angle('DMS'), '63-50-00' ):
        print "Simple-2 orientation test failed"
    o201ori = PolarObservation('201', "station")
    s201ori = Station( p201ori, o201ori )
    o202ori = PolarObservation( "202", None, Angle(351.86944, "GON") )
    o203ori = PolarObservation( "203", None, Angle(287.07685, "GON") )
    o204ori = PolarObservation( "204", None, Angle(397.03364, "GON") )
    o205ori = PolarObservation( "205", None, Angle(54.56543, "GON") )
    o206ori = PolarObservation( "206", None, Angle(219.71049, "GON") )
    z201ori = Calculation.orientation(s201ori, [[p202ori,o202ori], [p203ori,o203ori], [p204ori,o204ori], [p205ori,o205ori], [p206ori,o206ori]])
    if not compare( z201ori.get_angle('DMS'), '63-50-00' ):
        print "Simple-3 orientation test failed"
    o301ori = PolarObservation('301', "station")
    s301ori = Station( p301ori, o301ori )
    o302ori = PolarObservation( "302", None, Angle("166-10-30", "DMS") )
    o303ori = PolarObservation( "303", None, Angle("281-13-55", "DMS") )
    z301ori = Calculation.orientation(s301ori, [[p302ori,o302ori], [p303ori,o303ori]])
    if not compare( z301ori.get_angle('DMS'), '55-41-44' ):
        print "Simple-4 orientation test failed"
    o401ori = PolarObservation('401', "station")
    s401ori = Station( p401ori, o401ori )
    o402ori = PolarObservation( "402", None, Angle("101-37-23", "DMS") )
    o403ori = PolarObservation( "403", None, Angle("103-53-37", "DMS") )
    z401ori = Calculation.orientation(s401ori, [[p402ori,o402ori], [p403ori,o403ori]])
    if not compare( z401ori.get_angle('DMS'), '201-15-38' ):
        print "Simple-5 orientation test failed"
    o401ori = PolarObservation('401', "station")
    s401ori = Station( p401ori, o401ori )
    o402ori = PolarObservation( "402", None, Angle("101-37-23", "DMS") )
    z401ori = Calculation.orientation(s401ori, [[p402ori,o402ori]])
    if not compare( z401ori.get_angle('DMS'), '201-15-32' ):
        print "Simple-6 orientation test failed"
    o501ori = PolarObservation('501', "station")
    s501ori = Station( p501ori, o501ori )
    o502ori = PolarObservation( "502", None, Angle("170-50-59", "DMS") )
    o503ori = PolarObservation( "503", None, Angle("258-46-56", "DMS") )
    o504ori = PolarObservation( "504", None, Angle("338-22-5", "DMS") )
    o505ori = PolarObservation( "505", None, Angle("28-15-23", "DMS") )
    z501ori = Calculation.orientation(s501ori, [[p502ori,o502ori], [p503ori,o503ori], [p504ori,o504ori], [p505ori,o505ori]])
    if not compare( z501ori.get_angle('DMS'), '241-44-41' ):
        print "Simple-6 orientation test failed"

    # polar points
    p101pol = Point("101", 13456.25, 12569.75)
    p201pol = Point("201", 13102.13, 11990.13)
    p202pol = Point("202", 13569.11, 12788.66)
    p203pol = Point("203", 13861.23, 12001.54)
    o101pol = PolarObservation('101', "station")
    s101pol = Station( p101pol, o101pol )
    o201pol = PolarObservation("201", None, Angle("112-15-15", "DMS"))
    o202pol = PolarObservation("202", None, Angle("288-06-30", "DMS"))
    o203pol = PolarObservation("203", None, Angle("45-21-12", "DMS"))
    o9pol = PolarObservation("9", None, Angle("145-10-16", "DMS"), None, Distance(206.17,"HD") )
    o10pol = PolarObservation("10", None, Angle("201-30-47", "DMS"), None, Distance(219.38,"HD") )
    z101pol = Calculation.orientation(s101pol, [[p201pol,o201pol], [p202pol,o202pol], [p203pol,o203pol]])
    if not compare( z101pol.get_angle('DMS'), '99-10-05' ):
        print "Simple-1 polar points test failed by orientation"
    s101pol.o.hz = z101pol
    p9pol = Calculation.polarpoint(s101pol, o9pol)
    p10pol = Calculation.polarpoint(s101pol, o10pol)
    if not compare( p9pol, Point( "9", 13270.4141, 12480.4691 ) ):
        print "Simple-1 polar points test failed by P9"
    if not compare( p10pol, Point( "10", 13267.5785, 12681.6903 ) ):
        print "Simple-1 polar points test failed by P10"
    pA1pol = Point("A1", 153.867, 456.430)
    pT1pol = Point("T1", -237.865, -297.772)
    pT2pol = Point("T2", -1549.927, 669.6126)
    pT3pol = Point("T3", 1203.064, -220.0314)
    oA1pol = PolarObservation('A1', "station")
    sA1pol = Station( pA1pol, oA1pol )
    oT1pol = PolarObservation("T1", None, Angle("73-02-35", "DMS"))
    oT2pol = PolarObservation("T2", None, Angle("142-43-39", "DMS"))
    oT3pol = PolarObservation("T3", None, Angle("348-24-26", "DMS"))
    oP1pol = PolarObservation("P1", None, Angle("112-43-47", "DMS"), None, Distance(673.699,"HD") )
    oP2pol = PolarObservation("P2", None, Angle("84-0-44", "DMS"), None, Distance(788.105,"HD") )
    zA1pol = Calculation.orientation(sA1pol, [[pT1pol,oT1pol], [pT2pol,oT2pol], [pT3pol,oT3pol]])
    if not compare( zA1pol.get_angle('DMS'), '134-24-16' ):
        print "Simple-2 polar points test failed by orientation"
    sA1pol.o.hz = zA1pol
    pP1pol = Calculation.polarpoint(sA1pol, oP1pol)
    pP2pol = Calculation.polarpoint(sA1pol, oP2pol)
    if not compare( pP1pol, Point( "P1", -466.8905, 194.6468 ) ):
        print "Simple-2 polar points test failed by P1"
    if not compare( pP2pol, Point( "P2", -335.8415, -161.0610 ) ):
        print "Simple-2 polar points test failed by P2"
    
    #traverse1
    # closed at one end and known bearings at one end (free traverse)
    p5241otra = Point("5241",646414.44,211712.77)
    p5245otra = Point("5245",646938.71,212635.92)
    p5246otra = Point("5246",646380.61,212793.97)
    p5247otra = Point("5247",646381.14,212476.49)
    o5247otra = PolarObservation('5247', "station")
    s5247otra = Station( p5247otra, o5247otra )
    o5241otra = PolarObservation( "5241", None, Angle("245-23-41", "DMS") )
    o5245otra = PolarObservation( "5245", None, Angle("141-56-11", "DMS") )
    o5246otra = PolarObservation( "5246", None, Angle("67-47-14", "DMS") )
    s5247otra.o.hz = Calculation.orientation(s5247otra, [[p5241otra,o5241otra], [p5245otra,o5245otra], [p5246otra,o5246otra]])
    if not compare( s5247otra.o.hz.get_angle('DMS'), '292-06-34' ):
        print "Traverse test for free traverse failed by orientation"
    
    o5247_111otra = PolarObservation("111", None, Angle("241-26-57","DMS"), None, Distance(123.42,"HD")) 
    s111otra = Station( None, PolarObservation('111', "station") )
    o111_5247otra = PolarObservation("5247", None, Angle("225-39-00","DMS")) 
    o111_112otra = PolarObservation("112", None, Angle("92-38-43","DMS"), None, Distance(142.81,"HD")) 
    s112otra = Station( None, PolarObservation('112', "station") )
    o112_111otra = PolarObservation("111", None, Angle("227-16-34","DMS")) 
    o112_113otra = PolarObservation("113", None, Angle("69-16-28","DMS"), None, Distance(253.25,"HD")) 
    s113otra = Station( None, PolarObservation('113', "station") )
    o113_112otra = PolarObservation("112", None, Angle("102-56-44","DMS")) 
    o113_114otra = PolarObservation("114", None, Angle("205-46-21","DMS"), None, Distance(214.53,"HD")) 
    s114otra = Station( None, PolarObservation('114', "station") )
    o114_113otra = PolarObservation("113", None, Angle("104-23-11","DMS")) 
    o114_115otra = PolarObservation("115", None, Angle("305-54-29","DMS"), None, Distance(234.23,"HD")) 
    s115otra = Station( None, PolarObservation("115", 'station') )
    plist = Calculation.traverse( [ [s5247otra,None,o5247_111otra], [s111otra,o111_5247otra,o111_112otra],
                           [s112otra,o112_111otra,o112_113otra],[s113otra,o113_112otra,o113_114otra],
                           [s114otra,o114_113otra,o114_115otra],[s115otra,None,None] ] )
    if not compare( plist[0], Point('111', 646394.9860, 212353.8491) ):
        print "Traverse test for free traverse failed by point 111"
    if not compare( plist[1], Point('112', 646302.1362, 212245.3429) ):
        print "Traverse test for free traverse failed by point 112"
    if not compare( plist[2], Point('113', 646077.3941, 212128.60997) ):
        print "Traverse test for free traverse failed by point 113"
    if not compare( plist[3], Point('114', 646131.5459, 211921.02697) ):
        print "Traverse test for free traverse failed by point 114"
    if not compare( plist[4], Point('115', 646103.4028, 211688.4938) ):
        print "Traverse test for free traverse failed by point 115"

    #traverse2
    # closed at both ends and known bearings at both ends
    pKtra = Point("K",599767.21,148946.70)
    pVtra = Point("V",599733.75,149831.76)
    p1015tra = Point("1015",598642.17,148436.26)
    p1016tra = Point("1016",600136.60,148588.85)
    p1017tra = Point("1017",600264.30,149325.79)
    p1018tra = Point("1018",598258.90,149496.78)
    p1019tra = Point("1019",600092.33,150676.80)

    oKtra = PolarObservation('K', "station")
    sKtra = Station( pKtra, oKtra )
    oK_1017tra = PolarObservation( "1017", None, Angle("61-28-18", "DMS") )
    oK_1016tra = PolarObservation( "1016", None, Angle("142-53-28", "DMS") )
    oK_1015tra = PolarObservation( "1015", None, Angle("254-23-32", "DMS") )
    oK_1tra = PolarObservation( "1", None, Angle("17-14-18", "DMS"), None, Distance(139.82,"HD") )
    sKtra.o.hz = Calculation.orientation(sKtra, [[p1017tra,oK_1017tra], [p1016tra,oK_1016tra], [p1015tra,oK_1015tra]])
    if not compare( sKtra.o.hz.get_angle('DMS'), '351-12-05' ):
        print "Test traverse closed at both ends and known bearings at both ends failed by orientation1"
    
    s1tra = Station( None, PolarObservation('1', "station") )
    o1_Ktra = PolarObservation("K", None, Angle("79-28-20","DMS"), None, Distance(139.85,"HD")) 
    o1_2tra = PolarObservation("2", None, Angle("236-13-46","DMS"), None, Distance(269.32,"HD")) 
    o1_501tra = PolarObservation("501", None, Angle("204-58-10","DMS"), None, Distance(59.12,"HD")) 
    s2tra = Station( None, PolarObservation('2', "station") )
    o2_3tra = PolarObservation("3", None, Angle("82-18-45","DMS"), None, Distance(169.40,"HD")) 
    o2_1tra = PolarObservation("1", None, Angle("217-58-34","DMS"), None, Distance(269.36,"HD")) 
    s3tra = Station( None, PolarObservation('3', "station") )
    o3_2tra = PolarObservation("2", None, Angle("262-18-44","DMS"), None, Distance(169.45,"HD")) 
    o3_Vtra = PolarObservation("V", None, Angle("41-18-10","DMS"), None, Distance(345.90,"HD")) 
    o3_502tra = PolarObservation("502", None, Angle("344-28-25","DMS"), None, Distance(55.46,"HD")) 

    oVtra = PolarObservation('V', "station")
    sVtra = Station( pVtra, oVtra )
    oV_3tra = PolarObservation( "3", None, Angle("257-44-08", "DMS"), None, Distance(345.94,"HD") )
    oV_1018tra = PolarObservation( "1018", None, Angle("346-24-11", "DMS") )
    oV_1019tra = PolarObservation( "1019", None, Angle("112-12-06", "DMS") )
    oV_1017tra = PolarObservation( "1017", None, Angle("222-50-58", "DMS") )
    sVtra.o.hz = Calculation.orientation(sVtra, [[p1018tra,oV_1018tra], [p1019tra,oV_1019tra], [p1017tra,oV_1017tra]])
    if not compare( sVtra.o.hz.get_angle('DMS'), '270-47-46' ):
        print "Test traverse closed at both ends and known bearings at both ends failed by orientation2"

    plist = Calculation.traverse( [ [sKtra,None,oK_1tra], [s1tra,o1_Ktra,o1_2tra], [s2tra,o2_1tra,o2_3tra],
                                   [s3tra,o3_2tra,o3_Vtra], [sVtra,oV_3tra,None] ] )
    if not compare( plist[0], Point('1', 599787.74865, 149085.0079) ):
        print "Test traverse closed at both ends and known bearings at both ends failed by point 1"
    if not compare( plist[1], Point('2', 599718.9691, 149345.3886) ):
        print "Test traverse closed at both ends and known bearings at both ends failed by point 2"
    if not compare( plist[2], Point('3', 599802.5094, 149492.7786) ):
        print "Test traverse closed at both ends and known bearings at both ends failed by point 3"

    #traverse3
    # closed at both ends and known bearing at one end
    pA5tra = Point("A5",646333.5695,276616.4171)
    pA11tra = Point("A11",646502.8710,276361.2386)
    pA4tra = Point("A4",646284.6886,276659.2165)

    oA5tra = PolarObservation('A5', "station")
    sA5tra = Station( pA5tra, oA5tra )
    oA5_A4tra = PolarObservation( "A4", None, Angle("311-12-21", "DMS") )
    oA5_A6tra = PolarObservation( "A6", None, Angle("136-36-49", "DMS"), Angle("100-13-22", "DMS"), Distance(58.405,"SD") )
    sA5tra.o.hz = Calculation.orientation(sA5tra, [[pA4tra,oA5_A4tra]])
    if not compare( sA5tra.o.hz.get_angle('DMS'), '359-59-57' ):
        print "Test traverse closed at both ends and known bearing at one end failed by orientation"
    
    sA6tra = Station( None, PolarObservation('A6', "station") )
    oA6_A5tra = PolarObservation("A5", None, Angle("316-36-49","DMS"), Angle("79-56-53","DMS"), Distance(58.378,"SD"))
    oA6_A7tra = PolarObservation("A7", None, Angle("136-43-52","DMS"), Angle("101-55-08","DMS"), Distance(43.917,"SD"))
    sA7tra = Station( None, PolarObservation('A7', "station") )
    oA7_A6tra = PolarObservation("A6", None, Angle("316-43-52","DMS"), Angle("78-21-53","DMS"), Distance(43.878,"SD"))
    oA7_A8tra = PolarObservation("A8", None, Angle("141-48-30","DMS"), Angle("102-29-18","DMS"), Distance(48.459,"SD"))
    sA8tra = Station( None, PolarObservation('A8', "station") )
    oA8_A7tra = PolarObservation("A7", None, Angle("321-48-30","DMS"), Angle("77-49-44","DMS"), Distance(48.401,"SD"))
    oA8_A9tra = PolarObservation("A9", None, Angle("153-25-18","DMS"), Angle("100-01-16","DMS"), Distance(47.098,"SD"))
    sA9tra = Station( None, PolarObservation('A9', "station") )
    oA9_A8tra = PolarObservation("A8", None, Angle("333-25-18","DMS"), Angle("80-17-11","DMS"), Distance(47.040,"SD"))
    oA9_A10tra = PolarObservation("A10", None, Angle("153-59-32","DMS"), Angle("97-46-19","DMS"), Distance(58.077,"SD"))
    sA10tra = Station( None, PolarObservation('A10', "station") )
    oA10_A9tra = PolarObservation("A9", None, Angle("333-59-32","DMS"), Angle("82-27-53","DMS"), Distance(58.045,"SD"))
    oA10_A11tra = PolarObservation("A11", None, Angle("154-05-41","DMS"), Angle("97-06-32","DMS"), Distance(58.188,"SD"))
    
    sA11tra = Station( pA11tra, PolarObservation('A11', "station") )
    oA11_A10tra = PolarObservation("A10", None, Angle("334-05-41","DMS"), Angle("83-09-29","DMS"), Distance(58.151,"SD"))

    plist = Calculation.traverse( [ [sA5tra,None,oA5_A6tra], [sA6tra,oA6_A5tra,oA6_A7tra], [sA7tra,oA7_A6tra,oA7_A8tra],
             [sA8tra,oA8_A7tra,oA8_A9tra], [sA9tra,oA9_A8tra,oA9_A10tra], [sA10tra,oA10_A9tra,oA10_A11tra], [sA11tra,oA11_A10tra,None] ] )
    if not compare( plist[0], Point('A6', 646373.0353, 276574.6808) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A6"
    if not compare( plist[1], Point('A7', 646402.4768, 276543.4174) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A7"
    if not compare( plist[2], Point('A8', 646431.7153, 276506.2621) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A8"
    if not compare( plist[3], Point('A9', 646452.4490, 276464.8193) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A9"
    if not compare( plist[4], Point('A10', 646477.6637, 276413.1392) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A10"

    #traverse4
    # loop traverse
    pA5tra = Point("A5",646333.5695,276616.4171)
    pA4tra = Point("A4",646284.6886,276659.2165)

    oA5tra = PolarObservation('A5', "station")
    sA5tra = Station( pA5tra, oA5tra )
    oA5_A4tra = PolarObservation( "A4", None, Angle("311-12-21", "DMS") )
    oA5_A6tra = PolarObservation( "A6", None, Angle("136-36-49", "DMS"), Angle("100-13-22", "DMS"), Distance(58.405,"SD") )
    oA5_A11tra = PolarObservation( "A11", None, Angle("146-26-58", "DMS"), Angle("90-00-00", "DMS"), Distance(306.234,"SD") )
    sA5tra.o.hz = Calculation.orientation(sA5tra, [[pA4tra,oA5_A4tra]])
    if not compare( sA5tra.o.hz.get_angle('DMS'), '359-59-57' ):
        print "Test traverse closed at both ends and known bearing at one end failed by orientation"
    
    sA6tra = Station( None, PolarObservation('A6', "station") )
    oA6_A5tra = PolarObservation("A5", None, Angle("316-36-49","DMS"), Angle("79-56-53","DMS"), Distance(58.378,"SD"))
    oA6_A7tra = PolarObservation("A7", None, Angle("136-43-52","DMS"), Angle("101-55-08","DMS"), Distance(43.917,"SD"))
    sA7tra = Station( None, PolarObservation('A7', "station") )
    oA7_A6tra = PolarObservation("A6", None, Angle("316-43-52","DMS"), Angle("78-21-53","DMS"), Distance(43.878,"SD"))
    oA7_A8tra = PolarObservation("A8", None, Angle("141-48-30","DMS"), Angle("102-29-18","DMS"), Distance(48.459,"SD"))
    sA8tra = Station( None, PolarObservation('A8', "station") )
    oA8_A7tra = PolarObservation("A7", None, Angle("321-48-30","DMS"), Angle("77-49-44","DMS"), Distance(48.401,"SD"))
    oA8_A9tra = PolarObservation("A9", None, Angle("153-25-18","DMS"), Angle("100-01-16","DMS"), Distance(47.098,"SD"))
    sA9tra = Station( None, PolarObservation('A9', "station") )
    oA9_A8tra = PolarObservation("A8", None, Angle("333-25-18","DMS"), Angle("80-17-11","DMS"), Distance(47.040,"SD"))
    oA9_A10tra = PolarObservation("A10", None, Angle("153-59-32","DMS"), Angle("97-46-19","DMS"), Distance(58.077,"SD"))
    sA10tra = Station( None, PolarObservation('A10', "station") )
    oA10_A9tra = PolarObservation("A9", None, Angle("333-59-32","DMS"), Angle("82-27-53","DMS"), Distance(58.045,"SD"))
    oA10_A11tra = PolarObservation("A11", None, Angle("154-05-41","DMS"), Angle("97-06-32","DMS"), Distance(58.188,"SD"))
    sA11tra = Station( None, PolarObservation('A11', "station") )
    oA11_A10tra = PolarObservation("A10", None, Angle("334-05-41","DMS"), Angle("83-09-29","DMS"), Distance(58.151,"SD"))
    oA11_A5tra = PolarObservation("A5", None, Angle("326-26-13","DMS"), Angle("90-00-00","DMS"), Distance(306.233,"SD"))

    plist = Calculation.traverse( [ [sA5tra,None,oA5_A6tra], [sA6tra,oA6_A5tra,oA6_A7tra], [sA7tra,oA7_A6tra,oA7_A8tra],
             [sA8tra,oA8_A7tra,oA8_A9tra], [sA9tra,oA9_A8tra,oA9_A10tra], [sA10tra,oA10_A9tra,oA10_A11tra], [sA11tra,oA11_A10tra,None] ] )
    if not compare( plist[0], Point('A6', 646373.0539, 276574.6449) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A6"
    if not compare( plist[1], Point('A7', 646402.5093, 276543.3546) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A7"
    if not compare( plist[2], Point('A8', 646431.7631, 276506.1698) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A8"
    if not compare( plist[3], Point('A9', 646452.5118, 276464.6981) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A9"
    if not compare( plist[4], Point('A10', 646477.7451, 276412.9820) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A10"
    if not compare( plist[5], Point('A11', 646502.9712, 276361.0454) ):
        print "Test traverse closed at both ends and known bearing at one end failed by point A11"

    # test for polarpoint 3d
    ppp = Point("1",10,20,30)
    ooo = PolarObservation("1","station",Angle("0","DMS"),None,None,1.0)
    sss = Station(ppp,ooo)
    oo2 = PolarObservation("2",None,Angle("90","DMS"), Angle("45","DMS"), Distance(20,"SD"), 3.5)
    pp2 = Calculation.polarpoint(sss,oo2)
    if not compare( pp2, Point('2', 24.1421, 20.00000, 41.6421) ):
        print "Simple-1 polarpoint 3D test failed"

    ppp = Point("1",10,20,30)
    ooo = PolarObservation("1","station",Angle("0","DMS"),None,None,-1.0)
    sss = Station(ppp,ooo)
    oo2 = PolarObservation("2",None,Angle("90","DMS"), Angle("45","DMS"), Distance(20,"SD"), 3.5)
    pp2 = Calculation.polarpoint(sss,oo2)
    if not compare( pp2, Point('2', 24.1421, 20.00000, 39.6421) ):
        print "Simple-2 polarpoint 3D test failed"

    ppp = Point("1",10,20,30)
    ooo = PolarObservation("1","station",Angle("0","DMS"),None,None,1.0)
    sss = Station(ppp,ooo)
    oo2 = PolarObservation("2",None,Angle("90","DMS"), Angle("90","DMS"), Distance(20,"SD"), 3.5)
    pp2 = Calculation.polarpoint(sss,oo2)
    if not compare( pp2, Point('2', 30.0000, 20.0000, 27.5) ):
        print "Simple-3 polarpoint 3D test failed"
    
