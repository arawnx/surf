import nonvolatile
import peek
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        raise "Too few commands. Exiting"
    cmd = sys.argv[1]
    if cmd.lower() == "peek":
        dests = nonvolatile.get_all_dests()
        peek.peek_pdf(dests)
        subprocess.run(["zathura", "peek.pdf"])
    else:
        raise "Unknown command. Exiting"

if __name__ == "__main__":
    main()
