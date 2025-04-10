from typing import Tuple

# Based on https://github.com/mathgeniuszach/xdialog/blob/main/xdialog/zenity_dialogs.py - MIT license | - Expanded version by Henk717

def zenity_clean(txt: str):
    return txt\
        .replace("\\", "\\\\")\
        .replace("$", "\\$")\
        .replace("!", "\\!")\
        .replace("*", "\\*")\
        .replace("?", "\\?")\
        .replace("&", "&amp;")\
        .replace("|", "&#124;")\
        .replace("<", "&lt;")\
        .replace(">", "&gt;")\
        .replace("(", "\\(")\
        .replace(")", "\\)")\
        .replace("[", "\\[")\
        .replace("]", "\\]")\
        .replace("{", "\\{")\
        .replace("}", "\\}")\

def zenity(typ, filetypes=None, initialdir="", initialfile="", **kwargs) -> Tuple[int, str]:
    import shutil, subprocess, os, platform
    if not platform.system() == "Linux":
        raise Exception("This feature should only be used on Linux, if you see this error there is no TK fallback implemented in the code.")
    zenity_bin = shutil.which("zenity")
    if not zenity_bin:
            zenity_bin = shutil.which("yad")
    if not zenity_bin:
            raise Exception("Zenity not present")

    # Build args based on keywords
    args = ['/usr/bin/env', zenity_bin, '--'+typ]
    for k, v in kwargs.items():
        if v is True:
            args.append(f'--{k.replace("_", "-").strip("-")}')
        elif isinstance(v, str):
            cv = zenity_clean(v) if k != "title" else v
            args.append(f'--{k.replace("_", "-").strip("-")}={cv}')

    # Build filetypes specially if specified
    if filetypes:
        for name, globs in filetypes:
            if name:
                globlist = globs.split()
                args.append(f'--file-filter={name.replace("|", "")} ({", ".join(t for t in globlist)})|{globs}')

    # Default filename and folder
    if initialdir is None:
        initialdir=os.getcwd()
    if initialfile is None:
        initialfile=""
    initialpath = os.path.join(initialdir, initialfile)
    args.append(f'--filename={initialpath}')

    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        shell=False
    )
    stdout, _ = proc.communicate()

    return (proc.returncode, stdout.decode('utf-8').strip())

# note: In this section we wrap around file dialogues to allow for zenity

def zentk_askopenfilename(**options):
    try:
        result = zenity('file-selection', filetypes=options.get("filetypes"), initialdir=options.get("initialdir"), title=options.get("title"))[1]
    except:
        from tkinter.filedialog import askopenfilename
        result = askopenfilename(**options)
    return result

def zentk_askopenmultiplefilenames(**options):
    try:
        from os.path import isfile
        files = zenity('file-selection', filetypes=options.get("filetypes"), initialdir=options.get("initialdir"), title=options.get("title"), multiple=True, separator="\n")[1].splitlines()
        result = tuple(filter(isfile, files))
    except:
        from tkinter.filedialog import askopenfilenames
        result = askopenfilenames(**options)
    return result

def zentk_askdirectory(**options):
    try:
        result = zenity('file-selection', initialdir=options.get("initialdir"), title=options.get("title"), directory=True)[1]
    except:
        from tkinter.filedialog import askdirectory
        result = askdirectory(**options)
    return result

def zentk_asksaveasfilename(**options):
    try:
        result = zenity('file-selection', filetypes=options.get("filetypes"), initialdir=options.get("initialdir"), initialfile=options.get("initialfile"), title=options.get("title"), save=True)[1]
    except:
        from tkinter.filedialog import asksaveasfilename
        result = asksaveasfilename(**options)
    return result
