"""
    Utilities Module.


    For simple Address Book applet - Project 1 -
    CIS 422, W'14, University of Oregon.

    :author: Abdulrahman Alkhelaifi <abdul@cs.uoregon.edu>
"""

import cPickle as pickle

def open_addressbook(file_name):
    """
    Open an address book file, returning an AddressBook object.
    Raises IOError if file is not found or has no read permission.
    """
    address_book = None
    with open(file_name, 'rb') as data:
        address_book = pickle.load(data)
    return address_book

def save_addressbook(addressbook, file_name):
    """
    Save an AddressBook object to a file.
    Raises IOError if file exist and has no write permission.
    """
    with open(file_name, 'wb') as output:
        pickle.dump(addressbook, output, pickle.HIGHEST_PROTOCOL)

def abbreviate_state(state):
    """
    Return an abbreviation of the given state.
    Raises KeyError if key does not exist.
    """
    states_abbr = {'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 
                   'ARKANSAS': 'AR', 'CALIFORNIA': 'CA', 'COLORADO': 'CO',
                   'CONNECTICUT': 'CT', 'DELAWARE': 'DE',
                   'DISTRICT OF COLUMBIA': 'DC', 'FLORIDA': 'FL',
                   'GEORGIA': 'GA', 'HAWAII': 'HI', 'IDAHO': 'ID',
                   'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
                   'KANSAS': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA',
                   'MAINE': 'ME', 'MONTANA': 'MT', 'NEBRASKA': 'NE',
                   'NEVADA': 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
                   'NEW MEXICO': 'NM', 'NEW YORK': 'NY',
                   'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', 'OHIO': 'OH',
                   'OKLAHOMA': 'OK', 'OREGON': 'OR', 'MARYLAND': 'MD', 
                   'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN',
                   'MISSISSIPPI': 'MS', 'MISSOURI': 'MO', 'PENNSYLVANIA': 'PA',
                   'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
                   'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN', 'TEXAS': 'TX',
                   'UTAH': 'UT', 'VERMONT': 'VT', 'VIRGINIA': 'VA',
                   'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV', 
                   'WISCONSIN': 'WI', 'WYOMING': 'WY'}
    try:
        abbr = states_abbr[state.upper()]
    except:
        return state.upper()
    return abbr.upper()
    