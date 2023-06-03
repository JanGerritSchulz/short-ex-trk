import math
import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2023/short-ex-trk/run321167_Charmonium_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")
mass_histogram = ROOT.TH1F("mass", "mass", 100, 0.0, 5.0)

events.toBegin()
for event in events:
    event.getByLabel("globalMuons", tracks)
    product = tracks.product()
    if product.size() == 2:
        one = product[0]
        two = product[1]
        if not (one.charge()*two.charge() == -1):  continue
        energy = (math.sqrt(0.106**2 + one.p()**2) +
                  math.sqrt(0.106**2 + two.p()**2))
        px = one.px() + two.px()
        py = one.py() + two.py()
        pz = one.pz() + two.pz()
        mass = math.sqrt(energy**2 - px**2 - py**2 - pz**2)
        mass_histogram.Fill(mass)

c = ROOT.TCanvas ("c", "c", 800, 800)
mass_histogram.Draw()
c.SaveAs("mass.png")
