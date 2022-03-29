#----------------------------------------------------
# Assignment 3: Enroll Student
# 
# Author: Abdullah Hammawa, 1619949
# Collaborators/References: Docstrings from assignment description and myself
#----------------------------------------------------
class StudentNode:
    def __init__(self, iD, faculty, first, last):
        self.__iD = iD
        self.__faculty = faculty
        self.__first = first
        self.__last = last
        self.__nextLink = None
        self.__previousLink = None
        
        
    def setID(self, newID):
        self.__iD = newID
        
    def setFac(self, faculty):
        self.__faculty = faculty
        
    def setFirstName(self, first):
        self.__first = first
        
    def setLastName(self, last):
        self.__last = last
        
    def setNext(self, nextLink):
        self.__nextLink = nextLink
        
    def setPrevious(self, previousLink):
        self.__previousLink = previousLink
        
    def getID(self):
        """returns the student id as a string."""
        return self.__iD

    def getFac(self):
        """returns the student faculty"""
        return self.__faculty
    
    def getFirstName(self):
        """returns a string representing the student's first name"""
        return self.__first
    
    def getLastName(self):
        """returns a string representing the student's last name"""
        return self.__last
    
    def getNext(self):
        """returns the next node"""
        return self.__nextLink
    
    def getPrev(self):
        """returns the previous node"""
        return self.__previousLink
    
class EnrollTable:
    def __init__(self, capacity):
        self.__capacity = capacity
        self.__enrollmentTable = [None] * self.__capacity
        self.__size = 0
        
    def cmputIndex(self, studentID):
        """Uses the given studentID to calculate the position a student with that ID number would be inserted into the enrollment table
        input: studentID(str)
        returns: position(int)"""
        
        is_valid = (len(studentID) == 6)
        assert is_valid == True, "A valid student ID must contain six digits"
        try:
            # id_integer is just to make sure that the string of characters we're can actually be turned into an integer otherwise we raise an exception
            id_integer = int(studentID)
            student_numbers = studentID
            first_number = int(student_numbers[0]+student_numbers[1])
            second_number = int(student_numbers[2]+student_numbers[3])
            third_number = (int(student_numbers[4]+student_numbers[5]))**2
            numbers = [first_number, second_number, third_number]
            total = sum(numbers)
            position = total % self.__capacity
            return position
        except:
            print("Student ID may only contain numbers and no other characters")
    
        
    def insert(self, item):
        """inserts students into the enrollment table at a position dependent on their ID number
        input: item(StudentNode)
        returns: None"""
        table_index = self.cmputIndex(item.getID())
        studentID = int(item.getID())
        current = self.__enrollmentTable[table_index]
        # if the given position in the list is already empty we just go ahead and insert the node 
        if current == None:
            self.__enrollmentTable[table_index] = item
        #for if the item we're inserting happens to have the lowest student id
        elif studentID <= int(current.getID()):
            item.setNext(current)
            current.setPrevious(item)
            self.__enrollmentTable[table_index] = item            
        else:
            # for when we have to start traversing the singly linked list
            is_bigger =  False
            while is_bigger == False and current.getNext() != None:
                current = current.getNext()
                is_bigger = (studentID <= int(current.getID()))
            if current.getNext() == None and is_bigger == False:
                current.setNext(item)
                item.setPrevious(current)
            else:
                new_previousLink = current.getPrev()
                item.setPrevious(new_previousLink)
                item.setNext(current)
                new_previousLink.setNext(item)
                current.setPrevious(item)
        self.__size += 1
        
    def isStudent(self, studentID, current):
        """returns True if the inputted ID matches that of the inputted student
        input: studentID(str), current(StudentNode)"""
        is_student = (studentID == current.getID())
        return is_student
        
    
    def remove(self, studentID):
        """Attempts to remove the student who's ID number matches the inputted student ID. If said student is removed succesfully returns True and returns False otherwise
        input: studentID(str)"""
        table_index = self.cmputIndex(studentID)        
        # if the given position in the list is already empty we just go ahead and return false since there is nothing to remove
        current = self.__enrollmentTable[table_index]
        if current == None:
            return False
        else:
            # for when we have to start traversing the singly linked list 
            while self.isStudent(studentID, current) == False and current.getNext() != None:
                current = current.getNext()                   
            # the if statemnt rules out the scenario where we've traversed the whole list and we've come up with no matching student ID to remove
            if self.isStudent(studentID, current) == False:
                return False
            else:
                # in the case that the first node in the singly linked list is the student we're removing
                if current.getPrev() == None:
                    new_head = current.getNext()
                    self.__enrollmentTable[table_index] = new_head
                    current.setNext(None)
                elif current.getNext() == None:
                    new_tail = current.getPrev()
                    new_tail.setNext(None)
                else:
                    next_student = current.getNext()
                    previous_student = current.getPrev()
                    next_student.setPrevious(previous_student)
                    previous_student.setNext(next_student)
                    current.setNext(None)
                    current.setPrevious(None)
                self.__size -= 1
                return True

        
    def isEnrolled(self, student_ID):
        """returns True if the inputted student's ID is in the enrollment table and False otherwise
        input: student_ID(str)"""
        
        table_index = self.cmputIndex(student_ID)
        studentID = int(student_ID)        
        # if the given position in the list is already empty or the studentID we're checking against is less than the head of our singly linked list than we know said student is not enrolled
        if self.__enrollmentTable[table_index] == None or studentID < int(self.__enrollmentTable[table_index].getID()):
            return False
        else:
            # for when we have to start traversing the singly linked list
            current = self.__enrollmentTable[table_index]
            is_enrolled = (studentID == int(current.getID()))
            while is_enrolled == False and current.getNext() != None:
                current = current.getNext()
                is_enrolled = (studentID == int(current.getID()))
            if is_enrolled == True:
                return True
            else:
                return False
            
    def size(self):
        """returns the number of students in the enrollment_table"""
        
        return self.__size
    
    def isEmpty(self):
        """returns True if the enrollment table is Empty and False otherwise"""
        
        if self.__size == 0:
            return True
        else:
            return False
        
    def __str__(self):
        """returns a string representation of the enrollment table"""
        string = ''
        for i in range(self.__capacity):
            current = self.__enrollmentTable[i]
            if current == None:
                pass
            else:
                student_info = "\n{}: [{}, {}, {}, {}".format(self.cmputIndex(current.getID()), current.getID(), current.getFac(), current.getFirstName(), current.getLastName())
                string += student_info
                while current.getNext() != None:
                    current = current.getNext()
                    student_info = ", {}, {}, {}, {}".format(current.getID(), current.getFac(), current.getFirstName(), current.getLastName())
                    string += student_info
                string += ']'
        return string
            
                
