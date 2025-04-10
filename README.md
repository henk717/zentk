# zentk
zentk is an easy way to get zenity and yad based file dialogues for your TK projects, aimed to be a drop in solution.
On non Linux platforms or platforms where zenity and yad are not present zentk will automatically use tk.

The code was largely taken from xdialog, but expanded to allow default file directories.
Since we only wanted zenity for Linux we fall back for everything else.
When we tested xdialog we found kdialog to be unrelible with multiple filenames, and have chosen to focus this package only on zenity to keep it simple and compact for your code.
