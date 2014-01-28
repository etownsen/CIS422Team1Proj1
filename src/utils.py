"""
    Utilities Module.
    For simple Address Book applet - Project 1 - 
    CIS 422, W'14, University of Oregon.

    :author: Abdulrahman Alkhelaifi <abdul@cs.uoregon.edu>
"""

import cPickle as pickle

def open_ab(file_name):
    """
    Open an address book file, returning an AddressBook object.
    Raises IOError when file is not found.
    """
    ab = None
    with open(file_name, 'rb') as input:
        ab = pickle.load(input)
    return ab
    
def save_ab(ab, file_name):
    """
    Save an AddressBook object to a file.
    """
    with open(file_name, 'wb') as output:
        pickle.dump(ab, output, pickle.HIGHEST_PROTOCOL)
    