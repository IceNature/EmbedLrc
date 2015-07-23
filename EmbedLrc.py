import re
import os.path
import sys


version = '0.1.0'
print('EmbedLrc   ', version, sep='',)

supportAudioTypes = ['.mp3', '.flac', '.aac', '.wav']
supportLrcTypes = ['.lrc']


def ScanFiles(directory):
    filelist = []
    allObjects = [
        directory + os.sep + filename for filename in os.listdir(directory)]
    for m in allObjects:
        if os.path.isfile(m):
            filelist.append(m)
        elif os.path.isdir(m):
            filelist.extend(ScanFiles(m))
        else:
            pass
    return filelist


def GetMatchFiles(filelist, regexs):
    matchedFiles = []
    for regex in regexs:
        pattern = re.compile(regex)
        matchedFiles.extend(m for m in filelist if pattern.match(m))
    return matchedFiles

supportAudioTypes = ['.+\\' + m for m in supportAudioTypes]
supportLrcTypes = ['.+\\' + m for m in supportLrcTypes]

fileList = []
for arg in sys.argv:
    if os.path.isdir(arg):
        fileList.extend(ScanFiles(arg))
    else:
        print('Error:{0} is not a directory!'.format(arg))

audioList = []