#def testenrollStudent():
    ##testing StudentNode
    #Abdullah = StudentNode('123456', 'SCI', 'Abdullah', 'Hammawa')
    #Abdullah.setID('654321')
    #is_pass = (Abdullah.getID() == "654321")
    #assert is_pass == True, "fail the test" 
    #Abdullah.setFac('ENG')
    #is_pass = (Abdullah.getFac() == "ENG")
    #assert is_pass == True, "fail the test" 
    #Abdullah.setFirstName('LeBron')
    #is_pass = (Abdullah.getFirstName() == "LeBron")
    #assert is_pass == True, "fail the test"
    #Abdullah.setLastName("James")
    #is_pass = (Abdullah.getLastName() == "James")
    #assert is_pass == True, "fail the test" 
    #Abdullah.setNext("next student")
    #is_pass = (Abdullah.getNext() == "next student")
    #assert is_pass == True, "fail the test"
    #Abdullah.setPrevious('previous student')
    #is_pass = (Abdullah.getPrev() == "previous student")
    #assert is_pass == True, "fail the test" 
    #Abdullah.setNext(None)
    #Abdullah.setPrevious(None)
    
    ##tests for the enroll table class
    #enrollment_table = EnrollTable(51)
    #enrollment_table.insert(Abdullah) 
    #Leila = StudentNode('745221', 'ENG', 'Leila', 'Megevand')
    #enrollment_table.insert(Leila)
    #enrollment_table.isStudent('745221', Leila)
    #is_pass = (enrollment_table.cmputIndex('123456') == 20)
    #assert is_pass == True, "fail the test"        
    #is_pass = (enrollment_table.size() == 2)
    #assert is_pass == True, "fail the test"
    #is_pass = (enrollment_table.isEnrolled('745221') == True)
    #assert is_pass == True, "fail the test"    
    #is_pass = (enrollment_table.isEnrolled('832832') == False)
    #assert is_pass == True, "fail the test"
    #is_pass = (enrollment_table.remove('745221') == True)
    #assert is_pass == True, "fail the test" 
    #enrollment_table.remove("000000")
    #is_pass = (enrollment_table.remove('000000') == False)
    #assert is_pass == True, "fail the test"
    #enrollment_table.remove('654321')
    #is_pass = (enrollment_table.isEmpty() == True)
    #assert is_pass == True, "fail the test"    
    
    #input_file = open('input.txt', 'r')
    #for student in input_file:
        #student_info = student.split()
        #student_to_enroll = StudentNode(student_info[0], student_info[1], student_info[2], student_info[3])
        #enrollment_table.insert(student_to_enroll)
    #input_file.close()
    #print(enrollment_table)  
    #is_pass = (enrollment_table.isEnrolled('168258') == False)
    #assert is_pass == True, "fail the test"
    #is_pass = (enrollment_table.remove('168258') == False)
    #assert is_pass == True, "fail the test"    

    
