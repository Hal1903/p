import random as rand

import csv
from copy import deepcopy
# from minHeap import MinHeap
from typing import Callable, Any
import os

COMMENT = """
Date: Sept, 2023
Class: CS463G
"""

def getLine(index, dir, face):
    if (index%2==1):
        print("index must be even: one of 0,2,4,6")
        return
    A = []
    count = 1
    if dir == 0:
        #for i in range( -1, -len(face1[-1])-1, -2): # arr to 0. end pt -1 not included
        a = []
        count = index-len(face[-1])
        for j in range(len(face)-1, -1, -1): # -len(f) to 0 (end -1 is not included)
            if (count == -1):
                a.append(face[j][count])
                A.append(a)
                break
            a.append(face[j][count])
            a.append(face[j][count+1])
            count += 2
        # print("Taken Right")
    if dir == 1: # left 
        #for i in range( -1, -len(face[-1])-1, -2): # arr to 0. end pt -1 not included
        a = []
        count = index
        for j in range(len(face)-1, -1, -1): # -len(f) to -1
            if (count == 0):
                a.append(face[j][count])
                A.append(a)
                break
            #print("j and count=", j, count)
            a.append(face[j][count])
            a.append(face[j][count-1])
            count -= 2
        # print("Taken Left")
    if (len(A)==1):
        return A[0]
    return A


def reverse_2d_array(A): # Pyramix face n
    # Initialize an empty list to store the reversed arrays
    A_inv = []
    # Iterate over each array in the input 2D array
    for row in A:
        # Reverse the array and append it to A_inv
        A_inv.append(row[::-1])
    # print(f"Input: {A} Reversed array: {A_inv}")
    return A_inv
def reverse_1d_array(A):
    # print(f"Input: {A} Reversed array: {A[::-1]}")
    return A[::-1]

