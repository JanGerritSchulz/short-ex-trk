import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2023/short-ex-trk/run321167_ZeroBias_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")
beamspot = fwlite.Handle("reco::BeamSpot")

dxy_vs_phi_000 = ROOT.TProfile("dxy_vs_phi_000", "dxy_vs_phi_000", 100, -3.14, 3.14) 
dxy_vs_phi_beamspot = ROOT.TProfile("dxy_vs_phi_beamspot", "dxy_vs_phi_beamspot", 100, -3.14, 3.14) 

events.toBegin()
for event in events:
    event.getByLabel("generalTracks", tracks)
    event.getByLabel("offlineBeamSpot", beamspot)
    for track in tracks.product():
        dxy_vs_phi_000.Fill(track.phi(), track.dxy(ROOT.math.XYZPoint(0, 0, 0)))
        dxy_vs_phi_beamspot.Fill(track.phi(), track.dxy(beamspot.product()))

dxy_vs_phi_000.SetAxisRange(-0.2, 0.2, "Y")
dxy_vs_phi_beamspot.SetAxisRange(-0.2, 0.2, "Y")

c = ROOT.TCanvas("c", "c", 800, 800)
dxy_vs_phi_000.Draw()
dxy_vs_phi_beamspot.SetMarkerColor(ROOT.kRed)
dxy_vs_phi_beamspot.SetLineColor(ROOT.kRed)
dxy_vs_phi_beamspot.Draw("same")
c.SaveAs("beamspot.png")
