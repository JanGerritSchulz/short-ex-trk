import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355558_DoubleMuonLowMass_MINIAOD.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositePtrCandidate>")

mass_histogram = ROOT.TH1F("mass_histogram", "mass_histogram", 100, 1., 1.2)

events.toBegin()
for i, event in enumerate(events):
    event.getByLabel("slimmedLambdaVertices", "", secondaryVertices)
    for j, vertex in enumerate(secondaryVertices.product()):
        mass_histogram.Fill(vertex.mass())

c = ROOT.TCanvas()
mass_histogram.Draw()
c.SaveAs("mass_lambda_miniaod.png")
