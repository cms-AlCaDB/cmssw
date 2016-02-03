import FWCore.ParameterSet.Config as cms

from CondCore.CondDB.CondDB_cfi import *
electronIdPdfs = cms.ESSource("PoolDBESSource",
    CondDB,
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('ElectronLikelihoodPdfsRcd'),
        tag = cms.string('ElectronLikelihoodPdfs_v3_offline')
    ))
)

electronIdPdfs.connect = 'frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS'


