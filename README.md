command line tool allows navigation through file system. Actions include listing files, txt files, directories, and all contents of current working directory. This allows traversal through the file system in order to find desired debug log. Once debug log is found you can selected it by using the 'S' action to select it and open it. If you already know the name of the debug log navigate to the directory that holds the debug log then use the 'S' select action to open and read the file. The script is configured to use default settings that use some basic delimiters for Salesforce debug logs, any lines in the debug log that contain the default delimiters will be seperated from the file. If you want to enter more filtering criterium then when prompted add all delimiters seperated by commas and the script will filter out lines containing your delimiters.
