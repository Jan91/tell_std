#! /usr/bin/python

import numpy as np
import pandas as pd

ob_name = 'test'
csv_file = 'tell_data.csv'

def write_obx(sd, ob_name):

	template = open('template/template_ob_slt.obx', 'r')
	ob 		 = open('obs_slt/Tell_slt_'+ob_name+'.obx', 'w')
	
	ln = -1

	for line in template:
		ln += 1
		s = line.split()
		if len(s) > 0:

			if str(s[0]) == 'name':
				ob.write(str(s[0])+'\t'+ '"Tell_slt_'+ob_name+'"'+'\n')		
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
				ob.write(str(s[0])+'\t'+ '"Tell_slt_'+ob_name+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (47 < ln < 64):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u05'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (47 < ln < 64):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v04'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (47 < ln < 64):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n04'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (67 < ln < 83):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u08'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (67 < ln < 83):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v07'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (67 < ln < 83):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n06'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (86 < ln < 102):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u10'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (86 < ln < 102):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v09'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (86 < ln < 102):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n09'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (105 < ln < 121):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u13'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (105 < ln < 121):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v12'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (105 < ln < 121):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n12'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (124 < ln < 140):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u16'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (124 < ln < 140):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v15'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (124 < ln < 140):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n12'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (143 < ln < 159):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u08'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (143 < ln < 159):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v07'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (143 < ln < 159):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n06'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (162 < ln < 178):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u10'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (162 < ln < 178):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v09'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (162 < ln < 178):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n09'])+'"'+'\n')


			elif str(s[0]) == 'DET1.WIN1.UIT1' and (181 < ln < 197):
				ob.write(str(s[0])+'\t'+'"'+str(sd['u50'])+'"'+'\n')

			elif str(s[0]) == 'DET2.WIN1.UIT1' and (181 < ln < 197):
				ob.write(str(s[0])+'\t'+'"'+str(sd['v50'])+'"'+'\n')

			elif str(s[0]) == 'DET3.DIT' and (181 < ln < 197):
				ob.write(str(s[0])+'\t'+'"'+str(sd['n50'])+'"'+'\n')


			else:
				ob.write(str(s[0])+'\t'+str(s[1])+'\n')
		else:
			ob.write('\n')
	template.close()
	ob.close()
	print('OB written as TELL_'+ob_name+'_slt.obx')


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
			write_obx(sd, str(sd['star'])+'_'+str(sd['month'])+'_'+str(sd['ev_mo'][:3]))

		except (IndexError):
			pass

data_from_csv(csv_file)
