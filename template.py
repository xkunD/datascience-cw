#!/usr/bin/env python3
"""Analyse a given dataset of sick people and their contacts. Identify
characteristics related to disease spreading as set out in the coursework
brief.
"""

import sys
import os.path
from format_list import format_list

# Function for section 2
def file_exists(file_name):
    """Verify that the file exists.

    Args:
        file_name (str): name of the file

    Returns:
        boolean: returns True if the file exists and False otherwise.
    """
    # Remove pass and fill in your code here
    return os.path.isfile(file_name)
        
# Function for section 3
def parse_file(file_name):
    """Read the input file, parse the contents and return a dictionary
    containing sick people and their contacts.

    Args:
        file_name (str): Contains the name of the file.

    Returns:
        dict: Contains contact tracing information. The keys are the sick
        people. The corresponding values are stored in a list that contains
        the names of all the people that the sick person has had contact with.
    """
    # Remove pass and fill in your code here

    contact_dict = {}
    with open(file_name, 'r') as file:
        for line in file:
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
                    # continue
    return contact_dict


# Function for section 5
def find_patients_zero(contacts_dic):
    """Return list of people who do not appear in any sick person's contact
    list. 

    Args:
        contacts_dic (dic): each entry is a sick person's name (key) and their
        list of contacts.

    Returns:
        list: names of people who do not appear in any sick person's contact
        list.
    """

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

# Function for section 6
def find_potential_zombies(contacts_dic):
    """Return list of people who do not appear to be sick yet. They appear in
    the contact lists but do not have their own contacts entry.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: names of people who are not listed as sick.
    """
    # Remove pass and fill in your code here
    pass

# Function for section 7
def find_not_zombie_nor_zero(contacts_dic, patients_zero_list, zombie_list):
    """Return names of those people who are neither a zombie nor a patient
    zero.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        patients_zero_list (list): sick people identified as patient zero(es).
        zombie_list (list): contacts who are not a sick person (don't have
        their own contact list).

    Returns:
        list: people who are neither a zombie nor a patient zero.
    """
    # Remove pass and fill in your code here
    pass

# Function for section 8
def find_most_viral(contacts_dic):
    """Return the most viral contacts: those sick people with the largest
    contact list

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: contains the names of sick people who have the largest contact
        lists
    """
    # Remove pass and fill in your code here
    pass
    
# Function for section 9
def find_most_contacted(contacts_dic):
    """Return the contact or contacts who appear in the most sick persons'
    contact list.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: contains the names of contacts who appear in the most sick
        persons' contact list.
    """
    # Remove pass and fill in your code here
    pass
    
# Function for section 10
def find_maximum_distance_from_zombie(contacts_dic, zombie_list):
    """Return the maximum distance from a zombie for everyone in the dataset.
    The maximum distance from a potential zombie is the longest contact
    tracing path downwards in the dataset from a sick person to a potential
    zombie.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their
        list of contacts.
        zombie_list (list): all zombies

    Returns:
        dic: contains heights (maximum distance) of person from a zombie
    """
    # Remove pass and fill in your code here
    pass


# "Additional Credit" Functions here

def find_spreader_zombies(contacts_dic, zombie_list):
    # Remove pass and fill in your code here
    pass

def find_regular_zombies(contacts_dic, zombie_list):
    # Remove pass and fill in your code here
    pass

def find_predator_zombies(contacts_dic, zombie_list):
    # Remove pass and fill in your code here
    pass

def find_cycles_in_data(contacts_dic):
    pass    # Replace this return statement with your cycle detector when ready

# Pretty printing functions. You have one function per section that
# must output a string as specified by contact_tracing.pdf 

def pretty_print_section_3():
    pass

def pretty_print_section_4(contact_dictionary):
    print("Contact Records:")
    for sick_record in contact_dictionary:
        print(f"{sick_record} had contact with {format_list(contact_dictionary[sick_record])}")

def pretty_print_section_5(patient_zero_list):
    print("Patient Zero(s):", format_list(patient_zero_list))

def pretty_print_section_6(potential_zombies_list):
    pass

def pretty_print_section_7(not_zombie_or_patient_zero_list):
    pass

def pretty_print_section_8(most_viral_list):
    pass

def pretty_print_section_9(most_contacted_list):
    pass

def pretty_print_section_10(heights_dictionary):
    pass

# Additional credit printing functions

def pretty_print_section_11(spreader_zombie_list):
    pass

def pretty_print_section_12(regular_zombie_list):
    pass

def pretty_print_section_13(zombie_predator_list):
    pass

def pretty_print_section_14(cycles_state):
    pass
    
# =======================================================
# =======================================================
# Attention Student. Please do not modify any code below
# here. Doing so may result in lost marks.
# =======================================================
# =======================================================
def main():
    """
    Main logic for the program.
    DO NOT MODIFY THIS FUNCTION. THIS MAY RESULT IN LOST MARKS!
    """
    filename = ""
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    # Section 2. 
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3.
    contacts_dic = parse_file(filename)

    # Section 4. 
    pretty_print_section_4(contacts_dic)

    # Section 5. 
    patients_zero_list = find_patients_zero(contacts_dic)
    pretty_print_section_5(patients_zero_list)

    # Section 6. 
    zombie_list = find_potential_zombies(contacts_dic)
    pretty_print_section_6(zombie_list)

    # Section 7.
    not_zombie_nor_zero = find_not_zombie_nor_zero(contacts_dic,
                                    patients_zero_list, zombie_list)
    pretty_print_section_7(not_zombie_nor_zero)

    # Section 8. 
    most_viral_list = find_most_viral(contacts_dic)
    pretty_print_section_8(most_viral_list)

    # Section 9. 
    most_contacted = find_most_contacted(contacts_dic)
    pretty_print_section_9(most_contacted)

    # Section 14.
    cycles = find_cycles_in_data(contacts_dic)
    pretty_print_section_14(cycles)

    if cycles:  # This evaluates to false if cycles = None
        print("Cycles detected")
    else:       
        # Section 10. 
        heights_dic = find_maximum_distance_from_zombie(contacts_dic, zombie_list)
        pretty_print_section_10(heights_dic)

    print("\nFor additional credit:")

    # Section 11.
    spreader = find_spreader_zombies(contacts_dic, zombie_list)
    pretty_print_section_11(spreader)

    # Section 12.
    regular = find_regular_zombies(contacts_dic, zombie_list)
    pretty_print_section_12(regular)

    # Section 13.
    predator = find_predator_zombies(contacts_dic, zombie_list)
    pretty_print_section_13(predator)

if __name__ == "__main__":
    main()
