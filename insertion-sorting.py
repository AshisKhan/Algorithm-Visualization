### INSERTION SORTING ALGORITHM

import tkinter as tkin
import random


def swap_two_position(position_0, position_1):
    Bar1_x1, _, Bar1_x2, _ = canvas.coords(position_0)
    Bar2_x1, _, Bar2_x2, _ = canvas.coords(position_1)
    canvas.move(position_0, Bar2_x1 - Bar1_x1, 0)
    canvas.move(position_1, Bar1_x2 - Bar2_x2, 0)


def _insertion_sort():
    global barList
    global lengthList

    for i in range(len(lengthList)):
        indicator = lengthList[i]
        indicator_bar = barList[i]
        position = i

        while position > 0 and lengthList[position - 1] > indicator:
            lengthList[position] = lengthList[position - 1]
            barList[position], barList[position - 1] = barList[position - 1], barList[position]
            swap_two_position(barList[position], barList[position - 1])   # <-- updates the display
            yield                                       # <-- suspends the execution
            position -= 1                                    # <-- execution resumes here when next is called

        lengthList[position] = indicator
        barList[position] = indicator_bar
        swap_two_position(barList[position], indicator_bar)


worker = None    # <-- Not a thread in spite of the name.

def insertion_sort():     # <-- commands the start of both the animation, and the sort
    global worker
    worker = _insertion_sort()
    animate()


def animate():      # <-- commands resuming the sort once the display has been updated
                    # controls the pace of the animation
    global worker
    if worker is not None:
        try:
            next(worker)
            window.after(10, animate)    # <-- repeats until the sort is complete,
        except StopIteration:            # when the generator is exhausted
            worker = None
        finally:
            window.after_cancel(animate) # <-- stop the callbacks


def shuffle():
    global barList
    global lengthList
    canvas.delete('all')
    xstart = 5
    xend = 15
    barList = []
    lengthList = []

    for x in range(1, 60):
        randomY = random.randint(1, 390)
        x = canvas.create_rectangle(xstart, randomY, xend, 395, fill='green')
        barList.append(x)
        xstart += 10
        xend += 10

    for bar in barList:
        x = canvas.coords(bar)
        length = x[3] - x[1]
        lengthList.append(length)

    for i in range(len(lengthList)-1):
        if lengthList[i] == min(lengthList):
            canvas.itemconfig(barList[i], fill='red')
        elif lengthList[i] == max(lengthList):
            canvas.itemconfig(barList[i], fill='orange')


window = tkin.Tk()
window.title('Sorting')
window.geometry('600x500')
canvas = tkin.Canvas(window, width='600', height='400')
canvas.grid(column=0,row=0, columnspan = 50)

insert = tkin.Button(window, text='Insertion Sort', command=insertion_sort)
shuf = tkin.Button(window, text='Shuffle', command=shuffle)
insert.grid(column=1,row=1)
shuf.grid(column=0, row=1)

shuffle()
window.mainloop()
