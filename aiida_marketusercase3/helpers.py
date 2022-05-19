import math 
from aiida_marketusercase3.templates import *

################## Consider moving these into a 'constants' file or something... ########################
rhoXylene = 864
rhoATSB = 967
mwATSB = 249.35
dnozzle = 0.0008
mwO2 = 32
sigmaATSB = 0.0303
sigmaXylene = 0.0282
myATSB = 1.8
myXylene = 0.0006475
gap_inner_diameter = 0.0017
gap_outer_diameter = 0.0024
mwMethane = 16.04
mwAir = 28.96
atm  = 101325
rgas = 8.314
Tref = 298.15
########################################################################################################

def prepare_inputs(user_input):
    inputs = {}
    inputs['PilotMethaneVolumeFlowRate'] = user_input['Pilotch4fr']
    inputs['PilotOxygenVolumeFlowRate'] =  user_input['Piloto2fr']
    inputs['DispersionVolumeFlowRate'] = user_input['Dispfr']
    inputs['FanExtractionVolumeFlowRate'] = user_input['Fanrate']
    inputs['PreCursorVolumeFlowRate'] = user_input['Precurfr']
    inputs['ATSBConcentration'] = user_input['ATSBcons']
    
    ## this is from model3, but i've added it to make the c-header part work...
    #inputs['ActiveSurfaceArea'] =  user_input['A0']
    #inputs['PalladiumMassFraction'] =  user_input['X_pd']
    #inputs['ActivationEnergy'] =  user_input['Ea']
    #inputs['CatalystSupportMacroPorosity'] =  user_input['por_cat']
    #inputs['MacroporeTortuosity'] =  user_input['tort']
    #inputs['MacroPoreAverageRadius'] =  user_input['rp']
    
    alphaATSB   = inputs['ATSBConcentration']*mwATSB/rhoATSB
    rhomix      = alphaATSB*rhoATSB+(1.0-alphaATSB)*rhoXylene
    ATSBmf      = alphaATSB*rhoATSB/(alphaATSB*rhoATSB + (1.0-alphaATSB)*rhoXylene)
    Xylenemf    = 1.0 - ATSBmf
    sigmaprec   = sigmaATSB*ATSBmf + (1.0-ATSBmf)*sigmaXylene
    Precmfr     = inputs['PreCursorVolumeFlowRate']/1000.0/1000.0/60.0*rhomix
    Precvel     = inputs['PreCursorVolumeFlowRate']/1000.0/1000.0/60.0/(math.pi/4.0*dnozzle**2)
    Dispmfr     = mwO2*atm*(inputs['DispersionVolumeFlowRate']/1000.0/60.)/rgas/Tref/1000.0
    myprec      = math.exp(ATSBmf*math.log(myATSB)+Xylenemf*math.log(myXylene)-11.24*ATSBmf*Xylenemf)
    Dispgapa    = math.pi/4.0*(gap_outer_diameter**2-gap_inner_diameter**2)
    Dispgavel   = inputs['DispersionVolumeFlowRate']/1000.0/60.0/Dispgapa
    Re          = rhomix*(Dispgavel - Precvel)*dnozzle/myprec
    We          = rhomix*(Dispgavel-Precvel)**2*dnozzle/sigmaprec
    Pilotch4mfr = mwMethane*atm*(inputs['PilotMethaneVolumeFlowRate']/1000.0/60.0)/rgas/Tref/1000.0
    PilotO2mfr  = mwO2*atm*(inputs['PilotOxygenVolumeFlowRate']/1000.0/60.0)/rgas/Tref/1000.0
    Dropsmd     = 51.0*dnozzle*Re**(-0.39)*We**(-0.18)*(Precmfr/Dispmfr)**0.29
    Pilotmfr    = Pilotch4mfr + PilotO2mfr
    Pilotch4mf  = Pilotch4mfr/Pilotmfr
    Piloto2mf   = 1.0 - Pilotch4mf
    Fanextrate  = inputs['FanExtractionVolumeFlowRate']*(atm*mwAir/rgas/Tref/1000.0)/3600.0
    
    # originally these were all stored in an 'outputs' dictionary 
    inputs['ATSBMassFraction'] = ATSBmf
    inputs['XyleneMassFraction'] = Xylenemf
    inputs['PreCursorMassFlowRate'] = Precmfr
    inputs['PreCursorVelocity'] = Precvel
    inputs['DispersionMassFlowRate'] = Dispmfr
    inputs['DropletSauterMeanDiameter'] = Dropsmd
    inputs['PilotMassFlowRate'] = Pilotmfr
    inputs['PilotMethaneMassFlowRate'] = Pilotch4mf
    inputs['PilotOxygenMassFlowRate'] = Piloto2mf
    inputs['FanExtractionMassFlowRate'] = Fanextrate
    return inputs

def write_journalfile(inputs, fileout):
    """
    replace the calculated values in the template by mapping the variables in
    the journal template to concepts in the ontology
    """
    out = journal_template.format(ATSBmf=inputs['ATSBMassFraction'], 
                         Xylenemf=inputs['XyleneMassFraction'], 
                         Precmfr=inputs['PreCursorMassFlowRate'], 
                         Precvel=inputs['PreCursorVelocity'], 
                         Dispmfr=inputs['DispersionMassFlowRate'], 
                         Dropsmd=inputs['DropletSauterMeanDiameter'], 
                         Pilotmfr=inputs['PilotMassFlowRate'], 
                         Pilotch4mf=inputs['PilotMethaneMassFlowRate'], 
                         Piloto2mf=inputs['PilotOxygenMassFlowRate'], 
                         Fanextrate=inputs['FanExtractionMassFlowRate'])
    """
    Write the new journal file to disk
    """
    fileout.write(out)
    return



def write_header(inputs, fileout):
    header_template
    """
    replace the calculated values in the template by mapping the variables in
    the journal template to concepts in the ontology
    """
    out = header_template.format(A0=inputs['ActiveSurfaceArea'], 
                         X_pd=inputs['PalladiumMassFraction'], 
                         Ea=inputs['ActivationEnergy'], 
                         por_cat=inputs['CatalystSupportMacroPorosity'], 
                         tort=inputs['MacroporeTortuosity'], 
                         rp=inputs['MacroPoreAverageRadius'], 
                         k0=10000.0) #Not ontologized yet


    """
    Write the new header file to disk
    """
    fileout.write(out)
    return