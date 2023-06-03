// -*- C++ -*-
//
// Package:    MyDirectory/PrintOutTracks_MVA
// Class:      PrintOutTracks_MVA
//
/**\class PrintOutTracks_MVA PrintOutTracks_MVA.cc MyDirectory/PrintOutTracks/plugins/PrintOutTracks_MVA.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Brunella D'Anzi
//         Created:  Tue, 20 Dec 2022 19:31:29 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
 #include "FWCore/Utilities/interface/InputTag.h"
 #include "DataFormats/TrackReco/interface/Track.h"
 #include "DataFormats/TrackReco/interface/TrackFwd.h"
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


using reco::TrackCollection;

class PrintOutTracks_MVA : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit PrintOutTracks_MVA(const edm::ParameterSet&);
      ~PrintOutTracks_MVA();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
  //      edm::EDGetTokenT<TrackCollection> tracksToken_;  //used to select what tracks to read from configuration file
  edm::EDGetTokenT<edm::View<reco::Track> > tracksToken_;  //used to select which tracks to read from configuration file
  int indexEvent_;
  edm::EDGetTokenT<edm::View<float> > mvaValsToken_;
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
PrintOutTracks_MVA::PrintOutTracks_MVA(const edm::ParameterSet& iConfig)
  :
  //  tracksToken_(consumes<TrackCollection>(iConfig.getUntrackedParameter<edm::InputTag>("tracks")))
  tracksToken_(consumes<edm::View<reco::Track> >(iConfig.getUntrackedParameter<edm::InputTag>("tracks", edm::InputTag("generalTracks")) )), mvaValsToken_( consumes<edm::View<float> >(iConfig.getUntrackedParameter<edm::InputTag>("mvaValues", edm::InputTag("generalTracks", "MVAValues")) ) )
{
   //now do what ever initialization is needed
  indexEvent_ = 0;
}


PrintOutTracks_MVA::~PrintOutTracks_MVA()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
PrintOutTracks_MVA::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   std::cout << "Event " << indexEvent_ << std::endl;
   edm::Handle<edm::View<reco::Track> > trackHandle;
   iEvent.getByToken(tracksToken_, trackHandle);   
   if ( !trackHandle.isValid() ) return;
   const auto numTotal = trackHandle->size();
   edm::Handle<edm::View<float> > trackMVAstoreHandle;
   iEvent.getByToken(mvaValsToken_,trackMVAstoreHandle);
   if ( !trackMVAstoreHandle.isValid() ) return;
   auto numLoose = 0;
   auto numTight = 0;
   auto numHighPurity = 0;
   const edm::View<reco::Track>& tracks = *trackHandle;
   size_t iTrack = 0;
   for ( auto track : tracks ) {
     if (track.quality(track.qualityByName("loose"))     ) ++numLoose;
     if (track.quality(track.qualityByName("tight"))     ) ++numTight;
     if (track.quality(track.qualityByName("highPurity"))) ++numHighPurity;
     std::cout << "    Track " << iTrack << " "
	       << track.charge()/track.pt() << " "
	       << track.phi() << " "
	       << track.eta() << " "
	       << track.dxy() << " "
	       << track.dz()
	       << track.chi2() << " "
	       << track.ndof() << " "
	       << track.numberOfValidHits() << " "
	       << track.algoName() << " "
	       << trackMVAstoreHandle->at(iTrack)
	       << std::endl;
     iTrack++;
   }
   ++indexEvent_;
   std::cout << "Event " << indexEvent_
	     << " numTotal: " << numTotal
	     << " numLoose: " << numLoose
	     << " numTight: " << numTight
	     << " numHighPurity: " << numHighPurity
	     << std::endl;

#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void
PrintOutTracks_MVA::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
PrintOutTracks_MVA::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PrintOutTracks_MVA::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PrintOutTracks_MVA);
