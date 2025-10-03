import DataFormats.FWLite as fwlite
import math
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

deltaz_histogram = ROOT.TH1F("deltaz", "deltaz", 1000, -20.0, 20.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    pv = primaryVertices.product()
    for i in xrange(pv.size() - 1):
        for j in xrange(i + 1, pv.size()):
            deltaz_histogram.Fill(pv[i].z() - pv[j].z())

c = ROOT.TCanvas ("c", "c", 800, 800)
deltaz_histogram.Draw()
c.SaveAs("deltaz.png")
