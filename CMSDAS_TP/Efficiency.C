#include "src/compare_efficiency.C"
#include "src/DoFit.cpp"
#include "src/get_conditions.cpp"
#include "src/get_efficiency.cpp"
#include "src/change_bin.cpp"
#include "src/make_hist.cpp"

void Efficiency()
{
    //We start by declaring the nature of our dataset. (Is the data real or simulated?)
    bool IsMC   = false;
    //Which efficiency do you want to study?
    string MuonId   = "probe_isTrkMatch";
    //Which quantity do you want to use?
    string quantity = "eta"; //pt, eta or phi
    
    /*-----------------------------------I N S E R T    C O D E    H E R E-----------------------------------*/
    float bins[] =  {-2.4, -1.6, -1.1, -0.6, -0.2, 0.2, 0.6, 1.1, 1.6, 2.4}; // Eta bins
    int bin_n     =  9; // Eta bins
     /*------------------------------------------------------------------------------------------------------*/
    
    
    //Now we must choose initial conditions in order to fit our data
    float *init_conditions = new float[3];
    /*-----------------------------------I N S E R T    C O D E    H E R E-----------------------------------*/
    init_conditions[0] = 91.0;
    init_conditions[1] = 2.495;
    init_conditions[2] = 5.0;
    /*------------------------------------------------------------------------------------------------------*/
    
    
    string* conditions = get_conditions(bin_n, bins, "probe_" + quantity);
    float ** yields_n_errs = new float*[bin_n];
    
      for (int i = 0; i < bin_n; i++)
      {
          if (IsMC)
              yields_n_errs[i] = doFit(conditions[i], MuonId, quantity, init_conditions,true, IsMC);
          else
              yields_n_errs[i] = doFit(conditions[i], MuonId, quantity, init_conditions,true, IsMC);
              //doFit returns: [yield_all, yield_pass, err_all, err_pass]
      }
     TH1F *yield_ALL  = make_hist("ALL" , yields_n_errs, 0, bin_n, bins, IsMC);
     TH1F *yield_PASS = make_hist("PASS", yields_n_errs, 1, bin_n, bins, IsMC);
    
    //----------------------SAVING RESULTS TO Histograms.root--------------------//
    //useful if we require to change the fit on a specific set of bins
     string* file_name = new string[2];
     file_name[0] = "Histograms_Data.root";
     file_name[1] = "Histograms_MC.root";
     TFile* EfficiencyFile = TFile::Open(file_name[IsMC].c_str(),"RECREATE");
     yield_ALL->SetDirectory(gDirectory);
     yield_PASS->SetDirectory(gDirectory);
     EfficiencyFile->Write();
    //-----------------------------------------------------------------//
    
    //If all of the fits seem correct we can proceed to generate the efficiency
    get_efficiency(yield_ALL, yield_PASS, quantity, IsMC);
     
    //In case you want to change the fit on a specific, comment the loop and "result saving" code and uncomment the following function
    //change_bin(bin number, /*condition (you can copy the title from the generated fit .pdf)*/, MuonId, quantity, IsMC, init_conditions);
    // Example for the last bin issue in Data
    //change_bin(bin_n, "probe_eta>1.600000 && probe_eta<=2.400000", MuonId, quantity, IsMC, init_conditions, "Histograms_Data.root");
    //bins start on 1
    
    //Once we've calculated the efficiency for both data sets, we can generate
    //a plot that combines both results
    //compare_efficiency(quantity, "Efficiency_Result/" + quantity + "/Efficiency_MC.root", "Efficiency_Result/" + quantity + "/Efficiency_Run2018.root");
}
