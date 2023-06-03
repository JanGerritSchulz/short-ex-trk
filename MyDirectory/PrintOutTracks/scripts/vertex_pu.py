import DataFormats.FWLite as fwlite
import math
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2023/short-ex-trk/run321167_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

events.toBegin()
for i, event in enumerate(events):
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    print "Pile-up:", primaryVertices.product().size()
    if i > 100: break
