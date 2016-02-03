import FWCore.ParameterSet.Config as cms

from CondCore.CondDB.CondDB_cfi import *
L1RPCHwConfigOffline = cms.ESSource("PoolDBESSource",
    CondDB,
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('L1RPCHwConfigRcd'),
        tag = cms.string('L1RPCHwConfig_v1')
    )),
    connect = cms.string('oracle://cms_orcoff_prod/CMS_COND_31X_RPC')
)



