'''
THIS PROGRAM READS MTU-5C / MTU-8A / RXU-8A METADATA AND TS DATA FROM BINARY FILES
Phoenix Geophysics "PhoenixGeoPy" LIBRARIES ARE USED FOR READING THE METADATA (https://github.com/torresolmx/PhoenixGeoPy.git)
AUTHOR: Dr. Erhan ERDOGAN
'''
# from utils import ImportTsFolder
import gui_tools
from PyQt6.QtWidgets import QApplication
import time
import sys, utils5C

# from SigMT.UtilsSigMT import utils
# from SigMT.Core import bandavg
if __name__ == '__main__':
    
    GUI=QApplication(sys.argv)
    TS_FOLDER=gui_tools.ImportTsFolder()
    path=TS_FOLDER.LoadTsFolder()

    """ 
    -------------------------------------------------------------------------------------------
    - CLASS FOR READING THE METADATA FROM recmeta.json or empower_recmeta.json (if exists)
    - CHECK 'import_recmeta.py' from utils5C

    -------------------------------------------------------------------------------------------
    """
    META=utils5C.ParseMetaData(path)
    # EXAMPLE:
    # GEOGRAPHICAL METADATA - RECEIVER COORDINATES
    LAT=META.RECEIVER_CORD['LAT']
    LON= META.RECEIVER_CORD['LON']
    ALT=META.RECEIVER_CORD['ALT']
    # EXAMPLE:
    # SURVEY METADATA - SURVEY INFORMATION
    print('CREW=', META.SURVEY_INFO['OPERATORS'])
    print('COMPANY=',META.SURVEY_INFO['COMPANY'])
    print('SITE NAME=',META.SURVEY_INFO['SITE'])
    # CHECK 'import_recmeta-GetSurveyInfo' FOR OTHER METADATA INFORMATION

    # EXAMPLE:
    # CHANNEL INFORMATION SUCH AS DIPOLE LENGTHS AND SENSOR SERIAL NUMBERS, GAINS ETC
    CHANNELS=META.Channels()
    print(CHANNELS['E_CH']['DIPOLE_LENGTH'])    
    print(CHANNELS['H_CH']['SENSOR_SERIAL'])    
    # CHECK 'import_recmeta-Channels' FOR OTHER METADATA INFORMATION
    
    TS=utils5C.ReadTs(path)
    
    """ 
    -------------------------------------------------------------------------------------------
    - CLASS FOR PARSING TIME SERIES FROM BINARY FILES
    - CHECK 'read_ts.py' from utils5C
    - THIS CLASS CURRENTLY WORKS ONLY FOR td_150 DECIMATED CONTINUOUS FILES
    - OTHER SAMPLING OPTIONS WILL BE IMPEMENTED IN THE FUTURE
    - CLASS RETURNS TS DATA AND GENERIC CAIBRATIONS - SENSOR TYPE IS READ FROM RECMETA AND GENERIC CAL IS SELECTED AUTOMATICALLY
    -------------------------------------------------------------------------------------------
    """
    file_type='td_150'
    TS_td_150,SENSOR_CALIBRATION=TS.ImportTsData(file_type)
    
    # EXAMPLE:
    # ACCESS ex (E1) TS DATA AS FOLLOWS
    print(TS_td_150['H1'])
    # EXAMPLE:
    # ACCESS GENERIC CAL 
    print(SENSOR_CALIBRATION['H1'])
