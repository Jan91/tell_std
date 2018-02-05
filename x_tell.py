#! /usr/bin/python

import pandas as pd
import os, re, sys, datetime, time
import matplotlib.dates as mdates
import ephem

from pylab import *
from numpy import arange

class DegreeFormatter(Formatter):
	def __call__(self, x, pos=None):
		# \u00b0 : degree symbol
		return r'$%d^\circ$' % ((x / pi) * 180.0)

def alt_to_airmass(altitude):
	'''
	Calculate apparent altitude to airmass 
	based on Pickering (2002)
	'''
	return 1./(sin(radians(altitude + 244/(165+47*altitude**(1.1)))))


#colors = ["#a6cee3", "#1f78b4", "#b2df8a",
#"#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f",
#"#ff7f00", "#cab2d6", "#6a3d9a", "#a6cee3",
#"#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
#"#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6",
#"#6a3d9a", "#a6cee3", "#1f78b4", "#b2df8a",
#"#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f",
#"#ff7f00", "#cab2d6", "#6a3d9a", "#a6cee3",
#"#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
#"#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6",
#"#6a3d9a"]

df = pd.read_csv('stdsop-B-Stars_single.csv', sep=', ', index_col=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7])

searchfor = ['5', '6', '7', '8', '9']
north  = df['dec1'] > -20.
Vstar  = df['type'].str.contains('V')
B56789 = df['type'].str.contains('|'.join(searchfor))

#df_filt =  df[north & Vstar & B56789]
df_filt =  df[north & B56789]
df_filt["RA"] = df_filt["ra1"].map(str)+':'+df_filt["ra2"].map(str)+':'+df_filt["ra3"].map(str)
df_filt["DEC"] = df_filt["dec1"].map(str)+':'+df_filt["dec2"].map(str)+':'+df_filt["dec3"].map(str)
df_final = df_filt[['name', 'RA', 'DEC', 'type']]


