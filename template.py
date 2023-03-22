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
            try:
                patient, *contacts_list = line.rstrip().split(',')
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
    # find all patients and contacts as sets
    patients = set(contacts_dic.keys()) 
    contacts = set().union(*contacts_dic.values())
    
    # find patients who are not in anyone's contact list
    patients_zero = list(patients - contacts)             

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
    # find all patients and contacts as sets
    patients = set(contacts_dic.keys())             
    contacts = set().union(*contacts_dic.values())  

    # find contacts who is not a patient
    potential_zombies = list(contacts - patients)   

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
    
    # get patients who's contacts are not in either list
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
            # found person with larger max contacts
            max_len = len(contacts_list)
            most_viral_list = [patient]
        
        elif len(contacts_list) == max_len:
            # found person with same max contacts
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
    # count the number of times each contact appears to a dictionary
    count_dic = {} 
    for contacts_list in contacts_dic.values():
        for name in contacts_list:
            count_dic[name] = count_dic.get(name, 0) + 1

    max_count = max(count_dic.values())     # find the maximum count

    # find contacts whose count == maximum_count
    most_contacted_list = []
    for name, count in count_dic.items():
        if count == max_count:
            most_contacted_list.append(name)

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
    # create a dic and set distances of all people to 0
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
        list: contains the names of sick people who only contacted with 
        potential zombies.
    """
    spreader_zombies_list = []

    for patient, contacts_list in contacts_dic.items():
        if all (contact in zombie_list for contact in contacts_list):
            # when this paitent's contacts are all zombie
            spreader_zombies_list.append(patient)

    return spreader_zombies_list


def find_regular_zombies(contacts_dic, zombie_list):
    """Return list of sick people that contacted with both potential zombies 
       and people who are already sick.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        zombie_list (list): all zombies

    Returns:
        list: contains the names of sick people who contacted with both 
        potential zombies and other sick people.
    """
    regular_zombies_list = []
    patients_list = contacts_dic.keys()

    for patient, contacts in contacts_dic.items():
        # check if this patient contacted with other patients / zombies
        contact_with_patient = set(patients_list).intersection(contacts)
        contact_with_zombie = set(zombie_list).intersection(contacts)
        # if has contacts with both:
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
        list: contains the names of sick people who only contacted with people 
        who are already sick.
    """
    # predator: all contacts are patients
    predator_zombies_list = []
    patient_list = contacts_dic.keys()

    for patient, contacts_list in contacts_dic.items():
        if all(contact in patient_list for contact in contacts_list):
            # if this paitent's contacts are all in patient list
            predator_zombies_list.append(patient)

    return predator_zombies_list


def depth_first_search(patient, visited, stack, contacts_dic):
    """Performs a depth-first search (DFS) to detect cycles in a directed 
       graph represented as a dictionary of contacts.

    Args:
        patient (str): The patient to start the DFS form.
        visited (set): A set of previously visited patients.
        stack (set): A set of patients currently in the DFS stack.
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        zombie_list (list): all zombies

    Returns:
        bool: return True if a cycle is detected and False otherwise.
    """
    visited.add(patient)
    stack.add(patient)

    for contact in contacts_dic.get(patient, []):
        if contact not in visited:      # not visited, continue do dfs
            if depth_first_search(contact, visited, stack, contacts_dic):
                return True
        elif contact in stack:          # a cycle is found
            return True
        
    stack.remove(patient)               # remove processed node   
    return False 


def find_cycles_in_data(contacts_dic):
    """Find whether the input dataset has a cycle or not.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        bool: return True if a cycle is detected and False otherwise.
    """
    visited = set()
    stack = set()
    
    # Perform DFS on each unvisited patient
    for patient in contacts_dic:
        if patient not in visited:
            if depth_first_search(patient, visited, stack, contacts_dic):
                return True         
            
    return False



# Pretty printing functions. You have one function per section that
# must output a string as specified by contact_tracing.pdf 

def pretty_print_section_3():
    print("Error found in file, continuing.")


def pretty_print_section_4(contact_dictionary):
    print("Contact Records:")
    for patient, contacts_list in sorted(contact_dictionary.items()):
        format_contacts = format_list(contacts_list)
        print(f"  {patient} had contact with {format_contacts}")


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
