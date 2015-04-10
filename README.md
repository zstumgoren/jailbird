#Jailbird

Jailbird is a Python scraper that parses the Florida Department of Corrections' inmate mortality [database](http://www.dc.state.fl.us/pub/mortality/) and creates a spreadsheet of every death reported to the agency since 2000. 

This is a tool used by the Miami Herald for its [investigation](http://www.miamiherald.com/news/special-reports/florida-prisons/) into suspicious inmate deaths at prisons statewide.


##How it works

###Part I

Jailbird first creates two csv files, `base.csv` and `data.csv`. It then pulls information from the database's XML page and writes it into `base.csv`. 

| Name       | DC Number  | Date of Death | Jail   | Cause    | Case Status |
|------------|------------|---------------|--------|----------|-------------|
| John Smith | 123456     | 04/08/2015    | Jail A | Natural  | Pending     |
| Jane Doe   | 789101     | 04/07/2015    | Jail B | Homicide | Pending     |
| John Doe   | 121314     | 04/05/2015    | Jail B | Natural  | Pending     |


###Part II
Jailbird then takes each cell in the DC Number column from `base.csv` and, using a base URL, loops through each inmate's FDOC profile, grabbing birth dates, races and genders. Finally, Jailbird compiles everything in `data.csv`. 

| Name       | DC Number  | Date of Death | Jail   | Cause    | Case Status | Sex    | Race    | Date of Birth |
|------------|------------|---------------|--------|----------|-------------|--------|---------|---------------|
| John Smith | 123456     | 04/08/2015    | Jail A | Natural  | Pending     | Male   | White   | 03/14/1987    |
| Jane Doe   | 789101     | 04/07/2015    | Jail B | Homicide | Pending     | Female | Black   | 05/12/1973    |
| John Doe   | 121314     | 04/05/2015    | Jail B | Natural  | Pending     | Unknown   | Unknown | Unknown       |


Jailbird has to navigate through more than 4,000 pages, so this take some time. Please allow at least 20 minutes. 

Some inmates might not have profiles. Jailbird will recognize it ran into a blank page when searching for an inmate and write 'Unkown' in the final three columns.

After the script runs, Jailbird deletes `base.csv` and leaves you with clean and updated inmate death information in `data.csv`.

##How to use it

1. Download/clone the Jailbird repository to your local machine.
2. In the command terminal, `cd` to  `../jailbird`.
3. Jailbird does need some tools to work. Enter `pip install -r requirements.txt`. This will install:
	* **BeautifulSoup**, an HTML parser.
	* **requests**, an HTTP library.
	* **html5lib**, a secondary, HTML document parser.
	* **lxml**, a XML parser.

	
4. Now enter `python jailbird.py`


##When to use it


The FDOC conducts maintenance work on its website between 11:30 p.m. and 2 p.m. Monday through Saturday. This means the agency blocks access to the inmate's profiles. If you run Jailbird during these hours, it will return "Unknown" in the last three columns for each row in `data.csv`.

This is a work in progress. Please submit a pull request if you think this can be improved, or let me know of any issues. Questions? Message me here or send me an email at [calcantara@miamiherald.com](mailto:calcantara@miamiherald.com).
