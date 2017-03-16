import os,shutil

_cur_file = ""
_cur_dir = os.getcwd()
_prev_dir = ['']
def _main():
    _response = ""

    while _response != "done":
        _response = raw_input("Job > ")
        _letsDoIt(_response)

def _letsDoIt(_input):
    _tokens = _input.split(' ')
    _task = _tokens[0]

    if _task == "make":
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
    elif _task == "enter":
        _toEnter = _tokens[1]
        _enter(_toEnter)
    elif _task == "leave":
        _leave()
    elif _task == "curr":
        _curr()
    elif _task == "del":
        _toDelete = _tokens[1]
        if len(_tokens) == 3:
            _preAccept = _tokens[2]
        else:
            _preAccept = "none"
        _remove(_toDelete, _preAccept)
    elif _task == "load":
        _toLoad = _tokens[1]
        _load(_toLoad)
    elif _task == "echo":
        _toEcho = _tokens[1]
        print(_toEcho)
    elif _task == "list" or _task == "ls":
        if len(_tokens) == 2:
            _toList = _tokens[1]
        else:
            _toList = _cur_dir
        _list(_toList)
    elif _task == "install":
        if len(_tokens) == 2:
            _toInstall = _token[1]
        else:
            _toInstall = ""
        _install(_toInstall)


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
    if _toInstall == "":
        if os.path.isfile("install.worker"):
            _load("install.worker")
        else:
            print("Sorry, nothing to install.")


if __name__=='__main__':
        _main()
