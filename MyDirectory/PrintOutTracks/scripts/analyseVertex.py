import math
import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("file:../test/output.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")

for i, event in enumerate(events):
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", secondaryVertices)
    for secondary in secondaryVertices.product():
        px = secondary.px()
        py = secondary.py()
        pz = secondary.pz()
        p = secondary.p()
        for primary in primaryVertices.product():
            dx = secondary.vx() - primary.x()
            dy = secondary.vy() - primary.y()
            dz = secondary.vz() - primary.z()
            dl = math.sqrt(dx**2 + dy**2 + dz**2)
            print "Normalized momentum:", px/p, py/p, pz/p,
            print "Normalized displacement:", dx/dl, dy/dl, dz/dl
    if i > 20: break
