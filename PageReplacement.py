#Nathaniel Wiradiradja
#CSCI 340 Project 2

page_reference_strings = [
    [2, 6, 9, 2, 4, 2, 1, 7, 3, 0, 5, 2, 1, 2, 9, 5, 7, 3, 8, 5],
    [0, 6, 3, 0, 2, 6, 3, 5, 2, 4, 1, 3, 0, 6, 1, 4, 2, 3, 5, 7],
    [3, 1, 4, 2, 5, 4, 1, 3, 5, 2, 0, 1, 1, 0, 2, 3, 4, 5, 0, 1],
    [4, 2, 1, 7, 9, 8, 3, 5, 2, 6, 8, 1, 0, 7, 2, 4, 1, 3, 5, 8],
    [0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0],
] #Initialize page reference strings in a list containing lists to separate each ref string

frame_size = 3 #Declaring frame size

def optimal(refs):
    frame, faults = [], 0 #Initialize Frame as empty and faults as 0
    for idx, ref in enumerate(refs): #loop that iterates over each page reference in the input list refs, while also keeping track of the index of the current reference with idx.
        if ref not in frame: #Check if not already in memory
            faults += 1 #Increments the number of faults if the current page reference is not in memory.
            if len(frame) < frame_size: #If there are still empty frames in memory (less than frame_size), this block adds the current page reference to an empty frame in memory.
                frame.append(ref)
            else:
                furthest, replace_idx = -1, 0
            #If all frames are occupied, this block initializes variables furthest and replace_idx.
            #Furthest will be used to keep track of the furthest distance to the next reference to each page in memory,
            #And replace_idx will be used to keep track of the index of the page in memory that should be replaced.
                for i, f in enumerate(frame):
                    try:
                        next_idx = refs[idx+1:].index(f)
                    except ValueError:
                        next_idx = len(refs)
                    if next_idx > furthest:
                        furthest, replace_idx = next_idx, i
                #For Lines 26-32
                #This block iterates over each page in memory and checks how far in the future the next reference to the page occurs.
                #The page with the furthest distance to the next reference is then marked as the page to replace.
                frame[replace_idx] = ref
    return faults

def fifo(refs):
    frame, faults, idx = [], 0, 0
    #Initializes an empty list frame that will represent the frames in memory sets the number of faults to 0
    #Number of times a page fault occurs and initializes idx to 0
    for ref in refs: #Iterate through ref
        if ref not in frame: #Check if not already in memory
            faults += 1 #Increment Page fault
            if len(frame) < frame_size: #If there are still empty frames in memory (less than frame_size), this block adds the current page reference to an empty frame in memory.
                frame.append(ref)
            else: #If all frames are occupied, this block replaces the page at index idx in memory with the current page reference.
                frame[idx] = ref
            idx = (idx + 1) % frame_size #Updates the index of the frame to replace next, by incrementing idx and using the modulo operator to ensure that idx stays within the range of frame indices.
    return faults

def lru(refs):
    frame, faults, recent = [], 0, {}
    #Initializes an empty list frame that will represent the frames in memory, sets the number of faults to 0,
    #Initializes an empty dictionary recent to keep track of the most recently used pages in memory.
    for idx, ref in enumerate(refs): #Iterates over each page reference in the input list refs, while also keeping track of the index of the current reference with idx.
        if ref not in frame: #Check if not in memory
            faults += 1 #Increments Page fault
            if len(frame) < frame_size: #If there are still empty frames in memory (less than frame_size), this block adds the current page reference to an empty frame in memory.
                frame.append(ref)
            else:
                lru_page = min(recent, key=recent.get)
                del recent[lru_page]
                frame[frame.index(lru_page)] = ref
                #For Lines 58-61
                # If all frames are occupied, this block identifies the least recently used (LRU) page in memory by finding the page with the smallest value in the recent dictionary.
                # It then removes the LRU page from both the recent dictionary and the memory frame, and replaces it with the current page reference.
        recent[ref] = idx #Updates the recent dictionary with the index of the current page reference, indicating that it has just been used.
    return faults

def second_chance(refs):
    frame, faults, idx, ref_bits = [], 0, 0, {}
    #Initializes an empty list frame that will represent the frames in memory, sets the number of faults to 0,
    #The number of times a page fault occurs during the simulation, initializes idx to 0
    #Initializes an empty dictionary ref_bits to keep track of whether a page in memory has been referenced.
    for ref in refs:
        if ref not in frame:
            faults += 1
            while True:
                frame_idx = idx % frame_size
                if len(frame) < frame_size:
                    frame.append(ref)
                    break
                if frame[frame_idx] not in ref_bits or not ref_bits[frame[frame_idx]]:
                    frame[frame_idx] = ref
                    break
                ref_bits[frame[frame_idx]] = False
                idx += 1
            #For Lines 80-89
            #If all frames are occupied, this block implements the second chance algorithm. It first iterates through the frames,
            #Using the modulo operator to ensure that the index stays within the range of frame indices.
            #If there is an empty frame, the current page reference is added to it. If a page in memory has not been referenced (its ref_bits value is False),
            #It is replaced with the current page reference. If all pages in memory have been referenced (their ref_bits values are True),
            #The algorithm gives each page a second chance by setting its ref_bits value to False and moving to the next frame index.
        ref_bits[ref] = True #Updates the ref_bits dictionary with the current page reference
        idx = (idx + 1) % len(refs) #Updates the index of the frame to replace next
    return faults

algorithms = {'OPT': optimal, 'FIFO': fifo, 'LRU': lru, 'SEC': second_chance} #Maps Functions to names in format from Project specs

for prs in page_reference_strings:
    print("Page-Reference String:", ','.join(map(str, prs)))
    for name, algo in algorithms.items():
        faults = algo(prs)
        print(f"{name}: {faults}", end=" ")
    #For lines 104-106
    #Iterates over each algorithm in the algorithms dictionary and runs it on the current page reference string prs.
    #The number of page faults that occurred during the simulation is stored in the faults variable
    #The algorithm name and the number of faults are printed on the same line.
    print("\n")
