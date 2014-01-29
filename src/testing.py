
from validate import (validate_name,validate_city, validate_state, 
validate_address, validate_zip, validate_email, validate_email, validate_phone)
from addressbook import Contact, AddressBook


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
    a = Contact()
    a2 = Contact()
    a2.testing('fname', 'lname', '10 a st', 'eugene', 'or',
                 '97401', '541', 'a@a.com', 'apt 10')
    b = Contact()
    b.testing('bbb', 'john', '20 b st', 'Eugene', 'OR', '97402', '54535', 'b@b.com')
    c = Contact()
    c.testing('ccc', 'CCC', '30 c st', 'Eugene', 'OR', '97403', '541', 'c@c.com')
    b2 = Contact()
    b2.testing('bbb', 'BBB', '20 b st', '', 'OR', '97404', '541', 'b@b.com')
    arr = [a2, b, c, b2, a]
    ab = AddressBook(arr)
    print ab
    # ab.add(a)
    # ab.add(b)
    # ab.add(c)
    # ab.add(arr)
    #print ab
    # print ab.print_all_mailing()
    #res = ab.search('email', 'a@a.com')
    #print str(res[0][1])
    #res2 = ab.search('zipcode', '97404', res)
    #print res2
    #ab.sort(['lname', 'zipcode'])
    #utils.save_ab(ab, ab.name)
    #ab2 = utils.open_ab('mybook')
    #print ab2.print_all_mailing()
    #ab.delete(10)
    ab.export_contacts('f.tsv')
    ab3 = AddressBook()
    ab3.import_contacts('f.tsv')
    print ab3


def main():
    test_validate()
    test_addressbook()

if __name__ == "__main__":
    main()