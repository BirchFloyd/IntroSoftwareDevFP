'''
Author:  Birch Floyd
Date written: 3/9/2025
Assignment: Final Project - CSV Viewer
Short Desc: Tkinter app to open a CSV file, opens in multiple windows and has images to show what app you're using.
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk  
import csv

#Global variables
mainWin = None #Main window where everything starts
status = None #Label to show messages
dataTable = None #Table widget for CSV data
csvContent = [] #List to hold all the CSV rows

#Filter variables
filterCol = None #Dropdown menu choice for which column to filter
filterVal = None #Text box where user types what they want filtered
cols = {} #Dictionary to track whick columns are checked

def main():
    #Set up main window
    global mainWin
    mainWin = tk.Tk()
    mainWin.title("CSV Viewer")
    initMainWin()
    mainWin.mainloop()
    '''
    Main function to set up the main window and start the program
    
    Args:
    mainWin (Tk): Main Tkinter window object
    '''

def initMainWin():
    global status
    #Create the frame
    frame = tk.Frame(mainWin)
    frame.pack(padx=10, pady=10)
    
    #Add title and image as well as text to help user
    title = tk.Label(frame, text="Welcome to the", font=("Arial", 16))
    title.pack(pady=5)
    try:
        img = tk.PhotoImage(file="image1.png")
        lblImg = tk.Label(frame, image=img)
        lblImg.image = img #keep the image omg plz
        lblImg.pack(pady=5)
    except:
        lblImg = tk.Label(frame, text="Floyd's CSV Viewer Image could not load")
        lblImg.pack(pady=5)
    instr = tk.Label(frame, text="Click 'Open CSV' to load a file.", font=("Arial", 12))
    instr.pack(pady=5)
    
    #Set up buttons and status- status mostly unused now (I was using it for errors) but it was breaking and when i tried to remove it things formatted weirdly... and it looks professional so I'm leaving it.
    btns = tk.Frame(frame)
    btns.pack(pady=10)
    btnOpen = tk.Button(btns, text="Open CSV", command=openCSV)
    btnOpen.pack(side="left", padx=5)
    btnExit = tk.Button(btns, text="Exit", command=exitProg)
    btnExit.pack(side="left", padx=5)
    status = tk.Label(frame, text="Ready", font=("Arial", 10))
    status.pack(pady=5)
    '''
    Sets up the main window with title, image, and buttons
    
    Args:
    status (Label): Label for displaying messages
    frame (Frame): Container for main window widgets
    '''

def openCSV():
    global csvContent
    #Pick and load the CSV file
    fileName = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if not fileName:
        print("No file picked")
        return
    try:
        f = open(fileName, newline='')
        reader = csv.reader(f)
        csvContent = list(reader)
        f.close()
    except:
        print("Cant open file")
        return
    
    #Check if there’s data if so, open viewer
    if not csvContent:
        print("Empty CSV")
        return
    buildCSVWin()
    '''
    Opens a CSV file and stores its data for display
    
    Args:
    csvContent (list): List holding CSV rows
    fileName (str): Path to the selected CSV file
    '''

def buildCSVWin():
    global dataTable, filterCol, filterVal, cols
    #Split CSV into header and rows
    header = csvContent[0]
    rows = csvContent[1:]
    
    #Create new window
    csvWin = tk.Toplevel(mainWin)
    csvWin.title("CSV Data Viewer")
    
    #Add second image
    try:
        imgCSV = tk.PhotoImage(file="image2.png")
        lblImgCSV = tk.Label(csvWin, image=imgCSV)
        lblImgCSV.image = imgCSV #We be keeping images here (plz plz plz its 4am)
        lblImgCSV.pack(pady=5)
    except:
        lblImgCSV = tk.Label(csvWin, text="Now Viewing CSV Image could not load")
        lblImgCSV.pack(pady=5)
    
    #Filter controls
    filtFrame = tk.Frame(csvWin)
    filtFrame.pack(padx=10, pady=5, fill="x")
    tk.Label(filtFrame, text="Filter Column:").pack(side="left")
    filterCol = tk.StringVar(csvWin)
    filterCol.set(header[0])
    tk.OptionMenu(filtFrame, filterCol, *header).pack(side="left", padx=5)
    tk.Label(filtFrame, text="Filter Value:").pack(side="left")
    filterVal = tk.Entry(filtFrame)
    filterVal.pack(side="left", padx=5)
    btnApply = tk.Button(filtFrame, text="Apply Filter", command=updateTable)
    btnApply.pack(side="left", padx=5)
    
    #Checkboxes for columns
    chkFrame = tk.Frame(csvWin)
    chkFrame.pack(padx=10, pady=5, fill="x")
    cols.clear()
    for col in header:
        var = tk.BooleanVar(value=True)
        cols[col] = var
        tk.Checkbutton(chkFrame, text=col, variable=var).pack(side="left", padx=2)
    
    #Set up table and scrollbar
    tblFrame = tk.Frame(csvWin)
    tblFrame.pack(padx=10, pady=5, fill="both", expand=True)
    dataTable = ttk.Treeview(tblFrame, show="headings")
    dataTable.pack(side="left", fill="both", expand=True)
    scrlBar = ttk.Scrollbar(tblFrame, orient="vertical", command=dataTable.yview)
    scrlBar.pack(side="right", fill="y")
    dataTable.configure(yscrollcommand=scrlBar.set)
    
    #Adds close button then shows data
    btnClose = tk.Button(csvWin, text="Close Window", command=csvWin.destroy)
    btnClose.pack(pady=5)
    updateTable()
    '''
    Creates a new window to display CSV data with filters and table
    
    Args:
    dataTable (Treeview): Table widget for CSV data
    filterCol (StringVar): Variable for filter column selection
    filterVal (Entry): Entry widget for filter value
    cols (dict): Dictionary of column checkboxes
    '''

def updateTable():
    global dataTable, filterCol, filterVal
    #Get CSV parts
    header = csvContent[0]
    rows = csvContent[1:]
    
    #Shows columns
    selIndices = []
    index = 0
    for col in header:
        if cols[col].get() == True:
            selIndices.append(index)
        index += 1
    selCols = []
    for i in selIndices:
        selCols.append(header[i])
    
    #Clears table and resets it up
    for item in dataTable.get_children():
        dataTable.delete(item)
    dataTable["columns"] = selCols
    for col in selCols:
        dataTable.heading(col, text=col)
        dataTable.column(col, width=100)
    
    #Gets filter settings then add rows to the table
    filtCol = filterCol.get()
    filtVal = filterVal.get().strip()
    try:
        filtIndex = header.index(filtCol)
    except:
        print("Filter column not found")
        filtIndex = None
    print("updatedTable() before loop")
    for row in rows:
        if filtVal and filtIndex is not None: #Skip if filter don't match
            if row[filtIndex] != filtVal:
                continue
        rowOut = []
        for i in selIndices:
            rowOut.append(row[i])
        dataTable.insert("", tk.END, values=rowOut)
        print("Row Added")
    
    print("Table Updated With", len(dataTable.get_children()), "Rows")
    '''
    Updates the table with filtered CSV data based on user selections
    
    Args:
    dataTable (Treeview): Table widget for CSV data
    filterCol (StringVar): Variable for filter column selection
    filterVal (Entry): Entry widget for filter value
    '''

def exitProg():
    if tk.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        mainWin.destroy()
    '''
    Closes the program after user confirmation
    
    Args:
    mainWin (Tk): Main Tkinter window object
    '''

if __name__ == "__main__":
    main()