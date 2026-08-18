# python script to convert mp3-files to midi files using muscriptor
# converts mp3-files to midi files using muscriptor --> https://github.com/muscriptor/muscriptor

# class based, no global variables allowed.
# default dev environment: MacMini M4, VS Code, Python 3.1x but must run on windows or Linux just as easily. 
# default input folder is '/Volumes/data1/Yandex.Disk.localized/michiele/Muziek/Logic/Bounces'
# default output folder is '/Volumes/data1/Yandex.Disk.localized/michiele/Muziek/Midi bestanden'

# the Python app accepts command line arguments for:
#  -  input and output folders
#  -  for the muscriptor command to use
#  - files to explicitly convert (otherwise all mp3 files in the input folder are converted)

# When no command line options are given, start a desktop interface to select input and output folders and files to convert.
# the user can save the default settings in a ./cfg file for future use. Theconfig is used for default settings such as input output
# user can select per for all files which  which outut format: wav, midi or sheet, or per file indicate the default output format. The default ouput is midi.

# example commandline: "muscriptor transcribe ./Rufus\ du\ Sol\ -\ On\ my\ knees.mp3 --format midi --output score/WhaterverSongname.mid"

