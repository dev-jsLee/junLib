import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.util.files_move.folder_tree_up import FolderLifter

obj = FolderLifter(strip_quotes(input("Enter folder path : ")))
obj.lift_folders()