from .colors import Colors
from datetime import datetime
import os

class Logger:
    """A simple logger for console output"""

    class Level:
        INFO = "INFO"
        ERROR = "ERROR"
        FPS = "FPS"
        MANUAL = "MANUAL"

    def __init__(self, file=None):
        self.colors = Colors()
        self.file = file
        self.clear_console()

    def log(self, level, msg):
        dt_string = self.get_time()
        formatted_msg = f"{self.colors.DATE}[{dt_string}]{getattr(self.colors, level)}[{level}]:{self.colors.END} {msg}"

        print(formatted_msg)
        if self.file is not None:
            with open(self.file, "a") as f:
                f.write(formatted_msg + "\n")

    def info(self, msg):
        """Prints an info message to the console"""
        self.log(self.Level.INFO, msg)

    def error(self, msg):
        """Prints an error message to the console"""
        self.log(self.Level.ERROR, msg)

    def fps(self, fps):
        """Prints the FPS value to the console"""
        self.log(self.Level.FPS, fps)
    
    def manual(self):
        """Prints the manual to the console"""
        msg =  """
        Press F1 to enable/disable the cheat.
        Press F2 to enable/disable the rendering mode.
        Press F12 to exit the program.
        
        Cheat is enabled by default.
        Rendering mode is disabled by default.
        """
        self.log(self.Level.MANUAL, msg)

    def clear_console(self):
        """Clears the console"""
        os.system('cls' if os.name=='nt' else 'clear')
            
    @staticmethod
    def get_time():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
