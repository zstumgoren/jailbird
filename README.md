#Jailbird

Jailbird is a Python scraper that parses the Florida Department of Correction's inmate mortality [database](http://www.dc.state.fl.us/pub/mortality/) and creates a spreadsheet of every death reported to the agency since 2000. 

This is a tool used by the Miami Herald in its [investigation](http://www.miamiherald.com/news/special-reports/florida-prisons/) into a series of suspicious prison deaths. 


##How it works

Jailbird is works in two parts.

###Part I

Jailbird first creates two csv files, `base.csv` and `data.csv`. It then pulls information from the FDOC's XML page and creates a speadsheet into `base.csv`. It also works off a list that cleans prison names.

| Name       | DC Number  | Date of Death | Jail   | Cause    | Case Status |
|------------|------------|---------------|--------|----------|-------------|
| John Smith | 123456     | 04/08/2015    | Jail A | Natural  | Pending     |
| Jane Doe   | 789101     | 04/07/2015    | Jail B | Homicide | Pending     |
| John Doe   | 121314     | 04/05/2015    | Jail B | Natural  | Pending     |


###Part II
Jailbird then takes the DC Number from `base.csv` and loops through each inmate's FDOC profile page, grabbing birthdates, race and sex. It also copies everything `base.csv` and combines everything into `data.csv`. 

Jailbird has to navigate more than 4,000 entires, so this take some time. Please allow at least 20 minutes for it to run. 

After the script runs, Jailbird deletes `base.csv` and leaves you with clean and updated inmate death information in `data.csv`.

Ready to try it for yourself? 

##How to use it

1. Download/clone the repo and open the zip file.
2. In the command terminal, `cd` to the `jailbird` folder.
3. We need to install the requirements. Enter `pip install -r requirements.txt`. This will install:
	* **BeautifulSoup**, an HTML parser.
	* **requests**, an HTTP library.
	* **htmllib**, a secondary, HTML document parser.
	
4. Now enter `python jailbird.py`


##When to use it


The FDOC often does maintenence work on its website between 11:30 p.m. and 2 p.m. Monday through Saturday. This means the agency blocks access to the inmate's profile pages, and Jailbird will return "Unknown" in `data.csv` if you run it during those hours. 


This is a work in progress. Please submit a pull request if you think this can be improved. Questions? Message me here or send me at [calcantara@miamiherald.com](mailto:calcantara@miamiherald.com).