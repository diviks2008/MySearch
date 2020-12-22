# Description:

MySearch is designed to search for folders and files by name,
by content in files, by specified modification date,
by the specified size in megabytes.

## Main control:

##### "Search in:"

Double-clicking on the search path line will open the search path selection menu.
Default: search path, this is where the Mysearch program starts.

##### "Name:"

Specify a name for the file or search folder.
To search for files by extension, specify the file extension `(for example: .jpg)`

##### "Content:"

Enter the word that you want to find in the files.

##### "Modification date"

Specify the start (left margin) and end (right margin) of the file modified date
If there is no start date, then the search is performed with a time equal to zero.
If there is no end date, it is searched before the program start date.
`Date format: YYYY.mm.dd
(Example: 2020.11.05)`

##### "File zise"

Enter the minimum (left margin) and maximum (right margin) file size in MB.
If the required file size is less than 1 MB, then the value is indicated with a period.
`(example 100 MB: 100)
(example 120 KB: 0.12)
(example 120 Bytes: 0.00012)`

##### "Case sensitive"

If the flag is set, the search will be case sensitive.
The flag affects "Name:" and "Content:"

##### "Recursive"

Check the box to search for files recursively.
(search in all subfolders and subfolders)

#### Keyboard Keys:

1. "Esc" - Abort the search.
2. "F1" - Help.
3. "F3" - Display all folders and files in the "Found files" window
    (the mysearch.exclude file is ignored)

## General addition:

1. Folder names in the "Found files" field are highlighted on the left
    and right with icons '[' and ']' respectively `(Example: [folder])`
2. **Double click** on the FOLDER name in the "Found files" window to go to this folder
3. **Single click** on the file name in the "Found files" window:
    if there is no content search parameter in the "Content:" field,
    will display the contents of the test file in the "File content" window;
    if "Content:" is specified, it will show the match string
    and the line number in the "File content" window ("Start" can be omitted)
4. **Double click** on the file name in the "Found files" window,
    will open the file in the default editor.
5. **"Start"** button - start the search based on the search parameters
    (if there are no parameters, display a list of all folders and files
    excluding those specified in the mysearch.exclude file)

##### To run the program on Debian, Ubuntu, OpenSuse:
`sudo apt install python3-tk`
