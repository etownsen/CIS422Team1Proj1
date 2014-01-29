"""
    Address Book Module.


    For simple Address Book applet - Project 1 -
    CIS 422, W'14, University of Oregon.

    :author: Abdulrahman Alkhelaifi <abdul@cs.uoregon.edu>
"""

import csv
import validate
from operator import itemgetter, attrgetter

class Contact(object):
    """
    A class representing a single entry in the address book.
    """
    
    default_attrs = ['fname', 'lname', 'address', 'address2', 'city',
                     'state', 'zipcode', 'phone', 'email']
    
    def __init__(self):
        """
        Initialize a Contact object which is an entry in the address book.
        """
        for attr in Contact.default_attrs:
            setattr(self, attr, '')
        
    def testing(self, fname='', lname='', address='', city='', state='',
                 zipcode='', phone='', email='', address2=''):
        """
        Testing constructor that initializes a Contact object given the default
        attributes.
        """
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.email = email
        self.address2 = address2

    def __str__(self):
        """
        Return a string representation of the Contact object with
        no extra spaces or lines for empty fields.
        """
        info = self.get_filtered_info()
        info = [info['name'], info['delivery'], info['last'],
                info['phone'], info['email']]
        return '\n'.join(filter(None, info))

    def print_mailing(self):
        """
        Return a string representation in the standard mailing label format.

        | NAME (FIRST LAST) (e.g., ABC MOVERS)
        | DELIVERY (ADDRESS SECOND) (e.g., 1500 E MAIN AVE STE 201)
        | LAST (CITY STATE ZIP) (e.g., SPRINGFIELD VA 22162-1010)
        """
        info = self.get_filtered_info()
        del info['phone']
        del info['email']
        info = [info['name'], info['delivery'], info['last']]
        return '\n'.join(filter(None, info)).upper()

    def get_filtered_info(self):
        """
        Return a dictionary of filtered information for the Contact object.
        Useful when Contact has empty fields.

        | name: first last
        | delivery: address second
        | last: city state zipcode
        | phone: phone
        | email: email
        | address: address
        | second: second
        """
        name = ' '.join([self.fname, self.lname])
        address = ' '.join([self.address, self.address2])
        last = ' '.join([self.city, self.state, self.zipcode])
        info = {'name': name, 'delivery': address, 'last': last,
                'phone': self.phone, 'email': self.email,
                'address': self.address, 'second': self.address2}
        return {key : value.strip() for key, value in info.iteritems()}

class AddressBook(object):
    """
    A simple personal address book. Holds a list of Contact objects
    and provides multiple functionalities to handle them.
    """
    def __init__(self, contacts=[], name=''):
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
        return '\n'.join([str(entry) + '\n' for entry in self.contacts])

    def print_all_mailing(self):
        """
        Return a string representation of the whole address book
        in the standard mailing label format.
        """
        return '\n'.join([entry.print_mailing() + '\n'
                          for entry in self.contacts])

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
        Raises IndexError if index is not in the list.
        """
        del self.contacts[index]
        self.total -= 1

    def sort(self, attributes=['lname'], desc=False):
        """
        Sort the address book by the given list of attributes. The first
        attribute is used and ties are broken using the next attributes in
        the list.
        Raises AttributeError if one of the attributes does not exist.
        """
        attrs = attrgetter(*attributes)
        self.contacts.sort(key=lambda x: [x.lower() for x in attrs(x)],
                           reverse=desc)

    def search(self, attribute, value, search_list=None):
        """
        Search the address book for all entries with a given attribute
        and its value. This method can be called multiple times passing
        the result from each call as the third argument to narrow the search.
        """
        result = []
        if search_list is None:
            search_list = self.contacts
        for index, entry in enumerate(search_list):
            if type(entry) is tuple:
                index = entry[0]
                entry = entry[1]
            if getattr(entry, attribute).lower() == value.lower():
                result.append((index, entry))
        return result
        
    def import_contacts(self, file_name):
        """
        Import a contacts list from a tsv file.
        The format of the file is as follows:
        Last<tab>Delivery<tab>Second<tab>Recipient<tab>Phone<NL>
        followed by a list of contacts with the same format.
        Raises IOError if file is not found or has no read permission.
        """
        with open(file_name, 'rb') as tsvfile:
            tsv_reader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
            tsv_header = tsv_reader.next()
            for line in tsv_reader:
                fields = {key.lower() : value for key, value in zip(tsv_header, line)}
                entry = Contact()
                if 'last' in fields and fields['last']:
                    last = fields['last'].split()
                    for key, value in enumerate(last):
                        if validate.validate_zip(value)[0]:
                            entry.zipcode = value
                            del last[key]
                    try: 
                        entry.city = last[0]
                        entry.state = last[1]
                    except:
                        pass
                if 'delivery' in fields and fields['delivery']:
                    delivery = fields['delivery']
                    entry.address = delivery
                if 'second' in fields and fields['second']:
                    second = fields['second']
                    entry.address2 = second
                if 'recipient' in fields and fields['recipient']:
                    recipient = fields['recipient'].split()
                    entry.fname = recipient[0]
                    try: entry.lname = recipient[1]
                    except: pass
                if 'phone' in fields and fields['phone']:
                    phone = fields['phone']
                    entry.phone = phone
                self.add(entry)
    
    def export_contacts(self, file_name):
        """
        Export the contacts list to a tsv file.
        The format of the file is as follows:
        Last<tab>Delivery<tab>Second<tab>Recipient<tab>Phone<NL>
        followed by a list of contacts with the same format.
        Raises IOError if file exist and has no write permission.
        """
        with open(file_name, 'wb') as tsvfile:
            tsv_writer = csv.writer(tsvfile, delimiter='\t', quotechar='|')
            header = ['Last', 'Delivery', 'Second', 'Recipient']
            tsv_writer.writerow(header)
            for entry in self.contacts:
                info = entry.get_filtered_info()
                info = {key : value.upper() for key, value in info.iteritems()}
                info = [info['last'], info['address'], info['second'],
                        info['name'], info['phone']]
                tsv_writer.writerow(info)

    def merge(self, address_book):
        """
        Merge two address books.
        """
        pass
    
