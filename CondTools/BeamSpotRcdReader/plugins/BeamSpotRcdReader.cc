// -*- C++ -*-
//
// Package:    CondTools/BeamSpotRcdReader
// Class:      BeamSpotRcdReader
// 
/**\class BeamSpotRcdReader BeamSpotRcdReader.cc CondTools/BeamSpotRcdReader/plugins/BeamSpotRcdReader.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Marco Musich
//         Created:  Tue, 18 Oct 2016 11:00:44 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ESWatcher.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/DataRecord/interface/BeamSpotObjectsRcd.h"
#include "CondFormats/BeamSpotObjects/interface/BeamSpotObjects.h"

#include <sstream>
#include <fstream>

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class BeamSpotRcdReader : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit BeamSpotRcdReader(const edm::ParameterSet&);
      ~BeamSpotRcdReader();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);
      virtual void endJob() override;

      // ----------member data ---------------------------
      edm::ESWatcher<BeamSpotObjectsRcd> watcher_;
      edm::LuminosityBlockNumber_t firstLumi_;
      edm::LuminosityBlockNumber_t lastLumi_;
      std::auto_ptr<std::ofstream> output_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
BeamSpotRcdReader::BeamSpotRcdReader(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
   usesResource("TFileService");
   std::string fileName(iConfig.getUntrackedParameter<std::string>("rawFileName"));
   if (fileName.size()) {
     output_.reset(new std::ofstream(fileName.c_str()));
     if (!output_->good()) {
       edm::LogError("IOproblem") << "Could not open output file " << fileName << ".";
       output_.reset();
     }
   }
}


BeamSpotRcdReader::~BeamSpotRcdReader()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
BeamSpotRcdReader::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   std::ostringstream output;   

   if (watcher_.check(iSetup)) { // new IOV for this run(LS)
     
     output << " for runs: " << iEvent.id().run() << " - " << iEvent.id().luminosityBlock() << std::endl;
     // Get BeamSpot from EventSetup:
     edm::ESHandle< BeamSpotObjects > beamhandle;
     iSetup.get<BeamSpotObjectsRcd>().get(beamhandle);
     const BeamSpotObjects *mybeamspot = beamhandle.product();
     //std::cout << *mybeamspot << std::endl;
     output <<  *mybeamspot << std::endl;
   }

   // Final output - either message logger or output file:
   if (output_.get()) *output_ << output.str();
   else edm::LogInfo("") << output.str();
}


// ------------ method called once each job just before starting event loop  ------------
void 
BeamSpotRcdReader::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
BeamSpotRcdReader::endJob() 
{
}

void 
BeamSpotRcdReader::endLuminosityBlock(const edm::LuminosityBlock& lb, const edm::EventSetup& es){}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BeamSpotRcdReader::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BeamSpotRcdReader);
