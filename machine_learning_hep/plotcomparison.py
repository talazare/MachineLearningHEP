#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
##                 Author: Gian.Michele.Innocenti@cern.ch                  ##
## This program is free software: you can redistribute it and/or modify it ##
##  under the terms of the GNU General Public License as published by the  ##
## Free Software Foundation, either version 3 of the License, or (at your  ##
## option) any later version. This program is distributed in the hope that ##
##  it will be useful, but WITHOUT ANY WARRANTY; without even the implied  ##
##     warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    ##
##           See the GNU General Public License for more details.          ##
##    You should have received a copy of the GNU General Public License    ##
##   along with this program. if not, see <https://www.gnu.org/licenses/>. ##
#############################################################################

"""
main script for doing final stage analysis
"""
# pylint: disable=unused-wildcard-import, wildcard-import
from array import *
# pylint: disable=import-error, no-name-in-module, unused-import
import yaml
from ROOT import TFile, TH1F, TCanvas
from ROOT import gStyle, TLegend
from ROOT import gROOT
from ROOT import TStyle, gPad

# pylint: disable=import-error, no-name-in-module, unused-import
# pylint: disable=too-many-statements
def plotcomparison_ntrkl(case, arraytype, var):

    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptStat(0000)
    gStyle.SetPalette(0)
    gStyle.SetCanvasColor(0)
    gStyle.SetFrameFillColor(0)
    gStyle.SetOptTitle(0)
    print(var)
    with open("data/database_ml_parameters_%s.yml" % case, 'r') as param_config:
        data_param = yaml.load(param_config, Loader=yaml.FullLoader)

    folder_MB_allperiods = data_param[case]["analysis"][arraytype[0]]["data"]["resultsallp"]
    folder_triggered = data_param[case]["analysis"][arraytype[1]]["data"]["results"][3]
    br = data_param[case]["ml"]["opt"]["BR"]


    ccross = TCanvas('cCross', 'The Fit Canvas', 100, 600)
    ccross = TCanvas('cCross', 'The Fit Canvas')
    ccross.SetCanvasSize(1500, 1500)
    ccross.SetWindowSize(500, 500)
    ccross.SetLogx()

    legyield = TLegend(.3, .65, .7, .85)
    legyield.SetBorderSize(0)
    legyield.SetFillColor(0)
    legyield.SetFillStyle(0)
    legyield.SetTextFont(42)
    legyield.SetTextSize(0.035)

    fileres_MB_allperiods = TFile.Open("%s/finalcross%s%smulttot.root" % \
                            (folder_MB_allperiods, case, "MBvspt_ntrkl"))
    fileres_MB_SPD2018 = TFile.Open("%s/finalcross%s%smulttot.root" % \
                            (folder_triggered, case, "SPDvspt"))

    hempty = TH1F("hempty", "hempty", 100, 0, 30)
    hempty.GetYaxis().SetTitleOffset(1.2)
    hempty.GetYaxis().SetTitleFont(42)
    hempty.GetXaxis().SetTitleFont(42)
    hempty.GetYaxis().SetLabelFont(42)
    hempty.GetXaxis().SetLabelFont(42)
    hempty.GetYaxis().SetTitle("Corrected yield %s" % case)
    hempty.GetXaxis().SetTitle("p_{T} (GeV)")
    hempty.SetMinimum(1e-8)
    hempty.SetMaximum(1000)
    hempty.Draw()

    legyield = TLegend(.3, .65, .7, .85)
    legyield.SetBorderSize(0)
    legyield.SetFillColor(0)
    legyield.SetFillStyle(0)
    legyield.SetTextFont(42)
    legyield.SetTextSize(0.035)

    colors = [1, 2, 3, 4]
    legends = ["integrated from MB",
               "ntrkl 0-20 from MB",
               "ntrkl 20-60 from MB",
               "ntrkl 60-1000 from HighMultSPD"]
    for imult  in [0, 1, 2]:
        gPad.SetLogy()
        hyield = fileres_MB_allperiods.Get("histoSigmaCorr%d" % (imult))
        hyield.Scale(1./br)
        hyield.SetLineColor(colors[imult])
        hyield.SetMarkerColor(colors[imult])
        hyield.Draw("same")
        legyield.AddEntry(hyield, legends[imult], "LEP")
    legyield.Draw()

    hyieldSPD2018 = fileres_MB_SPD2018.Get("histoSigmaCorr3")
    hyieldSPD2018.Scale(1./br)
    hyieldSPD2018.SetLineColor(4)
    hyieldSPD2018.SetMarkerColor(4)
    hyieldSPD2018.Draw("same")
    legyield.AddEntry(hyieldSPD2018, legends[3], "LEP")
    ccross.SaveAs("ComparisonCorrYields_%s%s.eps" % (case, var))

plotcomparison_ntrkl("LcpK0spp", ["MBvspt_ntrkl", "SPDvspt"], "ntrkl")
plotcomparison_ntrkl("D0pp", ["MBvspt_ntrkl", "SPDvspt"], "ntrkl")