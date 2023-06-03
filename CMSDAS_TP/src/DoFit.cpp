using namespace RooFit;

float* doFit(string condition, string MuonID_str, string quant, float* init_conditions, bool save = true, bool isMC = false ) // RETURNS ARRAY WITH [yield_all, yield_pass, err_all, err_pass]    ->   OUTPUT ARRAY
{
    string* file_name = new string[2];
    file_name[0] = "TP_Z_Data_reduced.root";
    file_name[1] = "TP_Z_MC_reduced.root";
    TFile *file0    = TFile::Open(file_name[isMC].c_str());
    TTree *DataTree = (TTree*)file0->Get(("muon/StandAloneEvents"));
    
    float _mmin = 40.0;  float _mmax = 150.0;
    
    RooRealVar MuonID(MuonID_str.c_str(), MuonID_str.c_str(), 0, 1); //Muon_Id
    
    RooRealVar InvariantMass("pair_mass", "pair_mass", _mmin, _mmax);
    
    
    float* limits = new float[2];
    if (quant == "pt") {
        limits[0] = 0;
        limits[1] = 120;
    }
    if (quant == "eta") {
        limits[0] = -2.4;
        limits[1] = 2.4;
    }
    if (quant == "phi") {
        limits[0] = -2;
        limits[1] = 2;
    }
    RooRealVar quantity(("probe_" + quant).c_str(), ("probe_" + quant).c_str(), limits[0], limits[1]);
    
    RooFormulaVar* redeuce = new RooFormulaVar("PPTM", (condition ).c_str(), RooArgList(quantity));
    RooDataSet *Data_ALL    = new RooDataSet("DATA", "DATA", DataTree, RooArgSet(InvariantMass, MuonID, quantity),*redeuce);
    RooFormulaVar* cutvar = new RooFormulaVar("PPTM", (condition + " && " + MuonID_str + " == 1" ).c_str() , RooArgList(MuonID, quantity));
    RooDataSet *Data_PASSING = new RooDataSet("DATA_PASS", "DATA_PASS", DataTree, RooArgSet(InvariantMass, MuonID, quantity), *cutvar);//
    
    RooDataHist* dh_ALL     = Data_ALL->binnedClone();
    RooDataHist* dh_PASSING = Data_PASSING->binnedClone();
    
    TCanvas* c  = new TCanvas;
    c->Divide(2,1);
    
    RooPlot *frame = InvariantMass.frame(RooFit::Title("Invariant Mass"));
    // BACKGROUND VARIABLES
    RooRealVar alpha("alpha", "alpha", -0.1, -1.0, 0.1);

    // BACKGROUND FUNCTION
    RooExponential background("background","background", InvariantMass, alpha);
    
    // GAUSSIAN VARIABLES
    RooRealVar mean1("mean1","mean1",init_conditions[0],70,115);
    RooRealVar width("width","width",init_conditions[1],1.2,10.0);
    RooRealVar sigma("sigma","sigma",init_conditions[2],0.5,30);
    

    // FIT FUNCTIONS
    RooVoigtian signal("signal","signal",InvariantMass,mean1,width,sigma);
    
    float n_signal_initial1 =(Data_ALL->sumEntries(TString::Format("abs(pair_mass-%g)<0.015",init_conditions[0]))-Data_ALL->sumEntries(TString::Format("abs(pair_mass-%g)<0.030 && abs(pair_mass-%g)>.015",init_conditions[0],init_conditions[0]))) / Data_ALL->sumEntries();
    float n_signal_initial_total = n_signal_initial1 ;
    float n_back_initial = 1. - n_signal_initial1 ;
    
    RooRealVar n_signal_total("n_signal_total","n_signal_total",n_signal_initial_total,0.,Data_ALL->sumEntries());
    RooRealVar n_signal_total_pass("n_signal_total_pass","n_signal_total_pass",n_signal_initial_total,0.,Data_PASSING->sumEntries());
    
    RooRealVar n_back("n_back","n_back",n_back_initial,0.,Data_ALL->sumEntries());
    RooRealVar n_back_pass("n_back_pass","n_back_pass",n_back_initial,0.,Data_PASSING->sumEntries());
    RooAddPdf* model;
    RooAddPdf* model_pass;
    
    model      = new RooAddPdf("model","model", RooArgList(signal, background),RooArgList(n_signal_total, n_back));
    model_pass = new RooAddPdf("model_pass", "model_pass", RooArgList(signal, background),RooArgList(n_signal_total_pass, n_back_pass));
    
    // SIMULTANEOUS FIT
    RooCategory sample("sample","sample") ;
    sample.defineType("All") ;
    sample.defineType("PASSING") ;
    
    RooDataHist combData("combData","combined data",InvariantMass,Index(sample),Import("ALL",*dh_ALL),Import("PASSING",*dh_PASSING));
    
    RooSimultaneous simPdf("simPdf","simultaneous pdf",sample) ;
    
    simPdf.addPdf(*model,"ALL");
    simPdf.addPdf(*model_pass,"PASSING");
    
    RooFitResult* fitres = new RooFitResult;
    fitres = simPdf.fitTo(combData, RooFit::Save());
    
    // OUTPUT ARRAY
    float* output = new float[4];
    
    RooRealVar* yield_ALL = (RooRealVar*) fitres->floatParsFinal().find("n_signal_total");
    RooRealVar* yield_PASS = (RooRealVar*) fitres->floatParsFinal().find("n_signal_total_pass");
    
    output[0] = yield_ALL->getVal();
    output[1] = yield_PASS->getVal();
    
    output[2] = yield_ALL->getError();
    output[3] = yield_PASS->getError();
    
    frame->SetTitle("ALL");
    frame->SetXTitle("#mu^{+}#mu^{-} invariant mass [GeV/c^{2}]");
    Data_ALL->plotOn(frame);
    
    model->plotOn(frame);
    // model->plotOn(frame,RooFit::Components("signal"),RooFit::LineStyle(kDashed),RooFit::LineColor(kGreen));
    // model->plotOn(frame,RooFit::Components("background"),RooFit::LineStyle(kDashed),RooFit::LineColor(kRed));
    
    c->cd(1);
    frame->Draw("");
    
    RooPlot *frame_pass = InvariantMass.frame(RooFit::Title("Invariant Mass"));
    
    c->cd(2);
    
    frame_pass->SetTitle("PASSING");
    frame_pass->SetXTitle("#mu^{+}#mu^{-} invariant mass [GeV/c^{2}]");
    Data_PASSING->plotOn(frame_pass);
    
    // model_pass->plotOn(frame_pass);
    model_pass->plotOn(frame_pass,RooFit::Components("signal"),RooFit::LineStyle(kSolid),RooFit::LineColor(kGreen));
    model_pass->plotOn(frame_pass,RooFit::Components("background"),RooFit::LineStyle(kSolid),RooFit::LineColor(kRed));
    
    frame_pass->Draw();

    if(save)
    {
        
         if(isMC){
           
         c->SaveAs(("Fit_Result/" + condition + "_MC.pdf").c_str());
         
         }
         if(!isMC){
            
          c->SaveAs(("Fit_Result/" + condition + "_Data.pdf").c_str());
          
         }
    }
        
    // DELETING ALLOCATED MEMORY
    delete[] limits;
    //
    delete file0;
    //
    delete Data_ALL;
    delete Data_PASSING;
    //
    delete dh_ALL;
    delete dh_PASSING;
    //
    delete cutvar;
    delete redeuce;
    //
    
    //
    delete c;
    //
    delete model;
    delete model_pass;
    delete fitres;
    
    return output;
}
