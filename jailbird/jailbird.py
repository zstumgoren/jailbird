#  _____                 ___    __                   __     
# /\___ \            __ /\_ \  /\ \      __         /\ \    
# \/__/\ \     __   /\_\\//\ \ \ \ \____/\_\  _ __  \_\ \   
#    _\ \ \  /'__`\ \/\ \ \ \ \ \ \ '__`\/\ \/\`'__\/'_` \  
#   /\ \_\ \/\ \L\.\_\ \ \ \_\ \_\ \ \L\ \ \ \ \ \//\ \L\ \ 
#   \ \____/\ \__/.\_\\ \_\/\____\\ \_,__/\ \_\ \_\\ \___,_\
#    \/___/  \/__/\/_/ \/_/\/____/ \/___/  \/_/\/_/ \/__,_ /
#                                                          

import csv
import os
import requests
import urllib2
from bs4 import BeautifulSoup

# create starting files
load_xml_file = 'base.csv'
finished_file = 'data.csv'

load_xml = open(load_xml_file, 'w')
finished = open(finished_file, 'w')

load_xml.close()
finished.close()

# grab DOC's xml file
url = 'http://www.dc.state.fl.us/pub/mortality/mortality.xml'

# read it
xml = urllib2.urlopen(url).read()

# parse it
soup_xml = BeautifulSoup(xml, 'html5lib')