class Pyramix():
    def __init__(self) -> None:
        self.face1 = [          ['r'],
                            ['r','r','r'],
                        ['r','r','r','r','r'],
                      ['r','r','r','r','r','r','r']]
        self.face2 = [['b'],['b','b','b'],['b','b','b','b','b'],
                      ['b','b','b','b','b','b','b']]
        self.face3 = [['y'],['y','y','y'],['y','y','y','y','y'],
                      ['y','y','y','y','y','y','y']]
        self.face4 = [['g'],['g','g','g'],['g','g','g','g','g'],
                      ['g','g','g','g','g','g','g']]
        self.faces = [self.face1, self.face2, self.face3, self.face4]
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.children = []
    def update_faces(self): # needed for replaceLine
        self.face1 = self.faces[0]
        self.face2 = self.faces[1]
        self.face3 = self.faces[2]
        self.face4 = self.faces[3]
    def face_to_faces(self): # I was just lazy and scared to edit existing code. It's compensation
        self.faces[0] = self.face1
        self.faces[1] = self.face2
        self.faces[2] = self.face3
        self.faces[3] = self.face4  
    # primarily (or completely) for handling shifting the sides of the surface stickers
    def replaceLine(self, index, dir, f: int, line: list): # so it always starts from the bottom. Only for vertical. Use slicing for Horizontal.
        # index for the element in the last row
        if (index%2==1):
            print("index must be even: one of 0,2,4,6")
            return
        face = p.faces[f-1] # adjust face "1" to index 0 and "2" to idx 1
        l = 0
        if dir == 0: 
            count = index-len(face[-1])
            # print("line:", line, " with count", count)
            for j in range(len(face)-1, -1, -1): # -len(f) to 0 (end -1 is not included)
                if (count == -1):
                    face[j][count] = line[l]
                    l+=1
                    break
                # print(f"face[j]={face[j]}, line={line}: l={l}, count={count}, j={j}")
                #print("l and count=", l, count)
                face[j][count] = line[l] # solved: because line is for some reason a 2d arr, out of bound
                #if count+1 < len(face[j]) and l+1 < len(line):
                face[j][count+1] = line[l+1]
                l+=2
                count += 2
        elif dir == 1: # left 
            count = index
            for j in range(len(face)-1, -1, -1): # -len(f) to -1
                if (count == 0):
                    face[j][count] = line[l]
                    break
                #print("l and count=", l, count)
                face[j][count] = line[l]
                #if count+1 < len(face[j]) and l+1 < len(line):
                # print(f"face[j]={face[j]}, line={line}: l={l}, count={count}, j={j}")
                face[j][count-1] = line[l+1] # l+1 is issue, but why is l reaching 6
                l+=2
                count -= 2
        elif dir == 2: # horizontal
            pass
        self.update_faces()
    # rot_surf for changing just one face, not the side along with the face. Side will be handled by replaceLine function
    def  rotate_surface(self, f:int=0, dir:int=0):
        # if (f == 0):
        #     f = 1
        if (f < 1 or f > 4):
            print(f"The face f must be between 1-4: got {f}")
            return
        A = []
        face = self.faces[f-1]
        if dir == 0:  # Right rotation
            count = 1
            for i in range(0, len(face[-1]), 2):
                a = []
                count = i # keep track of which row looking at
                for j in range(len(face)-1, -1, -1):
                    if (count == 0): # reaching to the first elem or top count will be zero and terminate. No more to read.
                        a.append(face[j][count])
                        A.append(a)
                        break
                    a.append(face[j][count])
                    a.append(face[j][count-1])
                    count -= 2
            self.faces[f-1] = A
        if dir == 1: # left
            count = 1
            for i in range( -1, -len(face[-1])-1, -2): # arr to 0. end pt -1 not included
                a = []
                count = i
                for j in range(len(face)-1, -1, -1): # -len(f) to -1
                    if (count == -1):
                        a.append(face[j][count])
                        A.append(a)
                        break
                    a.append(face[j][count])
                    a.append(face[j][count+1])
                    count += 2
            self.faces[f-1] = reverse_2d_array(A)  
        self.update_faces()
        
    def horizontal_shift(self, row: int, dir: int): # left or right  --- not inverse yet, fix it --- FIX DONE
        if dir == 0: # right
            temp = self.face1[row]
            self.face1[row] = self.face3[row]
            self.face3[row] = self.face2[row]
            self.face2[row] = temp
            if (row==3):
                self.rotate_surface(4, 0) # rotate face4 right
        else: # left
            temp = self.face3[row]
            self.face3[row] = self.face1[row]
            self.face1[row] = self.face2[row]
            self.face2[row] = temp
            if (row==3):
                self.rotate_surface(4, 1) # rotate face4 right
        self.face_to_faces()
        self.update_faces()
        return self
    
    def vertical_shift_up(self, idx: int, lr: int): # up or down col->0-3 # issue here
        if idx % 2 == 1:
            print("idx cannot be odd")
            return
        i = 6-idx #-1-idx+7
        if lr == 0: # right 6
            temp = getLine(i, 1, self.face2) # 2
            # print(f"temp={temp}")
            self.replaceLine(i, 1, 2, reverse_1d_array(getLine(idx, 0, self.face1))) # affect 2 from 1 issue here
            self.replaceLine(idx, 0, 1, reverse_1d_array(getLine(i, 1, self.face4))) # affect 1 from 4
            self.replaceLine(i, 1, 4, temp) # affect 4 from 2
            if (idx==0):
                # self.rotate_surface()
                self.rotate_surface(3, 1) # or 0...? should be 1
                # rotate face3 to the left
        elif lr == 1: # left
            temp = getLine(i, 0, self.face3) # 3
            #self.replaceLine(i, 1, 2, reverse_1d_array(getLine(self.face4))) # affect 2 from 4
            # print(f"getline={getLine(idx, lr, self.face1)}, i={i} at face3 from face1 is to be affected")
            self.replaceLine(i, 0, 3, reverse_1d_array(getLine(idx, 1, self.face1))) # affect 3 from 1
            self.replaceLine(idx, 1, 1, reverse_1d_array(getLine(i, 0, self.face4))) # affect 1 from 4 issue here now
            self.replaceLine(i, 0, 4, temp) # affect 4 from 3 issue 9/6
            # affect 4 from 1
            #affect 1 from 2
            if (idx==6):
                self.rotate_surface(2, 0)  # rotate face2 to the right
        else:
            print("UNEXPECTED: from VSU")
            return
        return self
