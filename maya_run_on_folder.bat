// create a batch file that runs through all maya files in a folder 
// open each maya file in command line, perform operation rename and save and close same file


for /r %%i in (*) do echo %%i

for %%f in (directory\path\*) do ( something_here )


@ECHO OFF
setlocal enabledelayedexpansion
for %%f in (directory\path\*.txt) do (
  set /p val=<%%f
  echo "fullname: %%f"
  echo "name: %%~nf"
  echo "contents: !val!"
)

// https://stackoverflow.com/questions/138497/iterate-all-files-in-a-directory-using-a-for-loop
