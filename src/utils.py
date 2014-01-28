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
