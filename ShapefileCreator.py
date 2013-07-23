
import os, sys
from shapefile import Reader, Writer
from Tkinter import *
import tkFileDialog, tkMessageBox




def generatePRJ(SRID= 26943):
    if SRID == 26943:
        prj =  'PROJCS["NAD83 / California zone 3",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",38.43333333333333],PARAMETER["standard_parallel_2",37.06666666666667],PARAMETER["latitude_of_origin",36.5],PARAMETER["central_meridian",-120.5],PARAMETER["false_easting",2000000],PARAMETER["false_northing",500000],AUTHORITY["EPSG","26943"],AXIS["X",EAST],AXIS["Y",NORTH]]'
    elif SRID == 26910:
        prj = 'PROJCS["NAD83 / UTM zone 10N",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-123],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],AUTHORITY["EPSG","26910"],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
    elif SRID == 4326:
        prj = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],METADATA["World",-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]'
    else:
        prj = None
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

    shpWriter.field(headerEntry.get(), 'C', '255')
    shpWriter.field('Longitude', 'F')
    shpWriter.field('Latitude', 'F')
    
    geomtype =1
    shpWriter.shapeType = geomtype
    parsedGeometryList = []
    dicValList = []
    dicKeyList = []
    for k in dic.keys():
        dicValList.append(dic[k])
        valist = k,dic[k][0],dic[k][1]
        dicKeyList.append(valist)
                          
    [parsedGeometryList.append(filez) for filez in dicValList]
    [shpWriter.point(*parsedGeometry) for parsedGeometry in parsedGeometryList]
    
    [shpWriter.record(*dList) for dList in dicKeyList]

    shpWriter.save(shpname) 
    prj = generatePRJ(int(sridEntry.get()))
    if prj != None:
        prjfile = shpname.replace('.shp','') + '.prj' 
        prjfileOpen = open(prjfile, 'w')
        prjfileOpen.write(prj)
        prjfileOpen.close()
    return shpname

def makeSHProxy():
    latitude = float(latEntry.get())
    longitude = float(longEntry.get())
    desc = descEntry.get()
    dic = {desc:(longitude,latitude)}
    shp = makeSHP(dic)
    tkMessageBox.showinfo('Shapefile Created', 'Your shapefile of image locations has ben created here:\n'
                          '{0}'.format(shp))
    root.destroy()

root = Tk()
root.title('Shapefile Creator')
#root.withdraw()

frame = Frame(root, width= 600, height=20)
frame.pack()

lat = Label(root, text='Latitude')
lat.pack(side=TOP)
latEntry = Entry(root, width = 50)
latEntry.pack(side=TOP)

long_ = Label(root, text='Longitude')
long_.pack(side=TOP)
longEntry = Entry(root, width = 50)
longEntry.pack(side=TOP)

header = Label(root, text='Field Name')
header.pack(side=TOP)
headerEntry = Entry(root, width = 50)
headerEntry.pack(side=TOP)

desc = Label(root, text='Description')
desc.pack(side=TOP)
descEntry = Entry(root, width = 50)
descEntry.pack(side=TOP)

srid = Label(root, text='SRID')
srid.pack(side=TOP)
sridEntry = Entry(root, width = 50)
sridEntry.pack(side=TOP)
sridEntry.insert(END, '4326')


button = Button(root, width  =10, height=3, text='Make Shapefile', command= makeSHProxy)
button.pack(side=TOP)

root.mainloop()