# I kinda regret that I just went by lr with int, not bool...I can't use negation...
    def vertical_shift_down(self, idx: int, lr: int): # up or down
        if idx % 2 == 1:
            print("idx cannot be odd")
            return
        i = 6-idx #-1-idx+7
        if lr == 0: # right
            temp = getLine(idx, lr, self.face1) # 2
            # print(f"temp={temp}") # this zero is lr
            self.replaceLine(idx, lr, 1, reverse_1d_array(getLine(i, 1, self.face2))) # affect 1 from 2 issue here
            self.replaceLine(i, 1, 2, getLine(i, 1, self.face4)) # affect 2 from 4 no rev
            self.replaceLine(i, 1, 4, reverse_1d_array(temp)) # affect 4 from 1
            if (idx == 0):
                self.rotate_surface(3, 0)
        elif lr == 1: # issue here only
            temp = getLine(idx, lr, self.face1) # 2
            # print(f"temp={temp}")
            self.replaceLine(idx, lr, 1, reverse_1d_array(getLine(i, 0, self.face3))) # affect 1 from 3 issue here
            self.replaceLine(i, 0, 3, getLine(i, 0, self.face4)) # affect 3 from 4 no rev
            self.replaceLine(i, 0, 4, reverse_1d_array(temp)) # affect 4 from 1
            if (idx == 6):
                self.rotate_surface(2, 1)
        else:
            print("UNEXPECTED")
            return
        print("Down done")
        return self
    
    # Take param Depth (int, 1 to 4), so it recursively call up to 
    def rotate(self, dir, depth:int=0): # 0 for right
        if (depth >= 3):
            print(f"depth geq 3 not supported: got {depth}")
            return
        three = getLine(6, 1, self.face3) # bottom to top
        two = getLine(0, 0, self.face2) # same
        four = self.face4[-1]
        A = []
        if dir == 0:  # Right rotation
            self.rotate_surface(1, 0)
            
        # other faces: 2,3,4 change 3->2->4->3
            # print(f'face4={self.face4[-1]} faces[-1]={self.faces[-1][-1]} and two={two} and reversed two={reverse_2d_array(two)}')
            self.replaceLine(6, 1, 3, four) # reverse removed 9/6
            self.faces[-1][-1] = reverse_1d_array(two) #reverse_2d_array(two)
            self.face4[-1] = reverse_1d_array(two) #reverse_2d_array(two) #self.replaceLine(0, dir, 4, two) #p.faces[2] = four #self.face3 = four
            self.replaceLine(0, 0, 2, reverse_1d_array(three)) #p.faces[1]=reverse_2d_array(temp) # self.face2 = reverse_2d_array(temp)
            if (depth > 0):
                # print(f"depth={depth}")
                for d in range(1, depth+1):
# CHANGE THE CODE HERE, SEE VARIABLES ARE SAME AS LEFT ROT DEPTH > 1 STILL ISSUE
                    three = getLine(6-2*d, 1, self.face3) # bottom to top
                    two = getLine(0+2*d, 0, self.face2) # same
                    four = self.face4[-1-d]
                    self.replaceLine(6-2*d, 1, 3, four) # in left: reverse should not be removed
                    self.faces[-1][-1-d] = reverse_1d_array(two)
                    self.face4[-1-d] = reverse_1d_array(two)
                    self.replaceLine(2*d, 0, 2, reverse_1d_array(three)) # take line in right dir 4->2

