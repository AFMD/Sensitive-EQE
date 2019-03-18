#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 11:59:40 2018

@author: jungbluth
"""

import time, math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import serial
import itertools
import os, sys
import tkinter as tk
from tkinter import filedialog
import xlrd

# for the gui
from PyQt5 import QtCore, QtGui, QtWidgets
import GUI_Analysis_template


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        
        QtWidgets.QMainWindow.__init__(self)
        
        # Set up the user interface from Designer
        
        self.ui = GUI_Analysis_template.Ui_MainWindow()
        self.ui.setupUi(self)         

        # Tkinter
        
        root = tk.Tk()
        root.withdraw()
        
        # Create lists for reference / data files

        self.ref_1 = []
        self.ref_2 = []
        self.ref_3 = []
        self.ref_4 = []
        self.ref_5 = []
        
        self.data_1 = []
        self.data_2 = []
        self.data_3 = []
        self.data_4 = []
        self.data_5 = []
        
        # Handle Browse Buttons
        
        self.ui.browseButton_1.clicked.connect(self.writeText_1)
        self.ui.browseButton_2.clicked.connect(self.writeText_2)
        self.ui.browseButton_3.clicked.connect(self.writeText_3)        
        self.ui.browseButton_4.clicked.connect(self.writeText_4)       
        self.ui.browseButton_5.clicked.connect(self.writeText_5)        
        self.ui.browseButton_6.clicked.connect(self.writeText_6)        
        self.ui.browseButton_7.clicked.connect(self.writeText_7)        
        self.ui.browseButton_8.clicked.connect(self.writeText_8)        
        self.ui.browseButton_9.clicked.connect(self.writeText_9)  
        self.ui.browseButton_10.clicked.connect(self.writeText_10)
        
        # Handle Calculate Buttons
        
        self.ui.calculateButton_1.clicked.connect(lambda: self.pre_EQE(1, 0))
        self.ui.calculateButton_2.clicked.connect(lambda: self.pre_EQE(2, 0))
        self.ui.calculateButton_3.clicked.connect(lambda: self.pre_EQE(3, 0))
        self.ui.calculateButton_4.clicked.connect(lambda: self.pre_EQE(4, 0))
        self.ui.calculateButton_5.clicked.connect(lambda: self.pre_EQE(5, 0))
        
        # Handle Export Buttons
        
        self.ui.exportButton_1.clicked.connect(lambda: self.pre_EQE(1, 1))
        self.ui.exportButton_2.clicked.connect(lambda: self.pre_EQE(2, 1))
        self.ui.exportButton_3.clicked.connect(lambda: self.pre_EQE(3, 1))
        self.ui.exportButton_4.clicked.connect(lambda: self.pre_EQE(4, 1))
        self.ui.exportButton_5.clicked.connect(lambda: self.pre_EQE(5, 1))
        
        # Handle Clear Plot Button
        
        self.ui.clearButton.clicked.connect(self.clear_plot)
        
        # Handle Export All Data Button
        
        self.ui.exportButton_All.clicked.connect(self.export_All)
        
        # Data directory
        
        self.data_dir = '/home/jungbluth/Desktop/EQE Control Software/sEQE Data'

        # Import photodiode calibration files

        Si_file = pd.ExcelFile("FDS100-CAL.xlsx") # The files are in the sEQE Analysis folder
#        print(Si_file.sheet_names)
        self.Si_cal = Si_file.parse('Sheet1')
#        print(self.Si_cal)
        
        InGaAs_file = pd.ExcelFile("FGA21-CAL.xlsx")
        self.InGaAs_cal = InGaAs_file.parse('Sheet1')
        

        # Define variables        
        
        self.h = 6.626 * math.pow(10,-34) # [m^2 kg/s]
        self.c = 2.998 * math.pow(10,8) # [m/s]
        self.q = 1.602 * math.pow(10,-19) # [C]
        
        # To save the data
        
        self.save = False
        self.do_plot = True


# -----------------------------------------------------------------------------------------------------------        

    #### Functions to read in file and update text box

# -----------------------------------------------------------------------------------------------------------

    ### Functions for reference files
        
    def writeText_1(self):        
        self.change_dir(self.data_dir) # Change directory before opening file selector
        file_ = filedialog.askopenfilename()        
        if len(file_) != 0: # Check if a (non-empty) file has been imported
            self.path_1, self.filename_1 = os.path.split(file_)
            print("Path : ", self.path_1)
            print("Filename : ", self.filename_1)                     
            self.ui.textBox_1.clear() # Clear the text box in case sth has been uploaded already
            self.ui.textBox_1.insertPlainText(self.filename_1) # Insert filename into text box
            self.ref_1 = pd.DataFrame.from_csv(file_) # Turn file into dataFrame        
#            print(self.ref_1)
#            print(len(self.ref_1)) 
        
     
    def writeText_3(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()        
        if len(file_) != 0:
            self.path_3, self.filename_3 = os.path.split(file_)                             
            self.ui.textBox_3.clear()  
            self.ui.textBox_3.insertPlainText(self.filename_3)
            self.ref_2 = pd.DataFrame.from_csv(file_) 

   
    def writeText_5(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()       
        if len(file_) != 0:
            self.path_5, self.filename_5 = os.path.split(file_)                            
            self.ui.textBox_5.clear()  
            self.ui.textBox_5.insertPlainText(self.filename_5)
            self.ref_3 = pd.DataFrame.from_csv(file_)  

        
    def writeText_7(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()        
        if len(file_) != 0:
            self.path_7, self.filename_7 = os.path.split(file_)                             
            self.ui.textBox_7.clear()  
            self.ui.textBox_7.insertPlainText(self.filename_7)
            self.ref_4 = pd.DataFrame.from_csv(file_) 


    def writeText_9(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()       
        if len(file_) != 0:
            self.path_9, self.filename_9 = os.path.split(file_)                            
            self.ui.textBox_9.clear()  
            self.ui.textBox_9.insertPlainText(self.filename_9)
            self.ref_5 = pd.DataFrame.from_csv(file_)  

    
    ### Functions for data files


    def writeText_2(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()       
        if len(file_) != 0:
            self.path_2, self.filename_2 = os.path.split(file_)                  
            self.ui.textBox_2.clear()  
            self.ui.textBox_2.insertPlainText(self.filename_2)
            self.data_1 = pd.DataFrame.from_csv(file_) 

        
    def writeText_4(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()       
        if len(file_) != 0:
            self.path_4, self.filename_4 = os.path.split(file_)                             
            self.ui.textBox_4.clear()  
            self.ui.textBox_4.insertPlainText(self.filename_4)
            self.data_2 = pd.DataFrame.from_csv(file_) 
        
        
    def writeText_6(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()       
        if len(file_) != 0:
            self.path_6, self.filename_6 = os.path.split(file_)                            
            self.ui.textBox_6.clear()  
            self.ui.textBox_6.insertPlainText(self.filename_6)
            self.data_3 = pd.DataFrame.from_csv(file_)  
        
        
    def writeText_8(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()      
        if len(file_) != 0:
            self.path_8, self.filename_8 = os.path.split(file_)                            
            self.ui.textBox_8.clear()  
            self.ui.textBox_8.insertPlainText(self.filename_8)
            self.data_4 = pd.DataFrame.from_csv(file_)  
       
       
    def writeText_10(self):
        self.change_dir(self.data_dir)
        file_ = filedialog.askopenfilename()        
        if len(file_) != 0:
            self.path_10, self.filename_10 = os.path.split(file_)                          
            self.ui.textBox_10.clear()  
            self.ui.textBox_10.insertPlainText(self.filename_10)
            self.data_5 = pd.DataFrame.from_csv(file_) 

# -----------------------------------------------------------------------------------------------------------        

    #### Functions to calculate EQE

# -----------------------------------------------------------------------------------------------------------
  
    ### Function to select data and reference file   
  
    def pre_EQE(self, number, save_num):
        if save_num == 1:
            self.save = True
            
        if number == 1:
            startNM1 = self.ui.startNM_1.value() # Pick start wavelength
            stopNM1 = self.ui.stopNM_1.value() # Pick stop wavelength
            if len(self.ref_1) != 0 and len(self.data_1) != 0: # Check if (non-empty) refence / data files have been imported
                self.calculateEQE(self.ref_1, self.data_1, startNM1, stopNM1, 0)
            elif len(self.ref_1) == 0 and len(self.data_1) != 0: 
                print('Please import a valid reference file.') # Prompt to import a valid reference file
            elif len(self.ref_1) != 0 and len(self.data_1) == 0:
                print('Please import a valid data file.') # Prompt to import a valid data file
            else:
                print('Please import valid reference and data files.')  # Prompt to import valid reference and data files
                
        elif number == 2:
            startNM2 = self.ui.startNM_2.value()
            stopNM2 = self.ui.stopNM_2.value()
            if len(self.ref_2) != 0 and len(self.data_2) != 0:
                self.calculateEQE(self.ref_2, self.data_2, startNM2, stopNM2, 0)
            elif len(self.ref_2) == 0 and len(self.data_2) != 0: 
                print('Please import a valid reference file.') 
            elif len(self.ref_2) != 0 and len(self.data_2) == 0:
                print('Please import a valid data file.') 
            else:
                print('Please import valid reference and data files.')  
                
        elif number == 3:
            startNM3 = self.ui.startNM_3.value()
            stopNM3 = self.ui.stopNM_3.value()
            if len(self.ref_3) != 0 and len(self.data_3) != 0:
                self.calculateEQE(self.ref_3, self.data_3, startNM3, stopNM3, 0)
            elif len(self.ref_3) == 0 and len(self.data_3) != 0: 
                print('Please import a valid reference file.') 
            elif len(self.ref_3) != 0 and len(self.data_3) == 0:
                print('Please import a valid data file.') 
            else:
                print('Please import valid reference and data files.')  
                
        elif number == 4:
            startNM4 = self.ui.startNM_4.value()
            stopNM4 = self.ui.stopNM_4.value()
            if len(self.ref_4) != 0 and len(self.data_4) != 0:
                self.calculateEQE(self.ref_4, self.data_4, startNM4, stopNM4, 0)
            elif len(self.ref_4) == 0 and len(self.data_4) != 0: 
                print('Please import a valid reference file.') 
            elif len(self.ref_4) != 0 and len(self.data_4) == 0:
                print('Please import a valid data file.') 
            else:
                print('Please import valid reference and data files.')  
                
        elif number == 5:
            startNM5 = self.ui.startNM_5.value()
            stopNM5 = self.ui.stopNM_5.value()
            if len(self.ref_5) != 0 and len(self.data_5) != 0:
                self.calculateEQE(self.ref_5, self.data_5, startNM5, stopNM5, 0)
            elif len(self.ref_5) == 0 and len(self.data_5) != 0: 
                print('Please import a valid reference file.') 
            elif len(self.ref_5) != 0 and len(self.data_5) == 0:
                print('Please import a valid data file.') 
            else:
                print('Please import valid reference and data files.')  
                
        else:
            print("Error Code 1: Wrong number")
            
# -----------------------------------------------------------------------------------------------------------  
    def export_All(self):
        
        Wave_1 = []
        Wave_2 = []
        Wave_3 = []
        Wave_4 = []
        Wave_5 = []
        
        Energy_1 = []
        Energy_2 = []
        Energy_3 = []
        Energy_4 = []
        Energy_5 = []
        
        EQE_1 = []
        EQE_2 = []
        EQE_3 = []
        EQE_4 = []
        EQE_5 = []
        
        log_EQE_1 = []
        log_EQE_2 = []
        log_EQE_3 = [] 
        log_EQE_4 = []
        log_EQE_5 = []
        
   
        
        
        if len(self.ref_1) != 0 and len(self.data_1) != 0:
            startNM1 = self.ui.startNM_1.value() # Pick start wavelength
            stopNM1 = self.ui.stopNM_1.value() # Pick stop wavelength
            Wave_1, Energy_1, EQE_1, log_EQE_1 = self.calculateEQE(self.ref_1, self.data_1, startNM1, stopNM1, 1)
            if len(Wave_1) != 0:
                EQE_data_All = pd.DataFrame({'1.1 - Wavelength': Wave_1, '1.2 - Energy': Energy_1, '1.3 - EQE': EQE_1, '1.4 - Log EQE': log_EQE_1}) # Turn into dataFrame, the numbers are needed to organize the columns                              
            
        if len(self.ref_2) != 0 and len(self.data_2) != 0:
            startNM2 = self.ui.startNM_2.value() # Pick start wavelength
            stopNM2 = self.ui.stopNM_2.value() # Pick stop wavelength
            Wave_2, Energy_2, EQE_2, log_EQE_2 = self.calculateEQE(self.ref_2, self.data_2, startNM2, stopNM2, 1)       
            if len(Wave_2) != 0:
                EQE_data_All = pd.DataFrame({'2.1 - Wavelength': Wave_2, '2.2 - Energy': Energy_2, '2.3 - EQE': EQE_2, '2.4 - Log EQE': log_EQE_2}) # Turn into dataFrame, the numbers are needed to organize the columns                              
            
        if len(self.ref_3) != 0 and len(self.data_3) != 0:
            startNM3 = self.ui.startNM_3.value() # Pick start wavelength
            stopNM3 = self.ui.stopNM_3.value() # Pick stop wavelength
            Wave_3, Energy_3, EQE_3, log_EQE_3 = self.calculateEQE(self.ref_3, self.data_3, startNM3, stopNM3, 1)
            if len(Wave_3) != 0:
                EQE_data_All = pd.DataFrame({'3.1 - Wavelength': Wave_3, '3.2 - Energy': Energy_3, '3.3 - EQE': EQE_3, '3.4 - Log EQE': log_EQE_3}) # Turn into dataFrame, the numbers are needed to organize the columns                                   
            
        if len(self.ref_4) != 0 and len(self.data_4) != 0:
            startNM4 = self.ui.startNM_4.value() # Pick start wavelength
            stopNM4 = self.ui.stopNM_4.value() # Pick stop wavelength
            Wave_4, Energy_4, EQE_4, log_EQE_4 = self.calculateEQE(self.ref_4, self.data_4, startNM4, stopNM4, 1)            
            if len(Wave_4) != 0:
                EQE_data_All = pd.DataFrame({'4.1 - Wavelength': Wave_4, '4.2 - Energy': Energy_4, '4.3 - EQE': EQE_4, '4.4 - Log EQE': log_EQE_4}) # Turn into dataFrame, the numbers are needed to organize the columns                              

            
        if len(self.ref_5) != 0 and len(self.data_5) != 0:
            startNM5 = self.ui.startNM_5.value() # Pick start wavelength
            stopNM5 = self.ui.stopNM_5.value() # Pick stop wavelength
            Wave_5, Energy_5, EQE_5, log_EQE_5 = self.calculateEQE(self.ref_5, self.data_5, startNM5, stopNM5, 1)
            if len(Wave_5) != 0:
                EQE_data_All = pd.DataFrame({'5.1 - Wavelength': Wave_5, '5.2 - Energy': Energy_5, '5.3 - EQE': EQE_5, '5.4 - Log EQE': log_EQE_5}) # Turn into dataFrame, the numbers are needed to organize the columns                              
                          
            
        EQEfile_All = filedialog.asksaveasfilename() # Prompt the user to pick a folder / name to save data to 
        EQEfile_path_All, EQEfile_filename_All = os.path.split(EQEfile_All)   
        if len(EQEfile_path_All) != 0: # Check if the user actually selected a path
            self.change_dir(EQEfile_path_All) # Change the working directory
            EQE_data_All.to_csv(EQEfile_filename_All) # Save the data to a csv
            print('Saving data to: %s' % str(EQEfile_All))                       
        self.change_dir(self.data_dir) # Change the directory back          
            
            
            
# -----------------------------------------------------------------------------------------------------------  

    ### Function to calculate EQE
  
    def calculateEQE (self, ref_df, data_df, startNM, stopNM, export_num):
        
        power = self.calculatePower(ref_df) ### GET RID OF THIS ONCE THE Calculate Power FUNCTION HAS BEEN IMPLEMENTED IN sEQE.py               
        
        power_dict = {}    

        Wavelength = []  
        Energy = []                  
        EQE = []
        log_EQE = []
        
        
        for x in range(len(ref_df['Wavelength'])): # Iterate through columns of reference file
            power_dict[ref_df['Wavelength'][x]] = ref_df['Power'][x] # Add wavelength and corresponding power to dictionary
        
        if startNM >= data_df['Wavelength'][0] and stopNM <= data_df['Wavelength'][int(len(data_df['Wavelength']))-1]: # Check if the start and stop wavelength fit with data file
            if startNM >= ref_df['Wavelength'][0] and stopNM <= ref_df['Wavelength'][int(len(ref_df['Wavelength']))-1]: # Check if the start and stop wavelength fit with reference file
                
                for y in range(len(data_df['Wavelength'])): # Iterate through columns of data file
                    if startNM <= data_df['Wavelength'][y] <= stopNM: # Calculate EQE only if start <= wavelength <= stop, otherwise, ignore
#                        print(data_df['Wavelength'][y])
                        if data_df['Wavelength'][y] in power_dict.keys():  # Check if data wavelength is in reference file      
                            Wavelength.append(data_df['Wavelength'][y])
                            Energy_val = (self.h * self.c) / (data_df['Wavelength'][y] * math.pow(10,-9) * self.q) # Caluclate energy
                            Energy.append(Energy_val)
                            EQE_val = ((100 * data_df['Mean Current'][y] * self.h * self.c) / (data_df['Wavelength'][y] * math.pow(10,-9) * power_dict[data_df['Wavelength'][y]] * self.q)) # * 100 to turn into percent 
                            EQE.append(EQE_val)  
                            log_EQE.append(math.log10(EQE_val))
                        else: # If data wavelength is not in reference file
                            Wavelength.append(data_df['Wavelength'][y])
                            Energy_val = (self.h * self.c) / (data_df['Wavelength'][y] * math.pow(10,-9) * self.q)
                            Energy.append(Energy_val)
                            Power_int = self.interpolate(data_df['Wavelength'][y], ref_df['Wavelength'], ref_df['Power']) # Interpolate power
                            EQE_int = ((100 * data_df['Mean Current'][y] * self.h * self.c) / (data_df['Wavelength'][y] * math.pow(10,-9) * Power_int * self.q)) # * 100 to turn into percent 
                            EQE.append(EQE_int)
                            log_EQE.append(math.log10(EQE_int))
                            
                if len(Wavelength) == len(EQE) and len(Energy) == len(log_EQE): # Check if the lists have the same length
                    EQE_data = pd.DataFrame({'1 - Wavelength': Wavelength, '2 - Energy': Energy, '3 - EQE': EQE, '4 - Log EQE': log_EQE}) # Turn into dataFrame, the numbers are needed to organize the columns                  
#                    print(EQE_data)
                    
                    if export_num == 0: # To export one data file / plot the graphs                    
                        if self.save: # If the "Export Data" button has been clicked
                            EQEfile_ = filedialog.asksaveasfilename() # Prompt the user to pick a folder / name to save data to 
                            EQEfile_path, EQEfile_filename = os.path.split(EQEfile_)   
                            if len(EQEfile_path) != 0: # Check if the user actually selected a path
                                self.change_dir(EQEfile_path) # Change the working directory
                                EQE_data.to_csv(EQEfile_filename) # Save the data to a csv
                                print('Saving data to: %s' % str(EQEfile_))                       
                            self.change_dir(self.data_dir) # Change the directory back
                            self.save = False
                            
                        else: # If the "Calculate EQE" button has been clicked
                            if self.do_plot: # This is set to true during setup of the program                       
                                self.set_up_plot()
                                self.do_plot = False # Set self.do_plot to False to plot on the same graph
                            self.ax1.plot(Wavelength, EQE, linewidth = 5) # color = '#000000'
                            self.ax2.plot(Wavelength, log_EQE, linewidth = 5) # color = '#000000'
                            plt.draw()
                        
                    elif export_num == 1:
                        return (Wavelength, Energy, EQE, log_EQE)  
                   
                else:
                    print('Error Code 2: Length mismatch.')                   
                      
            else:
                print('Please select a valid wavelength range or import a different reference file.') # Prompt to select a valid wavelength range for reference file
                
        elif startNM < data_df['Wavelength'][0] and stopNM <= data_df['Wavelength'][int(len(data_df['Wavelength']))-1]: # 
            print('Please select a valid start wavelength.') # Prompt to select a valid start wavelength that is included in data file
            
        elif startNM >= data_df['Wavelength'][0] and stopNM > data_df['Wavelength'][int(len(data_df['Wavelength']))-1]:
            print('Please select a valid stop wavelength.') # Prompt to select a valid stop wavelength that is included in data file
            
        else:
            print('Please select a valid wavelength range.') # Prompt to select a valid wavelength range that is included in data file


    ### Function to calculate power ### MOVE THIS INTO sEQE PROGRAM

    def calculatePower(self, ref_df): ### FIX TO INCORPOARTE InGaAs FILE (already corrected in sEQE.py)
        
        cal_wave_dict = {} # Create an empty dictionary
        power = [] # Create an empty list
        
#        interpl= interp1d(self.Si_cal['Wavelength [nm]'], self.Si_cal['Responsivity [A/W]'])
            
        for x in range(len(self.Si_cal['Wavelength [nm]'])): # Iterate through columns of calibration file
            cal_wave_dict[self.Si_cal['Wavelength [nm]'][x]] = self.Si_cal['Responsivity [A/W]'][x] # Add wavelength and corresponding responsivity to dictionary

        for y in range(len(ref_df['Wavelength'])): # Iterate through columns of reference file
#            print(ref_df['Wavelength'][y])
            if ref_df['Wavelength'][y] in cal_wave_dict.keys(): # Check if reference wavelength is in calibraton file
                power.append(float(ref_df['Mean Current'][y]) / float(cal_wave_dict[ref_df['Wavelength'][y]])) # Add power to the list
            else: # If reference wavelength is not in calibration file
                resp_int = self.interpolate(ref_df['Wavelength'][y], self.Si_cal['Wavelength [nm]'], self.Si_cal['Responsivity [A/W]']) # Interpolate responsivity
#                resp_int = interpl(ref_df['Wavelength'][y])
                power.append(float(ref_df['Mean Current'][y]) / float(resp_int)) # Add power to the list
                
                
        ref_df['Power'] = power # Create new column in reference file
#        print(ref_df['Power']) 
            
        ref_df.to_csv('Sample_data.csv') # Turn dataFrame into .csv ### CHANGE THIS ONCE INCORPORATED INTO sEQE FILE
        
        return ref_df['Power']
           

    ### Function to interpolate values    
        
    def interpolate(self, num, x, y):
        f = interp1d(x, y)
        return f(num)
        
        

        
# -----------------------------------------------------------------------------------------------------------         
               
            
    def set_up_plot(self):                

        style.use('ggplot')
        fig1 = plt.figure()
                    
        self.ax1 = fig1.add_subplot(2,1,1)
#        plt.xlabel('Time (s)', fontsize=17, fontweight='medium')
        plt.ylabel('EQE', fontsize=17, fontweight='medium')              
        plt.grid(True)
#        plt.box()
        plt.title('EQE vs. Wavelength', fontsize=17, fontweight='medium')
        plt.tick_params(labelsize=14)
        plt.minorticks_on()
        plt.rcParams['figure.facecolor']='xkcd:white'
        plt.rcParams['figure.edgecolor']='xkcd:white'
        plt.tick_params(labelsize=15, direction='in', axis='both', which='major', length=8, width=2)
        plt.tick_params(labelsize=15, direction='in', axis='both', which='minor', length=4, width=2)

        self.ax2 = fig1.add_subplot(2,1,2)
        plt.xlabel('Wavelength (nm)', fontsize=17, fontweight='medium')
        plt.ylabel('Log(EQE)', fontsize=17, fontweight='medium')              
        plt.grid(True)
#        plt.box()
        plt.tick_params(labelsize=14)
        plt.minorticks_on()
        plt.rcParams['figure.facecolor']='xkcd:white'
        plt.rcParams['figure.edgecolor']='xkcd:white'
        plt.tick_params(labelsize=15, direction='in', axis='both', which='major', length=8, width=2)
        plt.tick_params(labelsize=15, direction='in', axis='both', which='minor', length=4, width=2)
        
#        plt.rcParams['font.family']='sans-serif'
#        plt.rcParams['font.sans-serif']='Times'
#        plt.xlim(0,3)      
#        plt.axis([tdata[0],tdata[-1],0.99*e,1.01*e]) 
        
        plt.show()
        
        
    def clear_plot(self):
        plt.close() # Close the current plot
        self.set_up_plot() # Set up a new plot, this is preferred over plt.clf() in case the plot window was closed
#        self.do_plot = True        
        
# -----------------------------------------------------------------------------------------------------------         
   
    def change_dir(self, directory):
        os.chdir(directory)  
           
# -----------------------------------------------------------------------------------------------------------         
   
    def naming(self, file_name, path_name, num): # Not currently being used
        
        name = os.path.join(path_name, file_name)
#        print('Naming: ', name)
        exists = os.path.exists(name)
        
        if exists:
#            print('Exists: yes')
            if num ==2:
                filename = file_name + '_%d' % num
            else:
                filename = file_name[:-1] + str(num)
#            print('New filename: ', filename)
            num += 1
#            print(num)
            self.naming(filename, path_name, num)
        else:
#            print('Exists: no')
#            print('Final finalname: ', file_name)
            return file_name


# -----------------------------------------------------------------------------------------------------------        
        
def main():

  app = QtWidgets.QApplication(sys.argv)
  monoUI = MainWindow()
  monoUI.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()