with open('base.csv', 'w') as csvfile:

	# add headers
	writer = csv.DictWriter(csvfile, fieldnames = ['Name', 'DC Number', 'Date of Death', 'Jail', 'Cause', 'Case Status'], delimiter = ',')

	# writer headers
	writer.writeheader()

	# get inmate information
	names = soup_xml.find_all('name')
	names = [name for name in names]
	years = soup_xml.find_all('dod')	
	jail = soup_xml.find_all('facid')
	cause = soup_xml.find_all('mod')
	status = soup_xml.find_all('status')
 	dc_num = soup_xml.find_all('dcnum')
	
 	print 'Scraping DOC XML site...'

 	# loop through it all
	for n, y, j, c, s, dc_n in zip(names, years, jail, cause, status, dc_num):

		# create jail names	list	
		jail_replacements = [
			('209-R.M.C.- MAIN UNIT', 'Reception and Medical Center'),
			('213-UNION C.I.', 'Union Correctional Institution'),
			('101-APALACHEE WEST UNIT','Apalachee Correctional Institution'),
			('102-APALACHEE EAST UNIT','Apalachee Correctional Institution'),
			('103-JEFFERSON C.I.','Jefferson Correctional Institution'),
			('104-JACKSON C.I.','Jackson Correctional Institution'),
			('105-CALHOUN C.I.','Calhoun Correctional Institution'),
			('106-CENTURY C.I.','Century Correctional Institution'),
			('107-HOLMES C.I.','Holmes Correctional Institution'),
			('108-WALTON C.I.','Walton Correctional Institution'),
			('109-GULF C.I.','Gulf Correctional Institution'),
			('110-NWFRC MAIN UNIT.','Northwest Florida Reception Center'),
			('111-GADSDEN C.F.','Gadsen Correctional Facility'),
			('112-BAY C.F.','Bay Correctional Facility'),
			('113-FRANKLIN C.I.','Franklin Correctional Institution'),
			('114-R.JUNCTION WORK CAMP','River Junction Work Camp'),
			('115-OKALOOSA C.I.','Okaloosa Correctional Institution'),
			('118-WAKULLA C.I.', 'Wakulla Correctional Institution'),
			('119-SANTA ROSA C.I.','Santa Rosa Correctional Institution'),
			('120-LIBERTY C.I.','Liberty Correctional Institution'),
			('122-WAKULLA ANNEX','Wakulla Correctional Institution'),
			('125-NWFRC ANNEX.','Northwest Florida Reception Center'),
			('110-NWFRC MAIN UNIT.','Northwest Florida Reception Center'),
			('135-SANTA ROSA ANNEX','Santa Rosa Correctional Institution'),
			('150-GULF C.I.- ANNEX','Gulf Correctional Institution'),
			('159-GRACEVILLE C.F.','Graceville Correctional Facility'),
			('161-OKALOOSA WORK CAMP','Okaloosa Correctional Institution'),
			('168-TALLAHASSEE C.R.C','Tallahassee Community Release Center'),
			('185-BLACKWATER C.F.', 'Blackwater Correctional Facility'),
			('201-COLUMBIA C.I.', 'Columbia Correctional Institution'),
			('205-FLORIDA STATE PRISON', 'Florida State Prison'),
			('206-FSP WEST UNIT', 'Florida State Prison'),
			('208-R.M.C.- WEST UNIT', 'Reception and Medical Center'),
			('209-R.M.C.- MAIN UNIT', 'Reception and Medical Center'),
			('209-R.M.C.-MAIN UNIT', 'Reception and Medical Center'),
			('210-NEW RIVER CI', 'New River Correctional Institution'),
			('211-CROSS CITY C.I.', 'Cross City Correctional Institution'),
			('213-UNION C.I.', 'Union Correctional Institution'),
			('215-HAMILTON C.I.', 'Hamilton Correctional Institution'),
			('216-MADISON C.I.', 'Madison Correctional Institution'),
			('218-TAYLOR C.I.', 'Taylor Correctional Institution'),
			('221-R.M.C WORK CAMP', 'Reception and Medical Center'),
			('223-MAYO C.I. ANNEX', 'Mayo Correctional Institution'),
			('224-TAYLOR ANNEX', 'Taylor Correctional Institution'),
			('230-SUWANNEE C.I', 'Suwannee Correctional Institution'),
			('231-SUWANNEE C.I. ANNEX', 'Suwannee Correctional Institution'),
			('232-SUWANNEE WORK CAMP', 'Suwannee Correctional Institution'),
			('250-HAMILTON ANNEX', 'Hamilton Correctional Institution'),
			('251-COLUMBIA ANNEX', 'Columbia Correctional Institution'),
			('255-LAWTEY C.I.', 'Lawtey Correctional Institution'),
			('267-BRIDGES OF JACKSONVI', 'The Jacksonville Bridge Community Release Center'),
			('279-BAKER C.I.', 'Baker Correctional Institution'),
			('281-LANCASTER C.I.', 'Lancaster Correctional Institution'),
			('282-TOMOKA C.I.', 'Tomoka Correctional Institution'),
			('304-MARION C.I.', 'Marion Correctional Institution'),
			('307-SUMTER C.I.', 'Sumter Correctional Institution'),
			('310-BREVARD C.I.', 'Brevard Correctional Institution'),
			('312-LAKE C.I.', 'Lake Correctional Institution'),
			('314-LOWELL C.I.', 'Lowell Correctional Institution'),
			('320-CFRC-MAIN', 'Central Florida Reception Center'),
			('321-CFRC-EAST', 'Central Florida Reception Center'),
			('323-CFRC-SOUTH', 'Central Florida Reception Center'),
			('336-HERNANDO C.I.', 'Hernando Correctional Institution'),
			('341-COCOA W.R.C.', 'The Cocoa Bridge Community Release Center'),
			('353-TTH OF KISSIMMEE', 'The Transition House of Kissimmee'),
			('363-BREVARD WORK CAMP', 'Brevard Correctional Institution'),
			('365-SUMTER WORK CAMP', 'Sumter Correctional Institution'),
			('367-LOWELL ANNEX', 'Lowell Correctional Institution'),
			('368-FL.WOMENS RECPN.CTR', 'Florida Women\'s Reception Center'),
			('374-KISSIMMEE C.R.C.', 'Kissimmee Community Release Center'),
			('401-EVERGLADES C.I.', 'Everglades Correctional Institution'),
			('402-S.F.R.C.', 'South Florida Reception Center'),
			('403-S.F.R.C SOUTH UNIT', 'South Florida Reception Center'),
			('404-OKEECHOBEE C.I.', 'Okeechobee Correctional Institution'),
			('405-SOUTH BAY C.F.', 'South Bay Correctional Facility'),
			('406-GLADES C.I.', 'Glades Correctional Institution'),
			('419-HOMESTEAD C.I.', 'Homestead Correctional Institution'),
			('420-MARTIN WORK CAMP', 'Martin Correctional Institution'),
			('430-MARTIN C.I.', 'Martin Correctional Institution'),
			('462-GLADES WORK CAMP', 'Glades Correctional Institution'),
			('463-DADE C.I.', 'Dade Correctional Institution'),
			('464-SAGO PALM RE-ENTRY C', 'Sago Palm Re-Entry Center'),
			('469-W.PALM BEACH C.R.C.', 'West Palm Beach Community Release Cente'),
			('473-OPA LOCKA C.R.C.', 'Opa Locka Community Release Center'),
			('475-BROWARD C.I.', 'Broward Correctional Institution'),
			('501-HARDEE C.I.', 'Hardee Correctional Institution'),
			('503-AVON PARK C.I.', 'Avon Park Correctional Institution'),
			('504-AVON PARK WORK CAMP', 'Avon Park Correctional Institution'),
			('510-CHARLOTTE C.I.', 'Charlotte Correctional Institution'),
			('511-MOORE HAVEN C.F.', 'Moore Haven Correctional Facility'),
			('529-HILLSBOROUGH C.I.', 'Hillsborough Correctional Institution'),
			('564-DESOTO ANNEX', 'DeSoto Correctional Institution'),
			('573-ZEPHYRHILLS C.I.', 'Zephyrhills Correctional Institution'),
			('576-HENDRY C.I.', 'Hendry Correctional Institution'),
			('580-POLK C.I.', 'Polk Correctional Institution'),
			('583-ST. PETE C.R.C.', 'St. Petersburg Community Release Center')
		]

		# grab jail variable
		new_names = j.contents[0]

		# loop through list and make replacements
		for name in jail_replacements:
			new_names = new_names.replace(*name)

		# create status list
		status_replacements = [
			('OPEN', 'Open'),
			('Open-FDLE', 'Open'),
			('Open- FDLE', 'Open'),
			('Open - FDLE', 'Open'),
			('Open/FDLE', 'Open'),
			('Open - MDPD / FDLE', 'Open'),
			('Open - MDPD/FDLE', 'Open'),
			('Open - PBSO', 'Open'),
			('Open - PBSO/FDLE', 'Open'),
			('Open-MDPD', 'Open'),
			('Open - MDPD', 'Open'),
			('Open/PBSO', 'Open'),
			('Open/MDPD', 'Open'),
			('Open - MCSO/FDLE', 'Open'),
			('Open FBI / FDLE', 'Open')
		]

		# grab jail variable
		new_status = s.contents[0]

		# loop through list and make replacements
		for item in status_replacements:
			new_status = new_status.replace(*item)

		# create row writer
		inmate_writer = csv.writer(csvfile)

		# write looped content into rows
		inmate_writer.writerow((
			n.contents[0],
			dc_n.contents[0],
			y.contents[0],
			new_names, 
			c.contents[0], 
			new_status,
		))

