import nonvolatile
import peek
import sys
import subprocess
import os
from xdg import xdg_data_home

def main():
    if len(sys.argv) < 2:
        raise "Too few commands. Exiting"
    cmd = sys.argv[1]
    if cmd.lower() == "peek":
        dests = nonvolatile.get_all_dests()
        peek.peek_pdf(dests)
        subprocess.run(["zathura", "peek.pdf"])
    elif cmd.lower() == "edit":
        surf_dir = xdg_data_home().joinpath("surfeit/")
        subprocess.run(["nvim", "-p", "inbox", "next-actions", "projects", "calendar", "waiting-for", "someday-maybe", "reference", "tickler"], cwd=surf_dir)
    else:
        raise "Unknown command. Exiting"

if __name__ == "__main__":
    main()
