import DataFormats.FWLite as fwlite
import ROOT
import math

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")

mass_histogram = ROOT.TH1F("mass", "mass", 100, 0.0, 5.0)

for i, event in enumerate(events):
    event.getByLabel("generalTracks", tracks)
    for track in tracks.product():
        print track.pt(), track.p(), track.px(), track.py(), track.pz()
        print "energy: ", math.sqrt(0.140**2 + track.p()**2)

        if len(tracks.product()) > 1:

            one = tracks.product()[0]
            two = tracks.product()[1]	      	       	  
	

            total_energy = math.sqrt(0.140**2 + one.p()**2) + math.sqrt(0.140**2 + two.p()**2)
            total_px = one.px() + two.px()
            total_py = one.py() + two.py()
            total_pz = one.pz() + two.pz()
            mass = math.sqrt(total_energy**2 - total_px**2 - total_py**2 - total_pz**2)

            mass_histogram.Fill(mass)

    if i > 1000: break
    
c = ROOT.TCanvas ("c", "c", 800, 800)
mass_histogram.Draw()
c.SaveAs("mass_2_tracks.png")
