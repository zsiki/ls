#!/usr/bin/env python
"""
    GNU Gama interface classes for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

import re
from base_classes import *
from xml.dom import minidom, Node

class GamaInterface(object):
    """
        interface class to GNU Gama
    """
    def __init__(self, dimension=2, probability=0.95, stdev_angle=3, stdev_dist=3, stdev_dist1=3):
        self.dimension = dimension
        self.probability = probability
        self.stdev_angle = stdev_angle
        self.stdev_dist = stdev_dist
        self.stdev_dist1 = stdev_dist1
        self.points = []
        self.observations = []

    def add_point(self, point, state='ADJ'):
        """
            Add point to adjustment
            :param point Point
            :state FIX or ADJ
        """
        for p, s in self.points:
            # avoid duplicated points
            if p.id == point.id:
                return
        self.points.append([point, state])

    def add_observation(self, obs):
        """
            Add observation to adjustment
            :param obs PolarObservation
        """
        self.observations.append(obs)

    def adjust(self):
        """
            Export data to GNU Gama xml, adjust the network and read result
            :return None/0 failure/success
        """
        # fix = 0 free network
        fix = 0
        adj = 0
        for p, s in self.points:
            if s == 'FIX':
                fix += 1
            else:
                adj += 1
        if adj == 0 or len(self.observations) == 0:
            # no unknowns or observations
            return None
        doc = minidom.Document()
        doc.appendChild(doc.createComment('Gama XML created by Land Surveying plugin for QGIS'))
        gama_local = doc.createElement('gama-local')
        gama_local.setAttribute('version', '2.0')
        doc.appendChild(gama_local)
        network = doc.createElement('network')
        network.setAttribute('axes-xy', 'ne')
        network.setAttribute('angles', 'left-handed')
        gama_local.appendChild(network)
        description = doc.createElement('description')
        if self.dimension == 1:
            description.appendChild(doc.createTextNode('GNU Gama 1D network'))
        elif self.dimension == 2:
            description.appendChild(doc.createTextNode('GNU Gama 2D network'))
        elif self.dimension == 3:
            description.appendChild(doc.createTextNode('GNU Gama 3D network'))
        network.appendChild(description)
        parameters = doc.createElement('parameters')
        parameters.setAttribute('sigma-apr', '1')
        parameters.setAttribute('conf-pr', str(self.probability))
        parameters.setAttribute('tol-abs', '1000')
        parameters.setAttribute('sigma-act', 'aposteriori')
        parameters.setAttribute('update-constrained-coordinates', 'yes')
        network.appendChild(parameters)
        points_observations = doc.createElement('points-observations')
        points_observations.setAttribute('distance-stdev', str(self.stdev_dist) + ' ' + str(self.stdev_dist1)) 
        points_observations.setAttribute('direction-stdev', str(self.stdev_angle))
        points_observations.setAttribute('angle-stdev', str(math.sqrt(self.stdev_angle * 2)))
        points_observations.setAttribute('zenith-angle-stdev', str(self.stdev_angle))
        network.appendChild(points_observations)
        for p, s in self.points:
            if self.dimension == 1 and not p.z is None:
                tmp = doc.createElement('point')
                tmp.setAttribute('id', p.id)
                tmp.setAttribute('z', str(p.z))
                if s == 'FIX':
                    tmp.setAttribute('fix', 'z')
                else:
                    if fix == 0:
                        tmp.setAttribute('adj', 'Z')
                    else:
                        tmp.setAttribute('adj', 'z')
                points_observations.appendChild(tmp)
            elif self.dimension == 2 and not p.e is None and not p.n is None:
                tmp = doc.createElement('point')
                tmp.setAttribute('id', p.id)
                tmp.setAttribute('y', str(p.e))
                tmp.setAttribute('x', str(p.n))
                if s == 'FIX':
                    tmp.setAttribute('fix', 'xy')
                else:
                    if fix == 0:
                        tmp.setAttribute('adj', 'XY')
                    else:
                        tmp.setAttribute('adj', 'xy')
                points_observations.appendChild(tmp)
            elif self.dimension == 3 and not p.e is None and not p.n is None and not p.z is None:
                tmp = doc.createElement('point')
                tmp.setAttribute('id', p.id)
                tmp.setAttribute('y', str(p.e))
                tmp.setAttribute('x', str(p.n))
                tmp.setAttribute('z', str(p.z))
                if s == 'FIX':
                    tmp.setAttribute('fix', 'xyz')
                else:
                    if fix == 0:
                        tmp.setAttribute('adj', 'XYZ')
                    else:
                        tmp.setAttribute('adj', 'xyz')
                points_observations.appendChild(tmp)
        for o in self.observations:
            if re.match('^station_', o.target):
                # station record
                sta = doc.createElement('obs')
                sta.setAttribute('from', re.sub('^station_', '', o.target))
                points_observations.appendChild(sta)
                ih = o.th
            else:
                # observation
                if self.dimension == 2:
                    # horizontal network
                    if not o.hz is None:
                        tmp = doc.createElement('direction')
                        tmp.setAttribute('to', o.target)
                        tmp.setAttribute('val', str(o.hz.get_angle('GON')))
                        sta.appendChild(tmp)
                    if not o.d is None:
                        if o.d.mode == 'SD' and not o.v is None or o.d.mode == 'HD':
                            # horizontal distance
                            tmp.setAttribute('to', o.target)
                            tmp = doc.createElement('distance')
                            tmp.setAttribute('to', o.target)
                            tmp.setAttribute('val', str(o.horiz_dist()))
                            sta.appendChild(tmp)
                elif self.dimension == 1:
                    # elevations only
                    pass
                elif self.dimension == 3:
                    # 3d
                    pass
                else:
                    # unknown dimension
                    return None
        print doc.toprettyxml(indent="  ")
        doc.writexml(open('proba.xml', 'w'))
        doc.unlink()

if __name__ == "__main__":
    """
        unit test
    """
    gi = GamaInterface()
    gi.add_point(Point('1', 0, 0, 0))
    gi.add_point(Point('2', 8.49, 0, 0.03))
    gi.add_point(Point('3', 8.49, -6.37, 0.03))
    gi.add_point(Point('4', 0, -6.37, 0))
    gi.add_observation(PolarObservation('station_1'))
    gi.add_observation(PolarObservation('2', Angle('20-34-28', 'DMS'),
        Angle('100-09-30', 'DMS'), Distance(8.620, 'SD')))
    gi.add_observation(PolarObservation('3', Angle('57-27-10', 'DMS'),
        Angle('98-09-12', 'DMS'), Distance(10.723, 'SD')))
    gi.add_observation(PolarObservation('4', Angle('110-33-59', 'DMS'),
        Angle('103-38-15', 'DMS'), Distance(6.549, 'SD')))
    gi.add_observation(PolarObservation('station_2'))
    gi.add_observation(PolarObservation('3', Angle('236-52-14', 'DMS'),
        Angle('102-39-47', 'DMS'), Distance(6.531, 'SD')))
    gi.add_observation(PolarObservation('4', Angle('290-03-00', 'DMS'),
        Angle('97-49-20', 'DMS'), Distance(10.709, 'SD')))
    gi.add_observation(PolarObservation('1', Angle('326-55-07', 'DMS'),
        Angle('99-45-42', 'DMS'), Distance(8.613, 'SD')))
    gi.add_observation(PolarObservation('station_3'))
    gi.add_observation(PolarObservation('4', Angle('84-35-53', 'DMS'),
        Angle('100-40-51', 'DMS')))
    gi.add_observation(PolarObservation('1', Angle('121-26-47', 'DMS'),
        Angle('98-35-36', 'DMS'), Distance(10.733, 'SD')))
    gi.add_observation(PolarObservation('2', Angle('174-32-00', 'DMS'),
        Angle('103-54-19', 'DMS'), Distance(6.562, 'SD')))
    gi.add_observation(PolarObservation('station_4'))
    gi.add_observation(PolarObservation('1', Angle('18-44-59', 'DMS'),
        Angle('103-30-16', 'DMS'), Distance(6.544, 'SD')))
    gi.add_observation(PolarObservation('2', Angle('71-52-06', 'DMS'),
        Angle('98-03-31', 'DMS'), Distance(10.716, 'SD')))
    gi.add_observation(PolarObservation('3', Angle('108-47-15', 'DMS'),
        Angle('100-02-28', 'DMS'), Distance(8.624, 'SD')))
    gi.adjust()
