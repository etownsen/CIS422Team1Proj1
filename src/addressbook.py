"""
    Address Book Module.
    For simple Address Book applet - Project 1 - 
    CIS 422, W'14, University of Oregon.

    :author: Abdulrahman Alkhelaifi <abdul@cs.uoregon.edu>
"""

import sys
import utils
import csv
from operator import itemgetter, attrgetter

class Contact:
    """
    A class representing a single entry in the address book.  
    """
    def __init__(self, fname='', lname='', address='', city='', state='', 
                 zipcode='', phone='', email=''):
        """
        Initialize a Contact object which is an entry in the address book.
        """
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.email = email
        
    def __str__(self):
        """
        Return a string representation of the contact.
        """
        return "{0} {1}\n{2}\n{3}, {4} {5}\n{6}\n{7}\n".format(self.fname, self.lname, 
                            self.address, self.city, self.state, self.zipcode,
                            self.phone, self.email)
        
    def print_mailing(self):
        """
        Return a string representation in the standard mailing label format.
        """
        return "{0} {1}\n{2}\n{3} {4} {5}\n".format(self.fname.upper(),
                            self.lname.upper(), self.address.upper(),
                            self.city.upper(), self.state.upper(), self.zipcode)

class AddressBook:  
    """
    A simple personal address book. Holds a list of Contact objects
    and provides multiple functionalities to handle them.
    """
    def __init__(self, contacts=[], name='bluebook.pk'):
        """
        Initialize an AddressBook object with an empty list
        or given a list of contacts.
        """
        self.name = name
        self.contacts = contacts
        self.total = len(contacts)
            
    def __str__(self):
        """
        Return a string representation of the whole address book.
        """
        return '\n'.join([str(entry) for entry in self.contacts])
    
    def print_all_mailing(self):
        """
        Return a string representation of the whole address book
        in the standard mailing label format.
        """
        return '\n'.join([entry.print_mailing() for entry in self.contacts])
    
    def add(self, entry):
        """
        Add an entry to the address book given a single Contact
        or a list of Contacts.
        """
        if type(entry) is list:
            self.contacts += entry
            self.total += len(entry)
        else:
            self.contacts.append(entry)
            self.total += 1
    
    def delete(self, index):
        """
        Remove an entry from the address book given its index. The index
        is returned by the search method.
        """
        try:
            del self.contacts[index]
            self.total -= 1
        except IndexError, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
    
    def sort(self, attributes=['lname'], desc=False):
        """
        Sort the address book by the given list of attributes. The first
        attribute is used and ties are broken using the next attributes in 
        the list. 
        """
        try:
            self.contacts.sort(key=attrgetter(*attributes), reverse=desc)
        except AttributeError, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
        
    def search(self, attribute, value, list=None):
        """
        Search the address book for all entries with a given attribute
        and its value. This method can be called multiple times passing the result
        from each call as the third argument to narrow the search.
        """
        result = []
        if list is None:
            list = self.contacts
        for index, entry in enumerate(list):
            if type(entry) is tuple:
                index = entry[0]
                entry = entry[1]
            if getattr(entry, attribute).lower() == value.lower():
                result.append((index, entry))
        return result               
    
    def import_contacts(self, file_name):
        """NOT FINISHED."""
        with open(file_name, 'rb') as tsvfile:
            result = csv.reader(tsvfile, delimiter='\t', quotechar='|')
            for line in result:
                last = line[0].split()
                second = ""
                recipient = line[2].split()
                fname = recipient[0]
                lname = recipient[1]
                address = line[1]
                city = last[0]
                state = last[1]
                zipcode = last[2]
                phone = line[3]
                entry = Contact(fname, lname, address, city, state, zipcode, phone)
                self.add(entry)
    
    def export_contacts(self, file_name):
        """NOT FINISHED."""
        res = []
        for entry in self.contacts:
            last = ' '.join([entry.city, entry.state, entry.zipcode]).upper()
            delivery = entry.address.upper()
            second = ""
            recipient = ' '.join([entry.fname, entry.lname]).upper()
            phone = entry.phone
            line = '\t'.join([last, delivery, recipient, phone])
            res.append(line)
        res = '\n'.join(res)
        with open(file_name, 'wb') as f:
            f.write(res)

                  
def main():   
    a = Contact('aaa', 'AAA', '10 a st', 'Eugene', 'OR', '97401', '541', 'a@a.com')
    b = Contact('bbb', 'BBB', '20 b st', 'Eugene', 'OR', '97402', '541', 'b@b.com')
    c = Contact('ccc', 'CCC', '30 c st', 'Eugene', 'OR', '97403', '541', 'c@c.com')
    b2 = Contact('bbb', 'BBB', '20 b st', 'Eugene', 'OR', '97404', '541', 'b@b.com')
    #print a.print_mailing()
    arr = [b, c, b2, a]
    ab = AddressBook(arr) 
    # ab.add(a)
    # ab.add(b)
    # ab.add(c)
    #ab.add(arr)
    #print ab
    res = ab.search('fname', 'bbb')
    res2 = ab.search('zipcode', '97404', res)
    #print res
    #print res2
    ab.sort(['lname', 'zipcode'])
    #utils.save_ab(ab, ab.name)
    #ab2 = utils.open_ab('bluebook.pk')
    #print ab2
    #ab2.export_contacts('f.tsv')
    #ab3 = AddressBook()
    #ab3.import_contacts('f.tsv')
    #print ab3

    
if __name__ == "__main__": main()