def vis_plot(date_str, i_sta, i_end):

	# Date for the  VLT on Paranal:
	lat, lon, height, horizon = '-24:37.50', '-70:24.2', 2500, '-1.15'

	# split date into readable formart for datetime.datetime():
	date_tmp  = date_str.split('-')

	# create datetime date:
	date 	  = datetime.datetime(int(date_tmp[0]), int(date_tmp[1]), int(date_tmp[2]))

	# Define today, yesterday and tomorrow in datetime format:
	td 		  = datetime.timedelta(days=1)
	today 	  = datetime.date(date.year, date.month, date.day)
	yesterday = today - td
	tomorrow  = today + td
	
	# Describes a position on Earth's surface
	# given Longitude, Latitude, elevation and horizon of Paranal
	obs = ephem.Observer()
	obs.long, obs.lat, obs.elevation, obs.horizon = lon, lat, height, horizon
	obs.epoch = '2000' # J2000
	obs.date = today # Date = today
	
	# Define sund and moon
	sun = ephem.Sun()
	moon = ephem.Moon()
	
	# Calculate Difference between current UTC and current local time
	off1 = datetime.datetime.now() # Current local time
	off2 = datetime.datetime.utcnow() # Current UTC time 
	diff = off2 - off1
	

	sunset = obs.next_setting(sun).datetime() # sunset of today
	moonset = obs.next_rising(moon).datetime() # moonset of today
	obs.date = tomorrow
	sunrise = obs.next_rising(sun).datetime() # sunrise tomorrow
	moonrise = obs.next_rising(moon).datetime() # moonrise tomorrow
	

	if sunrise > sunset + td: 
		obs.date = today
		sunrise = obs.next_rising(sun).datetime()
		moonrise = obs.next_rising(moon).datetime()
	
	td1 = datetime.timedelta(minutes=20) # 20 minutes in datetime formate
	td2 = datetime.timedelta(minutes=2) # 2 minutes in datetime format
		
	ras, decs, names, types = [], [], [], []
	for row in df_final.iterrows():
		ras.append(row[1]['RA'])
		decs.append(row[1]['DEC'])
		names.append(row[1]['name'])
		types.append(row[1]['type'])
	

	stars2 = []

	for i in range(len(decs)):
		stars2.append(ephem.FixedBody())
		stars2[i]._dec = decs[i]
		stars2[i]._ra = ras[i]

	print "stars:", len(stars2)
	
	sunephem = ephem.Sun()
	moonephem = ephem.Moon()
	sunan, moonan = [], []
	objans, clocks, moondists = [], [], []
	end = sunrise+td1
	
	for star in stars2[i_sta:i_end]:
		objan = []
		moondist = []
		clock = sunset-td1
		while clock < end:
			obs.date = clock
			if star == stars2[i_sta]:
				clocks.append(clock)
				moonephem.compute(obs)
				sunephem.compute(obs)
				sunan.append(float(sunephem.alt))
				moonan.append(float(moonephem.alt))
			star.compute(obs)
			objan.append(float(star.alt))
			moondist.append((ephem.separation((star.az, star.alt), 
			                                  (moon.az, moon.alt))))
			clock += td2
		objans.append(objan)
		moondists.append(moondist)
	
	#moonill = float(moonephem.moon_phase)*100
	#moonill = '%.2f'%moonill
	
	fig = figure(facecolor='white', figsize=(12, 9))
	fig.suptitle('Object visibility for Paranal on ' + str(today),fontsize=20)
	
	fig1 = fig.add_subplot(1,1,1)
	fig.subplots_adjust(bottom=0.08, top=0.88, left=0.09, right=0.75)
	i = i_sta

	for objan in objans:
		#if min(alt_to_airmass(np.array(objan)*180/pi)) > 1.2:
		#if names[i] in ['Hip022913', 'Hip022597', 'Hip024789']: # Jan B
		#if names[i] in ['Hip043765']: # Jan E
		if names[i] in ['Hip071615', 'Hip049704', 'Hip052158', 'Hip047022', 'Hip047352', 'Hip064722']: #Jan E

		#if names[i] in ['Hip022913', 'Hip022597', 'Hip024789', 'Hip027829', 'Hip029704', 'Hip031686']: # Feb B
		#if names[i] in ['Hip076069', 'Hip072505', 'Hip084810']: # Feb E

		#if names[i] in ['Hip024789', 'Hip029704', 'Hip031686', 'Hip035053', 'Hip039535']: # Mar B
		#if names[i] in ['Hip076069', 'Hip085385', 'Hip090337', 'Hip093200']: # Mar E

		#if names[i] in ['Hip038734', 'Hip039535', 'Hip040807']: # Apr A
		#if names[i] in ['Hip082673', 'Hip090337', 'Hip089684']: # Apr E

		#if names[i] in ['Hip045252', 'Hip047022']: May A
		#if names[i] in ['Hip094936', 'Hip094511', 'Hip099259', 'Hip098641', 'Hip108875', 'Hip107173']: #May E
		
		#if names[i] in ['Hip049704', 'Hip064722', 'Hip072154']:
		#if names[i] in ['Hip110573', 'Hip108875', 'Hip107173']: # Jun E

		#if names[i] in ['Hip072505', 'Hip076069']: # Jul B
		#if names[i] in ['Hip008387', 'Hip014143']: # Jul E

		#if names[i] in ['Hip076069', 'Hip082673', 'Hip085385']: # Aug B
		#if names[i] in ['Hip013327', 'Hip014764', 'Hip008387']: # Aug E

		#if names[i] in ['Hip089684',  'Hip090337', 'Hip094511', 'Hip094936', 'Hip095450', 'Hip098641', 'Hip099295']: # Sep B
		#if names[i] in ['Hip014764', 'Hip022913', 'Hip022597', 'Hip024789']: # Sep E

		#if names[i] in ['Hip100858', 'Hip099295', 'Hip098641', 'Hip108875']: Oct B
		#if names[i] in ['Hip024789', 'Hip022913', 'Hip022597', 'Hip029704', 'Hip027829', 'Hip031686']: # Oct E

		#if names[i] in ['Hip108875', 'Hip107173', 'Hip110573']: # Nov B
		#if names[i] in ['Hip029704', 'Hip029429', 'Hip031686', 'Hip035053']: # Nov E

		#if names[i] in ['Hip117927', 'Hip008387', 'Hip013327', 'Hip014764']: # Dec B
		#if names[i] in ['Hip038734', 'Hip032080', 'Hip030693']: # Dec E
		#if names[i] in ['Hip038843', 'Hip040410', 'Hip040217', 'Hip043564']:
			plot(clocks, objan, label=names[i]+ " " + types[i] + '\nRA:'+str(stars2[i]._ra)+\
			'\nDec:'+str(stars2[i]._dec)+'\n')
		i += 1
	
	plot(clocks, sunan, '--',  color = 'yellow')
	plot(clocks, moonan, '--',  color = 'black')
	fig1.legend(markerscale=0.5, bbox_to_anchor=(1.13, 1.12), loc=2, 
			borderaxespad=0., prop = {'size':8})
	
	fig1.set_ylim([-1/18.*pi, 0.5*pi])
	fig1.set_ylabel(r'$\rm{Altitude}$', {'fontsize':20})
	fig1.set_xlabel(r'$\rm{Time}\, [UTC]$', {'fontsize':20})
	
	i1, j1, k1, count, setting = 1, 1 ,1 ,0, 1
	i2, j2, k2 = 1, 1, 1
	for sunangle in sunan:
	    if setting == 1:
	        if i1 == 1:
	            if sunangle < -2/180.*pi:
	                set1, i1 = clocks[count], 0
	        if j1 == 1:
	            if sunangle < -12/180.*pi:
	                set2, j1 = clocks[count], 0
	        if k1 == 1:
	            if sunangle < -18/180.*pi:
	                set3, k1, setting = clocks[count], 0, 0
	    else:
	        if i2 == 1:
	            if sunangle > -2/180.*pi:
	                rise1, i2 = clocks[count], 0
	        if j2 == 1:
	            if sunangle > -12/180.*pi:
	                rise2, j2 = clocks[count], 0
	        if k2 == 1:
	            if sunangle > -18/180.*pi:
	                rise3, k2 = clocks[count], 0
	    count += 1
	
	hours  = mdates.HourLocator()
	hoursFmt = mdates.DateFormatter(r'$%H$')
	minorFormattor = FormatStrFormatter('')
	

	axvspan(clocks[0],set1, facecolor = '0.7', edgecolor = '0.7', alpha = 0.9)
	axvspan(set1,set2, facecolor = '0.8', edgecolor = '0.8', alpha = 0.9)
	axvspan(set2,set3, facecolor = '0.9', edgecolor = '0.9', alpha = 0.9)
	axvspan(clocks[-1], rise3, facecolor = '0.7', edgecolor = '0.7', alpha = 0.9)
	axvspan(rise2,rise1, facecolor = '0.8', edgecolor = '0.8', alpha = 0.9)
	axvspan(rise3,rise2, facecolor = '0.9', edgecolor = '0.9', alpha = 0.9)
	
	
	axhline(y=0, color = 'grey')
	axhline(y=45/180.*pi, color = 'grey')
	
	#Paranal:
	axhline(y=14/180.*pi, color = 'grey')
	
	for alt in range(5, 91, 5):
		val = 1. / (sin(radians(alt + 244/(165+47*alt**(1.1)))))
		text(clocks[-1]+25*td2, alt/180.*pi , r'$%.2f$'%val, ha = 'left', 
			va='center', fontsize=12)
	
	text(clocks[-1]+45*td2, 45/180.*pi, r'$\rm{Airmass}$', ha = 'left', 
	    va='center', rotation = -90, fontsize=20)
	#text(clocks[0]-4*td1, -18/180.*pi, r'$\rm{Moon\,Illumination}\,'+moonill+'\%$', 
	#    ha = 'left', va='bottom', fontsize=16)
	     
	text(clocks[0]+36*td1, -18/180.*pi, 
		r'$\rm{Night\,Start}\,'+str(set3.hour)+':'+str(set3.minute)+'$', 
		ha = 'left', va='bottom', fontsize=16)
	
	fig2=fig1.figure.add_axes(fig1.get_position(), frameon = False)
	fig2.xaxis.tick_top()
	fig2.yaxis.tick_right()
	fig1.xaxis.tick_bottom()
	fig2.yaxis.set_label_position("right")
	fig2.xaxis.set_label_position("top")
	fig2.set_xlim(clocks[0]-diff, clocks[-1]-diff)
	fig2.set_ylim(0, 10)
	
	fig2.xaxis.set_major_formatter(hoursFmt)
	fig2.set_xlabel(r'$\rm{Local\, Time}\,(%s)$' %(time.tzname[1]), {'fontsize':20})
	
	fig1.xaxis.set_major_locator(hours)
	fig1.xaxis.set_major_formatter(hoursFmt)
	fig1.yaxis.set_major_locator(FixedLocator(arange(-90, 100, 10) * pi/180.))
	fig2.yaxis.set_major_locator(FixedLocator(arange(5, 10.0, 10)))
	fig2.yaxis.set_major_formatter(minorFormattor)
	fig1.yaxis.set_minor_locator(FixedLocator(arange(-90, 100, 1) * pi/180.))
	fig1.yaxis.set_major_formatter(DegreeFormatter())
	fig1.yaxis.set_minor_formatter(DegreeFormatter())
	fig1.yaxis.set_minor_formatter(minorFormattor)
	
	xticks(fontsize = 16)
	yticks(fontsize = 16)
	savefig(date_str + "_" + str(i_sta) + "_" + str(i_end) + "_vis.pdf", format='pdf')