print 'XML scrape complete.'

# open xml file and write it to finished file
with open('base.csv', 'r') as csvinput:

	with open('data.csv', 'w') as csvoutput:
		
		# create writer and reader for finished file
		writer = csv.writer(csvoutput, lineterminator='\n')

		reader = csv.reader(csvinput)

		# write headers
		writer.writerow([
			'Name',
			'DC Number',
			'Date of Death',
			'Jail',
			'Cause',
			'Case Status',
			'Sex',
			'Race',
			'Date of Birth'
		])

		row = next(reader)

		print 'Creating links and looping through inmate pages...'

		for row in reader:
			# row[1] is the DC number from xml_file. 
			# add to end of link for inmate's page
			url = 'http://www.dc.state.fl.us/InmateReleases/list.asp?DataAction=GetInmate&DCNumber=' + row[1]

			# go to website from link
			r = requests.get(url)

			soup = BeautifulSoup(r.content, "html.parser")

			# find sex
			find_sex = soup.find(text='Sex:')
			
			# this separates working and broken links
			if find_sex == 'Sex:':

				#write sex
				sex = find_sex.parent.findNext('td').contents[0].replace(u'\xa0', u' ').title()		
				# find race
				find_race = soup.find(text='Race:')

				#write race
				race = find_race.parent.findNext('td').contents[0].replace(u'\xa0', u' ').title()	

				# find date of birth
				find_dob = soup.find(text='Birth Date:')

				#write date of birth
				dob = find_dob.parent.findNext('td').contents[0].replace(u'\xa0', u' ').lstrip()
				
				# d1 = datetime.(y.contents[0])
				# d2 = datetime.(dob)
				# age = (d2-d1).days

				# add sex, race and date of birth rows.
				row.append(sex)
				row.append(race)
				row.append(dob)

				# row.append(age)
				
				# everything into rows
				writer.writerow(row)

			# write unknown in row if page doesn't exist.
			else:
				row.append('Unknown')
				row.append('Unknown')
				row.append('Unknown')
				writer.writerow(row)

#remove xml loading file.
os.remove("base.csv")

print 'Done!'