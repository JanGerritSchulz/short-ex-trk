import DataFormats.FWLite as fwlite
import ROOT
import math

events = fwlite.Events("/eos/user/c/cmsdas/2023/short-ex-trk/run321167_Charmonium_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")

mass_histogram = ROOT.TH1F("mass", "mass", 100, 0.0, 5.0)

events.toBegin()
for i, event in enumerate(events):
    if i >= 15: break            # only the first 15 events
    print "Event", i
    event.getByLabel("globalMuons", tracks)
    for j, track in enumerate(tracks.product()):
        print "    Track", j, track.charge()/track.pt(), track.phi(), track.eta(), track.dxy(), track.dz()