#for ss in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
#vis_plot("2018-12-15", 0,  10)
#vis_plot("2018-12-15", 11, 20)
#vis_plot("2018-12-15", 21, 30)
#vis_plot("2018-12-15", 31, 40)
#vis_plot("2018-12-15", 41, 50)
#vis_plot("2018-12-15", 51, 60)
#vis_plot("2018-12-15", 61, 70)
#vis_plot("2018-12-15", 71, 80)
#vis_plot("2018-12-15", 81, 90)
#vis_plot("2018-12-15", 91, 100)
#vis_plot("2018-12-15", 101, 110)
#vis_plot("2018-12-15", 111, 120)
#vis_plot("2018-12-15", 121, 130)
#vis_plot("2018-12-15", 131, 140)
#vis_plot("2018-12-15", 141, 150)
#vis_plot("2018-12-15", 151, 160)
#vis_plot("2018-12-15", 161, 170)
#vis_plot("2018-12-15", 171, 180)
#vis_plot("2018-12-15", 181, 190)
#vis_plot("2018-12-15", 191, 200)
#vis_plot("2018-12-15", 201, 210)
#vis_plot("2018-12-15", 211, 220)
#vis_plot("2018-12-15", 221, 230)
#vis_plot("2018-12-15", 231, 240)
#vis_plot("2018-12-15", 241, 250)
#vis_plot("2018-12-15", 251, 261)


