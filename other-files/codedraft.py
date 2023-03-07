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
    patients = set(contacts_dic.keys())  # get all contacts in the keys
    contacts = set().union(*contacts_dic.values())  # get all contacts that are contacted
    patient_zero = list(patients - contacts)  # find the missing contacts
    patient_zero.sort()
    return patient_zero


def find_patients_zero(contacts_dic):
    sorted_contacts = []
    patient_zero = []

    # iterate over each value list, and add its
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

def find_potential_zombies(contacts_dic):
    patients = set(contacts_dic.keys())  # get all contacts in the keys
    contacts = set().union(*contacts_dic.values())  # get all contacts that are contacted
    potential_zombies = list(contacts - patients)  # find the potential zombies
    return sorted(potential_zombies)

def find_not_zombie_nor_zero(contacts_dic, patients_zero_list, zombie_list):
    all_names = set(contacts_dic.keys()).union(*contacts_dic.values())
    not_zombie_nor_zero = list(all_names - set(patients_zero_list) - set(zombie_list))
    not_zombie_nor_zero.sort()
    return not_zombie_nor_zero
    
    # all_names = set()
    # for patient, contact_lst in contacts_dic.items():
    #     all_names.add(patient)
    #     for name in contact_lst:
    #         all_names.add(name)
    # not_zombie_nor_zero = list(all_names - set(patients_zero_list) - set(zombie_list))
    # not_zombie_nor_zero.sort()
    # return not_zombie_nor_zero

    # patients = set(contacts_dic.keys())  # get all contacts in the keys
    # all_names = set().union(*contacts_dic.values()).union(patients)  # get all contacts that are contacted
    # potential_zombies = list(all_names - set(patients_zero_list) - set(zombie_list))  # find the potential zombies
    # potential_zombies.sort()
    # return potential_zombies
def pretty_print_section_7(not_zombie_or_patient_zero_list):
    print("Neither Patient Zero or Potential Zombie:", \
          format_list(not_zombie_or_patient_zero_list))

def main():
    #print(file_exists("sfadsf"))
    # print(parse_file("testfile.txt"))
    # pretty_print_section_4(parse_file("testfile.txt"))
    # pretty_print_section_5(find_patients_zero_set(parse_file("DataSet1.txt")))\
    dic = parse_file("DataSet1.txt")
    print(find_potential_zombies(parse_file("DataSet1.txt")))
    pretty_print_section_7(find_not_zombie_nor_zero(dic,find_patients_zero(dic),find_potential_zombies(dic)))
if __name__ == '__main__':
    main()