#Jailbird


Jailbird is a Python scraper that parses the Florida Department of Correction's inmate mortality [database](http://www.dc.state.fl.us/pub/mortality/) and creates a spreadsheet of every death reported to the agency since 2000. 

This is a tool used by the Miami Herald in its [investigation](http://www.miamiherald.com/news/special-reports/florida-prisons/) into a series of suspicious prison deaths. 

##Requirements

Main parts: 

* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) 

* [Requests](http://docs.python-requests.org/en/latest/)


##How to use

1. Download and zip file.
2. In command terminal, `cd` to the jailbird folder.
3. Inside, enter `python jailbird.py`

Note: This scraper navigates through more than 4,000 inmate pages on the FDOC's website. After the scraper is finished, all the data should be in `data.csv`.

This is a work in progress. Please submit a pull request if you think this can be improved. Questions? Message me here or send me at [calcantara@miamiherald.com](mailto:calcantara@miamiherald.com).






