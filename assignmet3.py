#----------------------------------------------------
# Assignment 3: Main program
# 
# Author: Abdullah Hammawa, 1619949
# Collaborators/References: Docstrings from assignment description and myself
#----------------------------------------------------
from enrollStudent import StudentNode
from enrollStudent import EnrollTable 
from enrollStudent import PriorityQueue

def check_file(input_file):
    """checks to makes sure the file listing students is valid
    input: input_file
    returns: None"""
    
    try:
        file_to_check = open(input_file, 'r')
    except:
        raise Exception("The file {} cannot be opened".format(input_file))
    i = 1
    for student in file_to_check:
        student_info = student.split()
        if len(student_info[0]) != 6:
            raise Exception('In line {} of the input file the given ID number does not contain 6 digits'.format(i))
        if student_info[1] not in {'SCI', 'ENG', 'BUS', 'ART', 'EDU'}:
            raise Exception('The faculty abbreviation of the student in line {} of the input file is invalid'.format(i))
        try:
            int(student_info[0])
        except:
            raise Exception('The ID number of the student in line {} of the input file must be an integer'.format(i))         
    file_to_check.close()    

def enroll_students(input_file, enrollment_table, priorityQueue, capacity):
    """Enrolls students until the enrollment table is full. Once capacity is reached all new students are added to the Priority Queue
    input : input_file, enrollment_table, priorityQueue, capacity(int)
    returns: None"""
    
    file_to_use = open(input_file, 'r')
    i = 1
    for student in file_to_use:
        student_info = student.split()
        student_to_enroll = StudentNode(student_info[0], student_info[1], student_info[2], student_info[3])                
        if i < capacity:
            enrollment_table.insert(student_to_enroll)
            i += 1
        elif i >= capacity:
            priorityQueue.enqueue(student_to_enroll) 
    file_to_use.close()
    
def write_to_enrolled(enrollment_table):
    """Writes the enrollment table to a file called enrolled.txt
    input: enrollment_table
    returns: None"""
    
    enrolled_file = open('enrolled.txt', 'w')
    enrolled_file.write(enrollment_table.__str__())
    enrolled_file.close()
       
    
def append_to_waitlist(priorityQueue):
    """Appends the waitlist to a file called waitlist.txt
    input: priorityQueue
    returns: None"""    
    
    waitlist_file = open('waitlist.txt', 'a')
    waitlist_file.write(priorityQueue.__str__())
    waitlist_file.close()

    
def exiting():
    """Clears files and exits the program
    input: None
    returns: None"""
    
    exit_msg = "Exiting Program..."
    print(exit_msg)
    waitlist_file = open("waitlist.txt", "w")
    pass
    enrolled_file = open("enrolled.txt", "w")
    pass
    waitlist_file.close()
    enrolled_file.close() 
    return True

def drop_students(input_file, enrollment_table, priorityQueue):
    """Removes students in input file from the enrollment table than inserts them into the enrollment table in order of highest priority using priority Queue
    input: input_file, enrollment_table, priorityQueue
    returns: None"""
    
    students_to_drop = open(input_file, 'r')
    for student in students_to_drop:
        student_info = student.split()
        enrolled = enrollment_table.isEnrolled(student_info[0])
        if enrolled == False:
            warning_msg = "WARNING: {} {} (ID: {}) is not currently enrolled and cannot be dropped.".format(student_info[2], student_info[3], student_info[0])
            print('')
            print(warning_msg)
            print("")
        else:
            enrollment_table.remove(student_info[0])
            student_to_add = priorityQueue.dequeue()
            enrollment_table.insert(student_to_add)
    print(priorityQueue)
    print("")
    students_to_drop.close()    

def main():
    """Runs the program for enrolling students in full
    Input: None
    returns: None"""  
    
    exit_program = False
    capacity = 51
    enrollment_table = EnrollTable(capacity)
    priorityQueue = PriorityQueue()    
    while exit_program == False:
        #prompts the user to input valid instructions        
        instructions = input("Would you like to register or drop students [R/D]: ")
        if instructions in {'R','D', 'Q'}:         
            if instructions in {'R', 'D'}:
                input_file = input("Please enter a filename for student records: ")
                check_file(input_file)    
                if instructions == 'R':
                    enroll_students(input_file, enrollment_table, priorityQueue, capacity)
                    write_to_enrolled(enrollment_table)
                    print(enrollment_table)
                    print("")
                    print(priorityQueue)
                    print("")
                    append_to_waitlist(priorityQueue)
                elif instructions == 'D':
                    drop_students(input_file, enrollment_table, priorityQueue)
                    append_to_waitlist(priorityQueue)             
            elif instructions == 'Q':
                exit_program = exiting()               
main()