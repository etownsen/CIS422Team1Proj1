from validate import (validate_name,validate_city, validate_state, 
validate_address, validate_zip, validate_email, validate_email, validate_phone)
from addressbook import Contact, AddressBook
import utils

def test_validate():
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
    print 'state T: OR', validate_state('OR')
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
    print 'phone T: (541) 555-4444', validate_phone('(541) 555-4444')
    print 'phone F: 541555444', validate_phone('541555444')
 
def test_addressbook():
    ab = utils.open_addressbook('mybook')
    print ab
    ab.sort(['fname', 'lname']) 
    ab2 = AddressBook()
    ab2.import_contacts('Handsome')
    print ab2

def main():
    #test_validate()
    test_addressbook()

if __name__ == "__main__":
    main()