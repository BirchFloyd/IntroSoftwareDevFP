import tkinter as tk
from tkinter import filedialog
import csv

def main():
    root = tk.Tk()
    root.title("CSV Viewer")
    initGUI(root)
    root.mainloop()

def initGUI(root):
    global csvHeader, csvRows
    openButton = tk.Button(root, text="Open CSV", command=openCSV)
    csvHeader = []
    csvRows = []

def openCSV():
    file = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    try:
        with open(file, newline='') as csvfile:
            readFile = csv.reader(csvfile)
    except:
        print("Error opening csv")

def buildCheckboxes(header, rows):
    global csvHeader, csvRows
    csvHeader = header
    csvRows = rows

if __name__ == "__main__":
    main()
