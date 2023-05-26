#Nathaniel Wiradiradja
#Project 1
#CSCI 340

import random

class Task:
    def __init__(self, name, priority, burst_time):
        self.name = name
        self.priority = priority
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

    def __str__(self):
        return self.name

#First Come First Serve
def fcfs(tasks):
    arrival_time = 0
    current_time = 0 #Initialize time to 0
    gantt_chart = [] #Set gantt chart to empty list -> Will store values into it
    for task in tasks:
        task.waiting_time = current_time #Sets waiting time to current time i.e waiting time for T2 is 20, current time is 20
        start_time = current_time #Sets the start of the task to the current time. The current time is also the start of the task
        current_time += task.burst_time #Adds the task burst time to current time
        end_time = current_time #Sets the new current time after executing task to the end of that task
        task.turnaround_time = end_time - arrival_time #Calculates the turn around time for the specific task executed
        gantt_chart.append((task.name, start_time, end_time)) #populates the Gantt char with the start and end time of each task
    return gantt_chart

#Shortest Job First
def sjf(tasks):
    current_time = 0 #Initialize time to 0
    arrival_time = 0
    gantt_chart = [] #Set gantt chart to empty list -> Will store values into it
    remaining_tasks = tasks.copy() #Keeps track of tasks that still needs to be executed
    while remaining_tasks: #Loops until there are no more tasks
        next_task = min(remaining_tasks, key=lambda t: t.burst_time) #Finds task with shortest burst from the remaining tasks, lambda takes burst time from each task
        next_task.waiting_time = current_time #Updates waiting time
        start_time = current_time #Assigns start to current
        current_time += next_task.burst_time #Updates current time by adding the burst of next task and assiging the value to end
        end_time = current_time #Assigns end to current
        next_task.turnaround_time = end_time  #Calculates turnaround time
        remaining_tasks.remove(next_task)  #Removes next task
        gantt_chart.append((next_task.name, start_time, end_time)) #Populates chart
    return gantt_chart

#Priority Scheduling
#Lines 55-61 same in SJF
def ps(tasks):
    current_time = 0 #Initialize time to 0
    gnatt_chart = [] #Set gantt chart to empty list -> Will store values into it
    remaining_tasks = tasks.copy() #Keeps track of tasks that still needs to be executed
    while remaining_tasks: #Loops until there are no more tasks
        next_task = min(remaining_tasks, key=lambda t: t.priority) #Finds task with LOWEST Priority
        next_task.waiting_time = current_time
        start_time = current_time
        current_time += next_task.burst_time
        end_time = current_time
        next_task.turnaround_time = end_time - next_task.waiting_time
        gnatt_chart.append((next_task.name, start_time, end_time))
        remaining_tasks.remove(next_task)
    return gnatt_chart

#Round Robin
def rr(tasks, quantum):
    current_time = 0 #Initialize time to 0
    gantt_chart = [] #Set gantt chart to empty list -> Will store values into it
    remaining_tasks = tasks.copy() #Keeps track of tasks that still needs to be executed
    while remaining_tasks: #Loops until there are no more tasks
        next_task = remaining_tasks.pop(0) #Removes first task and assigns to next task
        start_time = current_time #Assigns current to start
        #For Lines 79-97
        #Checks if the Burst time is greater than quantam, if it is the the next task is executed
        #Then added back to the END of remaining_tasks
        #Last_executed_time of the next_task is set to current, end time is set to current time
        #If burst time is less than or equal to quantam time then the task is executed for entire burst time
        if next_task.burst_time > quantum:
            next_task.waiting_time += start_time - next_task.last_executed_time
            current_time += quantum
            next_task.burst_time -= quantum
            next_task.last_executed_time = current_time
            remaining_tasks.append(next_task)
            end_time = current_time
        else:
            next_task.waiting_time += start_time - next_task.last_executed_time
            current_time += next_task.burst_time
            end_time = current_time
            next_task.turnaround_time = end_time - next_task.arrival_time
            next_task.waiting_time = next_task.turnaround_time - next_task.burst_time
        gantt_chart.append((next_task.name, start_time, end_time))
        for task in remaining_tasks:
            if task.arrival_time <= current_time and task.last_executed_time is None:
                if task.waiting_time == 0: # check if the task has already been executed
                    task.waiting_time = current_time - task.arrival_time
    return gantt_chart





