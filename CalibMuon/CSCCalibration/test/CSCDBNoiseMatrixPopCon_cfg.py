# The following comments couldn't be translated into the new config version:

# eg to write payload to the oracle database 
#   replace CondDBCommon.connect = "oracle://cms_orcoff_int2r/CMS_COND_CSC"
# Database output service

import FWCore.ParameterSet.Config as cms

process = cms.Process("ProcessOne")
#PopCon config
process.load("CondCore.CondDB.CondDB_cfi")
process.CondDBCommon.connect = cms.string("sqlite_file:DBNoiseMatrix.db")
#process.CondDBCommon.connect = cms.string("oracle://cms_orcoff_prep/CMS_COND_CSC")
process.CondDBCommon.DBParameters.authenticationPath = '/afs/cern.ch/cms/DB/conddb'

process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        )
    ),
    destinations = cms.untracked.vstring('cout')
)

process.source = cms.Source("EmptyIOVSource",
    lastValue = cms.uint64(1),
    timetype = cms.string('runnumber'),
    #change the firstRun if you want a different IOV
    firstValue = cms.uint64(1),
    interval = cms.uint64(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    process.CondDBCommon,
    logconnect = cms.untracked.string('sqlite_file:matrixlog.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('CSCDBNoiseMatrixRcd'),
        tag = cms.string('CSCDBNoiseMatrix_ME42')
    ))
)

process.WriteNoiseMatrixWithPopCon = cms.EDAnalyzer("CSCNoiseMatrixPopConAnalyzer",
    SinceAppendMode = cms.bool(True),
    record = cms.string('CSCDBNoiseMatrixRcd'),
    loggingOn = cms.untracked.bool(True),
    debug = cms.bool(False),
    Source = cms.PSet(

    )
)

process.p = cms.Path(process.WriteNoiseMatrixWithPopCon)


