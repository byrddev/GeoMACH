from __future__ import division
import numpy
import sys
from PAM.components import Wing, Body, FullInterface, HalfInterface, body_sections
from PAM.configurations import Configuration


class Conventional(Configuration):

    def __init__(self):
        self.comps = {}
        self.keys = []

        self.addComp('fuse', Body([70,10,10,20,10,10,10,50,10,25,10,10],[25,25,25,25],[15]))
        self.addComp('wing', Wing([10,10,10,50],[10,20,10,10]))
        self.addComp('tail', Wing([30],[25]))
        self.addComp('nacelle', Body([50,10,20,30],[30],[20,10,10,20],full=True))
        self.addComp('pylon', Wing([30],[20],opentip=True))
        self.addComp('fin', Wing([30],[25],half=True))

        self.separateComps()

        self.addComp('wingfuse', FullInterface(self.comps, 'wing', 0, 'fuse', 2, [2,1], [3,6]))
        self.addComp('tailfuse', FullInterface(self.comps, 'tail', 0, 'fuse', 2, [1,8], [2,10]))
        self.addComp('pylonnacelle', FullInterface(self.comps, 'pylon', 0, 'nacelle', 1, [1,1], [2,3]))
        self.addComp('pylonwing', FullInterface(self.comps, 'pylon', 1, 'wing', 1, [2,1], [0,2]))
        self.addComp('finfuse', HalfInterface(self.comps, 'fin', 0, 'fuse', 1, [0,8], [0,10]))

        self.assembleComponents()

        c = self.comps
        c['fuse'].setSections(2,body_sections.rounded2)
        c['fuse'].setSections(3,body_sections.rounded2)
        c['fuse'].setSections(4,body_sections.rounded2)
        c['fuse'].setSections(5,body_sections.rounded2)
        c['fuse'].props['posx'].set([0,10],[0,1])
        c['fuse'].props['posy'].set([0.3,0.5,0.5],[0,0.15,1],w=[1.0,0,0],d=[1,0,0])
        c['fuse'].props['ry'].set([0.1,0.5,0.5,0.1],[0,0.15,0.75,1.0],w=[0.9985,0,0,0],d=[1,0,0,0])
        c['fuse'].props['rz'].set([0.1,0.5,0.5,0.1],[0,0.15,0.75,1.0],w=[0.9985,0,0,0],d=[1,0,0,0])

        c['wing'].offset[:] = [3.75, 0.3, 0.5]
        c['wing'].setAirfoil("rae2822.dat")
        c['wing'].props['posx'].set([0,3.2,4],[0,0.8,1],w=[0.4,1,0])
        c['wing'].props['posy'].set([0,0.9,2.1],[0,0.8,1],w=[0.5,1,0])
        c['wing'].props['posz'].set([0,4.5,5],[0,0.8,1],w=[0,1,0])
        c['wing'].props['prpx'].set([1,1],[0,1])
        c['wing'].props['prpy'].set([0,0],[0,1])
        c['wing'].props['chord'].set([2,0.25],[0,1])

        c['tail'].offset[:] = [8.5, 0.5, 0.35]
        c['tail'].props['posx'].set([0,1.6],[0,1],w=[0.2,0])
        c['tail'].props['posy'].set([0,0.3],[0,1],w=[0,0])
        c['tail'].props['posz'].set([0,1.7],[0,1])
        c['tail'].props['roty'].set([10,0],[0,1])
        c['tail'].props['prpx'].set([0,0],[0,1])
        c['tail'].props['prpy'].set([0,0],[0,1])
        c['tail'].props['chord'].set([0.85,0.15],[0,1])

        e = numpy.zeros((11,4))
        e[0,:] = [0.20, 0.03, 1, 1]
        e[1,:] = [0.30, 0.10, 0, 0]
        e[2,:] = [0.30, 0.29, 0.5, 0]
        e[3,:] = [0.00, 0.29, 1, 1]
        e[4,:] = [0.00, 0.31, 1, 1]
        e[5,:] = [0.50, 0.35, 1, 0]
        e[6,:] = [1.00, 0.30, 0, 0]
        e[7,:] = [1.00, 0.27, 0, 0]
        e[8,:] = [0.65, 0.27, 0, 0]
        e[9,:] = [0.65, 0.20, 1, 0]
        e[10,:] = [1.2, 0.05, 0, 0]
        e[:,:2] *= 0.8
        l = numpy.linspace(0,1,e.shape[0])
        c['nacelle'].offset[:] = [3.3, -0.05, 1.5]
        c['nacelle'].props['posx'].set(e[:,0],l)
        c['nacelle'].props['posy'].set([0,0],[0,1])
        c['nacelle'].props['ry'].set(e[:,1],l,e[:,2],e[:,3])
        c['nacelle'].props['rz'].set(e[:,1],l,e[:,2],e[:,3])

        c['pylon'].offset[:] = [3.8, 0.2, 1.5]
        c['pylon'].setAirfoil("naca0010")
        c['pylon'].props['posx'].set([0,0.2],[0,1])
        c['pylon'].props['posy'].set([0,0.08],[0,1])
        c['pylon'].props['posz'].set([0,0],[0,1])
        c['pylon'].props['prpx'].set([1,1],[0,1])
        c['pylon'].props['prpy'].set([0,0],[0,1])
        c['pylon'].props['chord'].set([0.75,0.75],[0,1])

        c['fin'].offset[:] = [8.5, 0.85, 0]
        c['fin'].props['posx'].set([0,1.5],[0,1])
        c['fin'].props['posy'].set([0,1.4],[0,1])
        c['fin'].props['posz'].set([0,0],[0,1])
        c['fin'].props['rotz'].set([10,0],[0,1])
        c['fin'].props['prpx'].set([1,1],[0,1])
        c['fin'].props['prpy'].set([0,0],[0,1])
        c['fin'].props['chord'].set([1,0.2],[0,1])

        self.computePoints()

if __name__ == '__main__':

    aircraft = Conventional()
    aircraft.oml0.write2Tec('conventional')
    aircraft.oml0.write2TecC('conventionalC')
    aircraft.plot()