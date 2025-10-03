# short-ex-trk
Code for the CMSDAS Schools Short Tracking Exercise

## The setup
This package is meant to provide solutions to the exercises 

* Setup in `CMSSW_14_1_0_pre4` 

```
scram p -n cmssw CMSSW_14_1_0_pre4
cd cmssw/src/
cmsenv
git clone git@github.com:JanGerritSchulz/short-ex-trk.git .
scram b -j 8
```

Then simply run the configs
```
cmsRun MyDirectory/PrintOutTracks/test/run_cfg.py
cmsRun MyDirectory/PrintOutTracks/test/run_cfg_MVA.py
cmsRun MyDirectory/PrintOutTracks/test/construct_secondary_vertices_cfg.py
```

or the scripts in 

`$CMSSW_BASE/src/MyDirectory/PrintOutTracks/scripts/`

----


