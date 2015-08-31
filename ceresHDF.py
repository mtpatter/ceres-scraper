#!/usr/bin/python
import sys
from pyhdf.SD import SD, SDC
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as mpimg
import gdal, osr

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def load(path):
  line_list = []
  f = open(path, "r")
  for line in f:
    line_list.append (line.strip('\n'))
  f.close
  # Efficiently concatenate Python string objects
  return line_list#(''.join(word_list)).split ()


def displayHDF(datavmean, param):
	plt.imshow(datavmean)#, interpolation="nearest")	

	def format_coord(x, y):
                col = int(x+0.5)
                row = int(y+0.5)
                #if col>=0 and col<numcols and row>=0 and row<numrows:
                z = datavmean[row,col]
                return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
	plt.gca().format_coord = format_coord
	plt.colorbar(shrink=0.5)
	plt.title(param)
	plt.show()

def convertCoord(lat, lon):
	#index #0 is defined at 89.5 N and #179 is 89.5 S
	y = abs(lat - 89.5)	
	x = lon + 179.5
	return x, y

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
if __name__ == '__main__':

  def oneImage():	
	hdfname = sys.argv[1]
	lat = float(sys.argv[2])
	lon = float(sys.argv[3])
	xc, yc = convertCoord(lat, lon)
			
	hd = SD(hdfname,SDC.READ)
	params = sorted(hd.datasets().keys())
	for i in range(len(params)): 
		print i, params[i]
	i = int(raw_input('\nChoose # of parameter to plot: '))
	datav = hd.select(params[i])
	datavmean = datav[0,:,:]
	print 'x pixel= ', xc
	print 'y pixel= ', yc
	print 'value at coordinate= ', datavmean[yc,xc]
	displayHDF(datavmean,params[i])
 
  def getCountyCoords():
  	countyfile = 'CenPop2010_Mean_CO.txt'
  	countydata = load(countyfile)
  	coordsDict = AutoVivification()
  	for line in countydata[1:]:
		linelist = line.split(',')
		#print '%s%s, %f, %f' % (linelist[0],linelist[1],float(linelist[5]),float(linelist[6]))
		fips = '%s%s' % (linelist[0],linelist[1])
		coordsDict[fips] = (float(linelist[5]),float(linelist[6]))
 	#fipslist =sorted(coordsDict.keys())
  	return coordsDict

  def convertCounties():	
  	hdfname = sys.argv[1]
	hd = SD(hdfname,SDC.READ)
  	params = sorted(hd.datasets().keys())
  	for i in range(len(params)):
        	print i, params[i]
  	i = 91 #int(raw_input('\nChoose # of parameter to plot: '))
  	datav = hd.select(params[i])
  	datavmean = datav[0,:,:]

  	countyCoordsDict = getCountyCoords()
  	fipslist = sorted(countyCoordsDict.keys())
  	#print countyCoordsDict 
 	countyXYDict= AutoVivification()
  	for county in fipslist:
		countyXYDict[county] = convertCoord(countyCoordsDict[county][0],countyCoordsDict[county][1])
  	#print countyXYDict['17031']	
  	countyValueDict = AutoVivification()
  	for county in fipslist:
		xcoord = countyXYDict[county][0]
		ycoord = countyXYDict[county][1]
		countyValueDict[county] = datavmean[ycoord,xcoord]
	
	basename = hdfname.split('.')[1]
	outfile = params[i].replace(" ","")+'_'+basename+'.txt'
  	writefile = open(outfile, 'w')
	print >> writefile, 'county,%s' % params[i] 
  	for county in fipslist:
		print >> writefile, '%s,%s' % (county, countyValueDict[county])


	
  oneImage()
  #convertCounties()


