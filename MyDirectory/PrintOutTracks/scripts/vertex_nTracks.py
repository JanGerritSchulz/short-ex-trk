import DataFormats.FWLite as fwlite
import math
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

events.toBegin()
for i,event in enumerate(events):
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    print "event",i
    pv = primaryVertices.product()
    for j in xrange(pv.size() - 1):
        print "vertex",j,"nTracks: ", pv[j].nTracks(), " track size", pv[j].tracksSize()
    if i > 100: break
    
