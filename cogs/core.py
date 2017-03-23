import sys,os,shutil,subprocess
try:
    from subprocess import DEVNULL  # Python 3.
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

_cur_file = ""
_cur_dir = os.getcwd()
_prev_dir = ['']

class Plugin:
        def __init__(self):
            self.make = ['make']
            self.enter = ['enter']
            self.leave = ['leave']
            self.curr = ['curr']
            self.delete = ['del']
            self.load = ['load']
            self.echo = ['echo']
            self.list = ['list', 'ls']
            self.install = ['install']
            self.clear = ['clear', 'cls', 'clr']
            self.done = ['done']
            self.cog = ['cog', 'cogs']
            self.exc = ['exc']
            self.update = ['update']

            self.command = self.update + self.make + self.enter + self.leave + self.curr + self.delete + self.load + self.echo + self.list + self.install + self.clear + self.done + self.cog + self.exc

        def action(self, command):
            _tokens = command.split(" ")
            _task = _tokens[0]
            if _task in self.make:
                _toMake = _tokens[1]
                if _toMake == "folder":
                    _folderName = _tokens[2]
                    _make(_folderName, "folder")
                elif _toMake == "file":
                    _fileName = _tokens[2]
                    _make(_fileName, "file")
                elif _toMake == "script":
                    _fileName = ""
                    _make(_fileName, "script")
            elif _task in self.enter:
                _toEnter = _tokens[1]
                _enter(_toEnter)
            elif _task in self.leave:
                _leave()
            elif _task in self.curr:
                _curr()
            elif _task in self.delete:
                _toDelete = _tokens[1]
                if len(_tokens) == 3:
                    _preAccept = _tokens[2]
                else:
                    _preAccept = "none"
                _remove(_toDelete, _preAccept)
            elif _task in self.load:
                _toLoad = _tokens[1]
                _load(_toLoad)
            elif _task in self.echo:
                _toEcho = _tokens[1]
                print(_toEcho)
            elif _task in self.list:
                if len(_tokens) == 2:
                    _toList = _tokens[1]
                else:
                    _toList = _cur_dir
                _list(_toList)
            elif _task in self.install:
                if len(_tokens) == 2:
                    _toInstall = _tokens[1]
                else:
                    _toInstall = ""
                _install(_toInstall)
            elif _task in self.clear:
                os.system('cls' if os.name == 'nt' else 'clear')
            elif _task in self.done:
                print("Goodbye.")
            elif _task in self.cog:
                if len(_tokens) == 2:
                    _toInstall = _tokens[1]
                else:
                    ## Run through all cogs, and check if they have an "active" tag.
                    ## Display how many are active.
                    _check_cogs()
                    return
            elif _task in self.exc:
                _toEx = _tokens[1:]
                _exc(_toEx)
            elif _task in self.update:
                print("This current does not work the way it should...")


## Everything to do with cogs. ##

def _install_cog(_toInstall):
    print("this is not done yet.")

def _check_cogs():
    print("this is not done yet.")

## Everything to do with the core. ##

def _make(_toMake, _fileOrFolder):
    global _cur_dir
    if _cur_dir == "":
        _cur_dir = os.getcwd()
    if _fileOrFolder == "file":
        with open(_cur_dir + "/" + _toMake, 'w') as out:
            out.write("Welcome to your new file!")
    elif _fileOrFolder == "folder":
        if not os.path.exists(_toMake):
            os.makedirs(_cur_dir + "/" + _toMake)
        else:
            print("\n\nSorry, that folder already exists.")
    elif _fileOrFolder == "script":
        _fileName = raw_input("Script Name? ")
        _commands = []
        _line = ""
        while _line != "done":
            _line = raw_input("> ")
            if _line != "done":
                _commands.append(_line)
        with open(_fileName, 'w') as out:
            for _line in _commands:
                out.write(_line + "\n")



def _enter(_toEnter):
    global _cur_dir
    global _prev_dir
    if _toEnter == "root":
        _cur_dir = ""
    else:
        if _cur_dir == "":
            _cur_dir = "/" + _toEnter
        else:
            _prev_dir.append(_cur_dir)
            _cur_dir = _cur_dir + "/" + _toEnter



def _leave():
    global _cur_dir
    global _prev_dir
    _size = len(_prev_dir)
    if _size == 1:
        _cur_dir = _prev_dir[_size - 1]
    else:
        _cur_dir = _prev_dir[_size - 1]
        _prev_dir.remove(_prev_dir[_size - 1])



def _curr():
    print(_cur_dir)



def _remove(_toDelete, _preAccept):
    if _preAccept == "none":
        _result = raw_input("Are you sure (yes/no)? ")
        if _result == "yes" or _result == "y":
            if os.path.isfile(_cur_dir + "/" + _toDelete):
                os.remove(_cur_dir + "/" + _toDelete)
            elif os.path.isdir(_cur_dir + "/" + _toDelete):
                shutil.rmtree(_cur_dir + "/" + _toDelete, ignore_errors=True, onerror=None)
    elif _preAccept == "-y":
        if os.path.isfile(_toDelete):
            os.remove(_cur_dir + "/" + _toDelete)
        elif os.path.isdir(_toDelete):
            shutil.rmtree(_cur_dir + "/" + _toDelete, ignore_errors=True, onerror=None)



def _load(_toLoad):
    _commands = []
    with open(_toLoad, 'r') as inFile:
        for _eachLine in inFile:
            _toAdd = _eachLine.strip('\n')
            _commands.append(_toAdd)
    for _line in _commands:
        _letsDoIt(_line)



def _list(_toList):
    ## Assuming the user wants to list the current dir. ##
    if _toList == "":
        _toList = _cur_dir
    # Open a file
    _dirs = os.listdir( _toList )
    # This would print all the files and directories
    for _file in _dirs:
       print ("- " + _file)



def _install(_toInstall):
    _tokens = _toInstall.split("/")
    if _toInstall == "":
        if os.path.isfile("install.worker"):
            _load("install.worker")
        else:
            print("Sorry, nothing to install.")
    elif _toInstall != "":
        _job = ["clone"]
        _job.append("https://github.com/" + _toInstall)
        subprocess.Popen(['git'] + list(_job), stdout=DEVNULL, stderr=DEVNULL)
        _enter(_tokens[1])
        _install("")

def _exc(_toEx):
    _tokens = _toEx.split('"')
    print(_tokens)
    os.system(_tokens)

def _update():
    ## We need to compare the version codes... so, i might make it execute a command.
    ## if it is newer on the server, than here... download through the _install function
    ## then, that should install it to... because i will create the install file.
    os.system('clear')
    print("This is not done yet.")
