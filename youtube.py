# Importing Necessary dependencies
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import ssl
from threading import Thread

"""
Imports Explained

tkinter -> Helps us with GUI
pytube -> Fetching media from Youtube
ssl -> Handles ssl certificate errors that may occur
threading -> helps speed up the program

"""

# This fixes the certificate error while downloading
ssl._create_default_https_context = ssl._create_unverified_context

# our folder name -> make it global since it would be accessed by different functions in the app
Folder_Name = ""


# file location function
def open_location():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if len(Folder_Name) > 1:
        LocationError.config(text=Folder_Name, fg="green")
    else:
        LocationError.config(text="Please Choose Folder!", fg="red")


# download Video function
def download_video():
    # Choice selection
    choice = YTChoices.get()
    url = YTEntry.get()
    select = ""

    # While True --in other words: get choice
    if len(url) > 1:
        YTError.config(text="")
        yt = YouTube(url)

        # Action on choices
        if choice == choices[0]:
            select = yt.streams.filter(progressive=True).first()
            YTError.config(text="Downloading ....")
        elif choice == choices[1]:
            select = yt.streams.filter(progressive=True, file_extension="mp4").last()
            YTError.config(text="Downloading ....")
        elif choice == choices[2]:
            select = yt.streams.filter(only_audio=True).first()
            YTError.config(text="Downloading ....")
        else:
            YTError.config(text="Paste Link again!", fg="red")

    # To the Download folder & After Download Success
    try:
        select.download(Folder_Name)
        YTError.config(text="Download completed!")
    except AttributeError:
        YTError.config(text="Can't be blank!", fg="red")


# Create a start_download method using the thread lib to fix not responding & multi links
def start_download():
    # This creates a new thread that calls the download_video method
    download = Thread(target=download_video)

    # Starts the new thread
    download.start()


root = Tk()
root.title("Youtube Downloader")
root.geometry("400x250+480+100")
root.columnconfigure(0, weight=1)

# styling & placement of different buttons and main funcs in the main window [root]

# Link Label
YTlabel = Label(root, text="Enter URL of the video")
YTlabel.grid()

# Entry Box
YTEntryVar = StringVar()
YTEntry = Entry(root, width=50, textvariable=YTEntryVar)
YTEntry.grid()

# ErrorMsg
YTError = Label(root, text="", fg="red", font=("jost", 10))
YTError.grid()

# AskingSaveFileLabel
saveLabel = Label(root, text="Save The Video File", font=("jost", 15, "bold"))
saveLabel.grid()

# Button To Save File
saveEntry = Button(root, width=10, bg="red", fg="white", text="Choose Path", command=open_location)
saveEntry.grid()

# ErrorMsg Location
LocationError = Label(root, text="", fg="red", font=("jost", 10))
LocationError.grid()

# Download Quality
YTQuality = Label(root, text="Select Quality", font=("jost", 10))
YTQuality.grid()

# combobox for choices
choices = ['720p', '144p', 'Only Audio']
YTChoices = ttk.Combobox(root, values=choices)
YTChoices.grid()

# Download Button
downloadButton = Button(root, text="Download", width=10, bg="red", fg="white", command=start_download)
downloadButton.grid()

# Developer Label
developer_label = Label(root, text="By Group-13", font=("jost", 15))
developer_label.grid()

# This keeps the window running until termination
root.mainloop()
