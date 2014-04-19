#!/usr/bin/env python
import os,sys
import string, re
from time import gmtime, localtime, strftime
import ROOT
from ROOT import TTree, TFile, TH1, TH1D, TCanvas, gROOT, gStyle, TLegend
 
intLUMI = 19600 

cuts = 'Mass2j_PFCor > 60.0 && Mass2j_PFCor < 100.0 && sqrt(JetPFCor_Pt[0]*JetPFCor_Pt[0]+JetPFCor_Pt[1]*JetPFCor_Pt[1]+2*JetPFCor_Pt[0]*JetPFCor_Pt[1]*cos(JetPFCor_Phi[0]-JetPFCor_Phi[1]))>70.0 && abs(JetPFCor_Eta[0]-JetPFCor_Eta[1])<0.8 && mva2j400mu > 0.5'


def DrawHiggsMass(inputRootFile, scale = 1.0):
 
    f = TFile('data/' + inputRootFile,"read")
    tree = f.Get("WJet")
    gROOT.cd()

    histName = inputRootFile.replace('.root','')
    hist = TH1D(histName, '', 20, 100., 900.)
    xaxis = hist.GetXaxis()
    yaxis = hist.GetYaxis()
    xaxis.SetTitle('Higgs mass [GeV]')
    yaxis.SetTitle('Events / 40 GeV')

    xaxis.SetLabelSize(0.05)
    xaxis.SetTitleSize(0.05)
    xaxis.SetNdivisions(505)
    yaxis.SetLabelSize(0.05)
    yaxis.SetTitleSize(0.05)
    yaxis.SetTitleOffset(1.6)
    yaxis.SetNoExponent()
 
    tree.Draw("fit_mlvjj>>"+histName, cuts, "goff")
    hist.Scale(scale)
    return hist



def GetHistVjets():

    wjets_scale   = 36257.2* intLUMI/ (18353019+57709905)
    ZJets_scale   = 3503.71  * intLUMI/30209426

    h1 = DrawHiggsMass('mu_WJets_merged.root', wjets_scale)
    h2 = DrawHiggsMass('mu_ZpJ.root', ZJets_scale)
    h1.Add(h2)
    h1.Scale(0.87)
    return h1


def GetHistTop():

    ttbar_scale   = 225.197 * intLUMI*1.08687/6893735
    SToppS_scale  = 1.75776  * intLUMI/139974
    SToppT_scale  = 30.0042  * intLUMI/1935066
    SToppTW_scale = 11.1773  * intLUMI/493458
    STopS_scale   = 3.89394  * intLUMI/259960
    STopT_scale   = 55.531  * intLUMI/3758221
    STopTW_scale  = 11.1773  * intLUMI/497657

    h1 = DrawHiggsMass('mu_TTbar.root', ttbar_scale)
    h2 = DrawHiggsMass('mu_STopS_Tbar.root', SToppS_scale)
    h3 = DrawHiggsMass('mu_STopT_Tbar.root', SToppT_scale)
    h4 = DrawHiggsMass('mu_STopTW_Tbar.root', SToppTW_scale)
    h5 = DrawHiggsMass('mu_STopS_T.root', STopS_scale)
    h6 = DrawHiggsMass('mu_STopT_T.root', STopT_scale)
    h7 = DrawHiggsMass('mu_STopTW_T.root', STopTW_scale)
    h1.Add(h2)
    h1.Add(h3)
    h1.Add(h4)
    h1.Add(h5)
    h1.Add(h6)
    h1.Add(h7)
    h1.Scale(0.85)
    return h1


def GetHistVV():

    WW_scale      = 54.838   * intLUMI/9450414
    WZ_scale      = 32.3161   * intLUMI/10000267
    ZZ_scale      = 8.059   * intLUMI/9702850

    h1 = DrawHiggsMass('mu_WW.root', WW_scale)
    h2 = DrawHiggsMass('mu_WZ.root', WZ_scale)
    h3 = DrawHiggsMass('mu_ZZ.root', ZZ_scale)
    h1.Add(h2)
    h1.Add(h3)
    return h1



if __name__ == "__main__":

    ######## Data histogram #########
    data = DrawHiggsMass('mu_data.root')
    data.SetMarkerStyle(20)
    data.SetMinimum(0.7)

    ######## W/Z+jets #########
    vjets = GetHistVjets()
    vjets.SetFillColor(2)

    ######## Top #########   
    top = GetHistTop()
    top.Add(vjets)
    top.SetFillColor(3)

    ######## Diboson #########   
    diboson = GetHistVV()
    diboson.Add(top)
    diboson.SetFillColor(7)

    ######## Higgs signal histograms #########   
    H190_scale = 6 * 8.782*0.115*1.5*2.* intLUMI/194504
    hist190 = DrawHiggsMass('mu_HWWMH190.root', H190_scale)
    H300_scale = 6 * 3.606*0.101*1.5*2.* intLUMI/197284
    hist300 = DrawHiggsMass('mu_HWWMH300.root', H300_scale)
    H500_scale = 6 * 1.439*0.080*1.5*2.* intLUMI/198470
    hist500 = DrawHiggsMass('mu_HWWMH500.root', H500_scale)

    hist300.SetLineStyle(2)
    hist500.SetLineStyle(3)

    hist190.SetLineWidth(2)
    hist300.SetLineWidth(2)
    hist500.SetLineWidth(3)

    ######## Now draw everything #########  
    gStyle.SetOptStat(0)
    gStyle.SetPadTopMargin(0.05);
    gStyle.SetPadBottomMargin(0.13);
    gStyle.SetPadLeftMargin(0.16);
    gStyle.SetPadRightMargin(0.05);

    c1 = TCanvas('c1', 'c1', 500, 500)
    data.Draw('e')
    diboson.Draw("same")
    top.Draw("same")
    vjets.Draw("same")
    hist190.Draw("same")
    hist300.Draw("same")
    hist500.Draw("same")
    data.Draw('esame')

    legend = TLegend(0.6,0.55,0.95,0.95);
    legend.AddEntry( data, "Data", "pl");
    legend.AddEntry( vjets, "W/Z+jets", "f");
    legend.AddEntry( top, "Top", "f");
    legend.AddEntry( diboson, "Diboson", "f");
    legend.AddEntry( hist190, "Higgs(200)", "l");
    legend.AddEntry( hist300, "Higgs(300)", "l");
    legend.AddEntry( hist500, "Higgs(500)", "l");
    legend.Draw()
    c1.SaveAs("Higgs_mass.png")
    c1.WaitPrimitive()



    ######## Subtracted plot #########  
    subdata = data.Clone('subdata')
    subdata.Add(diboson, -1.0)
    for i in range(1, data.GetNbinsX(), 1): 
        error = subdata.GetBinError(i)
        subdata.SetBinError(i, 4* error) # MC errors are ~4x stat error
    subdata.GetYaxis().SetRangeUser(-80, 180)
    c2 = TCanvas('c2', 'c2', 500, 500)
    subdata.Draw('e')
    hist190.Draw("same")
    hist300.Draw("same")
    hist500.Draw("same")
    subdata.Draw('esame')

    legend2 = TLegend(0.62,0.67,0.95,0.95);
    legend2.AddEntry( data, "Data - Background", "pl");
    legend2.AddEntry( hist190, "Higgs(200)", "l");
    legend2.AddEntry( hist300, "Higgs(300)", "l");
    legend2.AddEntry( hist500, "Higgs(500)", "l");
    legend2.Draw()
    c2.SaveAs("Higgs_mass_subtracted.png")
    c2.WaitPrimitive()


