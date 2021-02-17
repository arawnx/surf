import nonvolatile
import peek, echo
import sys
import subprocess
import os
from pathlib import *
from xdg import xdg_data_home

def main():
    if len(sys.argv) < 2:
        raise "Too few commands. Exiting"
    cmd = sys.argv[1]
    if cmd.lower() == "peek":
        dests = nonvolatile.get_all_dests()
        peek.peek_pdf(dests, Path("/tmp/peek"))
        subprocess.run(["zathura", "/tmp/peek.pdf"])
    elif cmd.lower() == "echo":
        dests = nonvolatile.get_all_dests()
        echo.echo_pdf(dests, Path("/tmp/echo"))
        subprocess.run(["zathura", "/tmp/echo.pdf"])
    elif cmd.lower() == "edit":
        surf_dir = xdg_data_home().joinpath("surfeit/")
        subprocess.run(["nvim", "-p", "inbox", "next-actions", "projects", "calendar", "waiting-for", "horizons", "someday-maybe", "reference", "tickler"], cwd=surf_dir)
    else:
        raise "Unknown command. Exiting"

if __name__ == "__main__":
    main()
