import os, sys
filenames = os.listdir('.')
if len(sys.argv) < 2:
    season = input('Indicate season number: ')
else:
    season = sys.argv[1]
filesRenamed = 0
extension = ['.avi','.mkv','.mp4']
index = 0
for filename in filenames:
    if filename[-4:] in extension:
        index += 1
        os.rename(filename, season + 'x' + '%02d' % (index) + filename[-4:])
        filesRenamed += 1
index = 0
for filename in filenames:
    if '.srt' in filename:
        index += 1
        os.rename(filename, season + 'x' + '%02d' % (index) + '.en' + extension)
        filesRenamed += 1
print('{num:d} files renamed'.format(num=filesRenamed) )
