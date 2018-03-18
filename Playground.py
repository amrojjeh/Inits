import os
from tkinter import *

window = Tk()
window.title("C++ Project Initializer")
window.resizable(0,0)

# Callback for the "Create" button
def Create(event):
	print("Creating..")

	if (Path.get().replace(" ", "") == ""):
		Log['text'] = "ERROR: No path has been given"	
		Log['fg'] = "red"	
		print("ERROR: No path has been given\n")
		return

	elif (not (os.path.isdir(Path.get()))):
		Log['text'] = "ERROR: Path is non-existent"
		Log['fg'] = "red"
		print("ERROR: Path is non-existent\n")
		return



	elif (Name.get().replace(" ", "") == ""):
		Log['text'] = "ERROR: No name has been given"
		Log['fg'] = "red"
		print("ERROR: No name has been given\n")
		return

	elif (os.path.exists(Path.get() + "\\" + Name.get())):
		Log['text'] = "ERROR: Folder already exists"
		Log['fg'] = "red"
		print("ERROR: Folder already exists\n")
		return

	# Make all directories
	projectPath = Path.get() + "\\" + Name.get()
	srcPath = Path.get() + "\\" + Name.get() + "\\" + "src\\"
	buildPath = Path.get() + "\\" + Name.get() + "\\" + "build\\"
	dependenciesPath = Path.get() + "\\" + Name.get() + "\\" + "dependencies\\"

	os.makedirs(projectPath)
	os.makedirs(srcPath)
	os.makedirs(buildPath)
	os.makedirs(dependenciesPath)

	# Make template C++ file
	with open(srcPath + "\\main.cpp", "w") as main:
		main.write(
"""#include <iostream>
int main(void)
{
	std::cout << "Hello World!" << std::endl;
	return 0;
}
""")

	# Make the build file
	build = """@echo off
if not defined DevEnvDir (call vcvarsall x86)
pushd build\\"""
	build += "\ncl ..\\src\\*.cpp /I ..\\Dependencies /D {} /link {}\npopd".format(Macros.get(), Dependencies.get())
	with open(projectPath + "\\build.bat", "w") as buildfile:
		buildfile.write(build)

	Log['text'] = "Project has created succesfully!"
	Log['fg'] = "green"
	print("Project created succesfully\n")


# Name of the program
Log = Label(text="THE C++ PROJECT INITIALIZER!")
Log.grid(row=0, column=0, sticky=N+S+E+W, columnspan=2)

# Ask for name of the project
Label(text="Name ").grid(row=1, column=0, sticky=W)
Name = Entry()
Name.grid(row=1, column=1, sticky=W, padx=10, pady=5)

# Ask for path
Label(text="Full path* ").grid(row=2, column=0, sticky=W)
Path = Entry()
Path.grid(row=2, column=1, sticky=W, padx=10, pady=5)

# Ask for dependencies
Label(text="Dependencies ").grid(row=3, column=0, sticky=W)
Dependencies = Entry()
Dependencies.grid(row=3, column=1, sticky=W, padx=10, pady=5)

# Ask for macro definitions
Label(text="Pre-defined Macros ").grid(row=4, column=0, sticky=W)
Macros = Entry()
Macros.grid(row=4, column=1, sticky=W, padx=10, pady=5)

# Create button
CreateButton = Button(text="Create!")
window.bind("<Return>", Create)
CreateButton.bind("<Button-1>", Create)
CreateButton.grid(row=5, column=0, sticky=N+S+E+W, columnspan=2)

window.mainloop()