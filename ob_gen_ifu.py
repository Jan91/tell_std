#! /usr/bin/python

import numpy as np
import pandas as pd

csv_file = 'tell_data.csv'

def write_obx(sd, ob_name):

	template = open('template/template_ob_ifu.obx', 'r')
	ob 		 = open('obs_ifu/Tell_ifu_'+ob_name+'.obx', 'w')
	
	for line in template:
		s = line.split()
		if len(s) > 0:

			if str(s[0]) == 'name':
				ob.write(str(s[0])+'\t'+ '"Tell_ifu_'+ob_name+'"'+'\n')		
			elif str(s[0]) == 'userComments':
				ob.write(str(s[0])+'\t'+ '"Telluric standard, created by Jan Bolmer"' +'\n')
			elif str(s[0]) == 'TARGET.NAME':
				ob.write(str(s[0])+'\t'+'"'+sd['star']+'"'+'\n')
			elif str(s[0]) == 'propRA':
				ob.write(str(s[0])+'\t'+'"'+str(float(sd['pm_ra'])/1000.)+'"'+'\n')
			elif str(s[0]) == 'propDEC':
				ob.write(str(s[0])+'\t'+'"'+str(float(sd['pm_dec'])/1000.)+'"'+'\n')
			elif str(s[0]) == 'ra':
				ob.write(str(s[0])+'\t'+'"'+sd['RA']+'"'+'\n')
			elif str(s[0]) == 'dec':
				ob.write(str(s[0])+'\t'+'"'+sd['DEC']+'"'+'\n')
			elif str(s[0]) == 'CONSTRAINT.SET.NAME':
				ob.write(str(s[0])+'\t'+'"No Name"'+'\n')
			elif str(s[0]) == 'atm':
				ob.write(str(s[0])+'\t'+'"no constraint"'+'\n')
			elif str(s[0]) == 'OBSERVATION.DESCRIPTION.NAME':
				ob.write(str(s[0])+'\t'+ '"Tell_ifu_'+ob_name+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1':
				ob.write(str(s[0])+'\t'+'"'+str(sd['u08'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1':
				ob.write(str(s[0])+'\t'+'"'+str(sd['v09'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT':
				ob.write(str(s[0])+'\t'+'"'+str(sd['n06'])+'"'+'\n')

			else:
				ob.write(str(s[0])+'\t'+str(s[1])+'\n')
		else:
			ob.write('\n')
	template.close()
	ob.close()
	print('OB written as TELL_'+ob_name+'_ifu.obx')


def data_from_csv(csv_file):

	data = pd.read_csv(csv_file, sep=',',
		delimiter=None, index_col=None)

	data = pd.DataFrame.transpose(data)

	for i in data:
		try:
			sd = {
			'star':   data[i]['star'],
			'month':  data[i]['month'],
			'ev_mo':  data[i]['ev_mo'],
			'RA':     data[i]['RA'],
			'DEC':    data[i]['DEC'],
			'pm_ra':  str(data[i]['Prop_motion']).split()[0],
			'pm_dec': str(data[i]['Prop_motion']).split()[1], 
			'V' : 	  data[i]['V'],
			'u05': 	  data[i]['u0.5'],	
			'u08': 	  data[i]['u0.8'],	
			'u10': 	  data[i]['u1.0'],	
			'u13': 	  data[i]['u1.3'],	
			'u16': 	  data[i]['u1.6'],	
			'u50': 	  data[i]['u5.0'],	 
			'v04': 	  data[i]['v0.4'],	
			'v07': 	  data[i]['v0.7'],	
			'v09': 	  data[i]['v0.9'],	
			'v12': 	  data[i]['v1.2'],	
			'v15': 	  data[i]['v1.5'],	
			'v50': 	  data[i]['v5.0'],	
			'n04': 	  data[i]['n0.4'],	
			'n06': 	  data[i]['n0.6'],	
			'n09': 	  data[i]['n0.9'],	
			'n12': 	  data[i]['n1.2'],	
			'n15': 	  data[i]['n1.5'],	
			'n50': 	  data[i]['n5.0']
			}
			# Create the OB:
			write_obx(sd, str(sd['star'])+'_'+str(sd['month'])+'_'+str(sd['ev_mo'])[:3])

		except (IndexError):
			pass

data_from_csv(csv_file)
