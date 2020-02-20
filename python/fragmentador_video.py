#!/usr/bin/python3
#1******************************************************************************************************************************OK
# Code Information:

# Last review date: 06/15/2018
# Creation Date: 06/15/2018
# Programmer: Eng. John Betancourt G.  Para Francisco Carlos Calderon B
# Phone: (+57) 311 813 7206 
# Emails: calderonf@gmail.com; john.betancourt93@gmail.com 
# Video Classifier and splitter

#2******************************************************************************************************************************OK
# Inclusion of dependencies

import os
import time
import subprocess
import numpy as np
import datetime

from tkinter import filedialog
from tkinter import *

# To clear all previous console outputs
clear = lambda: os.system('cls')
clear()

#3******************************************************************************************************************************OK
# Declaration of global variables
sources_directory_list  = [] # List of video sources
results_directory_list  = [] # List of video results

#4******************************************************************************************************************************OK
def FFMPEG_get_Length_Video(input_video_absolute_path):

    """
    Execute a FFMPEG in Windows console and gets video duration

    Parameters
    ----------
    arg1 : input_video_absolute_path
        absolute path to video source

    Returns
    -------
        duration of video specified in absolute path 'input_video_absolute_path'

    """

    # cmd FFMPEG command to get video duration
    cmd = 'ffprobe -i "{}" -show_entries format=duration -v quiet -of csv="p=0"'.format(input_video_absolute_path)
    
    # Execute command to prompt
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=subprocess.STDOUT
    )

    # return round(float(output))  # ugly, but rounds your seconds up or down
    return float(output)

#5******************************************************************************************************************************OK
def FFMPEG_Merge_Video_Files(path, sources_list):

    """
    Execute a FFMPEG in Windows console to merge videos in only one result

    Parameters
    ----------
    arg1 : path
        absolute path video sources to merge

    arg2 : sources_list
        list of directories of video sources to merge

    Returns
    -------
    return1 : result_name
        result file name of merging videos

    return2 : results_path
        path where result is located

    """

    # file name to create .txt file to specified video sources to merge
    file_name   = "merge_sources_list.txt"

    # Result file name of Merging source list
    result_name = "merge_video_souces.avi"

    # Create results folder
    results_path=os.path.join(path, "results")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Open .txt file to write video sources to merge
    file = open(os.path.join(results_path,file_name),"w") 

    # loop through all items in sources list
    for i in range(0,len(sources_list)):
        aux_sources_list = sources_list[i]
        # Write in .txt file the absolute path to each video source
        file.write("file '"+os.path.join(path, aux_sources_list['File_Name'])+"'\n")

    # Close file
    file.close() 

    # print some process information
    print("\nMerge source list created at:",results_path,"\n\tas:"+file_name)

    # cmd FFMPEG command to merge videos specified in Merge source list
    # ffmpeg -f concat -safe 0 -i mylist.txt -c copy output
    cmd = 'ffmpeg -f concat -safe 0 -i "{}" -c copy "{}"'.format(os.path.join(results_path,file_name), os.path.join(results_path,result_name))

    # print some process information
    print("\nMerging video sources, please wait:\n\tFFMPEG Command:"+cmd)

    # Execute command to run prompt
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=subprocess.STDOUT)

    # print some process information
    print("\nsources merged successfully")

    # Remove .txt file 
    os.remove(os.path.join(results_path,file_name))

    # return the result's absolute path
    return result_name, results_path

#6******************************************************************************************************************************OK
def FFMPEG_Split_Video_Files_(absolute_path, video_source_name, split_duration, delete_source):

    """
    Execute a FFMPEG in Windows console to split videos in many results according to 'split_duration'

    Parameters
    ----------
    arg1 : absolute_path
        Absolute path to video source

    arg2 : video_source_name
        File name of video source

    arg3 : split_duration
        [int-seconds] time to split video source in many videos

    arg4 : delete_source
        [bool] to delete or not the video source after the process

    Returns
    -------
        NO returns

    """

    # cmd FFMPEG command to split video located at 'absolute_path'
    # ffmpeg -i input.mp4 -c copy -map 0 -segment_time tt -f segment output%03d.avi
    cmd = 'ffmpeg -i "{}" -c copy -map 0 -reset_timestamps 1 -segment_time "{}" -f segment "{}%04d.avi"'.format(os.path.join(absolute_path,video_source_name), 
                                                                                      str(split_duration), #[seconds]
                                                                                      os.path.join(absolute_path,"Output_"))

   # print some process information
    print("\nSplitting video source, please wait:\n\tFFMPEG Command:"+cmd)

    # Execute command
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=subprocess.STDOUT)

    # Remove video source
    if delete_source:
        os.remove(os.path.join(absolute_path,video_source_name))

    # print some process information
    print("\nSource splitted successfully")

