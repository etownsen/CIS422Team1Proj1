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

class Contact(object):
    """
    A class representing a single entry in the address book.
    """
    def __init__(self, fname='', lname='', address='', city='', state='',
                 zipcode='', phone='', email='', address2=''):
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
        return {key:value.strip() for key, value in info.iteritems()}

class AddressBook(object):
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
        """NOT FINISHED."""
        # try and catch file exception and file not formatted
        with open(file_name, 'rb') as tsvfile:
            result = csv.reader(tsvfile, delimiter='\t', quotechar='|')
            for line in result:
                print line
                entry = Contact()
                # SET ATTRIBUTES
                # self.add(entry)

    def export_contacts(self, file_name):
        """NOT FINISHED."""
        res = []
        # try and catch file errors
        for entry in self.contacts:
            info = entry.get_filtered_info()
            info = [info['last'], info['address'], info['second'],
                    info['name'], info['phone']]
            line = '\t'.join(filter(None, info))
            res.append(line)
        res = '\n'.join(filter(None, res)).upper()
        with open(file_name, 'wb') as f:
            f.write(res)


def main():
    """
    Testing...
    """
    a = Contact()
    a2 = Contact('fname', 'lname', '10 a st', 'eugene', 'or',
                 '97401', '541', 'a@a.com', 'apt 10')
    b = Contact('bbb', '', '20 b st', 'Eugene', 'OR', '97402', '', 'b@b.com')
    c = Contact('ccc', 'CCC', '', 'Eugene', 'OR', '97403', '541', 'c@c.com')
    b2 = Contact('bbb', 'BBB', '20 b st', '', 'OR', '97404', '541', 'b@b.com')
    # print a.print_mailing()
    arr = [a2, b, c, b2, a]
    ab = AddressBook(arr)
    # ab.add(a)
    # ab.add(b)
    # ab.add(c)
    # ab.add(arr)
    print ab
    # print ab.print_all_mailing()
    res = ab.search('email', 'a@a.com')
    print str(res[0][1])
    res2 = ab.search('zipcode', '97404', res)
    print res2
    ab.sort(['lname', 'zipcode'])
    utils.save_ab(ab, ab.name)
    ab2 = utils.open_ab('bluebook.pk')
    # print ab2
    ab2.export_contacts('f.tsv')
    ab3 = AddressBook()
    ab3.import_contacts('f.tsv')
    print ab3


if __name__ == "__main__":
    main()
