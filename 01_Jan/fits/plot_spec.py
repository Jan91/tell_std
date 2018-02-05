#! /usr/bin/python

from astropy.io import fits
from pylab import *
import matplotlib.pyplot as plt
import pandas as pd

def get_data_from_fits(fitsfile):

	with fits.open(fitsfile) as hdul:
	
		hdr = hdul[0].header
		obj = hdr['OBJECT']
		
		data_hdr = hdul[1].header
		data = hdul[1].data
	
		df = pd.DataFrame(data={'wav': data[0][0], 'flux': data[0][1],
			'flux_err': data[0][2], 'a':data[0][3],
			'b':data[0][4], 'c': data[0][5], 'd':data[0][6]})

		return df['wav'], df['flux'], obj

files = ['Hip024789_uvb.fits', 'Hip024789_vis.fits', 'Hip024789_nir.fits']

fig = figure(facecolor='white', figsize=(14, 6))
ax = fig.add_axes([0.10, 0.15, 0.89, 0.79])

i = 0
for file in files:

	x, y, obj = get_data_from_fits(file)
	plot(x, y)
	if i == 0:
		ax.set_title(str(obj))
	i += 1

for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(2)
ax.tick_params(which='major', length=8, width=2)
ax.tick_params(which='minor', length=4, width=1.5)

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)
for tick in ax.yaxis.get_major_ticks():
	tick.label.set_fontsize(18)

ax.set_yscale('log')
ax.set_xscale('log')

ax.set_xticks([300, 400, 500, 600, 800, 1000, 1200, 1600, 2000, 2400])
ax.set_xticklabels(['300', '400', '500', '600', '800', '1000', '1200', '1600', '2000', '2400'])

ax.set_ylabel(r"$\sf Flux\, (erg/cm^{-2}/\AA/s)$", fontsize=20)
ax.set_xlabel(r"$\sf Wavelength$", fontsize=20)

fig.savefig("spec_Hip024789.pdf")



