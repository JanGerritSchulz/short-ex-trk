import DataFormats.FWLite as fwlite
import math
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
tracks = fwlite.Handle("std::vector<reco::Track>")

histogram = ROOT.TH2F("ntracks_vs_nvertex","ntracks_vs_nvertex",
                      30, 0.0, 29.0, 100, 0.0,2000.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("generalTracks", tracks)
    histogram.Fill(primaryVertices.product().size(), tracks.product().size())

c = ROOT.TCanvas( "c", "c", 1200, 800)
histogram.Draw()
c.SaveAs("ntracks_vs_nvertex.png")
