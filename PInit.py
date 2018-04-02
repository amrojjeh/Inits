from tkinter import *
from tkinter import messagebox
import zipfile
import os
import sys
import shutil
import urllib.request
import urllib.error

window = Tk()
window.title("C++ Project Initializer")
window.resizable(0,0)

def Valdiate():
	# Has a name ben given?
	if (Name.get().replace(" ", "") == ""):
		Log['text'] = "ERROR: No name has been given"
		Log['fg'] = "red"
		print("ERROR: No name has been given\n")
		return False

	# Has a path been given?
	elif (Path.get().replace(" ", "") == ""):
		Log['text'] = "ERROR: No path has been given"	
		Log['fg'] = "red"	
		print("ERROR: No path has been given\n")
		return False

	# Is the path given valid?
	elif (not (os.path.isdir(Path.get()))):
		Log['text'] = "ERROR: Path is non-existent"
		Log['fg'] = "red"
		print("ERROR: Path is non-existent\n")
		return False

	# Does the path already exist?
	elif (os.path.exists(Path.get() + "\\" + Name.get())):
		Log['text'] = "ERROR: Folder already exists"
		Log['fg'] = "red"
		print("ERROR: Folder already exists\n")
		return False
	return True

def MakeDirs(*Paths):
	for Path in Paths:
		os.makedirs(Path)

def SrcFile(srcPath):
	src = "#include <iostream>\n\n"
	src += "int main(int argc, char* argv[])\n"
	src += "{\n"
	src += "\tstd::cout << \"Hello World!\" << std::endl;\n"
	src += "\treturn 0;\n"
	src += "}"
	with open(srcPath + "\\main.cpp", "w") as main:
		main.write(src)

def BuildFile(projectPath):
	build = "@echo off\n"
	build += "if not defined DevEnvDir (call vcvarsall {})\n".format(ArchitectureSelected.get())
	build += "pushd build\\\n"
	build += "cl ..\\src\\*.cpp /I ..\\dependencies /D {} /link ..\dependencies\\{}\npopd".format(Macros.get(), Dependencies.get())
	with open(projectPath + "\\build.bat", "w") as buildfile:
		buildfile.write(build)

def GetSDL(dependenciesPath, buildPath):
		SDLVersion = "2.0.8"
		SDLZipPath = dependenciesPath + "SDL2.zip"
		SDLPath = dependenciesPath + "SDL\\"
		urllib.request.urlretrieve("http://libsdl.org/release/SDL2-devel-"+ SDLVersion +"-VC.zip", SDLZipPath)
		SDL = zipfile.ZipFile(SDLZipPath)
		SDL.extractall(dependenciesPath)
		SDL.close()
		os.remove(SDLZipPath)
		os.rename(dependenciesPath+"SDL2-"+SDLVersion, SDLPath)
		os.remove(SDLPath + "BUGS.txt")
		os.remove(SDLPath + "COPYING.txt")
		os.remove(SDLPath + "README.txt")
		os.remove(SDLPath + "README-SDL.txt")
		if (ArchitectureSelected.get() == "x64"):
			shutil.rmtree(SDLPath + "lib\\x86")
		else:
			shutil.rmtree(SDLPath + "lib\\x64")
		os.rename(SDLPath + "lib\\{}\\SDL2.dll".format(ArchitectureSelected.get()), buildPath + "SDL2.dll")
		os.rename(SDLPath + "lib\\{}\\SDL2.lib".format(ArchitectureSelected.get()), SDLPath + "SDL2.lib")
		os.rename(SDLPath + "lib\\{}\\SDL2main.lib".format(ArchitectureSelected.get()), SDLPath + "SDL2main.lib")
		for root, dirs, files in os.walk(SDLPath + "include"):
			for file in files:
				os.rename(SDLPath + "include\\" + file, SDLPath + "\\" + file)
		shutil.rmtree(SDLPath + "lib")
		shutil.rmtree(SDLPath + "docs")
		os.rmdir(SDLPath +  "include")


