import re
import os.path
import sys
from mutagen.id3 import ID3, USLT
import chardet


version = '0.1.2'
print('EmbedLrc   ', version, sep='')

supportAudioTypes = ['.mp3', '.flac', '.aac', '.wav']
supportLrcTypes = ['.lrc']


def ScanFiles(directory):
    filelist = []
    allObjects = [
        os.path.normpath(os.path.join(directory.strip(), filename)) for filename in os.listdir(directory)]
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


def CreateMap(filelist):
    tempMap = {}
    for file in filelist:
        tempMap[os.path.basename(file)[:-4]] = file
    return tempMap


supportAudioTypes = ['.+\\' + m for m in supportAudioTypes]
supportLrcTypes = ['.+\\' + m for m in supportLrcTypes]

fileList = []
args = sys.argv[1:]
for arg in args:
    if os.path.isdir(arg):
        fileList.extend(ScanFiles(arg))
    elif arg == 'EmbedLrc.py':
        pass
    else:
        print('Error:{0} is not a directory!'.format(arg))

if not fileList:
    print('No file input!')
    sys.exit(1)


audioList = CreateMap(GetMatchFiles(fileList, supportAudioTypes))
lrcList = CreateMap(GetMatchFiles(fileList, supportLrcTypes))

pattern_deltimetags = re.compile(r'\[.*?\]')
pattern_dellinebreaks = re.compile(r'^\s$')

for audioName in audioList.keys():
    if audioName in lrcList.keys():
        print('Writting into {0} ...'.format(audioList[audioName]), end='')
        lrctext = ''
        with open(lrcList[audioName], 'rb') as lrc:
            lrcRawText = lrc.read()
            encoding = chardet.detect(lrcRawText)['encoding']
            lrctext = lrcRawText.decode(encoding)
        lrctext = pattern_deltimetags.subn('', lrctext)[0]
        lrctext = pattern_dellinebreaks.subn('', lrctext)[0]
        audio = ID3(audioList[audioName])
        audio.delall('USLT')
        audio.add(USLT(text=lrctext, encoding=3))
        audio.save()
        print('done!')
    else:
        print('Can\'t find lrc file for {0}'.format(audioName))

