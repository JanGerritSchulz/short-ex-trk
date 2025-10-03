import DataFormats.FWLite as fwlite
import math
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)

def isGoodPV(vertex):
    if ( vertex.isFake()        or \
         vertex.ndof < 4.0      or \
         abs(vertex.z()) > 24.0 or \
         abs(vertex.position().Rho()) > 2):
           return False
    return True

events          = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
beamspot        = fwlite.Handle("reco::BeamSpot")
vtx_position, N_vtx = array( 'd' ), array( 'd' )

vtx_xy = ROOT.TH2F('vtx_xy','; x [cm]; y [cm]', 100,-0.05, 0.25, 100, -0.2, 0.1)
c = ROOT.TCanvas( "c", "c", 1200, 800)

sumx = 0.0
N    = 0
iIOV = 0
last_beamspot = None
last_beamspot_sigma = None

vtx_position, N_vtx = array( 'd' ), array( 'd' )
leg = ROOT.TLegend(0.45, 0.15, 0.6, 0.28)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("offlineBeamSpot", beamspot)

    if last_beamspot == None or last_beamspot != beamspot.product().x0():
        print "New beamspot IOV (interval of validity)..."

        ## first save tgraph and then reset
        if (iIOV > 0):
            theGraph   = ROOT.TGraph(len(vtx_position), N_vtx, vtx_position)
            theGraph.SetMarkerStyle(8)
            theGraph.SetTitle('IOV %s; N Vtx; X position'%iIOV)
            theGraph.Draw('AP')
            theGraph.GetYaxis().SetRangeUser(0.094, 0.099)
            
            line = ROOT.TLine(0,last_beamspot,N_vtx[-1],last_beamspot)
            line.SetLineColor(ROOT.kRed)
            line.SetLineWidth(2)
            line.Draw()

            line2 = ROOT.TLine(0,last_beamspot - last_beamspot_sigma,N_vtx[-1],last_beamspot - last_beamspot_sigma)
            line2.SetLineColor(ROOT.kOrange)
            line3 = ROOT.TLine(0,last_beamspot + last_beamspot_sigma,N_vtx[-1],last_beamspot + last_beamspot_sigma)
            line3.SetLineColor(ROOT.kOrange)
            line2.SetLineWidth(2)
            line3.SetLineWidth(2)
            line2.Draw()
            line3.Draw()
            
            leg.Clear()
            leg.AddEntry(theGraph,  'ave. vtx position',        'p')
            leg.AddEntry(line    ,  'center of the beamspot ' , 'l')
            leg.AddEntry(line2   ,  'center of the bs #pm beamspot width ' , 'l')
            leg.Draw()
            c.SaveAs("vtx_x_vs_N_%s.png"%iIOV)
            break

            vtx_position, N_vtx = array( 'd' ), array( 'd' )

        last_beamspot       = beamspot.product().x0()
        last_beamspot_sigma = beamspot.product().BeamWidthX()
        sumx = 0.0
        N = 0
        iIOV += 1

    for vertex in primaryVertices.product():
        if not isGoodPV(vertex):  continue
        N += 1
        sumx += vertex.x()
        if N % 1000 == 0:
            vtx_position.append(sumx/N)
            N_vtx       .append(N)
