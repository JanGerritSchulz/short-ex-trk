import DataFormats.FWLite as fwlite
import math
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    for vertex in primaryVertices.product():
        rho_z_histogram.Fill(abs(vertex.z()),
                             math.sqrt(vertex.x()**2 + vertex.y()**2))

c = ROOT.TCanvas("c", "c", 800, 800)
rho_z_histogram.Draw()
c.SaveAs("rho_z.png")