#7******************************************************************************************************************************OK
def FFMPEG_Get_Video_FPS(input_video_absolute_path):

    """
    Execute a FFMPEG in Windows console to get video source FPS

    Parameters
    ----------
    arg1 : input_video_absolute_path
        absolute path where video is located + file name

    Returns
    -------
        value of FPS [float] of specified video source

    """

    # Check if the source exists or not
    if not os.path.exists(input_video_absolute_path):
        sys.stderr.write("ERROR: filename %r was not found!" % (input_video_absolute_path,))
        return -1         
    
    # cmd FFMPEG command to get videos FPS
    cmd = 'ffprobe "{}" -v 0 -select_streams v -print_format flat -show_entries stream=r_frame_rate'.format(input_video_absolute_path)

    # Execute command
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=subprocess.STDOUT)

    # process to denormalize the result
    fps = str(output).split('"')[1].split('/')

    # Return the result [float] FPS
    return np.round(int(fps[0])/int(fps[1]),2)

#8******************************************************************************************************************************OK
def rename_split_results(results_path, Camera_Name, video__Start_Time, YYYYMTDD):
  
    """
    Rename video results with a consecutive time name

    Parameters
    ----------
    arg1 : results_path
        path where video results are located

    arg2 : Camera_Name
        camera identifier

    arg3 : video__Start_Time
        first video source start time with format HHMMSS

    arg4 : YYYYMTDD
        arg YearMontDay of video sources

    Returns
    -------
        NO Returns

    """

    # print some process information
    print("\nRenaming sources")

    # Source index/ counter
    i=1

    # loop through all files in path
    dirlist=os.listdir(results_path)
    dirlist.sort()
    for image_file in dirlist:

        # take only file with .avi extension
        # This form already return file by file in name order 
        if image_file.endswith("avi"): 
            
            # Get video duration of current item list
            duration = FFMPEG_get_Length_Video(os.path.join(results_path, image_file))
            
            # Build new name for video result
            new_name = 'CAM{}_{}{}_{}.avi'.format(Camera_Name, YYYYMTDD, video__Start_Time, i)

            # Rename video results with new name
            os.rename(os.path.join(results_path, image_file), 
                      os.path.join(results_path, new_name  ))

            # Get part of name to next video result
            video__Start_Time = int(video__Start_Time[0:2])*3600+int(video__Start_Time[2:4])*60 + int(video__Start_Time[4:6])+ int(duration)
            video__Start_Time = time.strftime('%H:%M:%S', time.gmtime(video__Start_Time)).replace(':','')

            # Increment counter
            i=i+1

#9******************************************************************************************************************************OK
def get_videos_path():

    """
    open a GUI to select folder

    Parameters
    ----------
    No input arguments

    Returns
    -------
        return string of a folder chosen by user, function returns None for no selection

    """

    root = Tk()
    root.withdraw()

    # Open GUI to select folder
    folder_selected = filedialog.askdirectory(initialdir="/VideosSDM/ReportesAforosSDM/CARGA2019/", title = "Select a folder")

    # Return user selection
    if folder_selected == "":
        return None
    else:
        return folder_selected 

