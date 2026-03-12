from PhoenixGeoPy.Reader.TimeSeries import DecimatedContinuousReader
import os, glob, utils5C
from pathlib import Path
import json

import matplotlib.pyplot as plt
import h5py
import xarray as xr
import utils5C
import time
class ReadTs():
    def __init__(self,TS_FOLDER):
       
        self.path=TS_FOLDER
        META=utils5C.ParseMetaData(self.path)
        CH_DATA=META.Channels()
        self.ch_index=CH_DATA['CH_INDEX']
        self.channels=CH_DATA['CHANNELS']
        self.Sensor_Type=CH_DATA['H_CH']['SENSOR_TYPE']
        self.ImportGenericCalibration()
        self.ListFiles()
        
        
        
        # self.FileType='td_150'
    
    def ListFiles(self):
        
        
        # GET FILE TYPES
        self.FILE_TYPE=set()
        
        for fname in os.listdir(self.path+"/"+str(self.ch_index[self.channels[0]])):
            if "." in fname:
                extension=fname.split(".")[-1]
                self.FILE_TYPE.add(extension)
        
        # GET FLIST (SORTED BY HEX)
        self.FILE_LIST={}
        for i in range(0,len(self.channels)):
            INDEX=[]
            flist=[]
            ch_path=(self.path+"/"+str(self.ch_index[self.channels[i]]))
            os.chdir(ch_path)
            for file in glob.glob('*.td_150'):                
                inhex=str(file[17:25])
                INDEX.append(int(inhex,32))
                flist.append(Path(file).stem)
            AA=zip(INDEX,flist)
            BB=sorted(AA)        
            CC=[x for _,x in BB ]
            self.FILE_LIST[self.channels[i]]=CC
            
        return(self.FILE_TYPE)
        
    def ImportTsData(self,FileType):
        TS_DATA = {}

        for ch_idx in range(len(self.channels)):
            ch_name = self.channels[ch_idx]
            ch_path = self.path + "/" + str(self.ch_index[ch_name]) + "/"

            data = []

            for file in self.FILE_LIST[ch_name]:
                parsed_data = DecimatedContinuousReader(ch_path + file + "." + FileType)
                sample_rate = parsed_data.header_info["sample_rate"]
                frag = parsed_data.header_info["frag_period"]

                # print(f"Reading file: {file}")

                for frag_idx in range(frag):
                    try:
                        chunk = parsed_data.read_data(sample_rate)
                    except ValueError:
                # file already closed / EOF reached unexpectedly
                        break

                    if chunk is None:
                        break

                    if len(chunk) == 0:
                        break

                    data.extend(chunk)

            # if the last read is shorter than sample_rate, it means EOF
                    if len(chunk) < sample_rate:
                        break

            TS_DATA[ch_name] = xr.DataArray(data)
           
        return(TS_DATA,self.Cal_Data)
    
    def ImportGenericCalibration(self):
        self.Cal_Data={}
        GENERIC_185U = Path(__file__).parent / "calibrationfiles/MTC_185U.json"
        GENERIC_155 = Path(__file__).parent / "calibrationfiles/MTC_155.json"
        GENERIC_5C = Path(__file__).parent / "calibrationfiles/MTU_5C.json"
        GENERIC_8A = Path(__file__).parent / "calibrationfiles/MTC_185U.json"
        
        ### GENERIC SENSOR CALIBRATIONS ###
        
        ### MTC-185 ULTRA
        with open(GENERIC_185U) as cal_file:
            MTC185U=json.load(cal_file)        
        
        CAL_MTC185U={}
        CAL_DATA=MTC185U['cal_data']
        DATA=CAL_DATA[0]['chan_data']
        CAL_MTC185U['FREQUENCY']=DATA[0]['freq_Hz']
        CAL_MTC185U['MAGNITUDE']=DATA[0]['magnitude']
        CAL_MTC185U['PHASE']=DATA[0]['phs_deg']

        ### MTC-185 ULTRA
        with open(GENERIC_155) as cal_file:
            MTC155=json.load(cal_file)        
        
        CAL_MTC155={}

        CAL_DATA=MTC155['cal_data']
        DATA=CAL_DATA[0]['chan_data']
        CAL_MTC155['FREQUENCY']=DATA[0]['freq_Hz']
        CAL_MTC155['MAGNITUDE']=DATA[0]['magnitude']
        CAL_MTC155['PHASE']=DATA[0]['phs_deg']
        
        # print(self.Sensor_Type.keys())
        
        for key in self.Sensor_Type.keys():
            if self.Sensor_Type[key]=='MTC-185':
                self.Cal_Data[key]=CAL_MTC185U
            if key=='MTC-155':
               self.Cal_Data[key]=CAL_MTC155
        
        
        
        
        #         print("Sensor=MTC-155")
        # plt.subplot(211)
        # plt.semilogx(CAL_MTC185U['FREQUENCY'], CAL_MTC185U['MAGNITUDE'], 'ro')
        # plt.ylabel("Amplitude (mV/nT)",fontweight="bold",fontsize=12) 
        # plt.xlabel("Frequency (Hz)",fontweight="bold",fontsize=12)
        # plt.gca().invert_xaxis()  
        # plt.grid(True,which='both')   
        # plt.subplot(212)
        # plt.semilogx(CAL_MTC185U['FREQUENCY'], CAL_MTC185U['PHASE'], 'ro')
        # plt.ylabel("Phase (Degree)",fontweight="bold",fontsize=12) 
        # plt.xlabel("Frequency (Hz)",fontweight="bold",fontsize=12)
        # plt.gca().invert_xaxis()  
        # plt.grid(True,which='both')   
        # plt.show()
        
        ## GENERIC RECEIVER CALIBRATIONS ###
        ## MTU-5C GENERIC CAL
        with open(GENERIC_5C) as cal_file:
            MTU5C=json.load(cal_file)
        
        CAL_MTU5C={}
        NUM_CH=MTU5C['num_channels']
        
        CAL_DATA=MTU5C['cal_data']
        for i in range(0,NUM_CH):
            TAG=CAL_DATA[i]['tag']
            NUM_RESP=CAL_DATA[i]['num_of_responses']
            CHAN_DATA=CAL_DATA[i]['chan_data']
            CAL_MTU5C[TAG]={}
            F=[]
            M=[]
            P=[]
            for j in range(0,NUM_RESP):
                F.append(CHAN_DATA[j]['freq_Hz'])
                M.append(CHAN_DATA[j]['magnitude'])
                P.append(CHAN_DATA[j]['phs_deg'])
            CAL_MTU5C[TAG]['FREQUENCY']=F
            CAL_MTU5C[TAG]['MAGNITUDE']=M
            CAL_MTU5C[TAG]['PHASE']=P
            
        
        
        # return(sensor_cal)
        # CH='H3'
        # for i in range(0,4):
        #     plt.subplot(211)
        #     plt.semilogx(CAL_MTU5C[CH]['FREQUENCY'][i], CAL_MTU5C[CH]['MAGNITUDE'][i], 'ro')
            
        #     if i==0:
        #         plt.gca().invert_xaxis()  
        #         plt.grid(True,which='both')   
        #         plt.ylabel("Amplitude-Normalized to 1",fontweight="bold",fontsize=12) 
        #         plt.xlabel("Frequency (Hz)",fontweight="bold",fontsize=12)
        #     plt.subplot(212)
        #     plt.semilogx(CAL_MTU5C[CH]['FREQUENCY'][i], CAL_MTU5C[CH]['PHASE'][i], 'ro')
            
        #     if i==0:
        #         plt.gca().invert_xaxis()  
        #         plt.grid(True,which='both')   
        #         plt.ylabel("Phase (Degree)",fontweight="bold",fontsize=12) 
        #         plt.xlabel("Frequency (Hz)",fontweight="bold",fontsize=12)
        # plt.show()