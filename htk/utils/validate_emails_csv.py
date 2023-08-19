#!/usr/bin/env python
"""
validate_emails.csv.py

See usage()
"""

# Python Standard Library Imports
import codecs
import csv
import getopt
import sys


class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        item = self.reader.next()
        #item = item.encode('utf-8')
        item = u'%s' % item
        return item

class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        row = [unicode(s, 'utf-8') for s in row]
        return row

    def __iter__(self):
        return self

class PlainReader(object):
    """A CSV reader that does not try to do any encoding
    """
    def __init__(self, f, dialect=csv.excel, **kwds):
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        row = [s for s in row]
        return row

    def __iter__(self):
        return self

def usage(message=None):
    if message:
        print message
    print """Validates email addresses in a CSV file

Usage: python validate_emails_csv.py -f FILENAME [(-c |--column=)EMAIL_COLUMN]
"""

def main():
    try:
        short_opts = 'hc:f:v'
        long_opts = [
            'help',
            'column='
            'file=',
            'verbose',
        ]
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)
    filename = None
    column = 'email'
    verbose = False
    for o, a in opts:
        if o == '-v':
            verbose = True
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--column'):
            column = a
        elif o in ('-f', '--file'):
            filename = a
        else:
            assert False, "unhandled option"

    if filename is None:
        usage('No CSV file specified.')
        sys.exit(2)

    validate_emails_csv(filename, column)

def validate_emails_csv(csv_filename, email_column_name):
    f = open(csv_filename, 'r')
    i = 0
    headers = None
    email_row_index = None
    valid_emails_count = 0
    invalid_emails_count = 0
    #reader = UnicodeReader(f)
    reader = PlainReader(f)
    for row in reader:
        if i == 0:
            headers = row
            email_row_index = get_email_row_index(headers, email_column_name)
        else:
            email = sanitize_email(row[email_row_index])
            if is_valid_email(email):
                valid_emails_count += 1
            else:
                print 'Invalid email on row %s: %s' % (i, email)
                invalid_emails_count += 1
        i += 1
    print 'Valid emails: %s\nInvalid emails: %s' % (
        valid_emails_count,
        invalid_emails_count,
    )

def get_email_row_index(headers, email_column_name):
    index = headers.index(email_column_name)
    return index

def sanitize_email(emailish):
    email = emailish.strip().lower()
    return email

def is_valid_email(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        is_valid = True
    except:
        is_valid = False
    return is_valid

if __name__ == '__main__':
    main()