#10*****************************************************************************************************************************OK
def create_file_report(path, file_name, sources_list,EliminarInf15Min=False,Tolerance=30, MaxDuration=900):

    """
    Create a report of video results

    Parameters
    ----------
    arg1 : file_name
        report file name

    arg2 : path
        path to save report

    arg3 : sources_listath
        sources list to read and write its information in report
        
    Optional 
    
    arg4 : EliminarInf15Min
		Delete all files with a duration of less than MaxDuration-Tolerance seconds
		
    arg5 : Tolerance
		tolerance of the file to remove
		
    arg6 : MaxDuration
		Max duration allowed and also the minimum minus the tolerance if EliminarInf15Min is set

    Returns
    -------
        NO Returns 

    """
		
		
		
    # Open file to write
    file = open(os.path.join(path, file_name),"w") 
    
    # Write head report information 
    file.write("File_Name;Year;Month;Day;Start_Time;Duration;End_Time") 

    # loop through all items in sources list
    for i in range(0,len(sources_list)):
        # Write information to .txt file
        
		# delete files woth a lenght of less than 15 minutes
        if 	EliminarInf15Min:
            if ((int(sources_list[i]['Duration'])) <= MaxDuration-Tolerance):
                # Remove .txt file 
                print("Removiendo archivo: "+sources_list[i]['File_Name']+ " Ya que su duracion es "+str(int(sources_list[i]['Duration'])))
                os.remove(os.path.join(path,sources_list[i]['File_Name']))	
            else:
                file.write(str("\n"+sources_list[i]['File_Name']       +";"+ # File Name
                                    sources_list[i]['YYYY']            +";"+ # Year
                                    sources_list[i]['MT']              +";"+ # Month
                                    sources_list[i]['DD']              +";"+ # Day
                                    sources_list[i]['Start_Time']      +";"+ # Video Start Time in format HHMMSS
                                    sources_list[i]['Duration_HHMMSS'] +";"+ # Duration in format HHMMSS
                                    sources_list[i]['End_Time']))            # Video End Time in format HHMMSS
        else:
            file.write(str("\n"+sources_list[i]['File_Name']       +";"+ # File Name
                                sources_list[i]['YYYY']            +";"+ # Year
                                sources_list[i]['MT']              +";"+ # Month
                                sources_list[i]['DD']              +";"+ # Day
                                sources_list[i]['Start_Time']      +";"+ # Video Start Time in format HHMMSS
                                sources_list[i]['Duration_HHMMSS'] +";"+ # Duration in format HHMMSS
                                sources_list[i]['End_Time']))            # Video End Time in format HHMMSS
									

    # Close file
    file.close() 

    # print some process information
    print("\nReport created at:",path,"\n\tas:"+file_name)

#11*****************************************************************************************************************************OK
def validate_sources(directory_list, tolerance_time):

    """
    Validate if videos sources are consecutive in Year, Month, Day, and time (with tolerance range time)

    Parameters
    ----------
    arg1 : directory_list
        list with video sources information to be validate

    arg2 : tolerance_time
        maximum time permitted between each video

    Returns
    -------
        [bool] if videos sources are consecutive returns True, otherwise False

    """

    # loop through all items in directory
    for i in range(0,len(directory_list)-1):
    
        # 1- Check if year its equal in the current item and the next one
        if directory_list[i]['YYYY']!=directory_list[i+1]['YYYY']:
            print("Error: one or more video sources have no the same year, Thus sources are no consecutive")
            return False

        # 2- Check if year its equal in the current item and the next one
        if directory_list[i]['MT']!=directory_list[i+1]['MT']:
            print("Error: one or more video sources have no the same Month, Thus sources are no consecutive")
            return False

        # 3- Check if year its equal in the current item and the next one
        if directory_list[i]['DD']!=directory_list[i+1]['DD']:
            print("Error: one or more video sources have no the same Day, Thus sources are no consecutive")
            return False

        # 4- Check if time is consecutive with the current item and the next one

        h, m, s = directory_list[i]['End_Time'].split(':')
        time_1 = int(h) * 3600 + int(m) * 60 + int(s)
        
        h, m, s = directory_list[i+1]['Start_Time'].split(':')
        time_2 = int(h) * 3600 + int(m) * 60 + int(s)
        
        # Calculate the time difference in the current video source and the next one
        diff_time = time_2-time_1

        # Check the time difference in the current video source and the next one are in the range of 'tolerance_time'
        if(abs(diff_time)>tolerance_time):
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Error: one or more video sources are no consecutive, out of tolerance time")
            return False

    # If everything looks good
    return True

