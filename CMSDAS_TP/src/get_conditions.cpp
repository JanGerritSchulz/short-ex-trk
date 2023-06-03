string* get_conditions(int bin_n, float* bins, string quantity)
{
    string* conditions = new string[bin_n];
    for (int i = 0; i < bin_n; i++)
    {
        conditions[i] = quantity + ">" + to_string(bins[i]) + " && " + quantity + "<=" + to_string(bins[i+1]);
        //+ " && " + " tag_pt > 27 && pair_dz < 4. && tag_isTight == 1 && (tag_charge * probe_charge == -1) && (tag_pfIso04_charged + max(tag_pfIso04_neutral + tag_pfIso04_photon - tag_pfIso04_sumPU/2,0.0)/tag_pt && probe_isSA && HLT_IsoMu24_v"
    }
    return conditions;
}
