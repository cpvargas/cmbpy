#tools for maps and their Fourier transform

from astropy.io import fits
from astropy.wcs import wcs
import numpy as np

def _selectsubmap(data,header,projection,bounds):
	"""
	selects a submap inside data at bounds
	"""
	RA0 = bounds[0]
	RA1 = bounds[1]
	DEC0 = bounds[2]
	DEC1 = bounds[3]
	verticesworld = np.array([[RA0,DEC0],[RA1,DEC1]])
	rawpix = projection.wcs_world2pix(verticesworld, 0) #0 for the representation
	pixcoords = np.array(np.round(rawpix,0), dtype=np.int)
	x0 = pixcoords[0][0]
	y0 = pixcoords[0][1]
	x1 = pixcoords[1][0]
	y1 = pixcoords[1][1]
	data = data[y0:y1+1,x0:x0+1]
	hdr= header.copy()
	hdr["NAXIS1"] = data.shape[1]
	hdr["NAXIS2"] = data.shape[0]
	hdr["CRPIX1"] -= x0
	hdr["CRPIX2"] -= y0
	w = wcs.WCS(hdr)
	return data,hdr,w

class cmbmap(object):
	def __init__(self,MapFile,bounds=None,WeightsFile=None):
		"""
		args: Mapfile: fits file containing the data

		(optional) 
		
		bounds = [RA0,RA1,DEC0,DEC1] desired bounds in deg
		
		WeightsFile: fits file contaning the weights of the
		data
		"""

		#getting headers, data and projections from MapFile

		#we use the 0 representation in which the inferior left corner
		#pixel is the [0,0] and also the element [0,0] on the array
		#the other representation is the 1 representation in which the
		#inferior left corner pixel is [1,1] used in ds9 for example

		self.mapheader = fits.getheader(MapFile, 0)
		self.datamap = fits.getdata(MapFile, 0)
		self.projection = wcs.WCS(self.mapheader)

		if bounds != None:
			self.bounds = bounds
			self.datamap,self.mapheader,self.projection = _selectsubmap(self.datamap, 
						    self.mapheader, self.projection, self.bounds)

		if WeightsFile != None:
			self.weightsmap = fits.getdata(WeightsFile, 0)
			if bounds != None:
				self.weightsmap = _selectsubmap(self.datamap, self.mapheader, 
								self.projection, self.bounds)[0]



