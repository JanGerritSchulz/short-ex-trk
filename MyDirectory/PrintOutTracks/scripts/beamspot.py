import DataFormats.FWLite as fwlite
import math
import ROOT

def isGoodPV(vertex):
    if ( vertex.isFake()        or 
         vertex.ndof < 4.0      or 
         abs(vertex.z()) > 24.0 or 
         abs(vertex.position().Rho()) > 2):
           return False
    return True

events          = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
beamspot        = fwlite.Handle("reco::BeamSpot")

vtx_xy = ROOT.TH2F('vtx_xy','; x [cm]; y [cm]', 100,-0.1,   0.3, 100, -0.25, 0.15)
vtx_xz = ROOT.TH2F('vtx_xz','; x [cm]; z [cm]', 100,-0.1,   0.3, 100,   -10,   10)
vtx_yz = ROOT.TH2F('vtx_yz','; y [cm]; z [cm]', 100,-0.25, 0.15, 100,   -10,   10)

sumx = 0.0
N    = 0
last_beamspot = None

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("offlineBeamSpot", beamspot)

    if last_beamspot == None or last_beamspot != beamspot.product().x0():
        print "New beamspot IOV (interval of validity)..."
        last_beamspot       = beamspot.product().x0()
        sumx = 0.0
        N = 0

    for vertex in primaryVertices.product():
        if not isGoodPV(vertex):  continue
        N += 1
        sumx += vertex.x()
        vtx_xy.Fill(vertex.x(), vertex.y())
        vtx_xz.Fill(vertex.x(), vertex.z())
        vtx_yz.Fill(vertex.y(), vertex.z())
        if N % 1000 == 0:
            print "Mean of primary vertices:", sumx/N,
            print "Beamspot:", beamspot.product().x0()
            
c = ROOT.TCanvas( "c", "c", 1200, 600)
c.Divide(3,1)
c.cd(1)
vtx_xy.Draw("colz")
c.cd(2)
vtx_xz.Draw("colz")
c.cd(3)
vtx_yz.Draw("colz")
c.SaveAs("vtx_scatter.png")
