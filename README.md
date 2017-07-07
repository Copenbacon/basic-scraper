# basic-scraper

A basic scraper built by following the tutorial at https://codefellows.github.io/sea-python-401d5/assignments/tutorials/scraper.html

Test data taken from http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Output=W&Business_Name=&Business_Address=&Longitude=&Latitude=&City=&Zip_Code=98109&Inspection_Type=All&Inspection_Start=2/1/2013&Inspection_End=2/1/2015&Inspection_Closed_Business=A&Violation_Points=&Violation_Red_Points=&Violation_Descr=&Fuzzy_Search=N&Sort=B

##Methods
```
get_inspection_page(**kwargs):
    """Fetch a set of search results for you. Accepts keyword arguments for
    the possible query parameters. Builds a dictionary of request query
    parameters from incoming keywords. Make a request to the King County
    server using this query. Return the bytes content of the response and the
    encoding if there is no error. Raise an error if there is a problem with
    the response.
    """

load_inspection_page(src):
    """Load the inspection page."""

parse_source(html, encoding='utf-8'):
    """Set up the HTML as DOM nodes for scraping. Takes the response body (or
    the file read from disk) and parses it using BeautifulSoup. Returns the
    parsed object for further processing."""

extract_data_listings(html):
    """Find the container that holds each individual listing."""

has_two_tds(elem):
    """Take an element as an argument and return True if the element is both a
    <tr> and contains exactly two <td> elements immediately within it."""

clean_data(td):
    """Clean up the values we get from scraping."""

extract_restaurant_metadata(elem):
    """Take the listing for a single restaurant, and return a Python
    dictionary containing the metadata we’ve extracted."""

is_inspection_row(elem):
    """Determines if a row we're looking at is the correct inspection row."""

extract_score_data(elem):
    """Give us the score data we want back."""
```