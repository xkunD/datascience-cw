import sys
import os.path
from format_list import format_list


def file_exists(file_name):
    return os.path.isfile(file_name)


def parse_file(file_name):

    contact_dict = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    sick_person, *contacts = line.strip().split(',')
                    contact_dict[sick_person] = contacts
                    # if not sick_person or not contacts:
                    #     print("Error found in file, continuing.")
                    # continue
                except ValueError:
                    print("Error found in file, continuing.")
                    continue
    return contact_dict
        
def pretty_print_section_4(contact_dictionary):
    print("Contact Records:")
    for sick_record in contact_dictionary:
        print(f"{sick_record} had contact with {format_list(contact_dictionary[sick_record])}")

def main():
    #print(file_exists("sfadsf"))
    # print(parse_file("testfile.txt"))
    pretty_print_section_4(parse_file("testfile.txt"))

if __name__ == '__main__':
    main()