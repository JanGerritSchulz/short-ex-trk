import DataFormats.FWLite as fwlite
import ROOT
ROOT.gROOT.SetBatch(True)

events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_MINIAOD.root")
eventsAOD = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")

tracks     = fwlite.Handle("std::vector<pat::PackedCandidate>")
losttracks = fwlite.Handle("std::vector<pat::PackedCandidate>")
tracksAOD = fwlite.Handle("std::vector<reco::Track>")

hist_pt       = ROOT.TH1F("pt",       "track pt; p_{T} [GeV]", 100, 0.0, 100.0)
histptZoomedIn= ROOT.TH1F("ptZoomedIn",       "track pt; p_{T} [GeV]", 100, 0.5, 0.505)
hist_eta      = ROOT.TH1F("eta",      "track eta; #eta", 60, -3.0, 3.0)
hist_phi      = ROOT.TH1F("phi",      "track phi; #phi", 64, -3.2, 3.2)

hist_normChi2     = ROOT.TH1F("hist_normChi2"    , "norm. chi2; norm #chi^{2}"        , 100, 0.0, 10.0)
hist_numPixelHits = ROOT.TH1F("hist_numPixelHits", "pixel hits; # pixel hits"         , 15, -0.5, 14.5)
hist_numValidHits = ROOT.TH1F("hist_numValidHits", "valid hits; # valid hits"         , 35, -0.5, 34.5)
hist_numTkLayers  = ROOT.TH1F("hist_numTkLayers" , "valid layers; # valid Tk layers"  , 25, -0.5, 24.5)

hist_pt_AOD       = ROOT.TH1F("ptAOD",       "track pt; p_{T} [GeV]", 100, 0.0, 100.0)
histptZoomedIn_AOD = ROOT.TH1F("ptZoomedInAOD",       "track pt; p_{T} [GeV]", 100, 0.5, 0.505)
hist_eta_AOD      = ROOT.TH1F("etaAOD",      "track eta; #eta", 60, -3.0, 3.0)
hist_phi_AOD      = ROOT.TH1F("phiAOD",      "track phi; #phi", 64, -3.2, 3.2)

hist_normChi2_AOD     = ROOT.TH1F("hist_normChi2AOD"    , "norm. chi2; norm #chi^{2}"        , 100, 0.0, 10.0)
hist_numPixelHits_AOD = ROOT.TH1F("hist_numPixelHitsAOD", "pixel hits; # pixel hits"         , 15, -0.5, 14.5)
hist_numValidHits_AOD = ROOT.TH1F("hist_numValidHitsAOD", "valid hits; # valid hits"         , 35, -0.5, 34.5)
hist_numTkLayers_AOD  = ROOT.TH1F("hist_numTkLayersAOD" , "valid layers; # valid Tk layers"  , 25, -0.5, 24.5)

hist_pt_AOD.SetLineColor(ROOT.kRed)
histptZoomedIn_AOD.SetLineColor(ROOT.kRed)
hist_eta_AOD.SetLineColor(ROOT.kRed)
hist_phi_AOD.SetLineColor(ROOT.kRed)

hist_normChi2_AOD.SetLineColor(ROOT.kRed)
hist_numPixelHits_AOD.SetLineColor(ROOT.kRed)
hist_numValidHits_AOD.SetLineColor(ROOT.kRed)
hist_numTkLayers_AOD.SetLineColor(ROOT.kRed)

for i, event in enumerate(events):
    event.getByLabel("packedPFCandidates", "", tracks)
    event.getByLabel("lostTracks", "", losttracks)

    alltracks  = [track for track in tracks.product()]
    alltracks += [track for track in losttracks.product()]

    for track in alltracks :
        if (not track.hasTrackDetails() or track.charge() == 0 ):
            continue
        if not track.trackHighPurity():
            continue
        hist_pt.Fill(track.pt())
        histptZoomedIn.Fill(track.pt())
        hist_eta.Fill(track.eta())
        hist_phi.Fill(track.phi())

        hist_normChi2    .Fill(track.pseudoTrack().normalizedChi2())
        hist_numPixelHits.Fill(track.numberOfPixelHits())
        hist_numValidHits.Fill(track.pseudoTrack().hitPattern().numberOfValidHits())
        hist_numTkLayers .Fill(track.pseudoTrack().hitPattern().trackerLayersWithMeasurement())

    if i > 1000: break

for i, event in enumerate(eventsAOD):
    event.getByLabel("generalTracks", tracksAOD)

    for j, track in enumerate(tracksAOD.product()) :
        if not track.quality(track.qualityByName("highPurity")):
            continue

        hist_pt_AOD.Fill(track.pt())
        histptZoomedIn_AOD.Fill(track.pt())
        hist_eta_AOD.Fill(track.eta())
        hist_phi_AOD.Fill(track.phi())

        hist_normChi2_AOD    .Fill(track.normalizedChi2())
        hist_numPixelHits_AOD.Fill(track.hitPattern().numberOfValidPixelHits())
        hist_numValidHits_AOD.Fill(track.hitPattern().numberOfValidHits())
        hist_numTkLayers_AOD .Fill(track.hitPattern().trackerLayersWithMeasurement())

    if i > 1000: break

c = ROOT.TCanvas( "c", "c", 800, 800)

hist_pt.Draw()
hist_pt_AOD.Draw("same")
c.SetLogy()
c.SaveAs("track_pt_miniaod.png")

histptZoomedIn_AOD.Draw()
histptZoomedIn.Draw("same")
c.SetLogy()
c.SaveAs("track_lowPt_miniaod.png")
c.SetLogy(False)
hist_eta_AOD.Draw()
hist_eta.Draw("same")
c.SaveAs("track_eta_miniaod.png")
hist_phi_AOD.Draw()
hist_phi.Draw("same")
c.SaveAs("track_phi_miniaod.png")

hist_normChi2_AOD.Draw()
hist_normChi2.Draw("same")
c.SaveAs("track_normChi2_miniaod.png")
hist_numPixelHits_AOD.Draw()
hist_numPixelHits.Draw("same")
c.SaveAs("track_nPixelHits_miniaod.png")
hist_numValidHits_AOD.Draw()
hist_numValidHits.Draw("same")
c.SaveAs("track_nValHits_miniaod.png")
hist_numTkLayers_AOD.Draw()
hist_numTkLayers.Draw("same")
c.SaveAs("track_nTkLayers_miniaod.png")
