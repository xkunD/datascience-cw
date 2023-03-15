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
    contact_dic = {}

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    patient, *contacts_list = line.strip().split(',')
                    contact_dic[patient] = contacts_list
                except ValueError:
                    pretty_print_section_3()

    return contact_dic


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
    patients = set(contacts_dic.keys())                 # all patients as a set
    contacts = set().union(*contacts_dic.values())      # all contacts as a set
    
    patients_zero = list(patients - contacts)       # get people not in contacts      

    return sorted(patients_zero)


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
    patients = set(contacts_dic.keys())             # all patients as a set
    contacts = set().union(*contacts_dic.values())  # all contacts as a set

    potential_zombies = list(contacts - patients)   # get non-sick contacts

    return sorted(potential_zombies)


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
    
    # all patients as a set
    patients = set(contacts_dic.keys())            
    
    # get people not in both
    not_zombie_nor_zero_list = \
        list(patients - set(patients_zero_list) - set(zombie_list))

    return sorted(not_zombie_nor_zero_list)


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
    max_len = 0
    most_viral_list = []

    for patient, contacts_list in contacts_dic.items():       
        if len(contacts_list) > max_len:
            # person with larger max contacts found
            max_len = len(contacts_list)
            most_viral_list = [patient]
        
        elif len(contacts_list) == max_len:
            # people with same max contacts found
            most_viral_list.append(patient)
            
    return sorted(most_viral_list)


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
    count_dic = {}
    for contact_list in contacts_dic.values():
        for name in contact_list:
            count_dic[name] = count_dic.get(name, 0) + 1
    
    max_count = max(count_dic.values())

    most_contacted_list = [contact for contact, count in count_dic.items() 
                      if count == max_count]

    return sorted(most_contacted_list)


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
    # create dictionary and set distances of all people to 0
    patient_list = contacts_dic.keys()
    heights_dic = dict.fromkeys(patient_list | zombie_list, 0)
    changed = True

    while changed:
        changed = False
        for patient in contacts_dic.keys():
            for contact in contacts_dic[patient]:
                if heights_dic[patient] <= heights_dic[contact]:
                    heights_dic[patient] = heights_dic[contact] + 1
                    changed = True

    return heights_dic


# "Additional Credit" Functions here

def find_spreader_zombies(contacts_dic, zombie_list):
    """Return list of sick people who only contacted with potential zombies.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        zombie_list (list): all zombies

    Returns:
        list: contains the names of sick people who only contacted with potential zombies.
    """
    # spreader: only contact with potential zombie (so all contact in zombie list)
    spreader_zombies_list = []

    for patient in contacts_dic.keys():
        is_spreader = True
        for contact in contacts_dic[patient]:
            if contact not in zombie_list:
                is_spreader = False # while loop instead of for?
        if is_spreader:
            spreader_zombies_list.append(patient)

    return spreader_zombies_list


def find_regular_zombies(contacts_dic, zombie_list):
    """Return list of sick people that contacted with both potential zombies and people who are already sick.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        zombie_list (list): all zombies

    Returns:
        list: contains the names of sick people who contacted with both potential zombies and people who are already sick.
    """
    regular_zombies_list = []
    patient_list = contacts_dic.keys()

    for patient, contacts in contacts_dic.items():
        contact_with_patient = set(patient_list).intersection(contacts)
        contact_with_zombie = set(zombie_list).intersection(contacts)
        
        if contact_with_patient and contact_with_zombie:
            regular_zombies_list.append(patient)

    return regular_zombies_list


def find_predator_zombies(contacts_dic, zombie_list):
    """Return list of sick people that only has contact with people who are sick.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        zombie_list (list): all zombies

    Returns:
        list: contains the names of sick people who contacted with both potential zombies and people who are already sick.
    """
    # predator: all contacts are patients
    predator_zombies_list = []
    patient_list = contacts_dic.keys()
    for patient, contacts_list in contacts_dic:
        if all(contact in patient_list for contact in contacts_list):
            predator_zombies_list.append(patient)
    return predator_zombies_list


def depth_first_search(patient, visited, stack, contacts_dic):
    visited.add(patient)
    stack.add(patient)
    for contact in contacts_dic.get(patient, []):
        if contact not in visited:
            if depth_first_search(contact, visited, stack, contacts_dic):
                return True
        elif contact in stack:
            return True
    stack.remove(patient)
    return False 

def find_cycles_in_data(contacts_dic):
    visited = set()
    for patient in contacts_dic:
        if patient not in visited:
            if depth_first_search(patient, visited, set(), contacts_dic):
                return True
    return False



# Pretty printing functions. You have one function per section that
# must output a string as specified by contact_tracing.pdf 

def pretty_print_section_3():
    print("Error found in file, continuing.")


def pretty_print_section_4(contact_dictionary):
    print("Contact Records:")
    for sick_record in sorted(contact_dictionary):
        print(f"  {sick_record} had contact with {format_list(sorted(contact_dictionary[sick_record]))}")


def pretty_print_section_5(patient_zero_list):
    print("\nPatient Zero(s):", format_list(patient_zero_list))


def pretty_print_section_6(potential_zombies_list):
    print("Potential Zombies:", format_list(potential_zombies_list))


def pretty_print_section_7(not_zombie_or_patient_zero_list):
    print("Neither Patient Zero or Potential Zombie:", \
          format_list(not_zombie_or_patient_zero_list))


def pretty_print_section_8(most_viral_list):
    print("Most Viral People:", format_list(most_viral_list))


def pretty_print_section_9(most_contacted_list):
    print("Most Contacted:", format_list(most_contacted_list))


def pretty_print_section_10(heights_dictionary):
    print("\nHeights:")
    for name, distance in heights_dictionary.items():
        print(f"  {name}: {distance}")


# Additional credit printing functions

def pretty_print_section_11(spreader_zombie_list):
    print("  Spreader Zombies:", end = " ")
    if spreader_zombie_list:
        print(format_list(spreader_zombie_list))
    else:
        print("(None)")


def pretty_print_section_12(regular_zombie_list):
    print("  Regular Zombies:", end = " ")
    if regular_zombie_list:
        print(format_list(regular_zombie_list))
    else:
        print("(None)")


def pretty_print_section_13(zombie_predator_list):
    print("  Zombie Predators:", end = " ")
    if zombie_predator_list:
        print(format_list(zombie_predator_list))
    else:
        print("(None)")


def pretty_print_section_14(cycles_state):
    print(cycles_state)
    
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
