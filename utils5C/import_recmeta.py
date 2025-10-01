import json, os

class ParseMetaData:
    def __init__(self,path):
        if os.path.exists(path+"/empower_recmeta.json"):
            self.json_path=(path+"/empower_recmeta.json")
        else:
            self.json_path=(path+"/recmeta.json")
        with open(self.json_path) as f:
            self.metadata = json.load(f)
        self.GetSurveyInfo()
        self.GetCoordinates()
        self.Channels()
    def GetCoordinates(self):
        self.RECEIVER_CORD={}
        self.RECEIVER_CORD['LAT']=self.metadata['timing']['gps_lat']
        self.RECEIVER_CORD['LON']=self.metadata['timing']['gps_lon']
        self.RECEIVER_CORD['ALT']=self.metadata['timing']['gps_alt']
        
        return(self.RECEIVER_CORD)
    def GetSurveyInfo(self):
        self.SURVEY_INFO={}
        self.SURVEY_INFO['OPERATORS']=self.metadata['layout']['Operator']
        self.SURVEY_INFO['COMPANY']=self.metadata['layout']['Company_Name']
        self.SURVEY_INFO['PROJECT']=self.metadata['layout']['Survey_Name']
        self.SURVEY_INFO['SITE']=self.metadata['layout']['Station_Name']
        self.SURVEY_INFO['Rec_Start']=self.metadata['start']
        self.SURVEY_INFO['Rec_Stop']=self.metadata['stop']
        # self.SURVEY_INFO['TIMEZONE']=self.metadata['layout']['timezone']           # ONLY IN empower_recmeta.json
        return(self.SURVEY_INFO)
    def Channels(self):
        Active_Channels=len(self.metadata['chconfig']['chans'])
        All_Channels=self.metadata['chconfig']['chans']
        MAP=self.metadata['channel_map']['mapping']
        self.MAG_TYPE={}                                             # MAG_TYPE['H1']...['H6'] -> RETURNS DETECTED SENSOR TYPE MTC-155/MTC-185
        self.MAG_SERIAL={}                                           # self.MAG_SERIAL['H1']...['H6'] -> RETURNS DETECTED SENSOR SERIAL NUMBER ! IMPORTANT IF THE FIELD CALIBRATIONS APPLIED
        self.MAG_GAIN={}                                             # self.MAG_SERIAL['H1']...['H6'] -> RETURNS (PREAMP x GAIN AND POSTAMP GAIN) (PREAMP GAIN IS 1 FOR MAG)    
        self.E_DIPOLE={}                                             # self.E_DIPOLE['E1']['E2'] -> RETURNS TOTAL DIPOLE LENGTH FOR E1/E2
        self.E_GAIN={}                                               # self.E_GAIN['E1']['E2'] -> RETURNS (PREAMP x GAIN AND POSTAMP GAIN) (PREAMP GAIN IS 8 FOR E)    
        self.CH_INDEX={}                                             # self.CH_INDEX['E1']...['E2']['H1']...['H6'] DEPENDING ON RECEIVER TYPE AND ACTIVE CHANNELS THIS INDEX SHOWS TS FOLDER FOR EACH CHANNEL
        self.CHANNELS=[]
        
        for i in range(0,Active_Channels):
            if All_Channels[i]['on']==1 and All_Channels[i]['ty']=="M":
                self.MAG_TYPE[All_Channels[i]['tag']]=All_Channels[i]['type_name']
                self.MAG_SERIAL[All_Channels[i]['tag']]=All_Channels[i]['serial']
                self.MAG_GAIN[All_Channels[i]['tag']]=All_Channels[i]['ga']*All_Channels[i]['pg']
                self.CHANNELS.append(All_Channels[i]['tag'])
                self.CH_INDEX[MAP[i]['tag']]=MAP[i]['idx']
            if All_Channels[i]['on']==1 and All_Channels[i]['ty']=="E":
                self.E_DIPOLE[All_Channels[i]['tag']]={}
                self.E_DIPOLE[All_Channels[i]['tag']]['length1']=All_Channels[i]['length1']
                self.E_DIPOLE[All_Channels[i]['tag']]['length2']=All_Channels[i]['length2']
                self.E_GAIN[All_Channels[i]['tag']]=All_Channels[i]['ga']*All_Channels[i]['pg']
                self.CHANNELS.append(All_Channels[i]['tag'])
                self.CH_INDEX[MAP[i]['tag']]=MAP[i]['idx']    
        CH_DATA={}
        CH_DATA['H_CH']={}
        CH_DATA['E_CH']={}
        CH_DATA['E_CH']['DIPOLE_LENGTH']=self.E_DIPOLE
        CH_DATA['E_CH']['E_GAIN']=self.E_GAIN
        
        CH_DATA['H_CH']['SENSOR_TYPE']=self.MAG_TYPE
        CH_DATA['H_CH']['SENSOR_SERIAL']=self.MAG_SERIAL
        CH_DATA['H_CH']['MAG_GAIN']=self.MAG_GAIN
        CH_DATA['CH_INDEX']=self.CH_INDEX
        CH_DATA['CHANNELS']=self.CHANNELS
        
        return(CH_DATA)
    
   