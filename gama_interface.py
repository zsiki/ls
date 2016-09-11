#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: gama_interface
    :platform: Linux, Windows
    :synopsis: interface modul to GNU Gama

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

import math
# surveying calculation modules
import config
from base_classes import *
from surveying_util import *
from PyQt4.QtCore import QDir, QFile, QFileInfo, QIODevice, QTemporaryFile, \
                        QProcess, QSettings
from PyQt4.QtXml import QDomDocument, QXmlSimpleReader, QXmlInputSource

class GamaInterface(object):
    """ Interface class to GNU Gama
    """
    def __init__(self, dimension=2, probability=0.95, stdev_angle=3, stdev_dist=3, stdev_dist1=3):
        """ Initialize a new GamaInterface instance.

            :param dimension: dimension of network (int), 1/2/3
            :param probability: porbability for statistical tests (float)
            :param stdev_angle: standard deviation for directions in cc (float)
            :param stdev_dist: base standard deviation for distances mm (float)
            :param stdev_dist1: standard deviation for distances mm/km (float)
        """
        self.dimension = dimension
        self.probability = probability
        self.stdev_angle = stdev_angle
        self.stdev_dist = stdev_dist
        self.stdev_dist1 = stdev_dist1
        self.points = []
        self.observations = []
        gama_path = QSettings().value("SurveyingCalculation/gama_path",config.gama_path)
        if QFileInfo(gama_path).exists():
            gama_prog = gama_path
        else:
            # get operating system dependent file name of gama_local
            plugin_dir = QDir().cleanPath( QFileInfo(__file__).absolutePath() )
            gama_prog = QDir(plugin_dir).absoluteFilePath("gama-local")
            if not QFileInfo(gama_prog).exists():
                if QFileInfo(gama_prog+".exe").exists():
                    gama_prog += '.exe'
                elif QFileInfo(gama_prog+"64.exe").exists():
                    gama_prog += '64.exe'
                else:
                    gama_prog = None
        self.gama_prog = gama_prog

    def add_point(self, point, state='ADJ'):
        """ Add point to adjustment

            :param point: point to ad network (Point)
            :param state: FIX or ADJ (str)
        """
        for p, s in self.points:
            # avoid duplicated points
            if p.id == point.id:
                return
        self.points.append([point, state])

    def add_observation(self, obs):
        """ Add observation to adjustment

            :param obs: observation to add (PolarObservation)
        """
        self.observations.append(obs)

    def remove_last_observation(self, st=False):
        """ remove last observation or station data

            :param st: False remove single observation, True remove station (Bool)
        """
        if len(self.observations):
            if st:
                o = self.observations.pop()
                while len(self.observations) and o.station is None:
                    o = self.observations.pop()
            else:
                self.observations.pop()

    def adjust(self):
        """ Export data to GNU Gama xml, adjust the network and read result

            :returns: result list of adjusment from GNU Gama
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
        
        doc = QDomDocument()
        doc.appendChild(doc.createComment('Gama XML created by SurveyingCalculation plugin for QGIS'))
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
            if self.dimension == 1:
                tmp = doc.createElement('point')
                tmp.setAttribute('id', p.id)
                if p.z is not None:
                    tmp.setAttribute('z', str(p.z))
                if s == 'FIX':
                    tmp.setAttribute('fix', 'z')
                else:
                    if fix == 0:
                        tmp.setAttribute('adj', 'Z')
                    else:
                        tmp.setAttribute('adj', 'z')
                points_observations.appendChild(tmp)
            elif self.dimension == 2:
                tmp = doc.createElement('point')
                tmp.setAttribute('id', p.id)
                if p.e is not None and p.n is not None:
                    tmp.setAttribute('y', str(p.e))
                    tmp.setAttribute('x', str(p.n))
                if s == 'FIX':
                    tmp.setAttribute('fix', 'xy')
                else:
                    if fix == 0:
                        # free network
                        tmp.setAttribute('adj', 'XY')
                    else:
                        tmp.setAttribute('adj', 'xy')
                points_observations.appendChild(tmp)
            elif self.dimension == 3:
                tmp = doc.createElement('point')
                tmp.setAttribute('id', p.id)
                if p.e is not None and p.n is not None:
                    tmp.setAttribute('y', str(p.e))
                    tmp.setAttribute('x', str(p.n))
                if p.z is not None:
                    tmp.setAttribute('z', str(p.z))
                if s == 'FIX':
                    tmp.setAttribute('fix', 'xyz')
                else:
                    if fix == 0:
                        tmp.setAttribute('adj', 'XYZ')
                    else:
                        tmp.setAttribute('adj', 'xyz')
                points_observations.appendChild(tmp)
        if self.dimension == 1:
            hd = doc.createElement('height-differences')
            points_observations.appendChild(hd)
        for o in self.observations:
            if o.station == 'station':
                # station record
                st_id = o.point_id
                if o.th is None:
                    ih = 0
                else:
                    ih = o.th
                if self.dimension in [2, 3]:
                    sta = doc.createElement('obs')
                    sta.setAttribute('from', o.point_id)
                    points_observations.appendChild(sta)
            else:
                # observation
                if self.dimension == 2:
                    # horizontal network
                    if o.hz is not None:
                        tmp = doc.createElement('direction')
                        tmp.setAttribute('to', o.point_id)
                        tmp.setAttribute('val', str(o.hz.get_angle('GON')))
                        sta.appendChild(tmp)
                    if o.d is not None:
                        # horizontal distance
                        hd = o.horiz_dist()
                        if hd is not None:
                            tmp = doc.createElement('distance')
                            tmp.setAttribute('to', o.point_id)
                            tmp.setAttribute('val', str(hd))
                            sta.appendChild(tmp)
                elif self.dimension == 1:
                    # elevations only 1d
                    if o.th is None:
                        th = 0
                    else:
                        th = o.th
                    if o.d is not None and o.v is not None:
                        tmp = doc.createElement('dh')
                        tmp.setAttribute('from', st_id)
                        tmp.setAttribute('to', o.point_id)
						# TODO hibaterjedes
                        tmp.setAttribute('stdev', '1')
                        sz = math.sin(o.v.get_angle())
                        w = self.stdev_dist + self.stdev_dist1 * o.d.d / 1000
                        ro_cc = 200 * 100 * 100 /math.pi
                        if o.d.mode == 'SD':
                            cz = math.cos(o.v.get_angle())
                            tmp.setAttribute('val', str(o.d.d * cz + ih -th))
                            tmp.setAttribute('stdev', str(math.sqrt(cz ** 2 * w ** 2 + (o.d.d * 1000) ** 2 * sz ** 2 * (self.stdev_angle / RO_CC) ** 2)))
                        else:
                            tz = math.tan(o.v.get_angle())
                            tmp.setAttribute('val', str(o.d.d / math.tan(o.v.get_angle()) + ih -th))
                            tmp.setAttribute('stdev', str(math.sqrt((1 / tz) ** 2 * w ** 2 + (o.d.d * 1000) ** 2 * (o.d.d * 1000) ** 2 * (1 / sz ** 2) ** 2 * (self.stdev_angle / RO_CC) ** 2)))
                        hd.appendChild(tmp)
                elif self.dimension == 3:
                    # 3d
                    if o.th is None:
                        th = 0
                    else:
                        th = o.th
                    if o.hz is not None:
                        tmp = doc.createElement('direction')
                        tmp.setAttribute('to', o.point_id)
                        tmp.setAttribute('val', str(o.hz.get_angle('GON')))
                        sta.appendChild(tmp)
                    if o.d is not None:
                        if o.d.mode == 'SD':
                            tmp = doc.createElement('s-distance')
                            tmp.setAttribute('val', str(o.d.d))
                            tmp.setAttribute('from_dh', str(ih))
                            tmp.setAttribute('to_dh', str(th))
                        else:
                            tmp = doc.createElement('distance')
                            tmp.setAttribute('val', str(o.d.d))
                        tmp.setAttribute('to', o.point_id)
                        sta.appendChild(tmp)
                    if o.v is not None:
                        tmp = doc.createElement('z-angle')
                        tmp.setAttribute('to', o.point_id)
                        tmp.setAttribute('val', str(o.v.get_angle('GON')))
                        tmp.setAttribute('from_dh', str(ih))
                        tmp.setAttribute('to_dh', str(th))
                        sta.appendChild(tmp)
                else:
                    # unknown dimension
                    return None
        # generate temp file name
        tmpf = QTemporaryFile( QDir.temp().absoluteFilePath('w') )
        tmpf.open(QIODevice.WriteOnly)
        tmpf.close()
        tmp_name = tmpf.fileName()
        f = QFile(tmp_name + '.xml')
        if f.open(QIODevice.WriteOnly):
            f.write(doc.toByteArray())
            f.close()
       
        # run gama-local
        if self.gama_prog is None:
            return None
        status = QProcess.execute(self.gama_prog, [ tmp_name+'.xml', '--text',
            tmp_name+'.txt', '--xml', tmp_name+'out.xml'])
        if status != 0:
            return None
        
        xmlParser = QXmlSimpleReader()
        xmlFile = QFile(tmp_name + 'out.xml')
        xmlInputSource = QXmlInputSource(xmlFile)
        doc.setContent(xmlInputSource,xmlParser)
        
        f_txt = QFile(tmp_name + '.txt') 
        f_txt.open(QIODevice.ReadOnly)
        res = f_txt.readAll().data()
        f_txt.close()
        
        # store coordinates
        adj_nodes = doc.elementsByTagName('adjusted')
        if adj_nodes.count() < 1:
            return res
        adj_node = adj_nodes.at(0)
        for i in range(len(adj_node.childNodes())):
            pp = adj_node.childNodes().at(i)
            if pp.nodeName() == 'point':
                for ii in range(len(pp.childNodes())):
                    ppp = pp.childNodes().at(ii)
                    if ppp.nodeName() == 'id':
                        p = Point(ppp.firstChild().nodeValue())
                    elif ppp.nodeName() == 'Y' or ppp.nodeName() == 'y':
                        p.e = float(ppp.firstChild().nodeValue())
                    elif ppp.nodeName() == 'X' or ppp.nodeName() == 'x':
                        p.n = float(ppp.firstChild().nodeValue())
                    elif ppp.nodeName() == 'Z' or ppp.nodeName() == 'z':
                        p.z = float(ppp.firstChild().nodeValue())
                ScPoint(p).store_coord(self.dimension)
        # remove input xml and output xml
        tmpf.remove()
        f_txt.remove()
        f.remove()
        xmlFile.remove()
        
        return res

if __name__ == "__main__":
    """
        unit test
    """
    gi = GamaInterface()
    gi.add_point(Point('1', 0, 0))
    gi.add_point(Point('2', 211.70, 0))
    gi.add_point(Point('3', 257.95, 375.64))
    gi.add_point(Point('4', 78.1562, 395.49))
    gi.add_point(Point('5', -60.35, 387.99))
    gi.add_observation(PolarObservation('1', 'station'))
    gi.add_observation(PolarObservation('2', None, Angle('42-56-02', 'DMS'),
        Angle('87-35-39', 'DMS'), Distance(211.886, 'SD')))
    gi.add_observation(PolarObservation('3', None, Angle('347-24-35', 'DMS'),
        Angle('88-54-24', 'DMS'), Distance(455.774, 'SD')))
    gi.add_observation(PolarObservation('4', None, Angle('324-06-32', 'DMS'),
        Angle('90-00-36', 'DMS'), Distance(403.150, 'SD')))
    gi.add_observation(PolarObservation('5', None, Angle('304-05-19', 'DMS'),
        Angle('89-58-23', 'DMS'), Distance(392.665, 'SD')))
    gi.add_observation(PolarObservation('2', 'station'))
    gi.add_observation(PolarObservation('1', None, Angle('304-20-43', 'DMS'),
        Angle('92-27-19', 'DMS'), Distance(211.894, 'SD')))
    gi.add_observation(PolarObservation('5', None, Angle('359-18-19', 'DMS'),
        Angle('91-03-52', 'DMS'), Distance(473.977, 'SD')))
    gi.add_observation(PolarObservation('4', None, Angle('15-41-16', 'DMS'),
        Angle('91-14-36', 'DMS'), Distance(417.565, 'SD')))
    gi.add_observation(PolarObservation('3', None, Angle('41-22-11', 'DMS'),
        Angle('90-02-29', 'DMS'), Distance(378.506, 'SD')))
    gi.add_observation(PolarObservation('5', 'station'))
    gi.add_observation(PolarObservation('4', None, Angle('324-16-52', 'DMS'),
        Angle('90-06-46', 'DMS'), Distance(138.703, 'SD')))
    gi.add_observation(PolarObservation('3', None, Angle('329-36-15', 'DMS'),
        Angle('88-27-29', 'DMS'), Distance(318.672, 'SD')))
    gi.add_observation(PolarObservation('2', None, Angle('22-20-43', 'DMS'),
        Angle('88-55-56', 'DMS'), Distance(473.959, 'SD')))
    gi.add_observation(PolarObservation('1', None, Angle('48-32-26', 'DMS'),
        Angle('90-01-16', 'DMS'), Distance(392.662, 'SD')))
    gi.add_observation(PolarObservation('4', 'station'))
    gi.add_observation(PolarObservation('2', None, Angle('346-38-25', 'DMS'),
        Angle('88-45-44', 'DMS'), Distance(417.543, 'SD')))
    gi.add_observation(PolarObservation('1', None, Angle('16-28-34', 'DMS'),
        Angle('89-59-40', 'DMS'), Distance(403.146, 'SD')))
    gi.add_observation(PolarObservation('5', None, Angle('92-11-53', 'DMS'),
        Angle('89-57-38', 'DMS'), Distance(138.704, 'SD')))
    gi.add_observation(PolarObservation('3', 'station'))
    gi.add_observation(PolarObservation('5', None, Angle('59-45-52', 'DMS'),
        Angle('91-33-41', 'DMS'), Distance(318.673, 'SD')))
    gi.add_observation(PolarObservation('1', None, Angle('2-01-09', 'DMS'),
        Angle('91-05-51', 'DMS'), Distance(455.772, 'SD')))
    gi.add_observation(PolarObservation('2', None, Angle('334-33-23', 'DMS'),
        Angle('89-57-40', 'DMS'), Distance(378.487, 'SD')))
    gi.adjust()
