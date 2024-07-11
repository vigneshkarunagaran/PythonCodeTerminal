# Python Code Executor

- This is a GUI application for executing Python code in a customized terminal with Realtime running logs
- Allows you to save and pass CMD line arguments using dropdown
- Allows you to zip your code as backup

---

## Libraries:
1.  customtkinter
2.  tkinter
3.  subprocess
4.  shutil

---

## Setup and Configuration
Install the module with pip:
```
pip3 install -r libs.txt
```
Before running the application, ensure that you have the following setup and configuration details:

- `codePath`: Path to the Python script you want to execute.
- `runArguments`: A dictionary containing key-value pairs for different run arguments.
- `backups`: A dictionary containing backup-related paths. Modify the values of `inputPath` and `backUpPath` variables in the `backups` dictionary to specify the input directory and the backup destination directory.

---
## Function: iter_except
- This function takes a callable function and a specific exception as arguments. 
- It repeatedly calls the function until the specified exception is raised. 
- It yields the values returned by the function on each iteration. If the specified exception is raised, the iteration is stopped.
```python
def iter_except(function, exception):
    """
    Calls a given function repeatedly until a specific exception is raised.

    Args:
        function (callable): The function to be called repeatedly.
        exception (Exception): The specific exception that, when raised, stops the iteration.

    Yields:
        Any: The values returned by the function on each iteration.

    Raises:
        exception: If the specified exception is raised by the function.

    Returns:
        None
    """
    try:
        while True:
            yield function()
    except exception:
        return
```
## Class: DisplaySubprocessOutputDemo
[Refrenced from Stackoverflow](https://stackoverflow.com/questions/665566/redirect-command-line-results-to-a-tkinter-gui)
- This class displays the output of a subprocess in a GUI window.
- It takes the root directory, repository, and command as arguments in the constructor. 
- The `reader_thread` method reads the subprocess output and puts it into a queue. 
- The `update` method retrieves items from the queue and updates the GUI with the items.
```python
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
        ...

    def reader_thread(self, q):
        """
        Read subprocess output and put it into the queue.

        Args:
            q (Queue): The queue to put the subprocess output into.

        Returns:
            None
        """
        ...

    def update(self, q):
        """
        Update GUI with items from the queue.

        Args:
            q (Queue): The queue containing items to update the GUI with.

        Returns:
            None
        """
        ...
```
## Class: App
- This class represents the GUI application for executing Python code and performing related tasks.
```python
class App(customtkinter.CTk):
    """
    A GUI application for executing Python code.

    Attributes:
        width (int): The width of the application window.
        height (int): The height of the application window.

    Methods:
        __init__(): Initializes the App class and configures the application window.
    """
    ...

    def __init__(self):
        """
        Initializes the App class by setting up the application window and its components.

        Returns:
            None
        """
        ...

    def option_changed(self, *args):
        """
        Handle the event when the selected option changes in the combobox.

        Args:
            args: Variable arguments.

        Returns:
            None
        """
        ...
```
## Screenshots
- Launch screen
![image](https://github.com/vigneshkarunagaran/CustomeTerminal/assets/59251885/5f8903fe-05c0-41e6-b566-858d666a3c91)
- `Run PY` Executes sample code with `-t` as sys argument
- `Argument drop down` allows user to choose various custome arguments available
![image](https://github.com/vigneshkarunagaran/CustomeTerminal/assets/59251885/69565280-94d4-4edf-8190-608a9288ec8e)
- `Clean Log` cleares the terminal area
- `Backup` Zips the code with date and time stamp and logs the same in readme.txt
![image](https://github.com/vigneshkarunagaran/CustomeTerminal/assets/59251885/90c3d93b-32ec-495b-8c5b-8c27be1b342f)


 