#12*****************************************************************************************************************************OK
def read_sources(selected_folder):
    
    """
    read .avi files at folder and return a list with each video information

    Parameters
    ----------
    arg1 : selected_folder
        absolute path where videos sources are located

    Returns
    -------
        return a list of videos sources directory

    """

    # Directory list to be returned
    directory_list=[]

    # if a folder was not selected, nothing to DO and quit
    if selected_folder == None:
        print("Error: No folder selected by user")
        return None

    # Print some information
    print("Selected folder:\n\t",selected_folder,"\n\nFiles with .avi extension:")

    # Source index/ counter
    i=1

    # loop through all files in path
    dirlist=os.listdir(selected_folder)
    dirlist.sort()
    for image_file in dirlist:

        # take only file with .avi extension
        # This form already return file by file in name order 
        if image_file.endswith("avi"): 

            print("\t",i,image_file)
            partial_info = image_file.split('_')

            # If file name is not supported, print some information and continue
            if len(partial_info) !=3:
                print("\t\tError: file name format no supported, source no included")
                continue

            # Split video's file name with a delimiter to get partial information 
            partial_information = image_file.split('_')
            
            # Get duration of video source
            duration=FFMPEG_get_Length_Video(os.path.join(selected_folder, image_file))

            # Get Frames per seconds of video source
            FPS = FFMPEG_Get_Video_FPS(os.path.join(selected_folder, image_file))

            # Get some time and date variables     
            Start_HHMMSS    = time.strftime('%H:%M:%S', time.gmtime(int(partial_information[1][12:14])+int(partial_information[1][10:12])*60+int(partial_information[1][8 :10])*3600))
            Duration_HHMMSS = time.strftime('%H:%M:%S', time.gmtime(duration))
            End_HHMMSS      = time.strftime('%H:%M:%S', time.gmtime(duration+int(partial_information[1][12:14])+int(partial_information[1][10:12])*60+int(partial_information[1][8 :10])*3600))

            # Add source to sources directory list
            directory_list.append({ 'File_Name'      :image_file,                               # File Name
                                    'path'           :selected_folder,                          # Path to file
                                    'Random_Number'  :partial_information[2].split('.')[0],     # Random number for file
                                    'FPS'            :FPS,                                      # Frames per second of video
                                    'Duration'       :duration,                                 # Seconds
                                    'Duration_HHMMSS':Duration_HHMMSS,                          # Duration in format HHMMSS
                                    'Start_Time'     :Start_HHMMSS,                             # Video Start Time in format HH:MM:SS
                                    'End_Time'       :End_HHMMSS,                               # Video End Time in format HH:MM:SS
                                    'Date'           :partial_information[1],                   # YYYYMMDDHHMMSS
                                    'Camera'         :partial_information[0].replace("CAM",""), # ID Camera 
                                    'YYYY'           :partial_information[1][  :4 ],            # Year
                                    'MT'             :partial_information[1][4 :6 ],            # Month
                                    'DD'             :partial_information[1][6 :8 ],            # Day
                                    'HH'             :partial_information[1][8 :10],            # Hour
                                    'MM'             :partial_information[1][10:12],            # Minute
                                    'SS'             :partial_information[1][12:14]})           # Second

            i=i+1
            
    # Return video sources information at specified path
    return directory_list

#13*****************************************************************************************************************************OK
# Main function - implementation example
if __name__ == '__main__':

    MaxDuration=900
    Tolerance=300
    # Set a timer to count the total process time
    process_time_start = time.time() 

    # Open a GUI to select folder
    path= get_videos_path()

    # Read .avi files at folder and return a list with each video information
    sources_directory_list = read_sources(path)
    
    # Create a report of video inputs
    create_file_report(path, "sources_report.csv", sources_directory_list)
    
    # Validate if videos sources are consecutive in Year, Month, Day, and time (with tolerance range time)
    validate_sources(sources_directory_list, Tolerance)

    # Execute a FFMPEG in Windows console to merge videos in only one result
    merged_videos_file_name, path_results = FFMPEG_Merge_Video_Files(path, sources_directory_list)
    
    # Execute a FFMPEG in Windows console to split videos in many results according to 'split_duration'
    FFMPEG_Split_Video_Files_(path_results, merged_videos_file_name, MaxDuration, True)

    # Print some process information
    print("\nVideo Results:")
    
    # Rename video results with a consecutive time name
    rename_split_results(path_results, 
                         sources_directory_list[0]['Camera'], 
                         sources_directory_list[0]['Start_Time'].replace(':',''), 
                         sources_directory_list[0]['YYYY']+
                         sources_directory_list[0]['MT']+
                         sources_directory_list[0]['DD'])

    # Read .avi files at folder and return a list with each video information (Now with video Results)
    results_directory_list = read_sources(path_results)

    # Create a report of video results
    create_file_report(path_results, "merge_video_sources_report.csv", results_directory_list, EliminarInf15Min=True)

    # Print and report the Total process time
    print("\nTotal process time -", time.strftime('%H:%M:%S',time.gmtime(int(time.time() - process_time_start))))
    
    # Wait for user confirmation
    input("Press Enter to continue...")
#******************************************************************************************************************************


   
