"""
    Utilities Module
    For simple Address Book applet - Project 1 - CIS 422, W'14, University of Oregon

    :author: Abdulrahman Alkhelaifi
"""

import cPickle as pickle
# from addressbook import AddressBook

def open_ab(file):
    """Open an address book file.
    
    Args:
      file: The file name of the address book.
    
    Returns:
      An address book object.
      
    Raises:
      IOError: An error when file is not found.
    """
    ab = None
    with open(file, 'rb') as input:
        ab = pickle.load(input)
    return ab
    
def save_ab(ab, file):
    """Save an address book to file.
    
    Args:
      ab: The address book to be saved.
      file: The file name of the address book.
      
    Raises:
      IOError: An error when file is not found.
    """
    with open(file, 'wb') as output:
        pickle.dump(ab, output, pickle.HIGHEST_PROTOCOL)
        
