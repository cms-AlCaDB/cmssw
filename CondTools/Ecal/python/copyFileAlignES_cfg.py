import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.load("EcalTrivialAlignment_cfi")

process.load("CondCore.CondDB.CondDB_cfi")
#process.CondDBCommon.connect = 'oracle://cms_orcoff_prep/CMS_COND_ECAL'
#process.CondDBCommon.DBParameters.authenticationPath = '/afs/cern.ch/cms/DB/conddb/'
process.CondDBCommon.connect = 'sqlite_file:ESAlign_2010.db'

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('*'),
    destinations = cms.untracked.vstring('cout')
)

process.source = cms.Source("EmptyIOVSource",
    firstValue = cms.uint64(1),
    lastValue = cms.uint64(1),
    timetype = cms.string('runnumber'),
    interval = cms.uint64(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    process.CondDBCommon,
    timetype = cms.untracked.string('runnumber'),
    toPut = cms.VPSet(
       cms.PSet(
          record = cms.string('ESAlignmentRcd'),
          tag = cms.string('ESAlignment_measured_v01_offline')
       )
    )
)

process.dbCopy = cms.EDAnalyzer("EcalDBCopy",
    timetype = cms.string('runnumber'),
    toCopy = cms.VPSet( 
       cms.PSet(
          record = cms.string('ESAlignmentRcd'),
          container = cms.string('ESAlignment')
       )
    )
)


process.prod = cms.EDAnalyzer("EcalTrivialObjectAnalyzer")

process.p = cms.Path(process.prod*process.dbCopy)

