from pathlib import Path
from mth5.clients import MakeMTH5
from mth5 import mth5
from mt_metadata import timeseries as metadata
class ConvertMTH5():
    def __init__(self,TS_FOLDER):
        self.path=TS_FOLDER

    # def Get_MTH5(self):
        # station_dir = Path(self.path)
        # survey=metadata.Survey()
        # survey.acquired_by.author = "ERHAN"
        # survey.fdsn.id= "Site-1"
        # survey.fdsn.network = "MT"
        # survey.name = "TEST"
        # m=mth5.MTH5(Path(r"/Users/ee/10766_2024-08-22-163027/from_phoenix.h5"))
        # m.channel_summary.clear_table()
        # m.channel_summary.summarize()

        # ch_df = m.channel_summary.to_dataframe()
        # ch_df
        
        # h5_reference = ch_df.iloc[0].hdf5_reference
        # ex = m.from_reference(h5_reference)
        # ex  
        # m.survey_group.metada.from_dict(survey.to_dict)
        # station_dir=Path(r"/Users/ee/10766_2024-08-22-163027")
        # station_dir = Path(r"D:\PROCESSING\Peru_Marcobre\10781_2024-07-31-193316")
        # receiver_calibration=Path(__file__).parent / r"calibrations/"
        # sensor_calibration=Path(__file__).parent / r"calibrations/"
        # print(sensor_calibration)
        # print(receiver_calibration)
        # print(station_dir)
        # phx_mth5_path = MakeMTH5.from_phoenix(station_dir,mth5_filename="from_phoenix.h5",sample_rates=[150, 24000],receiver_calibration_dict=receiver_calibration,
        #                                       sensor_calibration_dict=sensor_calibration)
        # phx_mth5_path = MakeMTH5.from_phoenix(station_dir,mth5_filename="from_phoenix.h5",sample_rates=[150, 24000],receiver_calibration_dict=Path(r"/Users/ee/Documents/EE_REPO/EM_TOOLS/utils5C/calibrations"),sensor_calibration_dict=Path(r"/Users/ee/Documents/EE_REPO/EM_TOOLS/utils5C/calibrations"),survey_group="MT")
        # phx_mth5_path = MakeMTH5.from_phoenix(station_dir,mth5_filename="from_phoenix.h5",sample_rates=[150, 24000],receiver_calibration_dict=receiver_calibration,sensor_calibration_dict=sensor_calibration)
        # from mth5.mth5 import MTH5
        # # with MTH5() as mth5_object:mth5_object.open_mth5(r"D:\PROCESSING\Peru_Marcobre\10781_2024-07-31-193316\from_phoenix_remote.h5", "a")
        # # print(MTH5.c)
        # with MTH5() as m:
        #     m.open_mth5(r"D:\PROCESSING\Peru_Marcobre\10781_2024-07-31-193316\from_phoenix_remote.h5", "w")
        # ch_df = m.channel_summary.to_dataframe()
        # h5_reference = ch_df.iloc[0].hdf5_reference
        # ex= m.from_reference(h5_reference)
        # ex
        # m.channel_summary.summarize()
        # ch_df=m.channel_summary.to_dataframe()
        # ch_df