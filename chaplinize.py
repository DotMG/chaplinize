import cv2 as cv
import glob
import os
import re
import sys, getopt
import csv
from UMatFileVideoStream import UMatFileVideoStream
from time import sleep

a_dir = '/tmp/err'
a_fil = ''
a_out = './'
a_max = 1

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:f:o:m:", ['help', 'dir=',
        'file=', 'outdir=', 'max='])
except getopt.GetoptError:
    print (sys.argv[0] + ' -d <dir_in> | -f <file_in> -o <out_dir>')
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print (sys.argv[0] + ' -d <dir_in> | -f <file_in> -o <out_dir>')
        sys.exit()
    elif opt in ('-d', '--dir'):
        a_dir = arg
    elif opt in ('-f', '--file'):
        a_fil = arg
    elif opt in ('-o', '--outdir'):
        a_out = arg
    elif opt in ('-m', '--max'):
        a_max = int(arg)

threshold = 1000
if not a_fil:
    a_fil = a_dir + '*.mp4'

finput='./00000000352000000.mp4'
# Miasa is the malagasy word meaning "to work"
# This procedure takes the first file in directory and processes it
#    creates a Chaplinized video and rename the file by appending ".done"
#    to its name.
def miasa():
    # get to finput the first file ending in .mp4
    gin = glob.glob(a_fil)
    if not gin:
        print( 'No file found at '+a_fil)
        sys.exit(2)
    finput = min(gin, key=os.path.basename);
    print (finput)
    csvfile = open('./data.csv', 'w')
    csvw = csv.writer(csvfile)
    video = UMatFileVideoStream(finput, 512).start()
    h = video.height
    w = video.width
    fps = video.fps
    nbf = video.nbframes
    newwidth = (w*400)//h
    #rgb = cv.UMat(h, w, cv.CV_8UC3)
    img, index = video.read()
    img0 = img
    img = cv.resize(img, (newwidth, 400))
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(img, 7)
    size = (w, h)
    # latest_out_new is the name of output file. Automagically sequenced.
    list_output = glob.glob(a_out + 'out-*')
    if (not list_output):
        latest_out = a_out + "out-000.mkv";
    else:
        latest_out = max(list_output, key=os.path.basename);
    mtc = re.search(r"\d\d\d", latest_out)
    latest_out_new = latest_out + 'z'
    if mtc != None:
        nxt = int(mtc.group()) + 1
        nxt_s = str(nxt).zfill(3)
        latest_out_new = re.sub(mtc.group(), nxt_s, latest_out)
    
    out = cv.VideoWriter(latest_out_new, cv.VideoWriter_fourcc(*'h264'), 25, size)
    a = 0
    f = 0
    lastfn = 0
    # Points of interest are in wrange and hrange
    wrange = range(newwidth // 16, newwidth, newwidth // 8)
    hrange = range(400 // 16, 400, 400 // 8)
    print ('nb frames : ', nbf)
    oldproc = 0.0
    lastevry = 0
    while not video.stopped:
        a = a+1
        for _ in range(24):
            if ( video.stopped ):
                break
            f = f+1
            if (f > nbf - 3):
                break
            video.skip()
        if ( not video.stopped ):
            f = f+1
            if (f > nbf - 3):
                break
            img, index = video.read()
            p = []
            img2 = cv.resize(img, (newwidth, 400))
            img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
            img2 = cv.medianBlur(img2, 7)
            z = img2.get().astype('uint8')
            for i in wrange:
                for j in hrange:
                    p.append( z[j, i] )
            delta = int(0)
            if (f > 49):
                for k in range(64):
                    delta += (int(p[k])-q[k])*(int(p[k])-q[k])
            evry = 200
            if (delta >= 200):
                evry -= 100
            if (delta >= 500):
                evry -= 50
            if (delta >= 1000):
                evry -= 25
            if (delta >= 2000):
                evry -= 4
            if (delta >= 3000):
                evry -= 3
            if (delta >= 4000):
                evry -= 3
            if (delta >= 5000):
                evry -= 3
            if (delta >= 6000):
                evry -= 2
            if (delta >= 7000):
                evry -= 1
            if (delta >= 8000):
                evry -= 1
            if (delta >= 9000):
                evry -= 1
            if (delta >= 10000):
                evry -= 1
            if (delta >= 11000):
                evry -= 1
            if (delta >= 12000):
                evry -= 1
            if (delta >= 13000):
                evry -= 1
            if (delta >= 14000):
                evry -= 1
            if (delta >= 15000):
                evry -= 1
            fnu = f
            if ((lastfn < fnu - fps) and (evry < fps)): 
                lastfn = fnu - fps;
            if lastevry == 0:
                lastevry = evry;
            for l in range(int(lastfn), int(fnu), (2*evry+lastevry)//3):
                if ((l == lastfn) or (l>fnu)):
                    continue
                img = video.pick(l)
                out.write(img)
                lastfn = l
            lastevry = evry
            p.append( fnu )
            p.append( delta )
            csvw.writerow( p )
            q = p
            processed = (int(f)*1000//nbf)/10
            if processed != oldproc:
                print(' _ '+str(processed)+'%    * * * * * * * * * * * * * * *', end='\r')
                oldproc = processed
    
    print ( '===> ', latest_out_new )
    out.release()
    csvfile.close()
    os.rename(finput, finput+'.done')

for _ in range(a_max):
    miasa()

sys.exit(1)
