#tools for maps and their Fourier transform
import numpy as np

from flipper import liteMap
from flipper import fftTools

class mapObject(object):
	def __init__(self, mapFile, weightFile, beamTransform, freqGHz, omega, beam_ell, mapBounds=None):
		"""
		args: 
		mapFile: (str) fits file with the data
		weightsFile: (str) fits file with the weights of the data
		beamTransform: plain text file with the Beam Transform in ell space
		freqGHz: (float) Map Frequency in GHz
		omega: (float) Beam Solid Angle in sr
		(optional)
		mapBounds = [RA0,RA1,DEC0,DEC1] desired bounds in deg
		"""		
