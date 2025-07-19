import os.path
import pandas as pd
from dss import dss
import datetime
import matplotlib.pyplot as plt
import numpy as np

def runDSS(controlmode, monitorMode=2):
    _csvPreFix = '11018_PV_CEA'
    np.random.seed(0)
    durationMins = 24 * 60
    obserBus = 'cea'
    extraTitle = f'Voltage of load at bus "{obserBus}"'
    # make sure that PV load does not have long flat 0 values, at least 1E-6 trivial value
    pvflucsource = os.path.join('b_profiles','LoadshapePV2_PU_minutely.csv')
    plotx = []
    ploty = []
    '''
    baseline_out = './2_Voltage/b_profiles/May9_cea_baseline.csv'
    smoothing_out = './2_Voltage/b_profiles/May9_cea_smoothing.csv'
    '''
    dss.Text.Command = 'redirect "./a_dss/IEEE123Master.dss"'
    dss.Text.Command = 'New "LoadShape.bldNormal" npts=1440 sinterval=60.0 ' \
                       'mult=(File=./b_profiles/SolarTAC_May9_cea_baseline.csv) '
    dss.Text.Command = 'New "LoadShape.bldSmoothing" npts=1440 sinterval=60.0 ' \
                       'mult=(File=./b_profiles/SolarTAC_May9_cea_smoothing.csv) '

    dss.Text.Command = 'New "LoadShape.PVLoadShape2" npts=1440 sinterval=60.0 ' \
                       'mult=(File=./b_profiles/SolarTAC_LoadshapePV2_PU_minutely.csv) Action=Normalize'
    dss.Text.Command = 'New XYCurve.MyPvsT npts=4  xarray=[0  25  75  100]  yarray=[1.2 1.0 0.8  0.6] '
    dss.Text.Command = 'New XYCurve.MyEff npts=4  xarray=[.1  .2  .4  1.0]  yarray=[.86  .9  .93  .97] '
    dss.Text.Command = 'New Tshape.MyTemp npts=24 interval=1 ' \
                       'temp=[25, 25, 25, 25, 25, 25, 25, 25, 35, 40, 45, 50  60 60  55 40  35  30  25 25 25 25 25 25]'

    dss.Text.Command = 'New PVSystem.PVSystem1745kW phases=3 bus1=nodePV kV=0.48 debugtrace=yes  ' \
                       'kVA=1745  irrad=1.0  Pmpp=1745 temperature=25 PF=1 ' \
                       ' %cutin=0.1 %cutout=0.1  effcurve=Myeff  P-TCurve=MyPvsT Daily=PVLoadShape2  TDaily=MyTemp'
    dss.Text.Command = 'New Transformer.transPV  phases=3 xhl=5.750000  ' \
                       'wdg=1 bus=nodePV kV=0.48 kVA=3000.000000 conn=wye' \
                        ' wdg=2 bus=300 kV=4.16 kVA=3000.000000 conn=wye'

    'Base voltage for load. For 2- or 3-phase loads, specified in phase-to-phase kV. ' \
    'For all other loads, the actual kV across the load branch. ' \
    'If wye (star) connected, then specify phase-to-neutral (L-N). ' \
    'If delta or phase-to-phase connected, specify the phase-to-phase (L-L) kV.'

    if controlmode == 0:
        extraTitle += '+ PV fluctuation, + baseline building load'
        dss.Text.Command = 'New Load.cea Bus1=47 phases=3 conn=wye Model=5 kV=4.16 kW=105 kvar=75 daily=bldNormal'
        # dss.Text.Command = 'New Load.cea2 Bus1=48 phases=3 conn=wye Model=2 kV=4.16 kW=210 kvar=150 daily=bldNormal'
        _operation = 'CEABaseline'
    if controlmode == 1:
        extraTitle += '+ PV fluctuation, + smoothing building load'
        dss.Text.Command = 'New Load.cea Bus1=47 phases=3 conn=wye Model=5 kV=4.16 kW=105 kvar=75 daily=bldSmoothing'
        # dss.Text.Command = 'New Load.cea2 Bus1=48 phases=3 conn=wye Model=2 kV=4.16 kW=210 kvar=150 daily=bldSmoothing'
        _operation = 'CEASmoothing'

    if monitorMode == 2:
        dss.Text.Command = 'New monitor.substationtaps3a element=Transformer.reg3a terminal=2 mode=2 ppolar=no'
        _colName = 'Tap (pu)'
        _CSV = _csvPreFix+'_TapOperations.csv'
    if monitorMode == 0:
        #mode=0,monitoring voltage profile
        dss.Text.Command = 'New monitor.substationtaps3a element=Transformer.reg3a terminal=2 mode=0 ppolar=no'
        _colName = 'V1'
        _CSV = _csvPreFix + '_VoltageProfile.csv'
    dss.Text.Command = 'set mode=daily stepsize=60s number=1'
    # dss.Text.Command = 'set controlmode=time'
    '1) Yes, 24 solutions are done and time advances. ' \
    'In Daily mode, you will probably want to use Static control mode most of the time. ' \
    '"Time" control mode is for short time steps of a few seconds or less. ' \
    'If you assign the Daily= property of a Load to a Loadshape, it will automatically vary.'

    solution = dss.ActiveCircuit.Solution
    circ = dss.ActiveCircuit

    NUM_STEPS = durationMins

    # Active the target load
    circ.Loads.Name = obserBus
    new_kVA = original_kVA = circ.Loads.kva
    print('original_kVA is', original_kVA)

    for step in range(NUM_STEPS):
        solution.Solve() # will solve

        circ.Loads.Name = obserBus # this activates the load
        # When you activate the Load, it is activated as the active element too
        # (that is, you can only inspect one element at a time; if you activate a line or transformer,
        # for example, active element will change to that).

        # Print the effective power for load 645
        eff_kVA = abs(complex(*circ.ActiveElement.TotalPowers))
        load_volts = circ.ActiveElement.VoltagesMagAng[::2][0]
        baseKV = circ.ActiveBus.kVBase
        load_volts = load_volts / (baseKV * 1000)  # convert to kV

        tmptime = datetime.timedelta(hours=solution.dblHour)
        print(f'Time= {tmptime}, '
              f'eff. power: {eff_kVA} kVA, spec. power: {new_kVA}, load voltage: {load_volts} V')
        #save time (with precision of hh:mm:ss) and voltage
        hhmmss = tmptime.total_seconds()
        plotx.append(datetime.datetime.utcfromtimestamp(hhmmss))
        ploty.append(load_volts)
        # Decide how to adjust the load by some external process...
        circ.Loads.Name = obserBus # you may need to reactivate the load


    # #Export monitors substationtaps3a
    # dss.Text.Command = 'export monitor substationtaps3a'
    # # #read saved data, ieee123_Mon_substationtaps3a_1.csv, skip the first row
    # df = pd.read_csv("ieee123_Mon_substationtaps3a_1.csv")
    # slecCol = df[_colName]

    # Export monitors substationtaps3a
    if monitorMode == 2:
        dss.Text.Command = 'export monitor substationtaps3a'
        df = pd.read_csv("ieee123_Mon_substationtaps3a_1.csv")
        slecCol = df[_colName]
    if monitorMode == 0:
        slecCol = ploty

    _savedPath = os.path.join('c_postprocess',_CSV)
    # #if _savedPath exists, read it, else create it
    if not os.path.exists(_savedPath):
        _savedCsv = pd.DataFrame(columns=[f'{_colName} CEABaseline',f'{_colName} CEASmoothing'])
        _savedCsv.to_csv(_savedPath, index=False)
    #
    _savedCsv = pd.read_csv(_savedPath)


    _savedCsv[f'{_colName} {_operation}'] = slecCol
    _savedCsv.to_csv(_savedPath, index=False)

    fig, ax1 = plt.subplots()
    data = pd.read_csv(pvflucsource, header=None)
    csv_plotx = range(len(data))
    csv_ploty = data.iloc[:, 0]
    ax1.plot(plotx, ploty, label=f'Voltage of load {obserBus}', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage (V)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(plotx, csv_ploty[:len(plotx)], label='PV Loadshape', color='red')
    ax2.set_ylabel('CSV Data', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add title and legend
    plt.title(extraTitle)
    fig.tight_layout()
    plt.legend()
    plt.show()

monitor_mode = 2
# monitor_mode = 0  # Set to 0 for voltage profile, 2 for tap operations
runDSS(0, monitor_mode)
runDSS(1, monitor_mode)