#if __name__ == '__main__':
    #testenrollStudent()        
    
class PriorityQueue:
    def __init__(self):
        self.__head =  None
        self.__tail =  None
        self.__priority = {'SCI': 4, 'ENG': 3, 'BUS': 2, 'ART': 1, 'EDU': 0}
        self.__priorityQueue = []
        self.__size = 0
    
    
    def is_higher_priority(self, item, current):
        """compares priority between two Students returns True if current has a higher priority than item and false otherwise
        input: item, current,(both StudentNode objects)"""
        student_faculty = item.getFac()
        student_priority = self.__priority.get(student_faculty)
        current_priority = self.__priority.get(current.getFac())        
        higher_priority = (student_priority <= current_priority)
        return higher_priority
    
    def enqueue(self, item):
        """Adds students to a location in the queue depending on their priority
        input:item(StudentNode)"""
        
        # if the priority queue is empty we just enqueue the student regardless
        if self.size() == 0:
            self.__tail = item
            self.__head = item
            self.__priorityQueue.append(item)
        else:
            current = self.__tail
            i = 0
            while self.is_higher_priority(item, current) == False and current.getNext() != None:
                current = current.getNext()
                i += 1
            # this conditional covers the situation where the student we're putting into the queue has the highest priority
            if self.is_higher_priority(item, current) == False:
                item.setPrevious(current)
                current.setNext(item)
                self.__head = item
                self.__priorityQueue.append(item)
            elif self.is_higher_priority(item, current) == True:
                # this conditional is for the situation where the student we're enqueueing has the lowest priority
                if current == self.__tail:
                    item.setNext(current)
                    current.setPrevious(item)
                    self.__tail = item
                # this is for when the student has neither the highest or lowest priority
                else:
                    new_previous_link = current.getPrev()
                    item.setPrevious(new_previous_link)
                    item.setNext(current)
                    new_previous_link.setNext(item)
                    current.setPrevious(item)
                self.__priorityQueue.insert(i, item)
        self.__size += 1
        
    def dequeue(self):
        """removes and returns the student with the highest priority from the queue"""
        try:            
            highest_priority_node = self.__priorityQueue.pop()
            self.__size -= 1        
            return highest_priority_node
        except:
            raise Exception('Cannot dequeue from an empty queue')
        
    def size(self):
        """returns the number of objects in the priority queue"""
        return len(self.__priorityQueue)
    
    def isEmpty(self):
        """returns True if the Priority Queue is empty and false otherwise"""
        if self.__size == 0:
            return True
        else:
            return False 
        
    def __str__(self):
        """returns a string representation of the priority queue
        input: None
        returns: priority queue as a strinng"""
        printedQueue = '['
        for i in range(1, self.__size + 1):
            current = self.__priorityQueue[-i]
            student_info = "{}, {}, {}, {},\n ".format(current.getID(), current.getFac(), current.getFirstName(), current.getLastName())
            if i == self.__size:
                student_info = "{}, {}, {}, {}".format(current.getID(), current.getFac(), current.getFirstName(), current.getLastName())
            printedQueue += student_info
        printedQueue += ']'
        return printedQueue
        
#def testPriorityQueue():
    #PQ = PriorityQueue()
    #test_file = open('sample_reg.txt', 'r')
    #for student in test_file:
        #student_info = student.split()
        #student_to_enroll = StudentNode(student_info[0], student_info[1], student_info[2], student_info[3])
        #PQ.enqueue(student_to_enroll)
    #test_file.close()
    #is_pass = (PQ.isEmpty() == False)
    #assert is_pass == True, "fail the test" 
    #is_pass = (PQ.size() == 6)
    #assert is_pass == True, "fail the test"    
    #print(PQ)
    #highest_priority = PQ.dequeue()
    #is_pass = (highest_priority.getFirstName() == 'Mary')
    #assert is_pass == True, highest_priority.getFirstName()#"fail the test" 
    #is_pass = (PQ.size() == 5)
    #assert is_pass == True, "fail the test"    
    #print('After dequeue')
    #print(PQ)
        
#if __name__ == '__main__':
    #testPriorityQueue()        