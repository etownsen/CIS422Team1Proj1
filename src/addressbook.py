"""
Created on Jan 20, 2014

@author: ak
"""

#import sys

class Contact:
    
    """A class representing a single entry in the address book."""

    def __init__(self, fname='', lname='', address='', city='', state='', zipcode='', phone='', email=''):
        """Construct a Contact object which is an entry in the address book"""
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.email = email
        
    def __str__(self):
        """Return a string representation in the mailing label format."""
        return "%s %s\n%s\n%s, %s %s\n" %(self.fname, self.lname, self.address, 
                                        self.city, self.state, self.zipcode)


class AddressBook:
    
    """Address Book class."""
    
    def __init__(self, contacts=None):
        """Construct an Address Book object."""
        if contacts is None:
            self.contacts = []
            self.total = 0
        else:
            self.contacts = contacts
            self.total = len(contacts)
    
    def add(self, entry):
        """Add an entry to the address book."""
        if type(entry) is list:
            self.contacts += entry
            self.total += len(entry)
        else:
            self.contacts.append(entry)
            self.total += 1
    
    def delete(self, index):
        """Remove an entry from the address book given its index."""
        try:
            del self.contacts[index]
            self.total -= 1
        except IndexError:
            #sys.stderr.write('ERROR: %s\n' % str(err))
            pass

    def search(self, attribute, value, list=None):
        """Search the address book for all entries with a given attribute
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
            if getattr(entry, attribute) == value:
                result.append((index, entry))
        return result
                
    def __str__(self):
        """Return a string representation of the whole address book."""
        return '\n'.join([str(entry) for entry in self.contacts])
    
def main():   
    a = Contact('aaa', 'AAA', '10 a st', 'Eugene', 'OR', '97401', '541', 'a@a.com')
    b = Contact('bbb', 'BBB', '20 b st', 'Eugene', 'OR', '97402', '541', 'b@b.com')
    c = Contact('ccc', 'CCC', '30 c st', 'Eugene', 'OR', '97403', '541', 'c@c.com')
    b2 = Contact('bbb', 'BBB', '20 b st', 'Eugene', 'OR', '97404', '541', 'b@b.com')
    arr = [a, b, c, b2]
    ab = AddressBook(arr) 
    # ab.add(a)
    # ab.add(b)
    # ab.add(c)
    #ab.add(arr)
    #print ab
    res = ab.search('fname', 'bbb')
    res2 = ab.search('zipcode', '97404', res)
    print res
    print res2

if __name__ == "__main__": main()