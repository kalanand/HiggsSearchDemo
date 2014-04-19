#!/usr/bin/env python
import os,sys
import string, re
from time import gmtime, localtime, strftime


dir = "/eos/uscms/store/user/lnujj/RDtrees_with_8TeV_MVA_v1/"

cuts = "((ggdevt == 2) || (ggdevt == 3)) && (fit_status==0) && (W_mt > 30) && (mva2j400mu>0.5) && (Mass2j_PFCor > 60.0) && (Mass2j_PFCor < 100.0) && sqrt(JetPFCor_Pt[0]*JetPFCor_Pt[0]+JetPFCor_Pt[1]*JetPFCor_Pt[1]+2*JetPFCor_Pt[0]*JetPFCor_Pt[1]*cos(JetPFCor_Phi[0]-JetPFCor_Phi[1]))>70.0 && abs(JetPFCor_Eta[0]-JetPFCor_Eta[1])<0.8 && (mva2j400mu > 0.5)"


Branches = ['fit_mlvjj', 'MassV2j_PFCor', 'Mass2j_PFCor', 'event_runNo', 
            'event_evtNo', 'event_nPV', 'event_met_pfmet', 
            'event_met_pfmetPhi', 'event_fastJetRho', 'JetPFCor_Pt',
            'JetPFCor_Eta', 'JetPFCor_Phi', 'W_mt',
            'W_muon_pt', 'W_muon_eta', 'W_muon_phi']


files = [             
    'RD_mu_HWWMH190_CMSSW532_private.root',
    'RD_mu_HWWMH200_CMSSW532_private.root',
    'RD_mu_HWWMH300_CMSSW532_private.root',
    'RD_mu_HWWMH500_CMSSW532_private.root',
    'RD_mu_STopS_Tbar_CMSSW532.root',
    'RD_mu_STopS_T_CMSSW532.root',
    'RD_mu_STopT_Tbar_CMSSW532.root',
    'RD_mu_STopT_T_CMSSW532.root',
    'RD_mu_STopTW_Tbar_CMSSW532.root',
    'RD_mu_STopTW_T_CMSSW532.root',
    'RD_mu_TTbar_CMSSW532.root',
    'RD_mu_WJets_CMSSW532_merged.root',
    'RD_mu_WW_CMSSW532.root',
    'RD_mu_WZ_CMSSW532.root',
    'RD_mu_ZpJ_CMSSW532.root',
    'RD_mu_ZZ_CMSSW532.root',
    'RD_WmunuJets_DataAll_GoldenJSON_19p3invfb.root'
    ]

     
def ReduceFile(inputRootFile):
    from ROOT import TTree, TFile, gROOT
    print 'Processing ', file 
    
    outRootFile = '' + inputRootFile
    strreplace = ['RD_', '_CMSSW532', '_private']
    for str in strreplace:  
        outRootFile = outRootFile.replace(str, '')

    fout = TFile(outRootFile,"recreate")
    f = TFile(dir + inputRootFile,"read")
    tree = f.Get("WJet")
    tree.SetBranchStatus('*', 0)
    for name in Branches: tree.SetBranchStatus(name, 1)
    
    gROOT.cd()
    tree2 = tree.CopyTree(cuts)
    fout.cd()
    tree2.Write()
    fout.Close()


if __name__ == "__main__":
    
    for file in files: ReduceFile(file)