# For some reason, face3 is not correct...FIX!!!!!
        elif dir == 1:  # Left rotation
            self.rotate_surface(1, 1)       
        # other faces temp=3
            self.replaceLine(6, dir, 3, reverse_1d_array(two)) # in left
            self.replaceLine(0, 0, 2, reverse_1d_array(four)) # take line in right dir 4->2
            self.faces[-1][-1] = three
            self.face4[-1] = three # temp=three
            # self.faces[2] = reverse_2d_array(two) # self.face3 = reverse_2d_array(two)
            # self.faces[1] = reverse_2d_array(four) # self.face2 = reverse_2d_array(four)
            # self.faces[-1] = temp # self.face4 = temp
            if (depth > 0):
                # print(f"rotate with depth={depth}")
                for d in range(1, depth+1):
                    three = getLine(6-2*d, 1, self.face3) # bottom to top
                    two = getLine(0+2*d, 0, self.face2) # same
                    four = self.face4[-1-d]
                    self.replaceLine(6-2*d, dir, 3, reverse_1d_array(two)) # in left
                    self.replaceLine(0+2*d, 0, 2, reverse_1d_array(four)) # take line in right dir 4->2
                    self.faces[-1][-1-d] = three
                    self.face4[-1-d] = three
        p.update_faces()
        return self
        # print("Update Done")

    def show(self):
        count = 7
        for i in self.face1:
            print(" "*count, end="")
            for j in i:
                print(j, end=" ")
            count-=2
            print('\n')
        count = 7
        for i in self.face2:
            print(" "*count, end="")
            for j in i:
                print(j, end=" ")
            count-=2
            print('\n')   
        count = 7     
        for i in self.face3:
            print(" "*count, end="")
            for j in i:
                print(j, end=" ")
            count-=2
            print('\n')
        count=7
        for i in self.face4:
            print(" "*count, end="")
            for j in i:
                print(j, end=" ")
            count-=2
            print('\n')

    # make sure the scope is right: changing p by randomize actually happens?
    def moveExe(self, moves: tuple): # tuple of arrays, takes a list of recorded_inputs-like array
        ms, A = moves
        # print(A)
        for a, m in zip(A, ms):
            n = a[1]
            dir = 0 #a[-1]
            # print(f"m={m}, A={a}")
            if (m==0): # h 
                self.horizontal_shift(n//2, dir) # out of range m=0, A=[2, 4, 1, 1] 
                # [ans, idx, lr, dir]
            elif (m==1): # v
                a2 = a[2]
                if (dir == 0):
                    self.vertical_shift_up(n, a2)
                else:
                    self.vertical_shift_down(n, a2)
            elif(m==2): # r
                self.rotate(dir, a[-2])
            else:
                print(f"ERROR: m={m} and terminated with parameters {a}")
                
    def invert(self, moves: list): # to compute how to invert all the moves. I'll implement it when I need to.
        ms, A = moves
        ms = reverse_1d_array(ms)
        A = reverse_1d_array(A)
        for a, m in zip(A, ms):
            n = a[1]
            dir = a[-1]
            # print(f"m={m}, A={a}")
            if (m==0): # h 
                self.horizontal_shift(n//2, not dir)
                # [ans, idx, lr, dir]
            elif (m==1): # v
                a2 = a[2]
                if (dir == 1):
                    self.vertical_shift_up(n, a2)
                else:
                    self.vertical_shift_down(n, a2)
            elif(m==2): # r
                self.rotate(not dir, a[-2])
            else:
                print(f"ERROR: m={m} and terminated with parameters {a}")
    def heuristic(self) -> int:
        letter_set = set()
        for face in self.faces:
            for row in face:
                for letter in row:
                    letter_set.add(letter)  # Add each unique letter to the set
        return len(letter_set)  # Return the number of distinct letters
    def __eq__(self, other):
        a = self.face1 == other.face1
        b = self.face2 == other.face2
        c = self.face3 == other.face3
        d = self.face4 == other.face4
        if (a*b*c*d == 1):
            return True
        else:
            return False  
    def __repr__(self):
        self.show()
        return str(self.g)

def randomArray(n):
    m = [] # shifts and rots
    A = [] # params for above
    # for i in range(0, n):
    for r in range(0, n):
        r = rand.randint(0, 2)
        m.append(r)
        ans = rand.randint(0, 2)
        if (int(ans) == 2):
            idx = rand.randrange(0, 5, 2)
            # print(f"idx adjusted: {idx}")
        else:
            idx = rand.randrange(0, 7, 2)
        depth = rand.randint(0, 2)
        lr = rand.randint(0, 1)
        dir = rand.randint(0, 1)

        A.append([ans, idx, lr, depth, dir])
    return (m, A)

import os
# os.system('cls' if os.name == 'nt' else 'clear')


"""
[note for myself] Use 16 for rand, use the rest for invert (and A*)
"""

seed = 1
rand.seed(seed)
p = Pyramix()
MOVE_COUNT = 5
# p.randomize(0)
# Invert: h: 1, v: only down, r: 1

"""
What I have tried is as follows:
- Using for loop deep-copy the objects and applies different rotation to each
- Manually creating few deep copies and applies rotations (as shown below)
- Checking id's
- Implementing copy constructors (was ineffective)

What I observed:
- each deep-copy has different id
- the rotation applies to the different deep-copied object
- the configuration after each rotation implies that deepcopy() actually behaves like shallow copy
  (config of p2 is retained by p3)
- I added print("down done") at the end of the rotation function I applied, and it shows up.
  The reason that the configuration has not changed is uncertain (maybe applied to something different?).
- for some reason, config of p is altered while the program should not have modified this
  
Also, when I use Pyramix object in another file, nothing works. 
For example, as I created Astar.py and import Pyramix via 'from pyramix import Pyramix',
constructor and show() is the only thing that works for Pyramix
The error message does not show up, too.
I never have encountered such error for years and have no idea how to resolve this now.
"""
import sys

if __name__ == "__main__":
    # List to store the recorded inputs
    os.system('cls' if os.name == 'nt' else 'clear')

    p = Pyramix()
    curr = p
    # p.horizontal_shift(0,0)
    # p.vertical_shift_down(2, 0)
    # p.show()
    # p2s = [p.dcopy() for _ in range(0, 4)]
    p2 = deepcopy(p)
    p2.horizontal_shift(0, 1)
    # vertical_shift_down(0,0)
     # worked
    
    print('-------------------p2---------------------')
    p2.show()
    p.show() # p has changed
    print('-------------------p3---------------------')
    p3 = deepcopy(p)
    p3.horizontal_shift(1, 1)
    # vertical_shift_down(2, 0)
    
    
    p3.show()
    p2.show() # p2 has not changed
    p.show()
    print('------------------------------------------')
    p4 = deepcopy(p)
    p4.horizontal_shift(2, 1)
    # vertical_shift_down(4, 0)
    
    
    p4.show()
    print('------------------------------------------')
    p.show()
    print("id(p) = %i" % id(p))
    print("id(p2) = %i" % id(p2))
    print("id(p3) = %i" % id(p3))
    print(f"id for face1 of p={id(p.face1)}")
    print(f"id for face1 of p2={id(p2.face1)}")
    print(f"id for face1 of p3={id(p3.face1)}")
    print(f"id for face1 of p={id(p.show)}")
    print(f"id for face1 of p2={id(p2.show)}")
    # for i in range(0, 4):
    #     print(f'-------------Index={i}*2----------------')
    #     p2s[i].vertical_shift_down(i*2, 0)
    #     p2s[i].show()
    #     print('-----------------------------------------')


    # recorded_inputs = []

    # first = input("0 to test, and 1 to start from scrambled: ")
    # first = bool(int(first))
    # print(first, type(first))
    # A = None
    # if first == 1:
    #     MOVE_COUNT = int(input("Number of moves for scrambling: "))
    #     A = randomArray(MOVE_COUNT)
    #     output_filename2 = "recorded_inputs_S2.csv"
    #     print(f"Inputs recorded and saved to {output_filename2}")
    #     with open(output_filename2, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         # Write the header
    #         writer.writerow(['ans', 'n', 'lr', 'dir'])
    #         # Write each list element to a row in the CSV
    #         m, a = A
    #         for row in a:
    #             writer.writerow(row) 
    #     p.moveExe(A)
    #     p.show()
    #     first = int(input("Do you want to invert? 1 for yes, 0 for No: "))
    #     if first==1:
    #         p.invert(A)
    #         print("Inversion Done")
    #         p.show()
    # # issue in 0,0,1,1

    # while True:
    #     ans = input("Face1 fixed operations:\n0: horizontal, 1: vertical, 2: rotate, -1 to quit\n ")
        
    #     # Quit condition
    #     if int(ans) == -1:
    #         print("Program Quit")
    #         break
        
    #     # Validate ans input
    #     if not ans.isnumeric() or (int(ans) not in [0, 1, 2]):
    #         print(f"Input={ans}: Type a numeric or Type 0, 1, or 2")
    #         continue
        
    #     n = None
    #     lr = None
    #     dir = None
        
    #     ans = int(ans)
        
    #     # Input for horizontal or rotation (ans == 0 or 2)
    #     if ans == 0 or ans == 2:
    #         n = input("Row or Depth number (top is 0, bottom is 3 / for depth, 0 for a single layer. 3 does nothing.)\n")
    #         if not n.isnumeric() or not (0 <= int(n) <= 3):
    #             print("Type a numeric between 0-3")
    #             continue
    #         n = int(n)
        
    #     # Input for vertical shift (ans == 1)
    #     if ans == 1:
    #         n = input("Index number of the last row of face1 that you want to move: ")
    #         lr = input("Direction of the line (Right=0, Left=1): ")
    #         if not (n.isnumeric() and lr.isnumeric() and int(lr) in [0, 1]):
    #             print("Type a numeric and Type 0 or 1 for direction")
    #             continue
    #         n = int(n)
    #         lr = bool(int(lr))

    #     # Input for direction
    #     dir = input("Right or Up: 0, Left or Down: 1\n")
    #     if not dir.isnumeric() or int(dir) not in [0, 1]:
    #         print("Type a numeric and Type 0 or 1 for direction")
    #         continue
    #     dir = bool(int(dir))

    #     # Add the current inputs to the recorded list
    #     recorded_inputs.append([ans, n, lr, dir])

    #     # Perform the operations
    #     if ans == 0:  # Horizontal shift
    #         p.horizontal_shift(n, dir)
    #         print("Horizontal Right Done" if dir == 0 else "Horizontal Left Done")
    #     elif ans == 1 and dir == 0:  # Vertical up
    #         p.vertical_shift_up(n, lr)
    #         print("Vertical Up Done")
    #     elif ans == 1 and dir == 1:  # Vertical down
    #         p.vertical_shift_down(n, lr)
    #         print("Vertical Down Done")
    #     elif ans == 2:  # Rotation
    #         p.rotate(dir, n)
    #         print("Rotation Done")
    #     else:
    #         print("Unexpected condition, returned to the first step")

    #     # Show the result and print the previous command
    #     p.show()
    #     print(f"Previous Command: {ans}, {dir} at {n}")

    # # After loop ends, save recorded inputs to CSV
    # output_filename = "recorded_inputs_S1.csv"

    # with open(output_filename, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['ans', 'n', 'lr', 'dir'])  # CSV header
    #     writer.writerows(recorded_inputs)

    # print(f"Inputs recorded and saved to {output_filename}")


