from __future__ import print_function
import subprocess
import shlex
import os
import sys


def run_command(command):
    """
    This function captures text output from a command-line program and
    displays it in the Python shell. Currently does not print the output
    until after the command has completed.

    Parameters
    ----------
    command : str
        Command to send to subprocess.

    Returns
    -------
    rc : str
        Output from command that was executed. For MultiDop, this is all the
        update text that is printed out by DDA.
    """
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                               bufsize=0)
    while True:
        output = process.stdout.readline()
        if sys.version_info >= (3, 0, 0):
            output = output.decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


def do_analysis(param_file, cmd_path='../src/DDA', remove=True):
    """
    Execute a 3DVAR multi-Doppler analysis. The analysis will be output to
    the output file specified within the param_file.

    Parameters
    ----------
    param_file : str
        Name of file containing the parameters needed by the DDA engine.

    Other Parameters
    ----------------
    cmd_path : str
        Full path to the DDA executable, including the executable itself.
    remove : bool
        True - Remove the temporary DDA executable after running the analysis.

        False - Don't do this. This option is best for parallel processing.

    """
    os.system('cp ' + cmd_path + ' .')
    rc = run_command('./DDA ' + param_file)
    if remove:
        os.remove('./DDA')
