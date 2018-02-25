import os, sys
filenames = os.listdir('.')
if len(sys.argv) < 3:
    extension = input('Indicate file extension (.avi, .srt...): ')
    season = input('Indicate season number: ')
else:
    extension = sys.argv[1]
    season = sys.argv[2]
for index, filename in enumerate(filenames):
    if '.py' in filename:
        continue
    elif extension == '.srt':
        os.rename(filename, season + 'x' + '%02d' % (index+1) + '.en' + extension)
    else:
        os.rename(filename, season + 'x' + '%02d' % (index+1) + extension)
print('{num:d} files renamed'.format(num=len(filenames)-1) )
