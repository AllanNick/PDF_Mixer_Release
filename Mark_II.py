from threading import Thread
import keyboard
import os
from PyPDF2 import PdfMerger
from time import sleep, time
import shutil
#import pyautogui

cwd = os.getcwd()
#files = ['a.txt','b.txt','c.txt','d.txt']
files = os.listdir()

timestamp = str(int(time()))
os.mkdir(timestamp)

for name in reversed(files):
    if name[-4:] != '.pdf':
        del files[files.index(name)]

merger = PdfMerger()
processing = 1

def queueing(origin_queue):
    step = 0
    selection = 0

    marks = []

    def step_control(var):
        nonlocal step
        draw_frame(step)
        if var == -1:
            if step > 0:
                step += var
        
        if var == 1:
            if step < 3-1:
                step += var
        draw_frame(step)
        
    def selection_control(var):
        global files
        nonlocal selection, step #step display only
        draw_frame(step)
        print(selection)
        max_ = len(files)

        if var == 1:
            if selection < max_-1:
                selection += var

        if var == -1:
            if selection > 0:
                selection += var
        draw_frame(step)

    def exchanger():
        nonlocal origin_queue, marks, step #step display only
        draw_frame(step)
        print(origin_queue,'->',end='')
        if len(marks) == 2:
            posi_1 = marks[0]
            posi_2 = marks[1]
            name_1 = origin_queue[posi_1]
            name_2 = origin_queue[posi_2]
            origin_queue[marks[0]] = name_2
            origin_queue[marks[1]] = name_1
        marks = []
        print(origin_queue)
        draw_frame(step)

    def mark_down():
        nonlocal marks
        nonlocal selection, step #step display only
        draw_frame(step)
        print('marked:',end='')
        if len(marks) < 2:
            marks.append(selection)
            print(selection)
        draw_frame(step)

    def cmd():
        print('commands:')
        print('  |_open explorer:open')
        print('  |_export file:output')
        command = input(':$>>')

    def save():
        global processing
        draw_frame(step)
        if step == 2:
            for file in files:
                if file[-4:]  == '.pdf':
                    merger.append(open(file, 'rb'))

            with open('combined.pdf','wb') as fout:
                merger.write(fout)
            #copy combined.pdf to timestamp:
            path_timestamp = os.path.join(cwd,timestamp)
            shutil.copy('combined.pdf',path_timestamp)
            #clean dir
            print('cleaning...')
            os.remove('combined.pdf')
            processing = 0
            print('combine should be done, program will exit')
#            pyautogui.hotkey('tab','delete')

            keyboard.press_and_release('tab+delete')
            sleep(0.1)
            
            sleep(10)
            exit()

    def open_explorer():
        global cwd, files
        nonlocal step
        if step == 0:
            os.system('explorer.exe %s'%(cwd))

            input('ENTER to continue>')

            files = os.listdir()

            for name in reversed(files):
                if name[-4:] != '.pdf':
                    del files[files.index(name)]

    def IO_Thrad():
        global processing
        while processing == 1:
            print('In thread')
            keyboard.add_hotkey('up',selection_control,args=(-1,))
            keyboard.add_hotkey('down',selection_control,args=(1,))
            keyboard.add_hotkey('[',step_control,args=(-1,))
            keyboard.add_hotkey(']',step_control,args=(1,))
            keyboard.add_hotkey('x',mark_down)
            keyboard.add_hotkey('/',exchanger)
            keyboard.add_hotkey('=',return_value)
            keyboard.add_hotkey('Enter',save)
            keyboard.add_hotkey('E',open_explorer)
            keyboard.wait('tab+delete')
            #print(step,selection)
        print('[INFO][Thread]IO_thread closed...')

    def return_value():
        global files
        nonlocal origin_queue, step
        files = origin_queue
        step = 2
        draw_frame(step)

    def draw_frame(step):
        #step = 1
        global cwd
        nonlocal marks
        nonlocal origin_queue
        print('\033c')

        print('PDF Mixer.')
        print('[C]Nick Software 2019-2023')
        print('---------Version:Mk.II_rev3--')

        if step == 0:
            print('''______            
import]adjust export''')
            print('''<-'[' or ']'-> to check step configs''')
            print('')
            print('current dir:>>%s'%(cwd))
            print('')
            print('''press 'E' to open explorer''')
            print('')
            print('then please copy the .pdf files in the window')
            #print('to input comand press ctrl+alt')


        if step == 1:
            print('''       ______            
import[adjust]export''')
            print('''<-'[' or ']'-> to check step configs''')
            print('')
            print('''use 'x' to sclect, use '/' to make adjust effect
two sclected files' position will be exchange
            ''')
            print('''press '=' to finish adjust''')
            j = 0
            for name in origin_queue:
                if j in marks:
                    print('*',end='')
                else:
                    print(' ',end='')
                
                if j == selection:
                    print('>',end='')
                else:
                    print(' ',end='')
                
                if len(name) < 15:
                    print(name)
                else:
                    print(name)
            #print('current select:%s'%(selection+1))
                j += 1

            
        if step == 2:
            print('''              ______            
import adjust[export''')
            print('''<-'[' or ']'-> to check step configs''')
            print('')
            print('this is EXPORT page')
            print('')
            print('when you finish adjust press Enter to export')
            print('file will be saved as combined.pdf')



    draw_frame(step)
    IO_Thrad()

queueing(files)
