import os, sys, collections, logging
_arg_string = ""
def _main():
    if len(sys.argv) > 1:
        global _arg_string
        for _arg in sys.argv[1:]:
            if _arg == "-i":
                _arg = "install"
            _arg_string += _arg + " "
        print(_arg_string)
        _letsDoIt(_arg_string)
    else:
        _response = ""
        while _response != "done":
            _response = raw_input("Job > ")
            _letsDoIt(_response)

def _letsDoIt(_input):

    path = os.path.dirname(os.path.abspath(__file__)) + '/cogs/'
    plugins = {}

    # Load plugins
    sys.path.insert(0, path)
    for f in os.listdir(path):
        fname, ext = os.path.splitext(f)
        if f.endswith('.py'):
            mod = __import__(fname)
            plugins[fname] = mod.Plugin()
    sys.path.pop(0)

    # Callback
    for plugin in plugins.values():
        commands = plugin.command
        for word in _input.split(' '):
            if word.lower().strip() in commands:
                plugin.action(_input)
                return
            else:
                print("Sorry, that command doesnt exist.")

if __name__=='__main__':
        _main()