#vis_plot("2018-01-15", 0,  10)
#vis_plot("2018-01-15", 11, 20)
#vis_plot("2018-01-15", 21, 30)
#vis_plot("2018-01-15", 31, 40)
#vis_plot("2018-01-15", 41, 50)
#vis_plot("2018-01-15", 51, 60)
#vis_plot("2018-01-15", 61, 70)
#vis_plot("2018-01-15", 71, 80)
#vis_plot("2018-01-15", 81, 90)
#vis_plot("2018-01-15", 91, 100)
#vis_plot("2018-01-15", 101, 110)
#vis_plot("2018-01-15", 111, 120)
#vis_plot("2018-01-01", 121, 130)
#vis_plot("2018-01-30", 131, 140)
#vis_plot("2018-01-30", 141, 150)
#vis_plot("2018-01-30", 151, 160)
#vis_plot("2018-01-30", 161, 170)
#vis_plot("2018-01-30", 171, 180)
#vis_plot("2018-01-01", 181, 190)
#vis_plot("2018-01-15", 191, 200)
#vis_plot("2018-01-15", 201, 210)
#vis_plot("2018-01-15", 211, 220)
#vis_plot("2018-01-15", 221, 230)
#vis_plot("2018-01-15", 231, 240)
#vis_plot("2018-01-15", 241, 250)
#vis_plot("2018-01-15", 251, 261)




#print ss, "done"


vis_plot("2018-01-01", 0, 261)
vis_plot("2018-01-15", 0, 261)
vis_plot("2018-01-30", 0, 261)


# Jan:
# B: 'Hip022597', 'Hip022913', 'Hip024789'
# E: 'Hip043765', not really a good star

# Feb:
# B: 'Hip022913', 'Hip022597', 'Hip024789', 'Hip027829', 'Hip029704', 'Hip031686'
# E: 'Hip076069', 'Hip072505', 'Hip084810'

# Mar:
# B: 'Hip024789', 'Hip029704', 'Hip031686', 'Hip035053', 'Hip039535'
# E: 'Hip076069', 'Hip085385', 'Hip090337', 'Hip093200' # not so good 

# Apr:
# B: 'Hip038734', 'Hip039535', 'Hip040807'
# E: 'Hip082673', 'Hip090337', 'Hip089684'

# May:
# B: take not main sequence!
# E: 'Hip094936', 'Hip094511', 'Hip099259', 'Hip098641', 'Hip108875', 'Hip107173' # ok

# Jun:
# B: take not main sequence!
# E: 'Hip110573', 'Hip108875', 'Hip107173' # good

# Jul:
# B: 'Hip072505', 'Hip076069'
# E: 'Hip008387', 'Hip014143' # ok

# Aug:
# B: 'Hip076069', 'Hip082673', 'Hip085385'
# E: 'Hip013327', 'Hip014764', 'Hip008387' 

# Sep:
# B: 'Hip089684', 'Hip090337', 'Hip094511', 'Hip094936', 'Hip095450', 'Hip098641', 'Hip099295'
# E: 'Hip014764', 'Hip022913', 'Hip022597', 'Hip024789'

# Oct:
# B: 'Hip100858', 'Hip099295', 'Hip098641', 'Hip108875'
# E: 'Hip024789', 'Hip022913', 'Hip022597', Hip029704, 'Hip027829', 'Hip031686' # perfect

# Nov:
# B: 'Hip108875', 'Hip107173', 'Hip110573'
# E: 'Hip029704', 'Hip029429', 'Hip031686', 'Hip035053' # ok

# Dec:
# B: 'Hip117927', 'Hip008387', 'Hip013327', 'Hip014764'
# E: 'Hip038734', 'Hip032080', 'Hip030693' # not perfect











