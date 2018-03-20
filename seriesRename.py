import os, sys
filenames = os.listdir('.')
if len(sys.argv) < 2:
    season = input('Indicate season number: ')
else:
    season = sys.argv[1]
filesRenamed = 0
extension = ['.avi','.mkv','.mp4']
index1 = 0
index2 = 0
for filename in filenames:
    if filename[-4:] in extension:
        index1 += 1
        os.rename(filename, season + 'x' + '%02d' % (index1) + filename[-4:])
        filesRenamed += 1
    if '.srt' in filename:
        index2 += 1
        os.rename(filename, season + 'x' + '%02d' % (index2) + '.en.srt')
        filesRenamed += 1

print('{num:d} files renamed'.format(num=filesRenamed) )
