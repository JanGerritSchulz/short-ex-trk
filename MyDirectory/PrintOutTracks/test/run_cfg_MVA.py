import FWCore.ParameterSet.Config as cms

process = cms.Process("RUN")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:/eos/user/c/cmsdas/2025/short-ex-trk/run355374_ZeroBias_AOD.root"))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))

process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR")))

process.PrintOutTracks = cms.EDAnalyzer("PrintOutTracks_MVA")
process.PrintOutTracks.tracks = cms.untracked.InputTag("generalTracks")
process.PrintOutTracks.mvaValues = cms.untracked.InputTag("generalTracks","MVAValues")
process.path = cms.Path(process.PrintOutTracks)
