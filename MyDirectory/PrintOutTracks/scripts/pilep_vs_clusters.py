import ROOT
import DataFormats.FWLite as fwlite
events = fwlite.Events("/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root")

clusterSummary = fwlite.Handle("ClusterSummary")

h = ROOT.TH2F("h", "h", 100, 0, 20000, 100, 0, 100000)

events.toBegin()
for event in events:
    event.getByLabel("clusterSummaryProducer", clusterSummary)
    cs = clusterSummary.product()
    try:
        h.Fill(cs.getNClus(cs.PIXEL),
               cs.getNClus(cs.PIXEL) + cs.getNClus(cs.STRIP))
    except TypeError:
        pass

c = ROOT.TCanvas("c", "c", 800, 800)
h.Draw()
h.Fit("pol1")
c.SaveAs("pileup_nclusters.png")
