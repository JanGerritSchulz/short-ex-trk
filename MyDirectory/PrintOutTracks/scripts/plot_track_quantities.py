import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("/eos/user/c/cmsdas/2023/short-ex-trk/run321167_ZeroBias_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")

hist_pt       = ROOT.TH1F("pt",       "track pt; p_{T} [GeV]", 100, 0.0, 100.0)
hist_eta      = ROOT.TH1F("eta",      "track eta; #eta", 60, -3.0, 3.0)
hist_phi      = ROOT.TH1F("phi",      "track phi; #phi", 64, -3.2, 3.2)

hist_loose_normChi2     = ROOT.TH1F("hist_loose_normChi2"    , "norm. chi2; norm #chi^{2}"        , 100, 0.0, 10.0)
hist_loose_numPixelHits = ROOT.TH1F("hist_loose_numPixelHits", "pixel hits; # pixel hits"         , 15, 0.0, 15.0)
hist_loose_numValidHits = ROOT.TH1F("hist_loose_numValidHits", "valid hits; # valid hits"         , 35, 0.0, 35.0)
hist_loose_numTkLayers  = ROOT.TH1F("hist_loose_numTkLayers" , "valid layers; # valid Tk layers"  , 25, 0.0, 25.0)
hist_highP_normChi2     = ROOT.TH1F("hist_highP_normChi2"    , "norm. chi2; norm #chi^{2}"        , 100, 0.0, 10.0)
hist_highP_numPixelHits = ROOT.TH1F("hist_highP_numPixelHits", "pixel hits; # pixel hits"         , 15, 0.0, 15.0)
hist_highP_numValidHits = ROOT.TH1F("hist_highP_numValidHits", "valid hits; # valid hits"         , 35, 0.0, 35.0)
hist_highP_numTkLayers  = ROOT.TH1F("hist_highP_numTkLayers" , "valid layers; # valid Tk layers"  , 25, 0.0, 25.0)

hist_highP_normChi2.SetLineColor(ROOT.kRed)
hist_highP_numPixelHits.SetLineColor(ROOT.kRed)
hist_highP_numValidHits.SetLineColor(ROOT.kRed)
hist_highP_numTkLayers.SetLineColor(ROOT.kRed)

for i, event in enumerate(events):
    event.getByLabel("generalTracks", tracks)
    for track in tracks.product():
        hist_pt.Fill(track.pt())
        hist_eta.Fill(track.eta())
        hist_phi.Fill(track.phi())

        if track.quality(track.qualityByName("loose")):
            hist_loose_normChi2    .Fill(track.normalizedChi2())
            hist_loose_numPixelHits.Fill(track.hitPattern().numberOfValidPixelHits())
            hist_loose_numValidHits.Fill(track.hitPattern().numberOfValidHits())
            hist_loose_numTkLayers .Fill(track.hitPattern().trackerLayersWithMeasurement())
        if track.quality(track.qualityByName("highPurity")):
            hist_highP_normChi2    .Fill(track.normalizedChi2())
            hist_highP_numPixelHits.Fill(track.hitPattern().numberOfValidPixelHits())
            hist_highP_numValidHits.Fill(track.hitPattern().numberOfValidHits())
            hist_highP_numTkLayers .Fill(track.hitPattern().trackerLayersWithMeasurement())

    if i > 500: break

c = ROOT.TCanvas( "c", "c", 800, 800)

hist_pt.Draw()
c.SetLogy()
c.SaveAs("track_pt.png")
c.SetLogy(False)

hist_eta.Draw()
c.SaveAs("track_eta.png")
hist_phi.Draw()
c.SaveAs("track_phi.png")

hist_highP_normChi2.DrawNormalized()
hist_loose_normChi2.DrawNormalized('same')
c.SaveAs("track_normChi2.png")
hist_highP_numPixelHits.DrawNormalized()
hist_loose_numPixelHits.DrawNormalized('same')
c.SaveAs("track_nPixelHits.png")
hist_highP_numValidHits.DrawNormalized()
hist_loose_numValidHits.DrawNormalized('same')
c.SaveAs("track_nValHits.png")
hist_highP_numTkLayers.DrawNormalized()
hist_loose_numTkLayers.DrawNormalized('same')
c.SaveAs("track_nTkLayers.png")
