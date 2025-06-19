# Created by Melina Roy
# Created on 2020-03-22 | Last update on 2020-06-10
# Pro-PDF Project: Standalone executable to edit PDF
# Functions:   1- Add blank page(s)
#              2- Combine two files
#              3- Combine multiple files
#              4- Delete page(s)
#              5- Extract pages in a new file


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import PyPDF2 as Pdf
import ntpath
import os
import re


# Attributes
# Colors
BG1 = "alice blue"  # Window background color
BG2 = "SeaGreen3"   # Button background color
BG3 = "dark turquoise"  # Main button background color
BG4 = "aquamarine"    # Button active background
FG1 = "black"   # Tile font color
FG2 = "grey17"  # Description font color
FG3 = "grey9"   # Main button font color
FG4 = "grey5"   # Quit button font color
FG5 = "#0aa687"  # Valid entry color
FG6 = "dark slate blue"     # Instruction entry color
RED = "red"     # Invalid entry color
# Fonts
WELCOME_FONT = ("Corbel", 20, "bold", "italic")
INTRO_FONT = ("Helvetica", 16)
NORMAL_FONT = ("Helvetica", 12)
SMALL_FONT = ("Helvetica", 8)
XSMALL_FONT = ("Helvetica", 6)
ENTRY_FONT = ("Helvetica", 10, "bold")
BUTTON_FONT = ("Keyboard", 14, "bold")
BUTTON_FONT2 = ("Keyboard", 10, "bold")
# Dimensions
WIDTH = 700    # Window dimensions
HEIGHT = 700    # Window dimensions
INTRO_PADy = 10
W_PAD = 10
INDENT_PADx = 25
BUT_PADy = 5
BUT_MAIN_PADy = 10
BUT_WIDTH = 25
LETTER_WIDTH = 612
LETTER_HEIGHT = 792
# Others
USER_FOLDER = os.path.join(os.environ['USERPROFILE']) + "\\"


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Frame Setup
        self.wm_title("Pro-PDF")
        self.resizable(1, 1)
        self.minsize(WIDTH, HEIGHT)
        self.root = tk.Frame(self)
        self.returnWin = None
        self.quitWin = None
        # Window centering
        x_coordinate = int(self.root.winfo_screenwidth()/2 - WIDTH/2)
        y_coordinate = int(self.root.winfo_screenheight()/2 - HEIGHT/2 - 20)
        self.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, x_coordinate,
                                           y_coordinate))
        # Check licence
        self.licence = None
        self.licensing()
        if self.licence:
            # Init StartPage
            self._frame = None
            self.switch_frame(StartPage)
        else:
            pass

    def licensing(self):
        name = "sys.txt"
        folder = "AppData/Local/zpkr-ojdam-ndakm-uooak"
        directory = USER_FOLDER + folder
        icon = directory + "\\" + "pro-pdf_icon.ico"
        path = directory + "\\" + name
        if os.path.isfile(path) and os.path.isfile(icon):
            self.licence = True
            self.iconbitmap(default=icon)
        else:
            self.licence = False
            text = "Vous n'avez pas les permissions pour exécuter ce programme."
            messagebox.showinfo("Erreur", text, icon="error")

    def return_window(self, frame, frame_class):
        if frame.entryFlag is True:
            self.returnWin = tk.Toplevel()
            self.returnWin.config(bg=BG1)
            self.returnWin.title("Retour au menu principal")
            w = 500
            h = 100
            x = int(self.root.winfo_screenwidth()/2 - w/2)
            y = int(self.root.winfo_screenheight()/2 - h/2)
            self.returnWin.geometry("{}x{}+{}+{}".format(w, h, x, y))
            self.returnWin.grid_rowconfigure(0, weight=1)
            self.returnWin.grid_rowconfigure(1, weight=1)
            self.returnWin.grid_columnconfigure(0, weight=1)
            self.returnWin.grid_columnconfigure(1, weight=1)
            message = "Êtes-vous certain de vouloir retourner au menu " \
                      "principal?\nLes entrées validées seront perdues."
            label = my_label(self.returnWin, message, i=0, j=0, align="center",
                             ypad=(INTRO_PADy, 0), col_span=2)
            label.config(justify="center")
            label.grid(sticky="nsew")
            oui = my_button(self.returnWin, "Oui", but_type="small", i=1, j=0,
                            but_w=10)
            oui.config(command=lambda: self.switch_frame(frame_class))
            non = my_button(self.returnWin, "Non", but_type="small", i=1, j=1,
                            but_w=10)
            non.config(command=lambda: self.returnWin.destroy())
            self.returnWin.transient(frame)  # set to be on top of the main window
            self.returnWin.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
            frame.wait_window(self.returnWin)  # pause anything on the main window until this one closes (optional)
        else:
            self.switch_frame(frame_class)

    def switch_frame(self, frame_class):
        if self.returnWin:
            self.returnWin.destroy()
        else:
            pass
        # Init new frame
        new_frame = frame_class(self)
        # Destroy old frame
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)

    def quit_window(self, frame):
        if frame.entryFlag is True:
            self.quitWin = tk.Toplevel()
            self.quitWin.config(bg=BG1)
            self.quitWin.title("Quitter")
            w = 500
            h = 100
            x = int(self.root.winfo_screenwidth() / 2 - w / 2)
            y = int(self.root.winfo_screenheight() / 2 - h / 2)
            self.quitWin.geometry("{}x{}+{}+{}".format(w, h, x, y))
            self.quitWin.grid_rowconfigure(0, weight=1)
            self.quitWin.grid_rowconfigure(1, weight=1)
            self.quitWin.grid_columnconfigure(0, weight=1)
            self.quitWin.grid_columnconfigure(1, weight=1)
            message = "Êtes-vous certain de vouloir quitter?" \
                      "\nLes entrées validées seront perdues."
            label = my_label(self.quitWin, message, i=0, j=0,
                             ypad=(INTRO_PADy, 0), col_span=2)
            label.config(justify="center")
            label.grid(sticky="nsew")
            oui = my_button(self.quitWin, "Oui", but_type="small", i=1, j=0,
                            but_w=10)
            oui.config(command=lambda: self.destroy())
            non = my_button(self.quitWin, "Non", but_type="small", i=1, j=1,
                            but_w=10)
            non.config(command=lambda: self.quitWin.destroy())
            self.quitWin.transient(frame)  # set to be on top of the main window
            self.quitWin.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
            frame.wait_window(self.quitWin)  # pause anything on the main window until this one closes (optional)
        else:
            self.destroy()


class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg=BG1)
        self.graphical_interface(master)
        self.entryFlag = False

    def graphical_interface(self, master):
        # Row and columns configuration
        x = 8
        for k in range(x):
            self.grid_rowconfigure(k, weight=1)
        y = 1
        for k in range(y):
            self.grid_columnconfigure(k, weight=1)
        # Intro
        txt_welcome = "Bienvenue sur Pro-PDF!"
        my_label(self, txt_welcome, lab_type="welcome")
        txt_intro = "Quelle tâche souhaitez-vous exécuter?"
        my_label(self, txt_intro, lab_type="intro", i=1)
        # Buttons
        # Add Pages Button
        txt_add_blank = "Ajouter des pages blanches"
        but_add_blank = my_button(self, txt_add_blank, i=2, ypad=BUT_PADy)
        but_add_blank.config(command=lambda: master.switch_frame(AddBlankPage))
        # Combine Two Files Button
        txt_combine_two = "Combiner deux fichiers"
        but_combine_two_page = my_button(self, txt_combine_two, i=3, ypad=BUT_PADy)
        but_combine_two_page.config(command=lambda: master.switch_frame(CombineTwoPage))
        # Combine Multi Files Button
        txt_combine_multi = "Combiner plusieurs fichiers"
        but_combine_multi_page = my_button(self, txt_combine_multi, i=4, ypad=BUT_PADy)
        but_combine_multi_page.config(command=lambda: master.switch_frame(CombineMultiPage))
        # Delete Pages Button
        txt_delete = "Supprimer des pages"
        but_del_page = my_button(self, txt_delete, i=5, ypad=BUT_PADy)
        but_del_page.config(command=lambda: master.switch_frame(DeletePage))
        # Extract Pages Button
        txt_extract = "Extraire des pages"
        but_extract_page = my_button(self, txt_extract, i=6, ypad=BUT_PADy)
        but_extract_page.config(command=lambda: master.switch_frame(ExtractPage))
        # Done/Quit Button
        but_quit = my_button(self, "Quitter", but_type="main", i=7, but_w=8,
                             ypad=(BUT_MAIN_PADy*2, W_PAD))
        but_quit.config(command=lambda: master.quit_window(self))


class AddBlankPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg=BG1)
        # Setup graphical interface
        self.graphical_interface(master)
        # Flag for entries
        self.entryFlag = False
        # File Variables
        self.file = File()
        self.newFile = File()
        # Variables for adding blank pages
        self.pageIndex = None
        self.nbBlank = None
        self.radioFlag = False
        # Label Variables
        self.fileLabel = None
        self.pageIndexLabel = None
        self.nbBlankLabel = None
        self.newFileLabel = None
        self.radioLabel = None
        self.executeLabel = None

    def graphical_interface(self, master):
        # Row and columns configuration
        x = 18
        for k in range(x):
            self.grid_rowconfigure(k, weight=1)
        y = 3
        for k in range(y):
            self.grid_columnconfigure(k, weight=1)
        # Content
        # Intro
        txt_return = "Retour"
        but_return = my_button(self, txt_return, but_type="main", but_w=7,
                               align="left")
        but_return.config(command=lambda: master.return_window(self, StartPage))
        txt_intro = "Ajouter des pages blanches"
        my_label(self, txt_intro, lab_type="intro", i=1, col_span=y)
        txt_warning = "IMPORTANT: Veuillez suivre les étapes dans l'ordre et " \
                      "valider avec \"OK\" après chaque étape.\nSi vous retournez " \
                      "à une étape antérieure, veuillez revalider avec \"OK\" " \
                      "toutes les étapes subséquentes."
        my_label(self, txt_warning, lab_type="small", i=2, col_span=y)
        # Main
        txt_1st = "1. Veuillez sélectionner le fichier dans lequel vous" \
                  " souhaitez\najouter des pages blanches."
        my_label(self, txt_1st, i=3, xpad=(W_PAD, 0), ypad=BUT_PADy)
        but_select = my_button(self, "Sélectionner", but_type="small", i=3,
                               j=1, but_w=11, align="right",
                               xpad=0, ypad=W_PAD)
        but_select.config(command=lambda: self.get_file(4, 0, span=y-1))
        my_label(self, "", lab_type="entry", i=4, j=0, xpad=INDENT_PADx)
        txt_2nd = "2. À la suite de quelle page du fichier sélectionné" \
                  "\ndésirez-vous ajouter des pages blanches?"
        txt_3rd = "Veuillez inscrire \"0\" si vous souhaitez ajouter des " \
                  "pages blanches au début."
        my_label(self, txt_2nd, i=5, ypad=(BUT_PADy, 0))
        my_label(self, txt_3rd, lab_type="small", i=6, align="left")
        page_index = tk.StringVar()
        my_entry(self, page_index, i=5, j=1)
        but_ok1 = my_button(self, "OK", but_type="small", i=5, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok1.config(
            command=lambda: self.confirm_int_entry("pageIndex",
                                                   page_index.get(), 7, 0,
                                                   "pageIndexLabel",
                                                   span=y-1))
        my_label(self, "", lab_type="entry", i=7, j=0, xpad=INDENT_PADx)
        txt_4th = "3. Combien de pages blanches souhaitez-vous ajouter" \
                  " au\nfichier?"
        my_label(self, txt_4th, i=8, ypad=BUT_PADy)
        nb_page = tk.StringVar()
        my_entry(self, nb_page, i=8, j=1)
        but_ok2 = my_button(self, "OK", but_type="small", i=8, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok2.config(
            command=lambda: self.confirm_int_entry("nbBlank", nb_page.get(),
                                                   9, 0, "nbBlankLabel",
                                                   unit=" page(s)", span=y-1))
        my_label(self, "", lab_type="entry", i=9, j=0, xpad=INDENT_PADx)
        txt_5th = "4. Souhaitez-vous enregistrer le nouveau fichier" \
                  " dans le\nmême dossier que le fichier d'origine?"
        txt_6th = "Si vous choisissez \"Non\", veuillez sélectionner le " \
                  "dossier de destination."
        my_label(self, txt_5th, i=10, ypad=(BUT_PADy, 0))
        my_label(self, txt_6th, lab_type="small", i=11, align="left")
        choice = tk.IntVar()
        tk.Radiobutton(self, text="Oui", variable=choice, value=1,
                       activebackground=BG1, bg=BG1).grid(
            row=10, column=1, sticky="ne", padx=W_PAD, pady=0)
        tk.Radiobutton(self, text="Non", variable=choice, value=2,
                       activebackground=BG1, bg=BG1).grid(
            row=10, column=1, sticky="se", padx=W_PAD, pady=0)
        but_ok4 = my_button(self, "OK", but_type="small", i=10, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok4.config(
            command=lambda: self.confirm_radio_entry(choice.get(), 12, 0,
                                                     span=y-1))
        my_label(self, "", lab_type="entry", i=12, j=0, xpad=INDENT_PADx)
        txt_7th = "5. Quel nom donnez-vous au fichier qui sera créé?"
        my_label(self, txt_7th, i=13, ypad=BUT_PADy)
        new_name = tk.StringVar()
        my_entry(self, new_name, i=13, j=1, w=20)
        but_ok3 = my_button(self, "OK", but_type="small", i=13, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok3.config(
            command=lambda: self.confirm_filename_entry(new_name.get(), 14, 0,
                                                        span=y - 1))
        my_label(self, "", lab_type="entry", i=14, j=0, xpad=INDENT_PADx)
        but_execute = my_button(self, "Exécuter", i=15, but_w=10,
                                ypad=BUT_MAIN_PADy, col_span=y)
        but_execute.config(command=lambda: self.blank_function(16, 0,
                                                               span=y))
        my_label(self, "", lab_type="entry", i=16, j=0, xpad=INDENT_PADx)
        # Done/Quit Button
        but_quit = my_button(self, "Quitter", but_type="main", i=17, but_w=8,
                             ypad=BUT_MAIN_PADy, col_span=y)
        but_quit.config(command=lambda: master.quit_window(self))

    def get_file(self, x, y, span=1):
        if self.fileLabel is not None:
            self.fileLabel.destroy()
        else:
            pass
        self.file.select_file()
        self.fileLabel = my_label(self, self.file.name, lab_type="entry",
                                  i=x, j=y, xpad=INDENT_PADx, col_span=span)
        if self.file.flag is False:
            self.fileLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_int_entry(self, var_str, value_str, x, y, label_str, unit="",
                          span=1):
        obj_label = getattr(self, label_str)
        if obj_label is not None:
            obj_label.destroy()
        else:
            pass
        # Check if a file was selected at previous step
        if self.file.flag is False:     # No file, return
            text = "Vérifier qu'un fichier a été sélectionné."
            label = my_label(self, text, lab_type="entry", i=x, j=y,
                             col_span=span)
            label.config(fg=RED)
            setattr(self, label_str, label)
        else:                           # File, continue
            try:
                setattr(self, var_str, int(value_str))
                # Check user input
                # If zero or negative, invalid entry
                if getattr(self, var_str) < 0:
                    setattr(self, var_str, "Entrée invalide.")
                    text = getattr(self, var_str)
                # If pageIndex, check if the file contains it
                elif var_str == "pageIndex":
                    input_file = open(self.file.path, "rb")
                    reader = Pdf.PdfFileReader(input_file)
                    nb_pages = reader.getNumPages()
                    input_file.close()
                    # Page not in file, invalid entry
                    if self.pageIndex > nb_pages:
                        text = "Pas de page " + str(self.pageIndex) +\
                               " dans le fichier sélectionné."
                        setattr(self, var_str, "Entrée invalide.")
                    else:
                        text = str(getattr(self, var_str)) + unit
                else:
                    text = str(getattr(self, var_str)) + unit
            except ValueError:      # If user input is not an integer
                setattr(self, var_str, "Entrée invalide.")
                text = getattr(self, var_str)
        label = my_label(self, text, lab_type="entry", i=x, j=y,
                         col_span=span)
        setattr(self, label_str, label)
        if isinstance(getattr(self, var_str), str):
            label.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_radio_entry(self, value, x, y, span=1):
        if self.radioLabel is not None:
            self.radioLabel.destroy()
        else:
            pass
        if value == 1:      # Same directory as input file
            if self.file.flag is False:     # Check if input file exists
                self.radioFlag = False
                text = "Vérifier qu'un fichier a été sélectionné."
            else:
                self.radioFlag = True
                self.newFile.directory = self.file.directory
                text = self.newFile.directory
        elif value == 2:    # Other directory than input file
            self.newFile.select_directory()     # Select new directory
            if self.newFile.directory == "Aucune sélection.":   # Check if a selection was made
                self.radioFlag = False
                text = self.newFile.directory
            else:
                self.radioFlag = True
                text = self.newFile.directory
        else:               # If no selection
            self.radioFlag = False
            text = "Veuillez sélectionner une option."
        # Check if file already exists or not
        if self.radioFlag is True and self.newFile.name and self.newFile.flag is True:
            self.newFile.path = self.newFile.directory + self.newFile.name
            if os.path.exists(self.newFile.path):
                self.radioFlag = False
                text = "Un fichier avec le même nom existe déjà dans ce" \
                       " dossier.\nVeuillez changer le nom du nouveau fichier" \
                       " ou choisir un autre dossier."
                self.newFile.flag = False
            else:
                self.newFile = File(self.newFile.path)
                self.newFile.flag = True
        else:
            pass
        self.radioLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.radioFlag is False:
            self.radioLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_filename_entry(self, value_str, x, y, span=1):
        self.newFile.name = None
        if self.newFileLabel is not None:
            self.newFileLabel.destroy()
        else:
            pass
        if self.radioFlag is False:
            self.newFile.flag = False
            text = "Veuillez choisir un dossier à l'étape précédente."
            self.newFileLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, col_span=span)
            self.newFileLabel.config(fg=RED)
        else:
            if value_str == "":         # If user input is empty, invalid entry
                self.newFile.flag = False
                text = "Veuillez inscrire un nom."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            # If special characters in user input, invalid entry
            elif check_special_character(value_str):
                self.newFile.flag = False
                text = "Veuillez ne pas inclure de caractères spéciaux."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            else:
                # Making sure file name ends with file type
                if value_str[-4:] == ".pdf":
                    name = value_str
                else:
                    name = value_str + ".pdf"
                self.newFile.name = name
                self.newFile.path = self.newFile.directory + self.newFile.name
                if os.path.exists(self.newFile.path):
                    self.newFile.flag = False
                    text = "Un fichier avec le même nom existe déjà dans ce" \
                           " dossier.\nVeuillez changer le nom du nouveau fichier" \
                           " ou choisir un autre dossier."
                    self.newFileLabel = my_label(self, text, lab_type="entry",
                                                 i=x, j=y, col_span=span)
                    self.newFileLabel.config(fg=RED)
                else:
                    self.newFile = File(self.newFile.path)
                    self.newFile.flag = True
                    self.entryFlag = True
                    self.newFileLabel = my_label(self, value_str, lab_type="entry",
                                                 i=x, j=y, col_span=span)

    def blank_function(self, x, y, span=1):
        if self.executeLabel is not None:
            self.executeLabel.destroy()
        else:
            pass
        self.executeLabel = my_label(self, "...", lab_type="entry",
                                     i=x, j=y, xpad=0, col_span=span)
        flag = "Entrée invalide."
        if self.file.flag is False or self.pageIndex == flag or\
                self.pageIndex is None or self.nbBlank == flag or\
                self.nbBlank is None or self.newFile.flag is False or\
                self.radioFlag is False:
            text = "Erreur. Veuillez vérifier que vos entrées sont valides " \
               "et que vous avez appuyé sur \"OK\"."
            self.executeLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, xpad=0,
                                         col_span=span)
            self.executeLabel.config(fg=RED)
        else:
            try:
                # Read file
                input_file = open(self.file.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                # Creating new file
                blank = Pdf.PdfFileWriter()
                blank.appendPagesFromReader(reader)
                # Add blank pages
                for _ in range(self.nbBlank):
                    blank.insertBlankPage(LETTER_WIDTH, LETTER_HEIGHT, self.pageIndex)
                # Write new file
                out = open(self.newFile.path, "wb")
                blank.write(out)
                input_file.close()
                out.close()
                self.executeLabel.config(text="...Terminé.")
            except PermissionError:
                text = "Erreur. Vérifier que le fichier " + \
                       self.newFile.name + \
                       " n'est pas déjà ouvert ou en lecture seule."
                self.executeLabel.config(text=text, fg=RED)


class CombineTwoPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg=BG1)
        # Setup graphical interface
        self.graphical_interface(master)
        # Flag for entries
        self.entryFlag = False
        # File Variables
        self.file = File()
        self.file2add = File()
        self.newFile = File()
        # Variables for combining files
        self.pageIndex = None
        self.pageIndexFlag = False
        self.pages = None
        self.pagesFlag = False
        self.pagesText = None
        self.radioFlag = False
        # Label Variables
        self.fileLabel = None
        self.pageIndexLabel = None
        self.file2addLabel = None
        self.pagesLabel = None
        self.newFileLabel = None
        self.radioLabel = None
        self.executeLabel = None
        # Other Widget Variables
        self.pagesEntry = None
        self.okButton = None

    def graphical_interface(self, master):
        # Row and columns configuration
        x = 21
        for k in range(x):
            self.grid_rowconfigure(k, weight=1)
        y = 3
        for k in range(y):
            self.grid_columnconfigure(k, weight=1)
        # Content
        # Intro
        txt_return = "Retour"
        but_return = my_button(self, txt_return, but_type="main", but_w=7,
                               align="left")
        but_return.config(command=lambda: master.return_window(self, StartPage))
        txt_intro = "Combiner deux fichiers"
        my_label(self, txt_intro, lab_type="intro", i=1, col_span=y)
        txt_warning = "IMPORTANT: Veuillez suivre les étapes dans l'ordre et " \
                      "valider avec \"OK\" après chaque étape.\nSi vous retournez " \
                      "à une étape antérieure, veuillez revalider avec \"OK\" " \
                      "toutes les étapes subséquentes."
        my_label(self, txt_warning, lab_type="small", i=2, col_span=y)
        # Main
        txt_1st = "1. Veuillez sélectionner le fichier auquel vous" \
                  " souhaitez\ncombiner un autre fichier."
        my_label(self, txt_1st, i=3, xpad=(W_PAD, 0), ypad=BUT_PADy)
        but_select = my_button(self, "Sélectionner", but_type="small", i=3,
                               j=1, but_w=11, align="right",
                               xpad=0, ypad=W_PAD)
        but_select.config(command=lambda: self.get_file(4, 0, span=y-1))
        my_label(self, "", lab_type="entry", i=4, j=0, xpad=INDENT_PADx)
        txt_2nd = "2. À la suite de quelle page du fichier sélectionné" \
                  "\ndésirez-vous ajouter l'autre fichier?"
        txt_3rd = "Veuillez inscrire \"0\" si vous souhaitez ajouter l'autre " \
                  "fichier au début."
        my_label(self, txt_2nd, i=5, ypad=(BUT_PADy, 0))
        my_label(self, txt_3rd, lab_type="small", i=6, align="left")
        page_index = tk.StringVar()
        my_entry(self, page_index, i=5, j=1)
        but_ok1 = my_button(self, "OK", but_type="small", i=5, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok1.config(
            command=lambda: self.confirm_int_entry(page_index.get(), 7, 0,
                                                   span=y-1))
        my_label(self, "", lab_type="entry", i=7, j=0, xpad=INDENT_PADx)
        txt_4th = "3. Veuillez choisir le fichier que vous souhaitez" \
                  " ajouter\nau fichier sélectionné précédemment."
        my_label(self, txt_4th, i=8, ypad=BUT_PADy)
        but_select2 = my_button(self, "Sélectionner", but_type="small", i=8,
                                j=1, but_w=11, align="right", xpad=0,
                                ypad=W_PAD)
        but_select2.config(command=lambda: self.get_file2(9, 0, span=y-1))
        my_label(self, "", lab_type="entry", i=9, j=0, xpad=INDENT_PADx)
        txt_5th = "4. Souhaitez-vous ajouter le fichier au complet ou" \
                  " une\nsélection de page(s)?"
        txt_6th = "Pour la 2e option, veuillez séparer les numéros de page" \
                  " par des virgules\net les étendues de pages par des traits-d'union. Ex: 1,3,5-7,12"
        my_label(self, txt_5th, i=10, ypad=(BUT_PADy, 0))
        my_label(self, txt_6th, lab_type="small", i=11, align="left")
        choice = tk.IntVar()
        tk.Radiobutton(self, text="Complet", variable=choice, value=1,
                       activebackground=BG1, bg=BG1).grid(
            row=10, column=1, sticky="ne", padx=W_PAD, pady=0)
        tk.Radiobutton(self, text="Sélection", variable=choice, value=2,
                       activebackground=BG1, bg=BG1).grid(
            row=10, column=1, sticky="se", padx=W_PAD, pady=0)
        but_ok2 = my_button(self, "OK", but_type="small", i=10, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok2.config(
            command=lambda: self.confirm_pages_entry(choice.get(), 12, 0,
                                                     span=y - 1))
        my_label(self, "", lab_type="entry", i=12, j=0, xpad=INDENT_PADx)
        txt_7th = "5. Souhaitez-vous enregistrer le nouveau fichier" \
                  " dans\nle même dossier que le fichier d'origine?"
        txt_8th = "Si vous choisissez \"Non\", veuillez sélectionner le " \
                  "dossier de destination."
        my_label(self, txt_7th, i=13, ypad=(BUT_PADy, 0))
        my_label(self, txt_8th, lab_type="small", i=14, align="left")
        choice2 = tk.IntVar()
        tk.Radiobutton(self, text="Oui", variable=choice2, value=1,
                       activebackground=BG1, bg=BG1).grid(
            row=13, column=1, sticky="ne", padx=W_PAD, pady=0)
        tk.Radiobutton(self, text="Non", variable=choice2, value=2,
                       activebackground=BG1, bg=BG1).grid(
            row=13, column=1, sticky="se", padx=W_PAD, pady=0)
        but_ok4 = my_button(self, "OK", but_type="small", i=13, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok4.config(
            command=lambda: self.confirm_radio_entry(choice2.get(), 15, 0,
                                                     span=y-1))
        my_label(self, "", lab_type="entry", i=15, j=0, xpad=INDENT_PADx)
        txt_9th = "6. Quel nom donnez-vous au fichier qui sera créé?"
        my_label(self, txt_9th, i=16, ypad=BUT_PADy)
        new_name = tk.StringVar()
        my_entry(self, new_name, i=16, j=1, w=20)
        but_ok3 = my_button(self, "OK", but_type="small", i=16, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok3.config(
            command=lambda: self.confirm_filename_entry(new_name.get(), 17, 0,
                                                        span=y - 1))
        my_label(self, "", lab_type="entry", i=17, j=0, xpad=INDENT_PADx)
        but_execute = my_button(self, "Exécuter", i=18, but_w=10,
                                ypad=BUT_MAIN_PADy, col_span=y)
        but_execute.config(command=lambda: self.combine_function(19, 0,
                                                                 span=y))
        my_label(self, "", lab_type="entry", i=19, j=0, xpad=INDENT_PADx)
        # Done/Quit Button
        but_quit = my_button(self, "Quitter", but_type="main", i=20, but_w=8,
                             ypad=BUT_MAIN_PADy, col_span=y)
        but_quit.config(command=lambda: master.quit_window(self))

    def get_file(self, x, y, span=1):
        if self.fileLabel is not None:
            self.fileLabel.destroy()
        else:
            pass
        self.file.select_file()
        self.fileLabel = my_label(self, self.file.name, lab_type="entry",
                                  i=x, j=y, xpad=INDENT_PADx, col_span=span)
        if self.file.flag is False:
            self.fileLabel.config(fg=RED)
            self.entryFlag = False
        else:
            self.entryFlag = True

    def confirm_int_entry(self, value_str, x, y, span=1):
        if self.pageIndexLabel is not None:
            self.pageIndexLabel.destroy()
        else:
            pass
        # Check if a file was selected at previous step
        if self.file.flag is False:     # No file, return
            self.pageIndexFlag = False
            text = "Vérifier qu'un fichier a été sélectionné."
        else:                           # File, continue
            try:
                self.pageIndex = int(value_str)
                # Check user input
                # If pageIndex, check if the file contains it
                input_file = open(self.file.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                nb_pages = reader.getNumPages()
                input_file.close()
                # Page not in file, invalid entry
                if self.pageIndex > nb_pages:
                    self.pageIndexFlag = False
                    text = "Pas de page " + str(self.pageIndex) +\
                           " dans le fichier sélectionné."
                # If zero or negative, invalid entry
                elif self.pageIndex < 0:
                    self.pageIndexFlag = False
                    text = "Entrée invalide."
                else:
                    self.pageIndexFlag = True
                    text = self.pageIndex
            except ValueError:      # If user input is not an integer
                self.pageIndexFlag = False
                text = "Entrée invalide."
        self.pageIndexLabel = my_label(self, text, lab_type="entry", i=x,
                                       j=y, col_span=span)
        if self.pageIndexFlag is False:
            self.pageIndexLabel.config(fg=RED)
            self.entryFlag = False
        else:
            self.entryFlag = True

    def get_file2(self, x, y, span=1):
        if self.file2addLabel is not None:
            self.file2addLabel.destroy()
        else:
            pass
        self.file2add.select_file()
        self.file2addLabel = my_label(self, self.file2add.name, lab_type="entry",
                                      i=x, j=y, xpad=INDENT_PADx,
                                      col_span=span)
        if self.file2add.flag is False:
            self.file2addLabel.config(fg=RED)
            self.entryFlag = False
        else:
            self.entryFlag = True

    def confirm_pages_entry(self, value, x, y, span=1):
        if self.pagesLabel is not None:
            self.pagesLabel.destroy()
        else:
            pass
        if self.pagesEntry is not None:
            self.pagesEntry.destroy()
            self.okButton.destroy()
        else:
            pass
        if self.file2add.flag is False:
            self.pagesFlag = False
            self.pagesText = "Vérifier qu'un fichier a été sélectionné à" \
                             " l'étape précédente."
            self.pagesLabel = my_label(self, self.pagesText,
                                       lab_type="entry", i=x, j=y,
                                       col_span=span)
            self.pagesLabel.config(fg=RED)
        else:
            if value == 1:      # Add whole file
                self.pages = []
                self.pagesFlag = True
                self.entryFlag = True
                input_file = open(self.file2add.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                nb_pages = reader.getNumPages()
                input_file.close()
                for i in range(nb_pages):
                    self.pages.append(i)
                self.pagesText = str(nb_pages) + " page(s)"
                self.pagesLabel = my_label(self, self.pagesText,
                                           lab_type="entry", i=x, j=y,
                                           col_span=span)
            elif value == 2:    # Range of pages in the file
                self.pagesText = "Veuillez inscrire la sélection de page."
                self.pagesLabel = my_label(self, self.pagesText,
                                           lab_type="entry", i=x, j=y,
                                           col_span=span)
                self.pagesLabel.config(fg=FG6)
                page_index = tk.StringVar()
                self.pagesEntry = my_entry(self, page_index, i=10, j=1, w=20)
                self.okButton = my_button(self, "OK", but_type="small", i=10,
                                          j=2, but_w=5, align="left",
                                          xpad=(INDENT_PADx, 0), ypad=0)
                self.okButton.config(
                    command=lambda: self.confirm_int_entry2(page_index.get(),
                                                            x, y, span=2))
            else:               # If no selection
                self.pagesFlag = False
                self.entryFlag = False
                self.pagesText = "Veuillez sélectionner une option."
                self.pagesLabel = my_label(self, self.pagesText,
                                           lab_type="entry", i=x, j=y,
                                           col_span=span)
                self.pagesLabel.config(fg=RED)

    def confirm_int_entry2(self, value_str, x, y, span=1):
        if self.pagesLabel is not None:
            self.pagesLabel.destroy()
        else:
            pass
        try:
            # Split user string to get pages and ranges of pages
            pages_list = value_str.split(",")
            series_str = []
            self.pages = []
            for element in pages_list:
                if "-" in element:
                    series_str.append(element.split("-"))
                else:
                    #  Do -1 because pyPdf2 page 1 = page 0
                    self.pages.append(int(element) - 1)
            if series_str or self.pages:
                self.pagesFlag = True
                self.pagesText = "Page(s) " + value_str
            else:
                self.pagesFlag = False
                self.pagesText = "Entrée invalide."
            if series_str:
                for block in series_str:
                    # If block element size not 2, invalid entry
                    if len(block) != 2:
                        self.pagesFlag = False
                        self.pagesText = "Entrée invalide."
                        break
                    else:  # Create all pages in the block
                        start = int(block[0]) - 1
                        self.pages.append(start)
                        end = int(block[1]) - 1
                        diff = end - start - 1
                        for i in range(diff):
                            start = start + 1
                            self.pages.append(start)
                        self.pages.append(end)
            else:
                del series_str
            self.pages.sort()
            # Check user input
            # If zero or negative, invalid entry
            # Page not in file, invalid entry
            input_file = open(self.file2add.path, "rb")
            reader = Pdf.PdfFileReader(input_file)
            nb_pages = reader.getNumPages()
            input_file.close()
            for n in self.pages:
                if n < 0:
                    self.pagesFlag = False
                    self.pagesText = "Entrée invalide."
                    break
                elif n >= nb_pages:
                    self.pagesFlag = False
                    n = n + 1
                    self.pagesText = "Pas de page " + str(n) + \
                                     " dans le fichier sélectionné."
                    break
                else:
                    pass
        except ValueError:
            self.pagesFlag = False
            self.pagesText = "Entrée invalide."
        self.pagesLabel = my_label(self, self.pagesText, lab_type="entry",
                                   i=x, j=y, col_span=span)
        if self.pagesFlag is False:
            self.pagesLabel.config(fg=RED)
            self.entryFlag = False
        else:
            self.entryFlag = True

    def confirm_radio_entry(self, value, x, y, span=1):
        if self.radioLabel is not None:
            self.radioLabel.destroy()
        else:
            pass
        if value == 1:  # Same directory as input file
            if self.file.flag is False:  # Check if input file exists
                self.radioFlag = False
                text = "Vérifier qu'un fichier a été sélectionné."
            else:
                self.radioFlag = True
                self.newFile.directory = self.file.directory
                text = self.newFile.directory
        elif value == 2:  # Other directory than input file
            self.newFile.select_directory()  # Select new directory
            if self.newFile.directory == "Aucune sélection.":  # Check if a selection was made
                self.radioFlag = False
                text = self.newFile.directory
            else:
                self.radioFlag = True
                text = self.newFile.directory
        else:  # If no selection
            self.radioFlag = False
            text = "Veuillez sélectionner une option."
        # Check if file already exists or not
        if self.radioFlag is True and self.newFile.name and self.newFile.flag is True:
            self.newFile.path = self.newFile.directory + self.newFile.name
            if os.path.exists(self.newFile.path):
                self.radioFlag = False
                text = "Un fichier avec le même nom existe déjà dans ce" \
                       " dossier.\nVeuillez changer le nom du nouveau fichier" \
                       " ou choisir un autre dossier."
                self.newFile.flag = False
            else:
                self.newFile = File(self.newFile.path)
                self.newFile.flag = True
        else:
            pass
        self.radioLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.radioFlag is False:
            self.radioLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_filename_entry(self, value_str, x, y, span=1):
        self.newFile.name = None
        if self.newFileLabel is not None:
            self.newFileLabel.destroy()
        else:
            pass
        if self.radioFlag is False:
            self.newFile.flag = False
            text = "Veuillez choisir un dossier à l'étape précédente."
            self.newFileLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, col_span=span)
            self.newFileLabel.config(fg=RED)
        else:
            if value_str == "":  # If user input is empty, invalid entry
                self.newFile.flag = False
                text = "Veuillez inscrire un nom."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            # If special characters in user input, invalid entry
            elif check_special_character(value_str):
                self.newFile.flag = False
                text = "Veuillez ne pas inclure de caractères spéciaux."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            else:
                # Making sure file name ends with file type
                if value_str[-4:] == ".pdf":
                    name = value_str
                else:
                    name = value_str + ".pdf"
                self.newFile.name = name
                self.newFile.path = self.newFile.directory + self.newFile.name
                if os.path.exists(self.newFile.path):
                    self.newFile.flag = False
                    text = "Un fichier avec le même nom existe déjà dans ce" \
                           " dossier.\nVeuillez changer le nom du nouveau fichier" \
                           " ou choisir un autre dossier."
                    self.newFileLabel = my_label(self, text, lab_type="entry",
                                                 i=x, j=y, col_span=span)
                    self.newFileLabel.config(fg=RED)
                else:
                    self.newFile = File(self.newFile.path)
                    self.newFile.flag = True
                    self.entryFlag = True
                    self.newFileLabel = my_label(self, value_str, lab_type="entry",
                                                 i=x, j=y, col_span=span)

    def combine_function(self, x, y, span=1):
        if self.executeLabel is not None:
            self.executeLabel.destroy()
        else:
            pass
        self.executeLabel = my_label(self, "...", lab_type="entry",
                                     i=x, j=y, xpad=0, col_span=span)
        if self.file.flag is False or self.pageIndexFlag is False or\
                self.file2add.flag is False or self.pagesFlag is False or\
                self.newFile.flag is False or self.radioFlag is False or\
                self.entryFlag is False:
            text = "Erreur. Veuillez vérifier que vos entrées sont valides " \
               "et que vous avez appuyé sur \"OK\"."
            self.executeLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, xpad=0,
                                         col_span=span)
            self.executeLabel.config(fg=RED)
        else:
            try:
                # Read file
                input_file1 = open(self.file.path, "rb")
                reader1 = Pdf.PdfFileReader(input_file1)
                input_file2 = open(self.file2add.path, "rb")
                reader2 = Pdf.PdfFileReader(input_file2)
                # Creating new file
                combine = Pdf.PdfFileWriter()
                # Combine files
                for i in range(self.pageIndex):
                    p = reader1.getPage(i)
                    combine.addPage(p)
                for i in range(reader2.getNumPages()):
                    if i in self.pages:
                        p = reader2.getPage(i)
                        combine.addPage(p)
                    else:
                        pass
                k = self.pageIndex
                for i in range(reader1.getNumPages() - self.pageIndex):
                    p = reader1.getPage(k)
                    combine.addPage(p)
                    k = k + 1
                # Write new file
                out = open(self.newFile.path, "wb")
                combine.write(out)
                input_file1.close()
                input_file2.close()
                out.close()
                self.executeLabel.config(text="...Terminé.")
            except PermissionError:
                text = "Erreur. Vérifier que le fichier " + \
                       self.newFile.name + \
                       " n'est pas déjà ouvert ou en lecture seule."
                self.executeLabel.config(text=text, fg=RED)


class CombineMultiPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg=BG1)
        # Setup graphical interface
        self.graphical_interface(master)
        # Flag for entries
        self.entryFlag = False
        # File Variables
        self.file = File()
        self.newFile = File()
        # Variables for combining files
        self.radioFlag = False
        # Label Variables
        self.fileLabel = None
        self.newFileLabel = None
        self.radioLabel = None
        self.executeLabel = None

    def graphical_interface(self, master):
        # Row and columns configuration
        x = 14
        for k in range(x):
            self.grid_rowconfigure(k, weight=1)
        y = 3
        for k in range(y):
            self.grid_columnconfigure(k, weight=1)
        # Content
        # Intro
        txt_return = "Retour"
        but_return = my_button(self, txt_return, but_type="main", but_w=7,
                               align="left")
        but_return.config(command=lambda: master.return_window(self, StartPage))
        txt_intro = "Combiner plusieurs fichiers"
        my_label(self, txt_intro, lab_type="intro", i=1, col_span=y)
        txt_warning = "IMPORTANT: Veuillez suivre les étapes dans l'ordre et " \
                      "valider avec \"OK\" après chaque étape.\nSi vous retournez " \
                      "à une étape antérieure, veuillez revalider avec \"OK\" " \
                      "toutes les étapes subséquentes."
        my_label(self, txt_warning, lab_type="small", i=2, col_span=y)
        # Main
        txt_1st = "1. Veuillez sélectionner les fichiers que vous" \
                  " souhaitez\ncombiner."
        txt_2nd = "Les fichiers à combiner doivent être dans le même" \
                   " dossier.\nIls seront combinés dans l'ordre " \
                   "qu'ils sont affichés dans ce dossier."
        my_label(self, txt_1st, i=3, xpad=(W_PAD, 0), ypad=BUT_PADy)
        my_label(self, txt_2nd, lab_type="small", i=4, align="left")
        but_select = my_button(self, "Sélectionner", but_type="small", i=3,
                               j=1, but_w=11, align="right",
                               xpad=0, ypad=W_PAD)
        but_select.config(command=lambda: self.get_files(5, 0, span=y-1))
        my_label(self, "", lab_type="entry", i=5, j=0, xpad=INDENT_PADx)
        txt_3rd = "2. Souhaitez-vous enregistrer le nouveau fichier" \
                  " dans\nle même dossier que le fichier d'origine?"
        txt_4th = "Si vous choisissez \"Non\", veuillez sélectionner le " \
                  "dossier de destination."
        my_label(self, txt_3rd, i=6, ypad=(BUT_PADy, 0))
        my_label(self, txt_4th, lab_type="small", i=7, align="left")
        choice2 = tk.IntVar()
        tk.Radiobutton(self, text="Oui", variable=choice2, value=1,
                       activebackground=BG1, bg=BG1).grid(
            row=6, column=1, sticky="ne", padx=W_PAD, pady=0)
        tk.Radiobutton(self, text="Non", variable=choice2, value=2,
                       activebackground=BG1, bg=BG1).grid(
            row=6, column=1, sticky="se", padx=W_PAD, pady=0)
        but_ok4 = my_button(self, "OK", but_type="small", i=6, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok4.config(
            command=lambda: self.confirm_radio_entry(choice2.get(), 8, 0,
                                                     span=y-1))
        my_label(self, "", lab_type="entry", i=8, j=0, xpad=INDENT_PADx)
        txt_5th = "3. Quel nom donnez-vous au fichier qui sera créé?"
        my_label(self, txt_5th, i=9, ypad=BUT_PADy)
        new_name = tk.StringVar()
        my_entry(self, new_name, i=9, j=1, w=20)
        but_ok3 = my_button(self, "OK", but_type="small", i=9, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok3.config(
            command=lambda: self.confirm_filename_entry(new_name.get(), 10, 0,
                                                        span=y - 1))
        my_label(self, "", lab_type="entry", i=10, j=0, xpad=INDENT_PADx)
        but_execute = my_button(self, "Exécuter", i=11, but_w=10,
                                ypad=BUT_MAIN_PADy, col_span=y)
        but_execute.config(command=lambda: self.combine_function(12, 0,
                                                                 span=y))
        my_label(self, "", lab_type="entry", i=12, j=0, xpad=INDENT_PADx)
        # Done/Quit Button
        but_quit = my_button(self, "Quitter", but_type="main", i=13, but_w=8,
                             ypad=BUT_MAIN_PADy, col_span=y)
        but_quit.config(command=lambda: master.quit_window(self))

    def get_files(self, x, y, span=1):
        if self.fileLabel is not None:
            self.fileLabel.destroy()
        else:
            pass
        self.file.select_multi_files()
        if self.file.flag is True:
            txt = str(len(self.file.path)) + " fichiers sélectionnés"
            self.fileLabel = my_label(self, txt, lab_type="entry",
                                      i=x, j=y, xpad=INDENT_PADx, col_span=span)
            self.entryFlag = True
        else:
            self.fileLabel = my_label(self, self.file.path, lab_type="entry",
                                      i=x, j=y, xpad=INDENT_PADx, col_span=span)
            self.fileLabel.config(fg=RED)
            self.entryFlag = False

    def confirm_radio_entry(self, value, x, y, span=1):
        if self.radioLabel is not None:
            self.radioLabel.destroy()
        else:
            pass
        if value == 1:  # Same directory as input file
            if self.file.flag is False:  # Check if input file exists
                self.radioFlag = False
                text = "Vérifier qu'un fichier a été sélectionné."
            else:
                self.radioFlag = True
                self.newFile.directory = self.file.directory[0]
                text = self.newFile.directory
        elif value == 2:  # Other directory than input file
            self.newFile.select_directory()  # Select new directory
            if self.newFile.directory == "Aucune sélection.":  # Check if a selection was made
                self.radioFlag = False
                text = self.newFile.directory
            else:
                self.radioFlag = True
                text = self.newFile.directory
        else:  # If no selection
            self.radioFlag = False
            text = "Veuillez sélectionner une option."
        # Check if file already exists or not
        if self.radioFlag is True and self.newFile.name and self.newFile.flag is True:
            self.newFile.path = self.newFile.directory + self.newFile.name
            if os.path.exists(self.newFile.path):
                self.radioFlag = False
                text = "Un fichier avec le même nom existe déjà dans ce" \
                       " dossier.\nVeuillez changer le nom du nouveau fichier" \
                       " ou choisir un autre dossier."
                self.newFile.flag = False
            else:
                self.newFile = File(self.newFile.path)
                self.newFile.flag = True
        else:
            pass
        self.radioLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.radioFlag is False:
            self.radioLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_filename_entry(self, value_str, x, y, span=1):
        self.newFile.name = None
        if self.newFileLabel is not None:
            self.newFileLabel.destroy()
        else:
            pass
        if self.radioFlag is False:
            self.newFile.flag = False
            text = "Veuillez choisir un dossier à l'étape précédente."
            self.newFileLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, col_span=span)
            self.newFileLabel.config(fg=RED)
        else:
            if value_str == "":  # If user input is empty, invalid entry
                self.newFile.flag = False
                text = "Veuillez inscrire un nom."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            # If special characters in user input, invalid entry
            elif check_special_character(value_str):
                self.newFile.flag = False
                text = "Veuillez ne pas inclure de caractères spéciaux."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            else:
                # Making sure file name ends with file type
                if value_str[-4:] == ".pdf":
                    name = value_str
                else:
                    name = value_str + ".pdf"
                self.newFile.name = name
                self.newFile.path = self.newFile.directory + self.newFile.name
                if os.path.exists(self.newFile.path):
                    self.newFile.flag = False
                    text = "Un fichier avec le même nom existe déjà dans ce" \
                           " dossier.\nVeuillez changer le nom du nouveau fichier" \
                           " ou choisir un autre dossier."
                    self.newFileLabel = my_label(self, text, lab_type="entry",
                                                 i=x, j=y, col_span=span)
                    self.newFileLabel.config(fg=RED)
                else:
                    self.newFile = File(self.newFile.path)
                    self.newFile.flag = True
                    self.entryFlag = True
                    self.newFileLabel = my_label(self, value_str, lab_type="entry",
                                                 i=x, j=y, col_span=span)

    def combine_function(self, x, y, span=1):
        if self.executeLabel is not None:
            self.executeLabel.destroy()
        else:
            pass
        self.executeLabel = my_label(self, "...", lab_type="entry",
                                     i=x, j=y, xpad=0, col_span=span)
        if self.file.flag is False or self.newFile.flag is False or self.radioFlag is False:
            text = "Erreur. Veuillez vérifier que vos entrées sont valides " \
               "et que vous avez appuyé sur \"OK\"."
            self.executeLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, xpad=0,
                                         col_span=span)
            self.executeLabel.config(fg=RED)
        else:
            try:
                # Creating the merger
                merger = Pdf.PdfFileMerger()
                # Combine files
                for path in self.file.path:
                    merger.append(path)
                # Write new file
                out = open(self.newFile.path, "wb")
                merger.write(out)
                out.close()
                self.executeLabel.config(text="...Terminé.")
            except PermissionError:
                text = "Erreur. Vérifier que le fichier " + \
                       self.newFile.name + \
                       " n'est pas déjà ouvert ou en lecture seule."
                self.executeLabel.config(text=text, fg=RED)


class DeletePage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg=BG1)
        # Setup graphical interface
        self.graphical_interface(master)
        # Flag for entries
        self.entryFlag = False
        # File Variables
        self.file = File()
        self.newFile = File()
        # Variables for deleting pages
        self.pages = None
        self.pagesFlag = False
        self.radioFlag = False
        # Label Variables
        self.fileLabel = None
        self.pagesLabel = None
        self.newFileLabel = None
        self.radioLabel = None
        self.executeLabel = None

    def graphical_interface(self, master):
        # Row and columns configuration
        x = 16
        for k in range(x):
            self.grid_rowconfigure(k, weight=1)
        y = 3
        for k in range(y):
            self.grid_columnconfigure(k, weight=1)
        # Content
        # Intro
        txt_return = "Retour"
        but_return = my_button(self, txt_return, but_type="main", but_w=7,
                               align="left")
        but_return.config(command=lambda: master.return_window(self, StartPage))
        txt_intro = "Supprimer des pages"
        my_label(self, txt_intro, lab_type="intro", i=1, col_span=y)
        txt_warning = "IMPORTANT: Veuillez suivre les étapes dans l'ordre et " \
                      "valider avec \"OK\" après chaque étape.\nSi vous retournez " \
                      "à une étape antérieure, veuillez revalider avec \"OK\" " \
                      "toutes les étapes subséquentes."
        my_label(self, txt_warning, lab_type="small", i=2, col_span=y)
        # Main
        txt_1st = "1. Veuillez sélectionner le fichier dans lequel vous" \
                  " souhaitez\nsupprimer des pages."
        my_label(self, txt_1st, i=3, ypad=BUT_PADy)
        but_select = my_button(self, "Sélectionner", but_type="small", i=3,
                               j=1, but_w=11, align="right", xpad=0,
                               ypad=W_PAD)
        but_select.config(command=lambda: self.get_file(4, 0, span=y-1))
        my_label(self, "", lab_type="entry", i=4, j=0, xpad=INDENT_PADx)
        txt_2nd = "2. Quelle(s) page(s) du fichier sélectionné désirez-vous"\
                  "\nsupprimer?"
        my_label(self, txt_2nd, i=5, ypad=(BUT_PADy, 0))
        txt_3rd = "Veuillez séparer les numéros de page par des virgules et" \
                  " les étendues de pages\npar des traits-d'union." \
                  "\nEx: 1,3,5-7,12"
        my_label(self, txt_3rd, lab_type="small", i=6, xpad=W_PAD,
                 align="left", ypad=(0, BUT_PADy))
        page_index = tk.StringVar()
        my_entry(self, page_index, i=5, j=1, w=20)
        but_ok1 = my_button(self, "OK", but_type="small", i=5, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok1.config(
            command=lambda: self.confirm_int_entry(page_index.get(), 7, 0,
                                                   span=y-1))
        my_label(self, "", lab_type="entry", i=7, j=0, xpad=INDENT_PADx)
        txt_4th = "3. Souhaitez-vous enregistrer le nouveau fichier" \
                  " dans le\nmême dossier que le fichier d'origine?"
        txt_5th = "Si vous choisissez \"Non\", veuillez sélectionner le dossier" \
                  " de destination."
        my_label(self, txt_4th, i=8, ypad=(BUT_PADy, 0))
        my_label(self, txt_5th, lab_type="small", i=9, align="left")
        choice = tk.IntVar()
        tk.Radiobutton(self, text="Oui", variable=choice, value=1,
                       activebackground=BG1, bg=BG1).grid(
            row=8, column=1, sticky="ne", padx=W_PAD, pady=0)
        tk.Radiobutton(self, text="Non", variable=choice, value=2,
                       activebackground=BG1, bg=BG1).grid(
            row=8, column=1, sticky="se", padx=W_PAD, pady=0)
        but_ok4 = my_button(self, "OK", but_type="small", i=8, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok4.config(
            command=lambda: self.confirm_radio_entry(choice.get(), 10, 0,
                                                     span=y - 1))
        my_label(self, "", lab_type="entry", i=10, j=0, xpad=INDENT_PADx)
        txt_6th = "4. Quel nom donnez-vous au fichier qui sera créé?"
        my_label(self, txt_6th, i=11, ypad=BUT_PADy)
        new_name = tk.StringVar()
        my_entry(self, new_name, i=11, j=1, w=20)
        but_ok2 = my_button(self, "OK", but_type="small", i=11, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok2.config(
            command=lambda: self.confirm_filename_entry(new_name.get(), 12, 0,
                                                        span=y - 1))
        my_label(self, "", lab_type="entry", i=12, j=0, xpad=INDENT_PADx)
        but_execute = my_button(self, "Exécuter", i=13, but_w=10,
                                ypad=BUT_MAIN_PADy, col_span=y)
        but_execute.config(command=lambda: self.delete_function(14, 0, span=y))
        my_label(self, "", lab_type="entry", i=14, j=0, xpad=INDENT_PADx)
        # Done/Quit Button
        but_quit = my_button(self, "Quitter", but_type="main", i=15, but_w=8,
                             ypad=BUT_MAIN_PADy, col_span=y)
        but_quit.config(command=lambda: master.quit_window(self))

    def get_file(self, x, y, span=1):
        if self.fileLabel is not None:
            self.fileLabel.destroy()
        else:
            pass
        self.file.select_file()
        self.fileLabel = my_label(self, self.file.name, lab_type="entry",
                                  i=x, j=y, xpad=INDENT_PADx, col_span=span)
        if self.file.flag is False:
            self.fileLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_int_entry(self, value_str, x, y, span=1):
        if self.pagesLabel is not None:
            self.pagesLabel.destroy()
        else:
            pass
        # Check if a file was selected at previous step
        if self.file.flag is False:         # No file, return
            self.pagesFlag = False
            text = "Vérifier qu'un fichier a été sélectionné."
        else:                               # File, continue
            try:
                # Split user string to get pages and ranges of pages
                pages_list = value_str.split(",")
                series_str = []
                self.pages = []
                for element in pages_list:
                    if "-" in element:
                        series_str.append(element.split("-"))
                    else:
                        #  Do -1 because pyPdf2 page 1 = page 0
                        self.pages.append(int(element) - 1)
                if series_str or self.pages:
                    self.pagesFlag = True
                    text = value_str
                else:
                    self.pagesFlag = False
                    text = "Entrée invalide."
                if series_str:
                    for block in series_str:
                        # If block element size not 2, invalid entry
                        if len(block) != 2:
                            self.pagesFlag = False
                            text = "Entrée invalide."
                            break
                        else:   # Create all pages in the block
                            start = int(block[0]) - 1
                            self.pages.append(start)
                            end = int(block[1]) - 1
                            diff = end - start - 1
                            for i in range(diff):
                                start = start + 1
                                self.pages.append(start)
                            self.pages.append(end)
                else:
                    del series_str
                self.pages.sort()
                # Check user input
                # If zero or negative, invalid entry
                # Page not in file, invalid entry
                input_file = open(self.file.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                nb_pages = reader.getNumPages()
                input_file.close()
                for n in self.pages:
                    if n < 0:
                        self.pagesFlag = False
                        text = "Entrée invalide."
                        break
                    elif n >= nb_pages:
                        self.pagesFlag = False
                        n = n + 1
                        text = "Pas de page " + str(n) + \
                               " dans le fichier sélectionné."
                        break
                    else:
                        pass
            except ValueError:
                self.pagesFlag = False
                text = "Entrée invalide."
        self.pagesLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.pagesFlag is False:
            self.pagesLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_radio_entry(self, value, x, y, span=1):
        if self.radioLabel is not None:
            self.radioLabel.destroy()
        else:
            pass
        if value == 1:  # Same directory as input file
            if self.file.flag is False:  # Check if input file exists
                self.radioFlag = False
                text = "Vérifier qu'un fichier a été sélectionné."
            else:
                self.radioFlag = True
                self.newFile.directory = self.file.directory
                text = self.newFile.directory
        elif value == 2:  # Other directory than input file
            self.newFile.select_directory()  # Select new directory
            if self.newFile.directory == "Aucune sélection.":  # Check if a selection was made
                self.radioFlag = False
                text = self.newFile.directory
            else:
                self.radioFlag = True
                text = self.newFile.directory
        else:  # If no selection
            self.radioFlag = False
            text = "Veuillez sélectionner une option."
        # Check if file already exists or not
        if self.radioFlag is True and self.newFile.name and self.newFile.flag is True:
            self.newFile.path = self.newFile.directory + self.newFile.name
            if os.path.exists(self.newFile.path):
                self.radioFlag = False
                text = "Un fichier avec le même nom existe déjà dans ce" \
                       " dossier.\nVeuillez changer le nom du nouveau fichier" \
                       " ou choisir un autre dossier."
                self.newFile.flag = False
            else:
                self.newFile = File(self.newFile.path)
                self.newFile.flag = True
        else:
            pass
        self.radioLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.radioFlag is False:
            self.radioLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_filename_entry(self, value_str, x, y, span=1):
        self.newFile.name = None
        if self.newFileLabel is not None:
            self.newFileLabel.destroy()
        else:
            pass
        if self.radioFlag is False:
            self.newFile.flag = False
            text = "Veuillez choisir un dossier à l'étape précédente."
            self.newFileLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, col_span=span)
            self.newFileLabel.config(fg=RED)
        else:
            if value_str == "":  # If user input is empty, invalid entry
                self.newFile.flag = False
                text = "Veuillez inscrire un nom."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            # If special characters in user input, invalid entry
            elif check_special_character(value_str):
                self.newFile.flag = False
                text = "Veuillez ne pas inclure de caractères spéciaux."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            else:
                # Making sure file name ends with file type
                if value_str[-4:] == ".pdf":
                    name = value_str
                else:
                    name = value_str + ".pdf"
                self.newFile.name = name
                self.newFile.path = self.newFile.directory + self.newFile.name
                if os.path.exists(self.newFile.path):
                    self.newFile.flag = False
                    text = "Un fichier avec le même nom existe déjà dans ce" \
                           " dossier.\nVeuillez changer le nom du nouveau fichier" \
                           " ou choisir un autre dossier."
                    self.newFileLabel = my_label(self, text, lab_type="entry",
                                                 i=x, j=y, col_span=span)
                    self.newFileLabel.config(fg=RED)
                else:
                    self.newFile = File(self.newFile.path)
                    self.newFile.flag = True
                    self.entryFlag = True
                    self.newFileLabel = my_label(self, value_str, lab_type="entry",
                                                 i=x, j=y, col_span=span)

    def delete_function(self, x, y, span=1):
        if self.executeLabel is not None:
            self.executeLabel.destroy()
        else:
            pass
        self.executeLabel = my_label(self, "...", lab_type="entry",
                                     i=x, j=y, xpad=0, col_span=span)
        if self.file.flag is False or self.pagesFlag is False or \
                self.newFile.flag is False or self.radioFlag is False:
            text = "Erreur. Veuillez vérifier que vos entrées sont valides\n"\
                   "et que vous avez appuyé sur \"OK\"."
            self.executeLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, xpad=0,
                                         col_span=span)
            self.executeLabel.config(fg=RED)
        else:
            try:
                # Read file
                input_file = open(self.file.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                # Creating new file
                deleted = Pdf.PdfFileWriter()
                # Delete pages
                for i in range(reader.getNumPages()):
                    if i not in self.pages:
                        p = reader.getPage(i)
                        deleted.addPage(p)
                    else:
                        pass
                # Write new file
                out = open(self.newFile.path, "wb")
                deleted.write(out)
                input_file.close()
                out.close()
                self.executeLabel.config(text="...Terminé.")
            except PermissionError:
                text = "Erreur. Vérifier que le fichier " + \
                       self.newFile.name + \
                       " n'est pas déjà ouvert ou en lecture seule."
                self.executeLabel.config(text=text, fg=RED)


class ExtractPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg=BG1)
        # Setup graphical interface
        self.graphical_interface(master)
        # Flag for entries
        self.entryFlag = False
        # File Variables
        self.file = File()
        self.newFile = File()
        # Variables for extracting pages
        self.pages = None
        self.pagesFlag = False
        self.radioFlag = False
        # Label Variables
        self.fileLabel = None
        self.pagesLabel = None
        self.newFileLabel = None
        self.radioLabel = None
        self.executeLabel = None

    def graphical_interface(self, master):
        # Row and columns configuration
        x = 16
        for k in range(x):
            self.grid_rowconfigure(k, weight=1)
        y = 3
        for k in range(y):
            self.grid_columnconfigure(k, weight=1)
        # Content
        # Intro
        txt_return = "Retour"
        but_return = my_button(self, txt_return, but_type="main", but_w=7,
                               align="left")
        but_return.config(command=lambda: master.return_window(self, StartPage))
        txt_intro = "Extraire des pages dans un nouveau fichier"
        my_label(self, txt_intro, lab_type="intro", i=1, col_span=y)
        txt_warning = "IMPORTANT: Veuillez suivre les étapes dans l'ordre et " \
                      "valider avec \"OK\" après chaque étape.\nSi vous retournez " \
                      "à une étape antérieure, veuillez revalider avec \"OK\" " \
                      "toutes les étapes subséquentes."
        my_label(self, txt_warning, lab_type="small", i=2, col_span=y)
        # Main
        txt_1st = "1. Veuillez sélectionner le fichier auquel vous" \
                  " souhaitez\nextraire des pages."
        my_label(self, txt_1st, i=3, ypad=BUT_PADy)
        but_select = my_button(self, "Sélectionner", but_type="small", i=3,
                               j=1, but_w=11, align="right", xpad=0,
                               ypad=W_PAD)
        but_select.config(command=lambda: self.get_file(4, 0, span=y-1))
        my_label(self, "", lab_type="entry", i=4, j=0, xpad=INDENT_PADx)
        txt_2nd = "2. Quelle(s) page(s) du fichier sélectionné désirez-vous"\
                  "\nextraire?"
        my_label(self, txt_2nd, i=5, ypad=(BUT_PADy, 0))
        txt_3rd = "Veuillez séparer les numéros de page par des virgules et" \
                  " les étendues de pages\npar des traits-d'union." \
                  "\nEx: 1,3,5-7,12"
        my_label(self, txt_3rd, lab_type="small", i=6, xpad=W_PAD,
                 align="left", ypad=(0, BUT_PADy))
        page_index = tk.StringVar()
        my_entry(self, page_index, i=5, j=1, w=20)
        but_ok1 = my_button(self, "OK", but_type="small", i=5, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok1.config(
            command=lambda: self.confirm_int_entry(page_index.get(), 7, 0,
                                                   span=y-1))
        my_label(self, "", lab_type="entry", i=7, j=0, xpad=INDENT_PADx)
        txt_4th = "3. Souhaitez-vous enregistrer le nouveau fichier" \
                  " dans le\nmême dossier que le fichier d'origine?"
        txt_5th = "Si vous choisissez \"Non\", veuillez sélectionner le dossier" \
                  " de destination."
        my_label(self, txt_4th, i=8, ypad=(BUT_PADy, 0))
        my_label(self, txt_5th, lab_type="small", i=9, align="left")
        choice = tk.IntVar()
        tk.Radiobutton(self, text="Oui", variable=choice, value=1,
                       activebackground=BG1, bg=BG1).grid(
            row=8, column=1, sticky="ne", padx=W_PAD, pady=0)
        tk.Radiobutton(self, text="Non", variable=choice, value=2,
                       activebackground=BG1, bg=BG1).grid(
            row=8, column=1, sticky="se", padx=W_PAD, pady=0)
        but_ok4 = my_button(self, "OK", but_type="small", i=8, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok4.config(
            command=lambda: self.confirm_radio_entry(choice.get(), 10, 0,
                                                     span=y - 1))
        my_label(self, "", lab_type="entry", i=10, j=0, xpad=INDENT_PADx)
        txt_6th = "4. Quel nom donnez-vous au fichier qui sera créé?"
        my_label(self, txt_6th, i=11, ypad=BUT_PADy)
        new_name = tk.StringVar()
        my_entry(self, new_name, i=11, j=1, w=20)
        but_ok2 = my_button(self, "OK", but_type="small", i=11, j=2, but_w=5,
                            align="left", xpad=(INDENT_PADx, 0), ypad=0)
        but_ok2.config(
            command=lambda: self.confirm_filename_entry(new_name.get(), 12, 0,
                                                        span=y - 1))
        my_label(self, "", lab_type="entry", i=12, j=0, xpad=INDENT_PADx)
        but_execute = my_button(self, "Exécuter", i=13, but_w=10,
                                ypad=BUT_MAIN_PADy, col_span=y)
        but_execute.config(command=lambda: self.extract_function(14, 0, span=y))
        my_label(self, "", lab_type="entry", i=14, j=0, xpad=INDENT_PADx)
        # Done/Quit Button
        but_quit = my_button(self, "Quitter", but_type="main", i=15, but_w=8,
                             ypad=BUT_MAIN_PADy, col_span=y)
        but_quit.config(command=lambda: master.quit_window(self))

    def get_file(self, x, y, span=1):
        if self.fileLabel is not None:
            self.fileLabel.destroy()
        else:
            pass
        self.file.select_file()
        self.fileLabel = my_label(self, self.file.name, lab_type="entry",
                                  i=x, j=y, xpad=INDENT_PADx, col_span=span)
        if self.file.flag is False:
            self.fileLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_int_entry(self, value_str, x, y, span=1):
        if self.pagesLabel is not None:
            self.pagesLabel.destroy()
        else:
            pass
        # Check if a file was selected at previous step
        if self.file.flag is False:         # No file, return
            self.pagesFlag = False
            text = "Vérifier qu'un fichier a été sélectionné."
        else:                               # File, continue
            try:
                # Split user string to get pages and ranges of pages
                pages_list = value_str.split(",")
                series_str = []
                self.pages = []
                for element in pages_list:
                    if "-" in element:
                        series_str.append(element.split("-"))
                    else:
                        #  Do -1 because pyPdf2 page 1 = page 0
                        self.pages.append(int(element) - 1)
                if series_str or self.pages:
                    self.pagesFlag = True
                    text = value_str
                else:
                    self.pagesFlag = False
                    text = "Entrée invalide."
                if series_str:
                    for block in series_str:
                        # If block element size not 2, invalid entry
                        if len(block) != 2:
                            self.pagesFlag = False
                            text = "Entrée invalide."
                            break
                        else:   # Create all pages in the block
                            start = int(block[0]) - 1
                            self.pages.append(start)
                            end = int(block[1]) - 1
                            diff = end - start - 1
                            for i in range(diff):
                                start = start + 1
                                self.pages.append(start)
                            self.pages.append(end)
                else:
                    del series_str
                self.pages.sort()
                # Check user input
                # If zero or negative, invalid entry
                # Page not in file, invalid entry
                input_file = open(self.file.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                nb_pages = reader.getNumPages()
                input_file.close()
                for n in self.pages:
                    if n < 0:
                        self.pagesFlag = False
                        text = "Entrée invalide."
                        break
                    elif n >= nb_pages:
                        self.pagesFlag = False
                        n = n + 1
                        text = "Pas de page " + str(n) + \
                               " dans le fichier sélectionné."
                        break
                    else:
                        pass
            except ValueError:
                self.pagesFlag = False
                text = "Entrée invalide."
        self.pagesLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.pagesFlag is False:
            self.pagesLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_radio_entry(self, value, x, y, span=1):
        if self.radioLabel is not None:
            self.radioLabel.destroy()
        else:
            pass
        if value == 1:  # Same directory as input file
            if self.file.flag is False:  # Check if input file exists
                self.radioFlag = False
                text = "Vérifier qu'un fichier a été sélectionné."
            else:
                self.radioFlag = True
                self.newFile.directory = self.file.directory
                text = self.newFile.directory
        elif value == 2:  # Other directory than input file
            self.newFile.select_directory()  # Select new directory
            if self.newFile.directory == "Aucune sélection.":  # Check if a selection was made
                self.radioFlag = False
                text = self.newFile.directory
            else:
                self.radioFlag = True
                text = self.newFile.directory
        else:  # If no selection
            self.radioFlag = False
            text = "Veuillez sélectionner une option."
        # Check if file already exists or not
        if self.radioFlag is True and self.newFile.name and self.newFile.flag is True:
            self.newFile.path = self.newFile.directory + self.newFile.name
            if os.path.exists(self.newFile.path):
                self.radioFlag = False
                text = "Un fichier avec le même nom existe déjà dans ce" \
                       " dossier.\nVeuillez changer le nom du nouveau fichier" \
                       " ou choisir un autre dossier."
                self.newFile.flag = False
            else:
                self.newFile = File(self.newFile.path)
                self.newFile.flag = True
        else:
            pass
        self.radioLabel = my_label(self, text, lab_type="entry", i=x, j=y,
                                   col_span=span)
        if self.radioFlag is False:
            self.radioLabel.config(fg=RED)
        else:
            self.entryFlag = True

    def confirm_filename_entry(self, value_str, x, y, span=1):
        self.newFile.name = None
        if self.newFileLabel is not None:
            self.newFileLabel.destroy()
        else:
            pass
        if self.radioFlag is False:
            self.newFile.flag = False
            text = "Veuillez choisir un dossier à l'étape précédente."
            self.newFileLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, col_span=span)
            self.newFileLabel.config(fg=RED)
        else:
            if value_str == "":  # If user input is empty, invalid entry
                self.newFile.flag = False
                text = "Veuillez inscrire un nom."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            # If special characters in user input, invalid entry
            elif check_special_character(value_str):
                self.newFile.flag = False
                text = "Veuillez ne pas inclure de caractères spéciaux."
                self.newFileLabel = my_label(self, text, lab_type="entry",
                                             i=x, j=y, col_span=span)
                self.newFileLabel.config(fg=RED)
            else:
                # Making sure file name ends with file type
                if value_str[-4:] == ".pdf":
                    name = value_str
                else:
                    name = value_str + ".pdf"
                self.newFile.name = name
                self.newFile.path = self.newFile.directory + self.newFile.name
                if os.path.exists(self.newFile.path):
                    self.newFile.flag = False
                    text = "Un fichier avec le même nom existe déjà dans ce" \
                           " dossier.\nVeuillez changer le nom du nouveau fichier" \
                           " ou choisir un autre dossier."
                    self.newFileLabel = my_label(self, text, lab_type="entry",
                                                 i=x, j=y, col_span=span)
                    self.newFileLabel.config(fg=RED)
                else:
                    self.newFile = File(self.newFile.path)
                    self.newFile.flag = True
                    self.entryFlag = True
                    self.newFileLabel = my_label(self, value_str, lab_type="entry",
                                                 i=x, j=y, col_span=span)

    def extract_function(self, x, y, span=1):
        if self.executeLabel is not None:
            self.executeLabel.destroy()
        else:
            pass
        self.executeLabel = my_label(self, "...", lab_type="entry",
                                     i=x, j=y, xpad=0, col_span=span)
        if self.file.flag is False or self.pagesFlag is False or \
                self.newFile.flag is False or self.radioFlag is False:
            text = "Erreur. Veuillez vérifier que vos entrées sont valides\n" \
                   "et que vous avez appuyé sur \"OK\"."
            self.executeLabel = my_label(self, text, lab_type="entry",
                                         i=x, j=y, xpad=0,
                                         col_span=span)
            self.executeLabel.config(fg=RED)
        else:
            try:
                # Read file
                input_file = open(self.file.path, "rb")
                reader = Pdf.PdfFileReader(input_file)
                # Creating new file
                extracted = Pdf.PdfFileWriter()
                # Extract pages
                for i in range(reader.getNumPages()):
                    if i in self.pages:
                        p = reader.getPage(i)
                        extracted.addPage(p)
                    else:
                        pass
                # Write new file
                out = open(self.newFile.path, "wb")
                extracted.write(out)
                input_file.close()
                out.close()
                self.executeLabel.config(text="...Terminé.")
            except PermissionError:
                text = "Erreur. Vérifier que le fichier " + \
                       self.newFile.name + \
                       " n'est pas déjà ouvert ou en lecture seule."
                self.executeLabel.config(text=text, fg=RED)


class File:

    def __init__(self, path=None):
        self.path = path
        if self.path is not None:
            self.directory = os.path.dirname(self.path) + "/"
            self.name = ntpath.basename(self.path)
            [self.nameOnly, self.type] = os.path.splitext(self.name)
            self.type = self.type[1:]
            self.flag = True
        else:
            self.directory = None
            self.name = None
            self.nameOnly = None
            self.type = None
            self.flag = False

    def select_file(self):
        self.path = filedialog.askopenfilename(
            initialdir=USER_FOLDER, title="Sélectionner un fichier .pdf",
            filetypes=[("PDF files", "*.pdf")], multiple=False)
        if not self.path:
            self.path = "Aucune sélection."
            self.name = self.path
            self.directory = None
            self.nameOnly = None
            self.type = None
            self.flag = False
        else:
            self.directory = os.path.dirname(self.path) + "/"
            self.name = ntpath.basename(self.path)
            [self.nameOnly, self.type] = os.path.splitext(self.name)
            self.type = self.type[1:]
            self.flag = True

    def select_multi_files(self):
        self.__init__()
        self.path = filedialog.askopenfilenames(
            initialdir=USER_FOLDER, title="Sélectionner les fichiers .pdf",
            filetypes=[("PDF files", "*.pdf")], multiple=True)
        if not self.path:
            self.path = "Aucune sélection."
            self.name = self.path
        elif len(self.path) < 2:
            self.path = "Seulement un fichier a été sélectionné. " \
                        "Veuillez en sélectionner au moins deux."
            self.name = self.path
        else:
            self.directory = []
            self.name = []
            self.nameOnly = []
            self.type = []
            for thisPath in self.path:
                self.type.append(thisPath[-3:])
                self.directory.append(os.path.dirname(thisPath) + "/")
                self.name.append(ntpath.basename(thisPath))
                [n, _] = os.path.splitext(ntpath.basename(self.name[-1]))
                self.nameOnly.append(n)
            self.flag = True

    def select_directory(self):
        self.directory = filedialog.askdirectory(
            title="Sélectionner le dossier de destination",
            initialdir=USER_FOLDER)
        if not self.directory:
            self.directory = "Aucune sélection."
            self.flag = False
        else:
            self.directory = self.directory + "/"


def my_button(frame, text, but_type="default", i=0, j=0, but_w=None,
              align="center", xpad=(W_PAD, W_PAD), ypad=(W_PAD, W_PAD),
              col_span=1):
    if isinstance(xpad, int):
        xpad = (xpad, xpad)
    else:
        pass
    if isinstance(ypad, int):
        ypad = (ypad, ypad)
    else:
        pass
    if but_w is None:
        button = tk.Button(frame, text=text, font=BUTTON_FONT,
                           width=BUT_WIDTH)
    else:
        button = tk.Button(frame, text=text, font=BUTTON_FONT, width=but_w)
    button.config(cursor="hand2", activebackground=BG4)
    if but_type == "default":    # Default Button
        button.config(bg=BG2, fg=FG3)
        if align == "left":
            button.grid(row=i, column=j, sticky="nsw", padx=xpad, pady=ypad,
                        columnspan=col_span)
        elif align == "right":
            button.grid(row=i, column=j, sticky="nse", padx=xpad, pady=ypad,
                        columnspan=col_span)
        else:
            button.grid(row=i, column=j, sticky="ns", padx=xpad, pady=ypad,
                        columnspan=col_span)
    elif but_type == "main":    # Main Buttons (controlling the app)
        button.config(bg=BG3, fg=FG4)
        if align == "left":
            button.grid(row=i, column=j, sticky="nsw", padx=xpad,
                        pady=ypad, columnspan=col_span)
        elif align == "right":
            button.grid(row=i, column=j, sticky="nse", padx=xpad,
                        pady=ypad, columnspan=col_span)
        else:
            button.grid(row=i, column=j, sticky="ns", padx=xpad,
                        pady=ypad, columnspan=col_span)
    elif but_type == "small":
        button.config(bg=BG2, fg=FG3, height=1, font=BUTTON_FONT2)
        if align == "left":
            button.grid(row=i, column=j, sticky="w", padx=xpad,
                        pady=ypad, columnspan=col_span)
        elif align == "right":
            button.grid(row=i, column=j, sticky="e", padx=xpad,
                        pady=ypad, columnspan=col_span)
        else:
            button.grid(row=i, column=j, padx=xpad,
                        pady=ypad, columnspan=col_span)
    return button


def my_label(frame, text, lab_type="default", i=0, j=0, xpad=(W_PAD, W_PAD),
             ypad=(0, 0), align="center", row_span=1, col_span=1):
    if isinstance(xpad, int):
        xpad = (xpad, xpad)
    else:
        pass
    if isinstance(ypad, int):
        ypad = (ypad, ypad)
    else:
        pass
    label = tk.Label(frame, text=text)
    label.config(bg=BG1)
    if lab_type == "default":    # Default Button
        label.config(fg=FG2, font=NORMAL_FONT, justify="left")
        label.grid(row=i, column=j, sticky="nsw", padx=xpad, pady=ypad,
                   rowspan=row_span, columnspan=col_span)
    elif lab_type == "welcome":    # Main Buttons (controlling the app)
        label.config(fg=FG1, font=WELCOME_FONT, justify="center")
        label.grid(row=i, column=j, sticky="nsew",
                   rowspan=row_span, columnspan=col_span)
    elif lab_type == "intro":
        label.config(fg=FG2, font=INTRO_FONT, justify="center")
        label.grid(row=i, column=j, sticky="nsew", pady=INTRO_PADy,
                   rowspan=row_span, columnspan=col_span)
    elif lab_type == "small":
        label.config(fg=FG2, font=SMALL_FONT)
        if align == "left":
            label.config(justify="left")
            label.grid(row=i, column=j, sticky="nsw", padx=xpad,
                       pady=ypad, rowspan=row_span, columnspan=col_span)
        else:
            label.grid(row=i, column=j, sticky="nsew", padx=xpad,
                       pady=ypad, rowspan=row_span, columnspan=col_span)
    elif lab_type == "entry":
        label.config(fg=FG5, font=ENTRY_FONT)
        if align == "left":
            label.config(justify="left")
            label.grid(row=i, column=j, sticky="nsw", padx=xpad,
                       pady=ypad, rowspan=row_span, columnspan=col_span)
        else:
            label.grid(row=i, column=j, sticky="nsew", padx=xpad,
                       pady=ypad, rowspan=row_span, columnspan=col_span)
    elif lab_type == "xsmall":
        label.config(fg=FG2, font=XSMALL_FONT)
        label.grid(row=i, column=j, sticky="nsw", padx=W_PAD,
                   rowspan=row_span, columnspan=col_span)
    return label


def my_entry(frame, var, i=0, j=0, w=10, xpad=(0, 0), col_span=1):
    if isinstance(xpad, int):
        xpad = (xpad, xpad)
    else:
        pass
    entry = tk.Entry(frame, textvariable=var, bd=1.5, insertwidth=2,
                     width=w, cursor="xterm")
    entry.grid(row=i, column=j, sticky="e", padx=xpad, pady=W_PAD,
               columnspan=col_span, ipady=3)
    entry.delete(0, tk.END)
    return entry


def check_special_character(string):
    # Make own character set and pass
    # this as argument in compile method
    regex = re.compile('[@!#$%^&*<>?/|}{~;:.,]')

    # Pass the string in search
    # method of regex object.
    if regex.search(string) is None:
        return False
    else:
        return True


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
