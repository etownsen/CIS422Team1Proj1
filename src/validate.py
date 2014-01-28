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
    if name==None: return False
    valid = re.match('^$|^[A-Za-z-]+$', name)
    if not valid:
        print "The name you entered is invalid.\nPlease try " + \
        "again using only alphabetical characters and hyphens."
        return False
    return True

def validate_address(address):
    """
    Match everything as name, with the addition of numbers, dashes,
    colons, periods, pound signs, and spaces.
    """
    if address==None: return False
    valid = re.match(r'^$|^[0-9]+[0-9A-Za-z \.#:-]+$', address)
    if not valid:
        print "The address you entered is invalid.\nPlease try " + \
        "again using the standard address format i.e. 1500 main st."
        return False
    return True

def validate_city(city):
    """
    Match everything as name, but with spaces and numbers.
    City name should start with letters.
    """
    if city==None: return False
    valid = re.match('^$|^[A-Za-z]+[A-Za-z0-9 -]+$', city)
    if not valid:
        print "The city name you entered is invalid.\nPlease try " + \
        "again using alphabetical characters, spaces and numbers.\n" +\
        "City name should start with letters not numbers."
        return False
    return True

def validate_state(state):
    """
    Match the full alphabet and spaces.
    """
    if state==None: return False
    valid = re.match('^$|^[A-Za-z ]+$', state)
    if not valid:
        print "The state name you entered is invalid.\nPlease try " + \
        "again using only alphabetical characters and spaces."
        return False
    return True

def validate_zip(zipcode):
    """
    Match either 5 (97403) or 9 (97403-1234) zip codes.
    """
    if zipcode==None: return False
    valid = re.match('^$|^[0-9]{5}(-[0-9]{4})?$', zipcode)
    if not valid:
        print "The zip code you entered is invalid.\nPlease try " + \
        "again using either 5 (97403) or 9 (97403-1234) zip codes."
        return False
    return True

def validate_email(email):
    """
    Match an email address in the standard format name@domain.tld.
    """
    if email==None: return False
    valid = re.match(r'^$|[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}', email)
    if not valid:
        print "The email address you entered is invalid.\nPlease try " + \
        "again using the standard format name@domain.tld."
        return False
    return True

def validate_phone(phone):
    """
    Match a 10 digits phone number in one of the following formats:
    1112223333 or (111)222-3333 or 111-222-3333.
    """
    if phone==None: return False
    #valid = re.match('^$|[0-9]{10,11}(x[0-9]{4})?$', phone)
    valid = re.match('^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$', phone)
    if not valid:
        print "The phone number you entered is invalid.\nPlease try again " + \
        "using 10 digits in one of the following formats:\n" + \
        "1112223333 or (111)222-3333 or 111-222-3333."
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
    print 'email F: \@b.c', validate_email('\@b.c')
    print 'email F: a@\.c', validate_email('a@\.c')
    print 'email F: a@b.\\', validate_email('a@b.\\')
    print
    print 'phone F: 5415554444x6666', validate_phone('5415554444x6666')
    print 'phone T: 541-555-4444', validate_phone('541-555-4444')
    print 'phone T: (541)555-4444', validate_phone('(541)555-4444')
    print 'phone F: 541555444', validate_phone('541555444')

if __name__ == "__main__":
    main()
