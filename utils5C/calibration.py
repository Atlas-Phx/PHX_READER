import numpy as np

class ApplyCalibration:
    def __init__(self,xfft,fft_freqs,calibration_data):
        self.calibrated_data = None
        self.calibration_data = calibration_data
        self.xfft = xfft
        self.fft_freqs = fft_freqs
    def Calibrate_Mag(self):
        
        magnitude=[]
        phase=[]
        calt=[]
        # FIX THIS PART !!!! CALIBRATION IS WRONG!!!!
        # magnitude = self.calibration_data['FREQUENCY'] * self.calibration_data['MAGNITUDE']
        for i in range(0,len(self.calibration_data['FREQUENCY'])):
            scale_factor=1.0 / 1000 + 0.0j
            # magnitude.append(self.calibration_data['FREQUENCY'][i] * self.calibration_data['MAGNITUDE'][i] )
            # phase.append(np.radians(self.calibration_data['PHASE'][i]))\
            magnitude.append(self.calibration_data['MAGNITUDE'][i] )
            phase.append(np.radians(self.calibration_data['PHASE'][i]))
            # calt.append((magnitude[i] * np.cos(phase[i]) + (1j * magnitude[i] * np.sin(phase[i]))) / 1000)
            calt.append(scale_factor*(magnitude[i] * (np.cos(phase[i]) + 1j * np.sin(phase[i]))))
        
        cal_all_band=np.interp(self.fft_freqs,self.calibration_data['FREQUENCY'],calt)
        self.calibrated_data = self.xfft / cal_all_band[:, np.newaxis]
        return(self.calibrated_data)

