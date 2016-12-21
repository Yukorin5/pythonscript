import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sunpy.map
from astropy.io import fits



def plot_sun_image(img, filename, wavelength=193, title = ''):
    #cmap = plt.get_cmap('sdoaia{}'.format(wavelength))
    cmap = plt.get_cmap('sohoeit195')
    plt.title(title)
    cax = plt.imshow(img,cmap=cmap,origin='lower',vmin=0, vmax=3000)#,vmin=vmin, vmax=vmax)
    plt.gcf().colorbar(cax)
    plt.savefig(filename)
    plt.close("all")

img = fits.open("eit-test.fits")[0].data

print(np.max(img))
print(np.min(img))

plot_sun_image(img, "eit-test.png", wavelength=193)
