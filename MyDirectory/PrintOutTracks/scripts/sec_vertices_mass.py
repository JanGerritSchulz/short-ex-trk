import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("file:../test/output.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")

mass_histogram = ROOT.TH1F("mass", "mass", 100, 0.4, 0.6)

events.toBegin()
for event in events:
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", secondaryVertices)
    for vertex in secondaryVertices.product():
        mass_histogram.Fill(vertex.mass())

c = ROOT.TCanvas ("c" , "c", 800, 800)
mass_histogram.Draw()
c.SaveAs("kshort_mass.png")
