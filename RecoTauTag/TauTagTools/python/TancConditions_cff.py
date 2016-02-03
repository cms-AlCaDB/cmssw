import FWCore.ParameterSet.Config as cms

from CondCore.CondDB.CondDB_cfi import *

TauTagMVAComputerRecord = cms.ESSource("PoolDBESSource",
	CondDB,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(cms.PSet(
		record = cms.string('TauTagMVAComputerRcd'),
		tag = cms.string('TauNeuralClassifier')
	)),
        connect = cms.string('sqlite_fip:CondCore/SQLiteData/data/RecoTauTagConditions_31X.db'),
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)

