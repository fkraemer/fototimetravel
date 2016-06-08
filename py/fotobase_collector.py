import exifread
import argparse
from os import walk
from time import mktime
from time import strptime, strftime

# -*- coding: utf-8 -*-

FOTOBASE_FILENAME = "fototimetravel_fotobase.dat";

parser = argparse.ArgumentParser(description='Create a DB with extracted image pathes and timestamps')
parser.add_argument('fotopath', type=str,
                   help="the path containing to be searched recursively for fotos")
parser.add_argument('path', type=str,
                   help="the path where the fotobase will be written to as {}".format(FOTOBASE_FILENAME))
parser.add_argument('-a',  action="store_true", default=False,
                   help="the new fotos will be appended to the existing ones in [p]/{}".format(FOTOBASE_FILENAME))

args = parser.parse_args()

def main():
    args = parser.parse_args()
    print "Starting recursive foto search in {}".format(args.fotopath)
    outputPath = "{}/{}".format(args.path,FOTOBASE_FILENAME)
    print "I will output to {}".format(outputPath)
    if args.a:
        print "... in appending mode"
    
    
    #for all image files in directory read the metadata
    targetTags = [ "Image DateTime",  "EXIF DateTimeDigitized" ]
    pics = []
    filesReadGlobal = 0
    for (dirpath, dirnames, filenames) in walk(args.fotopath):
        picsRead = 0
        print "Processing directory {}".format(dirpath)
        if len(filenames) == 0:
            continue
        for filename in filenames:
            # Return Exif tags
            fullfilename = "{}/{}".format(dirpath,filename)
            f = open(fullfilename, 'rb')
            tags = exifread.process_file(f, details=False, stop_tag=targetTags[0])
            s = None
            for targetTag in targetTags:
                if targetTag in tags.keys():         
                    s = tags[targetTag]
            if s:
                #t = mktime(s)
                try:
                    t = strptime(s.printable, '%Y:%m:%d %H:%M:%S')
                except ValueError as err:
                    print("Value error: {0}".format(err))
                #print strftime('%Y:%m:%d %H:%M:%S',t)
                tInSecs = mktime(t)
                
                pics.append("{};{}\n".format(fullfilename,tInSecs))
                picsRead = picsRead +1
            else:
                #TODO get date from filename (sometimes possible)
                print "couldnt read {}".format(fullfilename)
        if picsRead > 0:
            print "Read tags for [{}/{}][{:2.1f}]".format( picsRead,len(filenames),100*picsRead/float(len(filenames)) )
            filesReadGlobal = filesReadGlobal + picsRead
    #print pics
            
    
    print "\nTotal: Read tags for [{}/{}][{:2.1f}]".format( len(pics),filesReadGlobal,100*float(len(pics))/filesReadGlobal )
    print "writing fotobase to {}".format(outputPath)
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    f = open(outputPath, 'w+')
    f.writelines(pics)
    f.flush()
    f.close()
    print "Done."
    

if __name__ == "__main__":
    main()