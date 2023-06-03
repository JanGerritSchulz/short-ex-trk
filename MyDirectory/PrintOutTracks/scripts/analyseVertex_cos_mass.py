import math
import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("file:../test/output.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")

cosAngle_histogram = ROOT.TH1F("cosAngle", "cosAngle", 100, -1.0, 1.0)
cosAngle_zoom_histogram = ROOT.TH1F("cosAngle_zoom", "cosAngle_zoom", 100, 0.99, 1.0)

mass_histogram = ROOT.TH1F("mass", "mass", 100, 0.4, 0.6)
mass_goodCosAngle = ROOT.TH1F("mass_goodCosAngle", "mass_goodCosAngle", 100, 0.4, 0.6)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", secondaryVertices)
    for secondary in secondaryVertices.product():
        px = secondary.px()
        py = secondary.py()
        pz = secondary.pz()
        p = secondary.p()
        bestCosAngle = -1       # start with the worst possible
        for primary in primaryVertices.product():
            dx = secondary.vx() - primary.x()
            dy = secondary.vy() - primary.y()
            dz = secondary.vz() - primary.z()
            dl = math.sqrt(dx**2 + dy**2 + dz**2)
            dotProduct = px*dx + py*dy + pz*dz
            cosAngle = dotProduct / p / dl
            if cosAngle > bestCosAngle:
                bestCosAngle = cosAngle # update it if you've found a better one
        cosAngle_histogram.Fill(bestCosAngle)
        cosAngle_zoom_histogram.Fill(bestCosAngle)
        if bestCosAngle > 0.99:
            mass_goodCosAngle.Fill(secondary.mass())
        mass_histogram.Fill(secondary.mass())

c = ROOT.TCanvas("c", "c", 800, 800)
mass_histogram.Draw()
mass_goodCosAngle.SetLineColor(ROOT.kRed)
mass_goodCosAngle.Draw("same")
c.SaveAs("mass_improved.png")

c2 = ROOT.TCanvas("c2" , "c2" , 800, 800)
cosAngle_histogram.Draw()
c2.SaveAs("cosAngle.png")
cosAngle_zoom_histogram.Draw()
c2.SaveAs("cosAngle_zoom.png")

