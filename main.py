import datetime
import os
import shutil
import tkinter as tk
import webbrowser
from queue import Empty, Queue
from subprocess import PIPE, Popen
from threading import Thread
from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
rootDir = os.path.dirname(os.path.abspath(__file__))

# Config details
codePath = os.path.join(
    rootDir, "codeBase\sampleScript.py")  # Your script here

# your argument as key value pair
runArguments = {
    "None": "",
    "Full": "-f",
    "Test": "-t",
    "Sanity": "-s",
    "Regression": "-r"
}

# code backup details
backups = {
    "inputPath": os.path.join(rootDir, "codeBase", ""),
    "backUpPath": os.path.join(rootDir, "backupPath")
}


def iter_except(function, exception):
    try:
        while True:
            yield function()
    except exception:
        return


class DisplaySubprocessOutputDemo:
    def __init__(self, root, repo, cmd):
        """
        Initializes an instance of the class.

        Args:
            root (str): The root directory.
            repo (str): The repository.
            cmd (list): The command to execute.

        Returns:
        None
        """
        self.root = root
        self.cmd = cmd
        self.process = Popen(cmd, stdout=PIPE)
        self.repo = repo

        q = Queue(maxsize=1024)
        t = Thread(target=self.reader_thread, args=[q])
        t.daemon = True
        t.start()
        self.update(q)

    def reader_thread(self, q):
        """
        Read subprocess output and put it into the queue.

        Args:
            q (Queue): The queue to put the subprocess output into.

        Returns:
            None
        """
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update(self, q):
        """
        Update GUI with items from the queue.

        Args:
            q (Queue): The queue containing items to update the GUI with.

        Returns:
            None
        """
        for line in iter_except(q.get_nowait, Empty):
            if line is None:
                self.root.insert(tk.END, "Thread Completed")
                self.root.itemconfig(tk.END, {'bg': '#FFFF00'})
                self.root.see("end")
                return
            else:
                self.root.insert(tk.END, line)
                self.root.see("end")
                break
        self.root.after(10, self.update, q)


class App(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Python Code Executor")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure((1, 0), weight=0)

        # create sidebar1 frame
        self.controlFrame = customtkinter.CTkFrame(self)
        self.controlFrame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

        self.runArguments = list(runArguments.keys())
        self.selectedArguments = self.runArguments[0]
        self.option_var = tk.StringVar(self)
        self.combobox = customtkinter.CTkComboBox(self.controlFrame,
                                                  values=self.runArguments,
                                                  variable=self.option_var,
                                                  command=self.option_changed)
        self.combobox.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        self.combobox.set(self.runArguments[0])

        self.runCodeBt = customtkinter.CTkButton(
            self.controlFrame, text='Run PY', command=self.runTask)
        self.runCodeBt.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        # # create sidebar2 frame
        self.maintenanceFrame = customtkinter.CTkFrame(self)
        self.maintenanceFrame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")

        self.cleanBt = customtkinter.CTkButton(
            self.maintenanceFrame, text='Clean Log', command=self.cleanLog)
        self.cleanBt.grid(row=1, column=0, padx=20, pady=10)

        # create sidebar3 frame
        self.backupFrame = customtkinter.CTkFrame(self)
        self.backupFrame.grid(row=2, column=0, padx=20, pady=(20, 20), sticky="nsew")

        self.backupMessageEntry = customtkinter.CTkTextbox(self.backupFrame, width=150)
        self.backupMessageEntry.grid(row=0, column=0, padx=10, pady=10)
        self.backupMessageEntry.insert("1.0", text="Backup Message")

        self.backupBt = customtkinter.CTkButton(
            self.backupFrame, text="Backup", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.backupRepo)
        self.backupBt.grid(row=1, column=0, padx=20, pady=10)

        # create Task View
        self.logFrame = customtkinter.CTkFrame(self)
        self.logFrame.grid(row=0, column=1, rowspan=3, padx=20, pady=(20, 20), sticky="nsew")

        self.logTextArea = Listbox(self.logFrame, selectmode=MULTIPLE, font=('Times', 15))
        self.logTextArea.grid(row=0, column=0, sticky=N+S+W+E)
        self.logFrame.grid_columnconfigure(0, weight=1)
        self.logFrame.grid_rowconfigure(0, weight=1)

    def option_changed(self, *args):
        self.selectedArguments = self.option_var.get()

    def logMe(self, message, level=0):
        """
        Log a message to the logTextArea.

        Args:
            message (str): The message to log.
            level (int): The log level. 0 = Normal, 1 = Blue, 2 = Yellow.

        Returns:
            None
        """
        self.logTextArea.insert(tk.END, message)
        if level == 1:
            # blue
            self.logTextArea.itemconfig(tk.END, {'bg': '#50DDF0'})
        elif level == 2:
            # yellow
            self.logTextArea.itemconfig(tk.END, {'bg': '#FFFF00'})
        self.logTextArea.see("end")

    def runTask(self):
        """
        Run the selected task.

        Returns:
            None
        """
        self.logMe("Initiating Thread Environment", 1)
        runArgumentSelected = runArguments[self.selectedArguments]
        cmd = f'python {codePath} {runArgumentSelected}'
        if ".py" in cmd:
            self.logMe(f"Selected CMD {cmd}", 1)
            app = DisplaySubprocessOutputDemo(
                self.logTextArea, runArgumentSelected, cmd)
        else:
            self.logMe("codePath should be your main python file", 1)

    def cleanLog(self):
        """
        Clean the logTextArea.

        Returns:
            None
        """
        self.logTextArea.delete(0, END)
        self.logMe(f"Cleaning Logs Completed", 1)

    def zipMe(self, zipName, message):
        """
        Create a zip file of the specified directory.

        Args:
            zipName (str): The name of the zip file.
            message (str): The backup message.

        Returns:
            None
        """
        destinationPath = os.path.join(
            backups["backUpPath"], zipName)
        sourcePath = backups["inputPath"]

        shutil.make_archive(destinationPath, 'zip', sourcePath)
        with open(os.path.join(backups["backUpPath"], 'readme.txt'), 'a') as fo:
            fo.write(zipName+' - '+message)
        self.logMe(f"Backed up File: {destinationPath}", 1)
        webbrowser.open(backups["backUpPath"])

    def backupRepo(self):
        """
        Backup the repository.

        Returns:
            None
        """
        reportStartTime = datetime.datetime.now()
        timeOfExecution = (reportStartTime.strftime("%d-%b-%Y"),
                           reportStartTime.strftime("%H:%M:%S"))
        backUpMessage = self.backupMessageEntry.get("1.0", END)
        message = '['+timeOfExecution[0]+'][' + \
            timeOfExecution[1]+'] ' + backUpMessage

        if len(os.listdir(backups["backUpPath"])) != 0:
            currentVersions = str(max([int(x.split('_v')[1][:-4])
                                       for x in os.listdir(backups["backUpPath"]) if x.endswith('.zip')])+1)
        else:
            currentVersions = 0

        zipName = f"Code_Back_up_v{currentVersions}"
        self.zipMe(zipName,
                   message)


if __name__ == "__main__":
    app = App()
    app.mainloop()
