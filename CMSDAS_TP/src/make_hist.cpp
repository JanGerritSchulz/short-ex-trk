TH1F* make_hist(string name, float** values, int qnt, int bin_n, Float_t* binning, bool IsMc, bool DRAW = false)
{
    //AddBinContent
    //HISTOGRAM NEEDS TO HAVE VARIABLE BINS
   
    TH1F* hist = new TH1F(name.c_str(), name.c_str(), bin_n, binning[0],binning[bin_n]);
  
    for (int i = 0; i < bin_n; i++)
    {
        hist->SetBinContent(i+1, values[i][qnt]);
        hist->SetBinError(i+1, values[i][qnt+2]);
    }
    if (DRAW)
    {
        TCanvas* xperiment = new TCanvas;
        xperiment->cd();
        hist->Draw();
    }
    return hist;
}

