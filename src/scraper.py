# -*- coding: utf-8 -*-
"""Web Scraper for King County Health Inspection website."""

import requests
import io
from bs4 import BeautifulSoup
import sys
import re


INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'H'
}


def get_inspection_page(**kwargs):
    """Fetch a set of search results for you. Accepts keyword arguments for
    the possible query parameters. Builds a dictionary of request query
    parameters from incoming keywords. Make a request to the King County
    server using this query. Return the bytes content of the response and the
    encoding if there is no error. Raise an error if there is a problem with
    the response.
    """
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    el_response = requests.get(url, params=params)
    el_response.raise_for_status()
    return el_response.content, el_response.encoding


def load_inspection_page(src):
    """Load the inspection page."""
    src = io.open(src, encoding='utf8', mode='r')
    data = src.read()
    src.close()
    return data, 'utf-8'


def parse_source(html, encoding='utf-8'):
    """Set up the HTML as DOM nodes for scraping. Takes the response body (or
    the file read from disk) and parses it using BeautifulSoup. Returns the
    parsed object for further processing."""
    return BeautifulSoup(html, 'html5lib')


def extract_data_listings(html):
    """Find the container that holds each individual listing."""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(elem):
    """Take an element as an argument and return True if the element is both a
    <tr> and contains exactly two <td> elements immediately within it."""
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def clean_data(td):
    """Clean up the values we get from scraping."""
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restaurant_metadata(elem):
    """Take the listing for a single restaurant, and return a Python
    dictionary containing the metadata we’ve extracted."""
    metadata_rows = elem.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val_cell))
    return rdata


def is_inspection_row(elem):
    """"""
    is_tr = elem.name == 'tr'
    if not is_tr:
        return False
    td_children = elem.find_all('td', recursive=False)
    has_four = len(td_children) == 4
    this_text = clean_data(td_children[0]).lower()
    contains_word = 'inspection' in this_text
    does_not_start = not this_text.startswith('inspection')
    return is_tr and has_four and contains_word and does_not_start


def extract_score_data(elem):
    inspection_rows = elem.find_all(is_inspection_row)
    samples = len(inspection_rows)
    total = high_score = average = 0
    for row in inspection_rows:
        strval = clean_data(row.find_all('td')[2])
        try:
            intval = int(strval)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += intval
            high_score = intval if intval > high_score else high_score
    if samples:
        average = total/float(samples)
    data = {
        u'Average Score': average,
        u'High Score': high_score,
        u'Total Inspections': samples
    }
    return data


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)
    for listing in listings[:5]:
        metadata = extract_restaurant_metadata(listing)
        score_data = extract_score_data(listing)
        print(score_data)