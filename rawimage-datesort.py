#!/usr/bin/env python
##########################################################################
#       Title:
#    $RCSfile: $
#   $Revision: $$Name:  $
#       $Date: $
#   Copyright: $Author: $
# Description: 
#
#
#
#------------------------------------------------------------------------
#
#  $Log: $
#
#
##########################################################################
from optparse import OptionParser

import glob
import os
import sys
import shutil
import pyexiv2


def processImage(i,outdir):
    """
    For every image get the capture date,
    create a output folder (yyyy-mm-dd)
    and move the image to this folder.

    i - input image
    outdir - where to store the path/images

    """

    # get the meta info
    image = pyexiv2.ImageMetadata(i)
    image.read()

    key = 'Exif.Image.DateTime'
    datetime=[]
    if key in image.exif_keys:
        datetime = image[key]
    else:
        key = 'Exif.Photo.DateTimeOriginal'
        datetime = image[key]

    # create the output folder structre
    datedir = str(datetime.value.year) 
    datedir += '-'
    datedir += str( '%02i') % datetime.value.month
    datedir += '-'
    datedir += str('%02i') % datetime.value.day
    
    fulldatedir = os.path.abspath(os.path.join(outdir,datedir))
    
    # create the outdir
    if not os.path.exists(fulldatedir):
        os.makedirs(fulldatedir)
    
    # move the file
    shutil.move(i,fulldatedir)



def main():

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    parser.add_option("-o", "--outdir", dest="outdir",
                  help="output dir", default = '.')
    
    (options, args) = parser.parse_args()
    
    outdir = options.outdir

    # now pocess all the command line files
    for i in args:
        processImage(i,outdir)



if __name__ == "__main__":
    main()

