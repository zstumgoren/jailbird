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
from lxml import etree
#from bs4 import BeautifulSoup

### CODE REDESIGN EXERCISE ####
# Try to redesign the code below to use functions
# that do one thing (download the XML, parse the XML, etc.)
# and then invoke those functions in the "main" function.
# The "main" function is invoked, or triggered, at the very bottom
# of the script. The goal in doing this is to make it easier to
# quickly understand what the code is doing just by reading the top
# of the file, and to isolate potential bugs to specific functions.
# This pays dividends when you need to change things down the road,
# or when future you needs to re-run the script a year from now.


# The main function is the quarterback for your whole script (the "maestro", if you will).
# It invokes all the nicely packaged behavior (in functions) from below.
def main():
    # Create dictionary of jail name substitutions
    jail_replacements = get_jail_name_substitutions()
    # Get the xml
    xml_records = get_xml()
    # Get the clean data, passing in the jail_replacements read from an external file
    clean_data = get_clean_data(xml_records, jail_replacements)
    #TODO:  Write out the data (as an exercise)

def get_clean_data(xml_records, jail_replacements):
    clean_data = []
    # Loop through the records and extract data and perform cleanups
    for record in xml_records:
        # Below we pluck data using list position rather than an xml search. This is much more efficient if the data allows it (see note below).
        # We pluck the data and insert them int
        row = [
            record[0].text, # name
            record[1].text, # dc_num
            record[2].text, # dod
            jail_replacements[record[3].text], # fac_id, which we replace with a clen name
            record[4].text, # mod
            #TODO: apply a function to the below status to clean it up
            record[5].text, # status
        ]
        clean_data.append(row)
        # NOTE: The above positional indexing might not work if the XML is not structured consistently so that all xml vars are in order (Name, DCNum, DoD, etc.),
        # so perhaps a "find" strategy is preferable. Here's an example of the less efficient (but safer) alternative, if that's a known issue:
        # name = record.find('NAME').text
    return clean_data

def get_xml():
    # grab DOC's xml file
    url = 'http://www.dc.state.fl.us/pub/mortality/mortality.xml'
    xml_as_string = urllib2.urlopen(url)#.read()
    #soup_xml = BeautifulSoup(xml)
    # Instead of beautifulsoup, use lxml
    xml = etree.parse(xml_as_string)
    # Get the root node of the xml and its children, which are the 
    # individual records you care about
    xml_records = xml.getroot().getchildren()
    return xml_records

def get_jail_name_substitutions():
    # Use os module to get the directory of this script, which also contains our 
    # jail_replacements.csv. We can use this bit of code so you can invoke the script from
    # multiple places on the command line without pathing issues.
    directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the csv file
    file_path = os.path.join(directory, 'jail_name_substitutions.csv')
    # Create a dictionary to store the replacements. This will 
    # be much more efficient downstream when performing the cleanups.
    replacements = {}
    # Read in the data and transform into a dictionary, which allows you
    # to look up the clean name by the raw (or dirty) name and subsitute as needed downstream
    for raw_name, clean_name in csv.reader(open(file_path, 'rb')):
        replacements[raw_name] = clean_name
    # Finally, return the dictionary (it will be stored in the "jail_replacements" variable
    # in the "main" function above
    return replacements

### NOTE WE CALL MAIN HERE TO EXECUTE ALL OF ABOVE CODE ###
main()


