# The program for testing the download of EIT data.
#
# If you are missing of `suds` module do the following:
# pip install suds-jurko
#
# See also
# http://iswa.gsfc.nasa.gov/iswa_data_tree/observation/solar/soho/eit-195/1998/01/

from sunpy.net import vso
import astropy.units as u

# create a new VSOClient instance
client = vso.VSOClient()
# build our query
qr = client.query(vso.attrs.Time('2001/1/1', '2001/1/2'), vso.attrs.Instrument('eit'), vso.attrs.Wave(196*u.AA, 194*u.AA))

print(qr[0])


res=client.get(qr[0:1], path='./eit-test.fits').wait()
