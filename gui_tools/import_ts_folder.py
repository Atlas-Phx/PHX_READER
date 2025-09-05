import os
from PyQt6.QtWidgets import QFileDialog

class ImportTsFolder:
    def __init__(self):
        self.LoadTsFolder
        
    def LoadTsFolder(self):
        HOME_PATH=os.getenv("HOME")
        TS_DIR=QFileDialog.getExistingDirectory(caption="Select directory",directory=HOME_PATH,options=QFileDialog.Option.ShowDirsOnly,)
        return(TS_DIR)
