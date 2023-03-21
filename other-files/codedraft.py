import sys
import os.path
from format_list import format_list
import contextlib

def file_exists(file_name):
    return os.path.isfile(file_name)

def new_parse_file(file_name):
    contact_dict = {}
    contacted_dict = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(',')
                sick_person = parts[0]
                contacts = sorted(parts[1:])
                if sick_person not in contact_dict:
                    contact_dict[sick_person] = []
                contact_dict[sick_person].extend(contacts)
    for person in sorted(contact_dict.keys()):
        print(person)
        contacted_dict[person] = sorted(list(set(contact_dict[person])))
    return contacted_dict

def parse_file(file_name):
    
    contact_dict = {}    
    
    with open(file_name, 'r') as f: 
        for line in f:
            try:
                patient, *contacts_list = line.rstrip().split(',')
                if not patient or not contacts_list:
                    raise ValueError
                contact_dict[patient] = contacts_list
            
            except ValueError:
                print("Error found in file, continuing.", line)
    
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
    # Remove pass and fill in your code here
    patients = set(contacts_dic.keys())  # get all contacts in the keys
    contacts = set().union(*contacts_dic.values())  # get all contacts that are contacted
    patient_zero = list(patients - contacts)  # find the missing contacts
    patient_zero.sort()
    return patient_zero



def find_patients_zero_looping(contacts_dic):
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

def find_most_viral(contacts_dic):
    max_len = 0
    most_viral = []

    for patient, contacts_lst in contacts_dic.items():
        if len(contacts_lst) > max_len:
            max_len = len(contacts_lst)
            most_viral = [patient]
        elif len(contacts_lst) == max_len:
            most_viral.append(patient)

    most_viral.sort()
    return most_viral

def find_most_contacted(contacts_dic):
    contact_count = {}
    for contact_list in contacts_dic.values():
        for contact in contact_list:
            if contact in contact_count:
                contact_count[contact] += 1
            else:
                contact_count[contact] = 1
    
    # Find the contacts with the highest count
    max_count = max(contact_count.values())
    most_contacted = [contact for contact, count in contact_count.items() if count == max_count]
    most_contacted.sort()
    return most_contacted

# section 10
# note that zombie_list means potential zombies, who is not patient 
def find_maximum_distance_from_zombie(contacts_dic, zombie_list):
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

# section 11

def find_spreader_zombies_old(contacts_dic, zombie_list):
    spreader_zombies_list = []
    for patient in contacts_dic.keys():
        is_spreader = True
        for contact in contacts_dic[patient]:
            if contact not in zombie_list:
                is_spreader = False
        if is_spreader:
            spreader_zombies_list.append(patient)
    return spreader_zombies_list


def find_spreader_zombies(contacts_dic, zombie_list):
    spreader_zombies_list = []
    for patient, contacts_list in contacts_dic.items():
        if all (contact in zombie_list for contact in contacts_list):
            spreader_zombies_list.append(patient)
    return spreader_zombies_list

# sec 12                
def find_regular_zombies(contacts_dic, zombie_list):
    regular_zombies_list = []
    patient_list = contacts_dic.keys()

    for patient in patient_list:
        index = 0
        contact_with_patient = contact_with_zombie = False
        contact_list = contacts_dic[patient]

        while (not contact_with_patient or not contact_with_zombie)\
              and index < len(contact_list):
            if contact_list[index] in patient_list:
                contact_with_patient = True
            elif contact_list[index] in zombie_list:
                contact_with_zombie = True
            index += 1

        if contact_with_zombie and contact_with_patient:
            regular_zombies_list.append(patient)

    return regular_zombies_list


def find_predator_zombies(contacts_dic, zombie_list):
    # 一种是出现在了contact list里面但不是病人，也就是potential zombie；  - 不考虑了
    # 另一种是病人，但接触的所有人也都是病人（即没接触not in zombie list的人）
    predator_zombies_list = []
    patient_list = contacts_dic.keys()
    for patient, contacts_list in contacts_dic.items():
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

def main():
    
    # print(file_exists("sfadsf"))
    print(parse_file("testfile.txt"))
    # pretty_print_section_4(parse_file("testfile.txt"))
    # pretty_print_section_5(find_patients_zero(parse_file("DataSet1.txt")))
    dic = parse_file("DataSet1.txt")
    print(new_parse_file("DataSet1.txt"))
    # print(find_potential_zombies(parse_file("DataSet1.txt")))
    # pretty_print_section_7(find_not_zombie_nor_zero(dic,find_patients_zero(dic),find_potential_zombies(dic)))
    # pretty_print_section_8(find_most_viral(dic))
    # pretty_print_section_9(find_most_contacted(dic))
    zombie_list = find_potential_zombies(dic)
    # pretty_print_section_10(find_maximum_distance_from_zombie(dic, zombie_list))
    # print(find_spreader_zombies(dic, zombie_list))

    with open('output.txt', 'w') as file:
        # Use the redirect_stdout context manager to capture the output of prettyprint
        with contextlib.redirect_stdout(file):
            pretty_print_section_4(dic)
            pretty_print_section_5(find_patients_zero(dic))
            pretty_print_section_6(find_potential_zombies(dic))
            pretty_print_section_7(find_not_zombie_nor_zero(dic,find_patients_zero(dic), find_potential_zombies(dic)))                            
            pretty_print_section_8(find_most_viral(dic)) 
            pretty_print_section_9(find_most_contacted(dic)) 
            pretty_print_section_10(find_maximum_distance_from_zombie(dic, zombie_list))   
            pretty_print_section_11(find_spreader_zombies(dic, zombie_list))  
            pretty_print_section_12(find_regular_zombies(dic, zombie_list))
            pretty_print_section_13(find_predator_zombies(dic, zombie_list)) 
            print(parse_file(('DataSetCycle2.txt')))   
            print(find_cycles_in_data(parse_file('DataSetCycle1.txt')))   
            print(find_cycles_in_data(parse_file('DataSetCycle2.txt')))
            print(find_cycles_in_data(parse_file('DataSet1.txt')))                   
            

if __name__ == '__main__':
    main()