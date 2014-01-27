"""
    Validate Module.


    For simple Address Book applet - Project 1 -
    CIS 422, W'14, University of Oregon.

    :author: Abdulrahman Alkhelaifi <abdul@cs.uoregon.edu>
    :author: Evan Townsend <etownsen@cs.uoregon.edu>
"""

import re

def validate_name(name):
    """
    This will match strings of at least 1 character consisting of the upper
    and lower case alphabet as well as hyphens.
    """
    valid = re.match('^[A-Za-z-]+$', name)
    if not valid:
        # print "Invalid name"
        return False
    return True

def validate_address(address):
    """
    This matches everything as name, with the addition of numbers, dashes,
    colons, periods, pound signs, and spaces.
    """
    valid = re.match(r'^[0-9]+[0-9A-Za-z \.#:-]+$', address)
    if not valid:
        # print "Invalid name"
        return False
    return True

def validate_city(city):
    """
    Pretty much the same as the names, but with spaces and numbers.
    City name should start with letters.
    """
    valid = re.match('^[A-Za-z]+[A-Za-z0-9 -]+$', city)
    if not valid:
        # print "Invalid city"
        return False
    return True

def validate_state(state):
    """
    Full alphabet and spaces.
    """
    valid = re.match('^[A-Za-z ]+$', state)
    if not valid:
        # print "Invalid state"
        return False
    return True

def validate_zip(zipcode):
    """
    Matches either 5 (97403) or 9 (97403-1234) zip codes.
    """
    valid = re.match('^[0-9]{5}(-[0-9]{4})?$', zipcode)
    if not valid:
        # print "Invalid zipcode"
        return False
    return True

def validate_email(email):
    """
    Matches an email address.
    """
    valid = re.match(r'[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}', email)
    if not valid:
        # print "Invalid email"
        return False
    return True

def main():
    """
    Testing...
    """
    print 'name T: evan', validate_name('evan')
    print 'name T: ev-an', validate_name('ev-an')
    print 'name F: e123', validate_name('e123')
    print
    print 'address T: 1500 main st', validate_address('1500 main st')
    print 'address T: 1500 7th ave', validate_address('1500 7th ave')
    print 'address F: main st', validate_address('main st')
    print
    print 'city T: eugene', validate_city('eugene')
    print 'city T: new york', validate_city('new york')
    print 'city F: 111', validate_city('111')
    print
    print 'state T: Oregon', validate_state('Oregon')
    print 'state T: New Mexico', validate_state('New Mexico')
    print 'state F: ore-gon', validate_state('ore-gon')
    print 'state F: or12', validate_state('or12')
    print
    print 'zip T: 00000', validate_zip('00000')
    print 'zip T: 00000-1111', validate_zip('00000-1111')
    print 'zip F: 0', validate_zip('0')
    print 'zip F: 00001111', validate_zip('00001111')
    print 'zip F: 00000-111', validate_zip('00000-111')
    print 'zip F: 00000-11111', validate_zip('00000-11111')
    print
    print 'email T: a@b.com', validate_email('a@b.com')
    print 'email F: a@b', validate_email('a@b')
    print 'email F: a@b.', validate_email('a@b.')
    print 'email F: a@.c', validate_email('a@.c')
    print 'email F: @b.c', validate_email('@b.c')
    print 'email F: b.c', validate_email('b.c')

if __name__ == "__main__":
    main()
