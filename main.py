from gui import gui
from data import run_sentiment
import ttkbootstrap as ttkb
import pandas as pd

def main():
    # get the data
    results = run_sentiment()
    df = pd.DataFrame(results)

    # setup the gui
    root = ttkb.Window()
    app = gui(root, df)
    root.mainloop()

if __name__ == "__main__":
    main()