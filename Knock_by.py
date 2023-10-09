import sys
from bin.main import MainUtilMenu

if __name__ == "__main__":
    if "--debug" in sys.argv:
        MainUtilMenu().run()
    else:
        try:  
            MainUtilMenu().run()
        except Exception as e:
            print("You catch Fatal error!")