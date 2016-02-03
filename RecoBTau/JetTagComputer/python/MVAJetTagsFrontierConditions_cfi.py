import FWCore.ParameterSet.Config as cms

from CondCore.CondDB.CondDB_cfi import *

BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
	CondDB,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags_CMSSW_2_0_0_mc')
	)),
	connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)