### BELOW IS REST OF ORIGINAL CODE, FOR REFERENCE ###
#def rest_of_code(jail_replacements):
#    load_xml_file = 'base.csv'
#    finished_file = 'data.csv'
#
#    load_xml = open(load_xml_file, 'w')
#    finished = open(finished_file, 'w')
#
#    load_xml.close()
#    finished.close()
#
#
#    with open('base.csv', 'w') as csvfile:
#        writer = csv.DictWriter(csvfile, fieldnames = ['Name', 'DC Number', 'Date of Death', 'Jail', 'Cause', 'Case Status'], delimiter = ',')
#
#        # writer headers
#        writer.writeheader()
#
#        # get inmate information
#        names = soup_xml.find_all('name')
#        names = [name for name in names]
#        years = soup_xml.find_all('dod')	
#        jail = soup_xml.find_all('facid')
#        cause = soup_xml.find_all('mod')
#        status = soup_xml.find_all('status')
#        dc_num = soup_xml.find_all('dcnum')
#
#        print 'Scraping DOC XML site...'
#
#        # loop through it all
#        for n, y, j, c, s, dc_n in zip(names, years, jail, cause, status, dc_num):
#
#
#            # grab jail variable
#            #new_names = j.contents[0]
#
#            # loop through list and make replacements
#            #for name in jail_replacements:
#            #    new_names = new_names.replace(*name)
#
#            # We'll quickly fetch the clean name from the dictionary, 
#            # using the dirty name
#            dirty_jail_name = j.contents[0]
#            clean_jail_name = jail_replacements[dirty_jail_name]
#
#            # create status list
#            status_replacements = [
#                ('OPEN', 'Open'),
#                ('Open-FDLE', 'Open'),
#                ('Open- FDLE', 'Open'),
#                ('Open - FDLE', 'Open'),
#                ('Open/FDLE', 'Open'),
#                ('Open - MDPD / FDLE', 'Open'),
#                ('Open - MDPD/FDLE', 'Open'),
#                ('Open - PBSO', 'Open'),
#                ('Open - PBSO/FDLE', 'Open'),
#                ('Open-MDPD', 'Open'),
#                ('Open - MDPD', 'Open'),
#                ('Open/PBSO', 'Open'),
#                ('Open/MDPD', 'Open'),
#                ('Open - MCSO/FDLE', 'Open'),
#                ('Open FBI / FDLE', 'Open')
#            ]
#
#            # grab jail variable
#            new_status = s.contents[0]
#
#            # loop through list and make replacements
#            for item in status_replacements:
#                new_status = new_status.replace(*item)
#
#            # create row writer
#            inmate_writer = csv.writer(csvfile)
#
#            # write looped content into rows
#            inmate_writer.writerow((
#                n.contents[0],
#                dc_n.contents[0],
#                y.contents[0],
#                # Instead of new_names, we'll substitute the clean name
#                #new_names, 
#                clean_jail_name,
#                c.contents[0], 
#                new_status,
#            ))
#
#    print 'XML scrape complete.'
#
#    # open xml file and write it to finished file
#    with open('base.csv', 'r') as csvinput:
#
#        with open('data.csv', 'w') as csvoutput:
#            
#            # create writer and reader for finished file
#            writer = csv.writer(csvoutput, lineterminator='\n')
#
#            reader = csv.reader(csvinput)
#
#            # write headers
#            writer.writerow([
#                'Name',
#                'DC Number',
#                'Date of Death',
#                'Jail',
#                'Cause',
#                'Case Status',
#                'Sex',
#                'Race',
#                'Date of Birth'
#            ])
#
#            row = next(reader)
#
#            print 'Creating links and looping through inmate pages...'
#
#            for row in reader:
#                # row[1] is the DC number from xml_file. 
#                # add to end of link for inmate's page
#                url = 'http://www.dc.state.fl.us/InmateReleases/list.asp?DataAction=GetInmate&DCNumber=' + row[1]
#
#                # go to website from link
#                r = requests.get(url)
#
#                soup = BeautifulSoup(r.content, "html.parser")
#
#                # find sex
#                find_sex = soup.find(text='Sex:')
#                
#                # this separates working and broken links
#                if find_sex == 'Sex:':
#
#                    #write sex
#                    sex = find_sex.parent.findNext('td').contents[0].replace(u'\xa0', u' ').title()		
#                    # find race
#                    find_race = soup.find(text='Race:')
#
#                    #write race
#                    race = find_race.parent.findNext('td').contents[0].replace(u'\xa0', u' ').title()	
#
#                    # find date of birth
#                    find_dob = soup.find(text='Birth Date:')
#
#                    #write date of birth
#                    dob = find_dob.parent.findNext('td').contents[0].replace(u'\xa0', u' ').lstrip()
#                    
#                    # d1 = datetime.(y.contents[0])
#                    # d2 = datetime.(dob)
#                    # age = (d2-d1).days
#
#                    # add sex, race and date of birth rows.
#                    row.append(sex)
#                    row.append(race)
#                    row.append(dob)
#                    
#                    # everything into rows
#                    writer.writerow(row)
#
#                # write unknown in row if page doesn't exist.
#                else:
#                    row.append('Unknown')
#                    row.append('Unknown')
#                    row.append('Unknown')
#                    writer.writerow(row)
#
#    #remove xml loading file.
#    os.remove("base.csv")
#
#    print 'Done!'