# initialize tasks
t1 = Task("T1", 2, 20)
t2 = Task("T2", 4, 25)
t3 = Task("T3", 3, 25)
t4 = Task("T4", 3, 15)
t5 = Task("T5", 1, 10)
tasks = [t1, t2, t3, t4, t5]


# First Come First Serve
fcfs_tasks = tasks.copy()
gantt_chart = fcfs(fcfs_tasks) #Calls FCFS function passing fcfs_tasks and assigns the returned value of gantt_chart
print("First Come First Serve:")
print("Gantt chart:")
for task in gantt_chart: #Iterates over tuples in Gantt Chart
    print(f"{task[0]} [{task[1]} – {task[2]}] ", end="") #Prints in this Format
print()

avg_waiting_time = sum(task.waiting_time for task in fcfs_tasks) / len(fcfs_tasks) #Calculates Avg Waiting
avg_turnaround_time = sum(task.turnaround_time for task in fcfs_tasks) / len(fcfs_tasks) #Calculates Avg Turnaround
print(f"Avg. waiting time: {avg_waiting_time:.2f}") #Prints Avg waiting time
print(f"Avg. turnaround time: {avg_turnaround_time:.2f}") #Prints Avg turnaround time

#Shortest Job First
sjf_tasks = tasks.copy()
random.shuffle(sjf_tasks) #Shuffles the order of tasks
gantt_chart = sjf(sjf_tasks) #Calls SJF function and assigining the returned value to gantt chart
print("\nShorest Job First:")
print("Gantt chart:")
for task in gantt_chart: #Iterates through tuples
    print(f"{task[0]} [{task[1]} – {task[2]}] ", end="") #Prints in this Format
print()

avg_waiting_time = sum(task.waiting_time for task in sjf_tasks) / len(sjf_tasks) #Calculates Avg Waiting
avg_turnaround_time = sum(task.turnaround_time for task in sjf_tasks) / len(sjf_tasks) #Calculates Avg Turnaround
print(f"Avg. waiting time: {avg_waiting_time:.2f}") #Prints Avg Waiting
print(f"Avg. turnaround time: {avg_turnaround_time:.2f}") #Prints Avg Turnaround


#Priority Scheduling
ps_tasks = tasks.copy()
for task in ps_tasks:
    task.arrival_time = random.randint(0, 100) #Sets a random arrival time between 0-100 for each Task
ps_tasks.sort(key=lambda t: (t.priority, t.arrival_time)) #Sorts the tasks based off Priority and Arrival
gantt_chart = ps(ps_tasks)
print("\nPriority Scheduling:")
print("Gantt chart:")
for task in gantt_chart: #Iterates Through tuples
    print(f"{task[0]} [{task[1]} – {task[2]}] ", end="") #Prints in this Format
print()

avg_waiting_time = sum(task.waiting_time for task in ps_tasks) / len(ps_tasks) #Calculates Avg Waiting
avg_turnaround_time = sum(task.turnaround_time for task in ps_tasks) / len(ps_tasks) #Calculates Avg Turnaround
print(f"Avg. waiting time: {avg_waiting_time:.2f}") #Prints Avg Waiting
print(f"Avg. turnaround time: {avg_turnaround_time:.2f}") #Prints Avg Turnaround

#Round Robin
rr_tasks = tasks.copy()
for task in rr_tasks:
    task.last_executed_time = 0 #Set to 0
    task.arrival_time = 0 #Set to 0
gantt_chart = rr(rr_tasks, 10) #Calling RR function, Set Quantam to 10
print("\nRound Robin:")
print("Gantt chart:")
for task in gantt_chart:
    print(f"{task[0]} [{task[1]} – {task[2]}] ", end="") #Prints in this Format
print()

avg_waiting_time = sum(task.waiting_time for task in rr_tasks) / len(rr_tasks) #Calculates Avg Waiting
avg_turnaround_time = sum(task.turnaround_time for task in rr_tasks) / len(rr_tasks) #Calculates Avg Turnaround
print(f"Avg. waiting time: {avg_waiting_time:.2f}") #Prints Avg Waiting
print(f"Avg. turnaround time: {avg_turnaround_time:.2f}") #Prints Avg Turnaround