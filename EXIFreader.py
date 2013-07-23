from PIL import Image 
from PIL.ExifTags import TAGS
import os, sys
from shapefile import Reader, Writer
from Tkinter import *
import tkFileDialog, tkMessageBox


def read_exif(geodic):
    try:
            lat = [float(x)/float(y) for x, y in geodic['GPSInfo'][2]]
            latref = geodic['GPSInfo'][1]
            lon = [float(x)/float(y) for x, y in geodic['GPSInfo'][4]]
            lonref = geodic['GPSInfo'][3]

            
            lat = lat[0] + lat[1]/60.0 + lat[2]/3600.0
            lon = lon[0] + lon[1]/60.0 + lon[2]/3600.0
            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon
            picdata= lon,lat

            return picdata
    except:
        #this is dummy data - it puts the dot in the sahara desert
        dummydata = (10.552, 18.65224)
        return tup




def get_exif(filepath):
    ret = {}
    from PIL import Image
    i = Image.open(filepath)
    #i = imageobject
    info = i._getexif()
    
    #try:
    for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
   
    return ret


def generatePRJ():
    prj = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],METADATA["World",-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]'
    return prj

    
def saveSHP():
        
        root = Tk()
        root.withdraw()
        shp = tkFileDialog.asksaveasfilename(parent= root,initialdir='C:/',title='Save the Shapefile',initialfile='.shp',filetypes=[('ESRI Shapefile', '*.shp')])
        root.destroy()
        return shp


def makeSHP(dic):
    shpname = saveSHP()
    shpWriter = Writer()
    shpWriter.autoBalance = 1

    shpWriter.field('Filepath', 'C', '255')
    
    geomtype =1
    shpWriter.shapeType = geomtype
    parsedGeometryList = []
    dicValList = []
    dicKeyList = []
    for k in dic.keys():
        dicValList.append(dic[k])
        dicKeyList.append(k)
                          
    [parsedGeometryList.append(filez) for filez in dicValList]
    [shpWriter.point(*parsedGeometry) for parsedGeometry in parsedGeometryList]
    
    [shpWriter.record(dList) for dList in dicKeyList]

    shpWriter.save(shpname) 
    prj = generatePRJ()
    prjfile = shpname.replace('.shp','') + '.prj' 
    prjfileOpen = open(prjfile, 'w')
    prjfileOpen.write(prj)
    prjfileOpen.close()
    return shpname


root = Tk()
root.withdraw()
images =  tkFileDialog.askdirectory(parent=root,title='Choose the image folder',initialdir="C:\\") #sys.argv[1]
root.destroy()
files = os.listdir(images)
picdic = {}

for f in files:
     
    ff = os.path.join(images, f)
    dic = get_exif(ff)
    picdata =read_exif(dic)
    picdic[ff] = picdata
print picdic

shp = makeSHP(picdic)

tkMessageBox.showinfo('Shapefile Created', 'Your shapefile of image locations has ben created here:\n'
                      '{0}'.format(shp))
