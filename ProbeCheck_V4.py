# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 12:12:34 2022

@author: xiw
"""

# Title: Missing probes checker design version 4.0
# Contact: wxi@leegov.com
# Author: Wang Xi
# Last Updated: 10-07-2022

# Update notes: (1) only pick up 3-digit Bus number (2) remove text in stand-by list (3) remove '/' and ' / " from stand_by_list
# File Format: csv and folder


# Import libraries
import pandas as pd
import os
import math
import datetime
from datetime import datetime
from contextlib import redirect_stdout
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
from PIL import Image, ImageTk

# Setting working directory
# os.chdir(r'C:\Users\xiw\Desktop')
# os.getcwd()


def probechecker(Genfare_Prob_Summary, log_directory):
    
# export_name_ls = Genfare_Prob_Summary.split('\\') # export a text file in the end
# export_name = export_name_ls[-1]
    
    with open('Report.txt', 'w') as f:
        with redirect_stdout(f):

            # Read the Genfare report
            Gen_prob = pd.read_csv(Genfare_Prob_Summary, header=4)

            # Assign directory
            # iterate over files in that directory
            log_list = [] # empty list for log file names
            for filename in os.scandir(log_directory):
                if filename.is_file():
                    d = filename.path
                    d1 = d.split('\\')
                    log_list.append(d1[-1])

            def remove_suffix(input_string, suffix): # to remove '.0' from bus IDs when it happens
                if suffix and input_string.endswith(suffix):
                    return input_string[:-len(suffix)]
                return input_string

            # define a function to returns buses operated (need to be probed) in one day (one operation daily log)
            def bus_operated(log_file):

                date_ = log_file.split('.')
                log_date = date_[0]
                print('------Operation Log Date:', log_date)
                print()

                df_line_up = pd.read_excel(os.path.join(log_directory, log_file), sheet_name = 'Daily Line-Up')
                df_stand_by = pd.read_excel(os.path.join(log_directory, log_file), sheet_name = 'Stand-by', header = 1)

                # In the Daily Line Up tab
                end_row = df_line_up[df_line_up['ROUTE']=='PM / DOWN >'].index.values # find the index of 'PM / DOWN >', use it to indicate the last row of record

                list_bus_scheduled = df_line_up['BUS #'].tolist() # list of buses scheduled
                list_bus_scheduled = list_bus_scheduled[:int(end_row)] # use the end row index to cut off the rest of the list
                list_bus_scheduled = [str(item) for item in list_bus_scheduled] # convert number and text elements to text
                list_bus_scheduled = [x.strip(' ') for x in list_bus_scheduled] # delete accidental blank entries
                list_bus_scheduled = [x for x in list_bus_scheduled if x != 'nan'] # remove nan in the list
                
                              
                # check AM/PM shifts in one cell, for exmaple '932/508'
                remove_entries_hurr_ian = []
                for bus_hurr_ian in list_bus_scheduled:
                    if '/' in str(bus_hurr_ian):
                        s = bus_hurr_ian.split('/') # split the multiple entries
                        list_bus_scheduled = list_bus_scheduled + s
                        remove_entries_hurr_ian.append(bus_hurr_ian) # add to the buses to be removed from stand by list
                        
                for remove_entry_hurr_ian in remove_entries_hurr_ian:
                    list_bus_scheduled.remove(remove_entry_hurr_ian) # remove the clustered entries from raw stand by list
                
              
                
               

                
                list_bus_scheduled_1 = [] # remove '.0' from bus IDs
                for text in list_bus_scheduled:
                    int_text = remove_suffix(text, '.0')
                    list_bus_scheduled_1.append(int_text)
                list_bus_scheduled = list_bus_scheduled_1
                list_bus_scheduled = [int(item) for item in list_bus_scheduled]

            #     print('There are', len(list_bus_scheduled), 'buses found in list_bus_scheduled:', list_bus_scheduled) # print out the result

            #     list_bus_actual = df_line_up['Replaced with bus #'].tolist() # list of buses scheduled
                list_bus_actual = df_line_up.iloc[:,3].tolist() # list of bus that will replace the scheduled bus before the scheduled bus operates
                list_bus_actual = list_bus_actual[:int(end_row)] # use the end row index to cut off the rest of the list
                list_bus_actual = [str(item) for item in list_bus_actual] # convert number and text elements to text
                list_bus_actual = [x.strip(' ') for x in list_bus_actual] # delete accidental blank entries
                
                list_bus_actual_1 = [] # remove '.0' from bus IDs
                for text in list_bus_actual:
                    int_text = remove_suffix(text, '.0')
                    list_bus_actual_1.append(int_text)
                list_bus_actual = list_bus_actual_1
            #     print(list_bus_actual, len(list_bus_actual))


                # buses used due to broken down of another bus
                list_bus_swapwith = df_line_up.iloc[:,4].tolist() 
                list_bus_swapwith = list_bus_swapwith[:int(end_row)] # use the end row index to cut off the rest of the list
                list_bus_swapwith = [str(item) for item in list_bus_swapwith] # convert number and text elements to text
                list_bus_swapwith = [x.strip(' ') for x in list_bus_swapwith] # delete accidental blank entries 
                list_bus_swapwith = [ele for ele in list_bus_swapwith if ele.strip()] # delete accidental blank entries 
                list_bus_swapwith = [x for x in list_bus_swapwith if x != 'nan'] # remove nan in the list
                
                # remove hurricane Ian Driver's name on column index 4
                #for bus in list_bus_swapwith:
                    #if (str(bus)).isnumeric(): # if the bus ID is numeric
                        #list_bus_swapwith = [str(item) for item in list_bus_swapwith]
                
                # remove hurricane Ian Driver's name on column index 4
                list_bus_swapwith = [x for x in list_bus_swapwith if x[0].isdigit()]
               

                list_bus_swapwith_1 = [] # remove '.0' from bus IDs
                for text in list_bus_swapwith:
                    int_text = remove_suffix(text, '.0')
                    list_bus_swapwith_1.append(int_text)
                list_bus_swapwith = [int(item) for item in list_bus_swapwith_1]

                # The swapped bus could be swapped again with a another bus
                list_bus_swapwiths = df_line_up.iloc[:,7].tolist() # list of buses scheduled
                list_bus_swapwiths = list_bus_swapwiths[:int(end_row)] # use the end row index to cut off the rest of the list
                list_bus_swapwiths = [str(item) for item in list_bus_swapwiths] # convert number and text elements to text
                list_bus_swapwiths = [x.strip(' ') for x in list_bus_swapwiths] # delete accidental blank entries 
                list_bus_swapwiths = [ele for ele in list_bus_swapwiths if ele.strip()] # delete accidental blank entries 
                list_bus_swapwiths = [x for x in list_bus_swapwiths if x != 'nan'] # remove nan in the list

                list_bus_swapwiths_1 = [] # remove '.0' from bus IDs
                for text in list_bus_swapwiths:
                    int_text = remove_suffix(text, '.0')
                    list_bus_swapwiths_1.append(int_text)
                list_bus_swapwiths = [int(item) for item in list_bus_swapwiths_1]

                # The swapped bus could be swapped again with a another bus again
                list_bus_swapwithss = df_line_up.iloc[:,10].tolist() # list of buses scheduled
                list_bus_swapwithss = list_bus_swapwithss[:int(end_row)] # use the end row index to cut off the rest of the list
                list_bus_swapwithss = [str(item) for item in list_bus_swapwithss] # convert number and text elements to text
                list_bus_swapwithss = [x.strip(' ') for x in list_bus_swapwithss] # delete accidental blank entries 
                list_bus_swapwithss = [ele for ele in list_bus_swapwithss if ele.strip()] # delete accidental blank entries 
                list_bus_swapwithss = [x for x in list_bus_swapwithss if x != 'nan'] # remove nan in the list

                list_bus_swapwithss_1 = [] # remove '.0' from bus IDs
                for text in list_bus_swapwithss:
                    int_text = remove_suffix(text, '.0')
                    list_bus_swapwithss_1.append(int_text)
                list_bus_swapwithss = [int(item) for item in list_bus_swapwithss_1]

                list_bus_swapwith_all =  list_bus_swapwith + list_bus_swapwiths + list_bus_swapwithss # total buses send out to replaced broken down buses

                # print('There are', len(list_bus_swapwith_all), 'buses found in list_bus_replacedwith_all:', list_bus_swapwith_all) # print out the result

                multiple_entry_list= [] # sometimes there are multiple entries in one cell such as '932/508'
                raw_stand_by_list = df_stand_by['Bus No'].tolist() # convert the column to raw standing by list

                raw_stand_by_list = [str(item) for item in raw_stand_by_list] # convert number and text elements to text
            #     print(raw_stand_by_list)
                raw_stand_by_list = [x.strip(' ') for x in raw_stand_by_list] # delete accidental blank entries 
            #     print(raw_stand_by_list)
                raw_stand_by_list = [ele for ele in raw_stand_by_list if ele.strip()] # delete accidental blank entries 
            #     print(raw_stand_by_list)
                raw_stand_by_list = [x for x in raw_stand_by_list if x != 'nan'] # remove nan in the list
                
                raw_stand_by_list = [x for x in raw_stand_by_list if x[0].isdigit()] # remove text in the list
            #     print(raw_stand_by_list)
            

                remove_entries = []
                # process the raw standing by list

                # print(raw_stand_by_list)
                
                # check multiple in entries in one cell, for exmaple '929 / 433'(space btw) and '932/508'
                for bus in raw_stand_by_list:
                    if '/' in str(bus):
                        s1 = bus.split('/') # split the clustered entry, for example '932/508'
                        multiple_entry_list = multiple_entry_list + s1
                                
                        for bus_test in multiple_entry_list:
                            if ' ' in str(bus_test):
                                s2 = bus_test.split(' ')
                                multiple_entry_list.remove(bus_test)
                                multiple_entry_list = multiple_entry_list + s2
                                # raw_stand_by_list = raw_stand_by_list + bus.split("delimiter")
                                
                                multiple_entry_list.remove('')
                                # removing duplicated from the list using set()
                                multiple_entry_list = list(set(multiple_entry_list))
                        
                        # To get remove_entries
                        remove_entries.append(bus) # add to the buses to be removed from stand by list
    
                        
                # check multiple in entries in one cell, for exmaple 'Car-2008'
                for bus in raw_stand_by_list:
                    if '-' in str(bus):
                #         print(bus)
                        s = bus.split('-') # split the clustered entry
                #         print(s)
                        multiple_entry_list = multiple_entry_list + s
                        remove_entries.append(bus) # add to the buses to be removed from stand by list
                
                # check multiple in entries in one cell, for exmaple 'Car 2006'(space btw)
                # Update notes: since we remove letters from very beginning, so there is no 'car 2006' any more
                # for bus in raw_stand_by_list:
                    # if ' ' in str(bus):
                #         print(bus)
                        # s = bus.split(' ') # split the clustered entry
                #         print(s)
                        # multiple_entry_list = multiple_entry_list + s
                        # remove_entries.append(bus) # add to the buses to be removed from stand by list
                    
                                        
                # print('multiple', multiple_entry_list)
                # print('remove_entries', remove_entries)
                # print('raw',raw_stand_by_list)

                for remove_entry in remove_entries:
                    raw_stand_by_list.remove(remove_entry) # remove the clustered entries from raw stand by list

           
                raw_stand_by_list_1 = [] # remove '.0' from bus IDs
                for text in raw_stand_by_list:
                    int_text = remove_suffix(text, '.0')
                    raw_stand_by_list_1.append(int_text)

            #     print('raw',raw_stand_by_list)
                stand_by_list = [int(item) for item in raw_stand_by_list_1]

                # print(stand_by_list)

                stand_by_list = stand_by_list + multiple_entry_list # combine 
                # print(stand_by_list)

                # remove any text from the final standing by list before covert str to int
                sb_list = []
                for element in stand_by_list:
                    try:
                        sb_list.append(int(element))
                    except:
                        print('"', element, '" is not a valid Bus ID in Stand-by sheet.')

                stand_by_list = [int(item) for item in sb_list] # convert number and text elements to integer
                
                selected_elements = []
                for i in range(len(stand_by_list)):
                    if len(str(stand_by_list[i])) == 3:
                        selected_elements.append(stand_by_list[i])    
            #     print(stand_by_list)
            

                stand_by_list = list(set(selected_elements)) # remove duplicate and produce the final stand by bus list
                # print('Stand by buses:', stand_by_list)


                # Actually Operated Buses

                # find the index of actual operated buses
                for index, bus in enumerate(list_bus_actual):
            #         if math.isnan(bus) is False:
                    if (str(bus)).isnumeric(): # if the bus ID is numeric
                #         print(index, bus)
                        list_bus_scheduled[index] = list_bus_actual[index]  # replace the scheduled bus with actual bus

                list_bus_scheduled = [int(item) for item in list_bus_scheduled] # convert the float to int

            #     print(list_bus_scheduled, len(list_bus_scheduled))

                # add extra buses operated during the day due to actual operated buses broking down
                bus_extra = []
            #     print(list_bus_swapwith_all)
                for index, bus in enumerate(list_bus_swapwith_all):
                    if (str(bus)).isnumeric():
            #         if math.isnan(bus) is False:
                        bus_extra.append(bus)

                bus_extra = [int(item) for item in bus_extra] # convert the float to int

                # buses need probing

                bus_need_probe = list_bus_scheduled + bus_extra + stand_by_list
                bus_need_probe = list(set(bus_need_probe)) # remove duplicate buses

                print()
                print('Scheduled', len(list_bus_scheduled),'buses:', list_bus_scheduled)
                print()
                print('Stand-by buses:', len(stand_by_list), stand_by_list)
                print()
                print('Adding extra', len(bus_extra), 'buses due to issues:', bus_extra)
                print()
                print('Total operated', len(bus_need_probe), 'buses:', bus_need_probe)
                print()

                # find a time threshold to compare operated date time with data time in probing record
                # a lot of buses are wirelessly probed in the base in the early morning/late night
                # therefore if a bus is probed 4 AM when leaving the base on the day it operates, it does not count
                # currently we use 8 AM: Buses used should be probed after 8 AM.
                log_date_time = datetime.strptime(date_[0] + ' '+ '8:00', '%m-%d-%Y %H:%M') # 8:00 AM


                # find the start and end of the manual records
                IR_end = Gen_prob[Gen_prob['Location'].str.contains('Infrared Probing')].index[0]
                Gen_prob_IR = Gen_prob[0:IR_end]

                # find wifi probing
                Gen_prob2 = pd.read_csv(Genfare_Prob_Summary, header=IR_end + 3 + 4 )

                WIFI_end = Gen_prob2[Gen_prob2['Location'].str.contains('Wireless Probing')].index[0]
                Gen_prob_WIFI = Gen_prob2[0:WIFI_end]


                # check if the bus is probed after log_date_time
                summary_list_IR = []
                for busID in bus_need_probe: 
                    print('Bus ID', busID)

                    c = Gen_prob_IR[['Bus','Probe Time']][(Gen_prob_IR['Bus']==str(busID))] # find probing records of the bus
                    c_lst = c['Probe Time'].tolist() # convert the time column into a list
            #         print(c_lst)
                    c_lst.sort(key=lambda c_lst: datetime.strptime(c_lst, "%m/%d/%Y %H:%M:%S")) # sort time

                    try:
                        last_c = c_lst[-1]  # get the last probing records of the bus
                    except:
                        last_c = [] # if not such bus, last_c should be empty

                    if len(last_c) == 0:  # if bus number is not found in the probing records at all, it needs probing
                        s1 = '*** Bus # ' + str(busID) + ' needs IR probing to retrieve cash, not found in IR probing records.'
                        print(s1)
                        summary_list_IR.append(s1)

                    if len(last_c) != 0: # if bus is not probe after its operated date, it needs probing
                        last_probe_time = last_c
            #             print(last_probe_time)

                        try:
                            last_probe_time = datetime.strptime(last_probe_time, '%m/%d/%Y %H:%M:%S')
                        except:
                            last_probe_time = datetime.strptime(last_probe_time, '%m/%d/%Y %H:%M')

                        print('Operation Log time ', log_date_time)
                        print('Last probed time ', last_probe_time)
                        print()

                        if last_probe_time < log_date_time:
                            s2 = '*** Bus # ' + str(busID) + ' needs IR probing to retrieve cash, last probed on ' + str(last_probe_time)
                            print(s2)
                            summary_list_IR.append(s2)
                    print() 
                     
                    
                        
                        
                    

                Gen_prob_IRWF = pd.concat([Gen_prob_IR, Gen_prob_WIFI])

                summary_list_IRWF = []
                for busID in bus_need_probe:
                    print('Bus ID', busID)

                    c = Gen_prob_IRWF[['Bus','Probe Time']][(Gen_prob_IRWF['Bus']==str(busID))] # find probing records of the bus
                    c_lst = c['Probe Time'].tolist() # convert the time column into a list
                    c_lst.sort(key=lambda c_lst: datetime.strptime(c_lst, "%m/%d/%Y %H:%M:%S")) # sort time

                    try:
                        last_c = c_lst[-1]  # get the last probing records of the bus
                    except:
                        last_c = [] # if not such bus, last_c should be empty

                    if len(last_c) == 0:  # if bus number is not found in the probing records at all, it needs probing
                        s1 = '*** Bus # ' + str(busID) + ' needs IR or WIFI probing to get data, not found in IR or WIFI probing records.'
                        print(s1)
                        summary_list_IRWF.append(s1)

                    if len(last_c) != 0: # if bus is not probe after its operated date, it needs probing
                        last_probe_time = last_c
                        # print(last_probe_time)

                        try:
                            last_probe_time = datetime.strptime(last_probe_time, '%m/%d/%Y %H:%M:%S')
                        except:
                            last_probe_time = datetime.strptime(last_probe_time, '%m/%d/%Y %H:%M')

                        print('Operation Log time ', log_date_time)
                        print('Last probed time ', last_probe_time)
                        print()

                        if last_probe_time < log_date_time:
                            s2 = '*** Bus # ' + str(busID) + ' needs IR or WIFI probing to get data, last probed on ' + str(last_probe_time)
                            print(s2)
                            summary_list_IRWF.append(s2)
                    print()  

                return summary_list_IR, summary_list_IRWF

            # Check every operation log in the input folder
            final_IR = []
            final_IRWF = []
            for log_file in log_list:
                summary = bus_operated(log_file)
                final_IR = final_IR + summary[0]
                final_IRWF = final_IRWF + summary[1]
                print('********************************************************************************************')

            final_IR = list(set(final_IR))
            final_IRWF = list(set(final_IRWF))

            print('---------Summary IR------------:')
            for x in final_IR:
                print(x)
            print()
            print(len(final_IR), 'buses need IR probing to get cash.')
            print()

            print('---------Summary IR and WIFI------------:')
            for x in final_IRWF:
                print(x)
            print()
            print(len(final_IRWF), 'buses needs IR or WIFI probing to get data.')



# Processing image
# Resize bus logo
# logo = Image.open(r'C:\Users\xiw\Desktop\Probing GUI App Update\ico\red bus png.png')
# logo.size
# logo_resize = logo.resize((logo.width // 20, logo.height // 20))
# logo_resize.show()
# logo_resize.save("resized red bus png.png")

# Resize LeeTran logo
# logo = Image.open(r'C:\Users\xiw\Desktop\Probing GUI App Update\ico\leeTran logo.png')
# logo.size
# logo_resize = logo.resize((logo.width // 2, logo.height // 2)) # same as logo.reduce(2)
# logo_resize.show()
# logo_resize.save("resized LeeTran logo png.png")



# Set up GUI desktop app by using TKinter
window = tk.Tk()
entry1 = tk.StringVar()
entry2 = tk.StringVar()
path1 = []
path2 = []

# Set up windows background
canvas = tk.Canvas(window, width= 560, height = 350, bg="#5d8aa8")
canvas.pack(fill=tk.BOTH, expand=True)

# Set up GUI background
# logo = Image.open(r'C:\Users\xiw\Desktop\Probing GUI App Update\resized red bus png.png')
logo = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Probing GUI App Update\ico\resized LeeTran logo png.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo # cannot skip this line of code, it's necessary
logo_label.place(x = 50, y = 40)

logo1 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Probing GUI App Update\ico\cropped probing png.png')
logo1 = ImageTk.PhotoImage(logo1)
logo1_label = tk.Label(image=logo1)
logo1_label.image = logo1 # cannot skip this line of code, it's necessary
logo1_label.place(x = 180, y = 20)

# Define function
def check():
    probechecker(entry1.get(), entry2.get())


def addPath1():
    filename = filedialog.askopenfilename(initialdir='/', title="Select Probe Summary File Path", 
                                          filetypes=(("Probe Summary File Path", "*.csv"), ))
    path1.append(filename)
    print(filename)
    for path in path1:
        Label1 = tk.Label(window, text = path, bg='gray')
        E1.insert(0,filename)
        Label1.pack()

def addPath2():
    foldername = filedialog.askdirectory(initialdir='/', title="Select Operation Log Folder Path")
    path2.append(foldername)
    print(foldername)
    for path in path2:
        label2 = tk.Label(window, text = path, bg='gray')
        E2.insert(0,foldername)
        label2.pack()


window.title("ProbeChecker Version 4.0") 

B1 = tk.Button(window, text="Probe Summary File Path", command=addPath1, bg='White')
B1.pack()
B1.place(x = 10,y = 120)

E1 = tk.Entry(window, width=60, textvariable=entry1)
E1.place(x = 180,y = 120)

B2 = tk.Button(window, text="Operation Logs Folder Path", command=addPath2, bg='White')
B2.pack()
B2.place(x = 10,y = 160)

E2 = tk.Entry(window, width=60, textvariable=entry2)
E2.place(x = 180,y = 160)

B = tk.Button(window,text="Check Probe", fg="white", width=12, height=1, command=check, bg='#915c83')

# define button font
btnFont = font.Font(weight="bold",size=15)
B['font'] = btnFont
B.place(x = 180,y = 200)

# Instructions
instructions_det = tk.Label(window, text = " Instruction \n (1) click button \"Probe Summary File Path\" to select a probing csv file on your computer; \n (2) click button \"Operation Logs Folder Path\" to select a logs folder on your computer; \n (3) click button \"Check Probe\".", font="Raleway")
# define instruction details font
detFont = font.Font(size=10)
instructions_det['font'] = detFont
instructions_det.place(x = 20, y = 260)

# label for result
# result = tk.Label(window)

window.mainloop()

# convert py to exe
# auto-py-to-exe