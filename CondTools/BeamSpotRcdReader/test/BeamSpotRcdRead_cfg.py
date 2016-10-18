import FWCore.ParameterSet.Config as cms

process = cms.Process("READ")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000000) )

process.source = cms.Source("EmptySource",
                            numberEventsInRun = cms.untracked.uint32(5000),
                            firstRun = cms.untracked.uint32(273291),
                            numberEventsInLuminosityBlock = cms.untracked.uint32(1),
                            firstLuminosityBlock = cms.untracked.uint32(1)
                            )

# either from Global Tag
# process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cfi")
# from Configuration.AlCa.GlobalTag import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag,"auto:run2_data")

# ...or specify database and tag:  
from CondCore.CondDB.CondDB_cfi import *
CondDBBeamSpotObjects = CondDB.clone(connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'))
process.dbInput = cms.ESSource("PoolDBESSource",
                              CondDBBeamSpotObjects,
                              toGet = cms.VPSet(cms.PSet(record = cms.string('BeamSpotObjectsRcd'),
                                                         #tag = cms.string('BeamSpotObjects_2016B_v2_LumiBased_TEST_offline') # choose tag you want
                                                         tag = cms.string('BeamSpotObjects_2016_LumiBased_v0_offline')
                                                         )
                                                )
                              )

process.beamspot = cms.EDAnalyzer("BeamSpotRcdReader",
                                  rawFileName = cms.untracked.string("")
                                  )

#process.beamspot.rawFileName = 'beamspot_BeamSpotObjects_2016B_v2_LumiBased_TEST_offline.txt'
process.beamspot.rawFileName = 'beamspot_BeamSpotObjects_2016_LumiBased_v0_offline.txt'

####################################################################
# Output file
####################################################################
process.TFileService = cms.Service("TFileService",
                                   #fileName=cms.string("BeamSpotObjects_2016B_v2_LumiBased_TEST_offline.root")
                                   fileName=cms.string("BeamSpotObjects_2016_LumiBased_v0_offline.root")
                                   ) 
                                  
# Put module in path:
process.p = cms.Path(process.beamspot)