def GetDependencies(dependenciesPath, buildPath):
	# TODO: MIGHT TURN INTO A SWITCH STATEMENT IF MORE LIBRARIES ARE ADDED
	if (TemplateSelected.get() == "SDL2" and messagebox.askyesno("Install", "Install SDL2?")):
		GetSDL(dependenciesPath, buildPath)

# Callback for the "Create" button
def Create(event):
	if (not Valdiate()):
		return
	# Make all directories
	projectPath = Path.get() + "\\" + Name.get()
	srcPath = projectPath + "\\src\\"
	buildPath = projectPath + "\\build\\"
	dependenciesPath = projectPath + "\\dependencies\\"

	MakeDirs(projectPath, srcPath, buildPath, dependenciesPath)

	# Make template C++ file
	SrcFile(srcPath)

	# Make the build file
	BuildFile(projectPath)

	GetDependencies(dependenciesPath, buildPath)

	Log['text'] = "Project has created succesfully!"
	Log['fg'] = "green"
	print("Project created succesfully\n")

# Template callback
def TemplateChange(event):
	if (event == "Nothing"):
		Macros.delete(0, END)
		Dependencies.delete(0, END)
	if (event == "SDL2"):
		Macros.delete(0, END)
		Dependencies.delete(0, END)
		Dependencies.insert(0, "SDL\SDL2.lib")
		Macros.insert(0, "SDL_MAIN_HANDLED")

CurrentRow = 0

# Name of THIS program
Log = Label(window, text="THE C++ PROJECT INITIALIZER!")
Log.grid(row=CurrentRow, column=0, sticky=N+S+E+W, columnspan=2)
CurrentRow += 1

# Templates
TEMPLATES = ["Nothing", "SDL2"]
Label(window, text="Templates ").grid(row=CurrentRow, column=0, sticky=W)
TemplateSelected = StringVar(window, value=TEMPLATES[0])
OptionMenu(window, TemplateSelected, *TEMPLATES, command=TemplateChange)\
.grid(row=CurrentRow, column=1, sticky=W, padx=10, pady=5)
CurrentRow += 1

# Architecture
Label(window, text="Architecture").grid(row=CurrentRow, column=0, sticky=W)
ArchitectureSelected = StringVar(window, value="x86")
OptionMenu(window, ArchitectureSelected, "x86", "x64").grid(row=CurrentRow, column=1, padx=10, pady=5, sticky=W)
CurrentRow += 1

# Ask for name of the project
Label(window, text="Name ").grid(row=CurrentRow, column=0, sticky=W)
Name = Entry()
if len(sys.argv) >= 2:
	Name.insert(0, sys.argv[1])
Name.grid(row=CurrentRow, column=1, sticky=W, padx=10, pady=5)
CurrentRow += 1

# Ask for path
Label(window, text="Full path* ").grid(row=CurrentRow, column=0, sticky=W)
Path = Entry()
if len(sys.argv) >= 3:
	Path.insert(0, sys.argv[2])

Path.grid(row=CurrentRow, column=1, sticky=W, padx=10, pady=5)
CurrentRow += 1

# Ask for dependencies
Label(window, text="Dependencies ").grid(row=CurrentRow, column=0, sticky=W)
Dependencies = Entry()
Dependencies.grid(row=CurrentRow, column=1, sticky=W, padx=10, pady=5)
CurrentRow += 1

# Ask for macro definitions
Label(window, text="Pre-defined Macros ").grid(row=CurrentRow, column=0, sticky=W)
Macros = Entry()
Macros.grid(row=CurrentRow, column=1, sticky=W, padx=10, pady=5)
CurrentRow += 1

# Create button
CreateButton = Button(window, text="Create!")
window.bind("<Return>", Create)
CreateButton.bind("<Button-1>", Create)
CreateButton.grid(row=CurrentRow, column=0, sticky=N+S+E+W, columnspan=2)
CurrentRow += 1

window.mainloop()