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


# Function for section 5
def find_patients_zero_set(contacts_dic):
    """Return list of people who do not appear in any sick person's contact
    list. 

    Args:
        contacts_dic (dic): each entry is a sick person's name (key) and their
        list of contacts.

    Returns:
        list: names of people who do not appear in any sick person's contact
        list.
    """
    # Remove pass and fill in your code here
    all_contacts = set(contacts_dic.keys())  # get all contacts in the keys
    contacted_contacts = set().union(*contacts_dic.values())  # get all contacts that are contacted
    missing_contacts = list(all_contacts - contacted_contacts)  # find the missing contacts
    missing_contacts.sort()
    print(missing_contacts)


def find_patients_zero(contacts_dic):
    sorted_contacts = []
    patient_zero = []

    # iterate over each value list in sorted order, and add its
    # contacts to the set of contacted contacts in a sorted manner
    for contacts in contacts_dic.values():
        i = 0
        for name in contacts:
            while i < len(sorted_contacts) and name > sorted_contacts[i]:
                i += 1
            if i == len(sorted_contacts) or name < sorted_contacts[i]:
                sorted_contacts.insert(i, name)

    # iterate over the sorted list of all contacts, and add any missing
    # contacts to the missing_contacts list
    i = 0
    for name in contacts_dic.keys():
        while i < len(sorted_contacts) and name > sorted_contacts[i]:
            i += 1
        if i == len(sorted_contacts) or name < sorted_contacts[i]:
            patient_zero.append(name)

    return patient_zero

def pretty_print_section_5(patient_zero_list):
    print("Patient Zero(s):", format_list(patient_zero_list))



def main():
    #print(file_exists("sfadsf"))
    # print(parse_file("testfile.txt"))
    # pretty_print_section_4(parse_file("testfile.txt"))
    pretty_print_section_5(find_patients_zero(parse_file("DataSet1.txt")))


if __name__ == '__main__':
    main()