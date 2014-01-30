"""
    Validate Module.


    For simple Address Book applet - Project 1 -
    CIS 422, W'14, University of Oregon.

    :author: Abdulrahman Alkhelaifi <abdul@cs.uoregon.edu>
    :author: Evan Townsend <etownsen@cs.uoregon.edu>
    :author: Kevin Beick <kbeick@uoregon.edu>
"""

import re

def validate_name(name):
    """
    Match strings of at least 1 character consisting of the upper
    and lower case alphabet as well as hyphens.
    """
    if name==None: return False, ""
    valid = re.match('^$|^[A-Za-z-]+$', name)
    if not valid:
        msg = "The name you entered is invalid.\nPlease try " + \
         "again using only alphabetical characters and hyphens."
        return False, msg
    return True, ""

def validate_address(address):
    """
    Match everything as name, with the addition of numbers, dashes,
    colons, periods, pound signs, and spaces.
    """
    if address==None: return False, ""
    valid = re.match(r'^$|^[0-9]+[0-9A-Za-z \.#:-]+$', address)
    if not valid:
        msg = "The address you entered is invalid.\nPlease try " + \
        "again using the standard address format e.g. 1500 main st."
        return False, msg
    return True, ""

def validate_address2(address2):
    """
    Match everything as name, with the addition of numbers, dashes,
    colons, periods, pound signs, and spaces.
    """
    if address2==None: return False, ""
    valid = re.match(r'^$|^[A-Za-z \.#:-]+[0-9A-Za-z:-]+$', address2)
    if not valid:
        msg = "The address line 2 you entered is invalid.\nPlease try again."
        return False, msg
    return True, ""

def validate_city(city):
    """
    Match everything as name, but with spaces and numbers.
    City name should start with letters.
    """
    if city==None: return False, ""
    valid = re.match('^$|^[A-Za-z]+[A-Za-z0-9 -]+$', city)
    if not valid:
        msg = "The city name you entered is invalid.\nPlease try " + \
        "again using alphabetical characters, spaces and numbers.\n" +\
        "City name should start with letters not numbers."
        return False, msg
    return True, ""

def validate_state(state):
    """
    Match a state name or abbreviation.
    """
    states = ['ALABAMA','AL', 'ALASKA','AK', 'ARIZONA','AZ','ARKANSAS','AR',
     'CALIFORNIA','CA', 'COLORADO','CO', 'CONNECTICUT','CT',
     'DELAWARE','DE', 'DISTRICT OF COLUMBIA','DC', 'FLORIDA','FL',
     'GEORGIA','GA', 'HAWAII','HI', 'IDAHO','ID', 'ILLINOIS','IL',
     'INDIANA','IN', 'IOWA','IA', 'KANSAS','KS', 'KENTUCKY','KY',
     'LOUISIANA','LA', 'MAINE','ME', 'MONTANA','MT', 'NEBRASKA','NE',
     'NEVADA','NV', 'NEW HAMPSHIRE','NH', 'NEW JERSEY','NJ', 'NEW MEXICO','NM',
     'NEW YORK','NY', 'NORTH CAROLINA','NC', 'NORTH DAKOTA','ND', 'OHIO','OH',
     'OKLAHOMA','OK', 'OREGON','OR', 'MARYLAND','MD', 'MASSACHUSETTS','MA',
     'MICHIGAN','MI', 'MINNESOTA','MN', 'MISSISSIPPI','MS', 'MISSOURI','MO',
     'PENNSYLVANIA','PA', 'RHODE ISLAND','RI', 'SOUTH CAROLINA','SC',
     'SOUTH DAKOTA','SD', 'TENNESSEE','TN', 'TEXAS','TX', 'UTAH','UT',
     'VERMONT','VT', 'VIRGINIA','VA', 'WASHINGTON','WA', 'WEST VIRGINIA','WV',
     'WISCONSIN','WI', 'WYOMING','WY']
    if state==None: return False, ""
    if state.upper() not in states:
        msg = "The state name you entered is invalid.\nPlease try again."
        return False, msg
    return True, ""

def validate_zip(zipcode):
    """
    Match either 5 (97403) or 9 (97403-1234) zip codes.
    """
    if zipcode==None: return False, ""
    valid = re.match('^$|^[0-9]{5}(-[0-9]{4})?$', zipcode)
    if not valid:
        msg = "The zip code you entered is invalid.\nPlease try " + \
        "again using either 5 (97403) or 9 (97403-1234) zip codes."
        return False, msg
    return True, ""

def validate_email(email):
    """
    Match an email address in the standard format name@domain.tld.
    """
    if email==None: return False, ""
    valid = re.match(r'^$|[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}', email)
    if not valid:
        msg = "The email address you entered is invalid.\nPlease try " + \
        "again using the standard format name@domain.tld."
        return False, msg
    return True, ""

def validate_phone(phone):
    """
    Match a 10 digits phone number in one of the following formats:
    
    | 1112223333 or (111)222-3333 or 111-222-3333.
    """
    if phone==None: return False, ""
    valid = re.match('^$|^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$', phone)
    if not valid:
        msg = "The phone number you entered is invalid.\nPlease try again " + \
        "using 10 digits in one of the following formats:\n" + \
        "1112223333 or (111)222-3333 or 111-222-3333."
        return False, msg
    return True, ""
