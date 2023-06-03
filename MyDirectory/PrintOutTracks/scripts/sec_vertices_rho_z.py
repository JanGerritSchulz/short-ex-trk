import DataFormats.FWLite as fwlite
import math
import ROOT
ks_rho_z_histogram     = ROOT.TH2F("ks_rho_z","K_{s} #rho-#z;z [cm];#rho [cm]", 100, 0.0, 30.0, 100, 0.0, 10.0)
lambda_rho_z_histogram = ROOT.TH2F("lambda_rho_z","#Lambda #rho-z;z [cm];#rho [cm]", 100, 0.0, 30.0, 100, 0.0, 10.0)

events = fwlite.Events("file:../test/output.root")
KShorts = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
Lambdas = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")

events.toBegin()
for event in events:
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", KShorts)
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Lambda", Lambdas)
    for vertex in KShorts.product():
        ks_rho_z_histogram.Fill(abs(vertex.vz()), math.sqrt(vertex.vx()**2 + vertex.vy()**2))
    for vertex2 in Lambdas.product():
        lambda_rho_z_histogram.Fill(abs(vertex2.vz()), math.sqrt(vertex2.vx()**2 + vertex2.vy()**2))

c = ROOT.TCanvas( "c", "c", 1200, 800)
c.Divide(2,1)
c.cd(1)
ks_rho_z_histogram.Draw("colz")
c.cd(2)
lambda_rho_z_histogram.Draw("colz")
c.SaveAs("kShorts_rho_z.png")
