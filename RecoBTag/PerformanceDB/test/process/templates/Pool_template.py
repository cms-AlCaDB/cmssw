import FWCore.ParameterSet.Config as cms

from CondCore.CondDB.CondDB_cfi import *

PoolDBESSource = cms.ESSource("PoolDBESSource",
                              CondDB,
                              toGet = cms.VPSet(
    #
    # working points
    #
    cms.PSet(
    record = cms.string('PerformancePayloadRecord'),
    tag = cms.string('NAME_T'),
    label = cms.untracked.string('NAME_T')
    ),
    cms.PSet(
    record = cms.string('PerformanceWPRecord'),
    tag = cms.string('NAME_WP'),
    label = cms.untracked.string('NAME_WP')
    ),
))

                              
                              
                              
