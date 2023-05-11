# Developed by: Ariana Feng
# Date: March 28, 2023
# Desc: A Health Information System program. The system reads patient data from a plain-text file seperated by commas.
#       New patient data can be added and data can be deleted. Information includes: Patient ID, date of visit, body
#       temperature, heart rate (beats per minute), respiratory rate (breaths per minute), systolic blood
#       pressure (mmHg), diastolic blood pressure(mmHg), and oxygen saturation. There are 8 options from main menu.
# Inputs: Main menu choice, patient ID, new patient stats, date for finding visits by date.
# Outputs: Patient details and errors if there are any.


from typing import List, Dict, Optional
import re

def readPatientsFromFile(fileName):
    """
    Reads patient data from a plaintext file.

    fileName: The name of the file to read patient data from.
    Returns a dictionary of patient IDs, where each patient has a list of visits.
    The dictionary has the following structure:
    {
        patientId (int): [
            [date (str), temperature (float), heart rate (int), respiratory rate (int), systolic blood pressure (int), diastolic blood pressure (int), oxygen saturation (int)],
            [date (str), temperature (float), heart rate (int), respiratory rate (int), systolic blood pressure (int), diastolic blood pressure (int), oxygen saturation (int)],
            ...
        ],
        patientId (int): [
            [date (str), temperature (float), heart rate (int), respiratory rate (int), systolic blood pressure (int), diastolic blood pressure (int), oxygen saturation (int)],
            ...
        ],
        ...
    }
    """
#creating an empty dictionary
    patients={}
    try:
        # Open a file for reading
        infile = open(fileName, 'r')
        lines = infile.readlines()
        try:
            for line in lines:
                patientDataList = line.strip().split(",")       #take away the blank spaces and splitting by commas
                patientId = patientDataList[0]
                if len(patientDataList) == 8:                #makes sure there are 8 elements in the patient data list

                    try:
                        patientId = int(patientId)
                        patientDataList.pop(0)              #'pop'(remove) the first element which will be key for dictionary
                        patientDataList[1] = float(patientDataList[1])
                        for i in range(2, 7):      #values from temp to oxy saturation has to be an integer hence for loop is from 2 to 7
                            patientDataList[i] = int(patientDataList[i])
                        #try and except block raises error if data is not within range
                        try:
                            if not(35.0 <= patientDataList[1] <= 42.0):
                                raise ValueError(f"Invalid temperature value ({patientDataList[1]}) in line: {line}")
                            if not(30<=patientDataList[2]<=180):
                                raise ValueError(f"Invalid heart rate value ({patientDataList[2]}) in line: {line}")
                            if not(5<=patientDataList[3]<=40):
                                raise ValueError(f"Invalid respiratory rate ({patientDataList[3]}) in line: {line}")
                            if not(70 <= patientDataList[4] <= 200):
                                raise ValueError(f"Invalid systolic blood pressure value ({patientDataList[4]}) in line: {line}")
                            if not(40<=patientDataList[5]<=120):
                                raise ValueError(f"Invalid diastolic blood pressure value ({patientDataList[5]}) in line: {line}")
                            if not(70 <= patientDataList[6] <= 100):
                                raise ValueError(f"Invalid oxygen saturation value ({patientDataList[6]}) in line: {line}")
                            if patientId not in patients.keys():
                                patients[patientId] = []
                                patients[patientId].append(patientDataList)
                            else:
                                patients[patientId].append(patientDataList)
                        except ValueError as exception:
                            print(str(exception))
                    except ValueError:
                        print(f"Invalid data type in line: {line}")
                #else statement corresponds to the if, print invalid number of fields.
                else:
                    print(f"Invalid number of fields {len(patientDataList)} in line: {patientDataList}")
        #except block if there are errors in file
        except:
            print("An unexpected error occurred while reading the file")
        #closing file since we opened it for reading
        finally:
            infile.close()
    #if file can't be found it altomatically exits
    except IOError:
        print(f"The file {fileName} could not be found.")
        exit()
    return patients

##########################################################################################################


def displayPatientData(patients, patientId=0):
    """
    Displays patient data for a given patient ID.

    patients: A dictionary of patient dictionaries, where each patient has a list of visits.
    patientId: The ID of the patient to display data for. If 0, data for all patients will be displayed.
    """
# if patientId is 0, it prints all patient number in the dictionary, and their data for each visit
    if patientId == 0:
        for patientNumber in patients:
            print(f"Patient ID: {patientNumber}")
            for visit in patients[patientNumber]:
                print(f" Visit Date: {visit[0]}")
                print(f"  Temperature: {visit[1]:.2f} C")
                print(f"  Heart Rate: {visit[2]} bpm")
                print(f"  Respiratory Rate: {visit[3]} bpm")
                print(f"  Systolic Blood Pressure: {visit[4]} mmHg")
                print(f"  Diastolic Blood Pressure: {visit[5]} mmHg")
                print(f"  Oxygen Saturation: {visit[6]} %")
    #if user input of patientId is not in dictionary, it prints not found message
    elif patientId not in patients:
        print(f"Patient with ID {patientId} not found.")
    #if user inputs a specific patientId, it only prints the data for that patient
    else:
        print(f"Patient ID: {patientId}")
        for visit in patients[patientId]:
            print(f" Visit Date: {visit[0]}")
            print(f"  Temperature: {visit[1]:.2f} C")
            print(f"  Heart Rate: {visit[2]} bpm")
            print(f"  Respiratory Rate: {visit[3]} bpm")
            print(f"  Systolic Blood Pressure: {visit[4]} mmHg")
            print(f"  Diastolic Blood Pressure: {visit[5]} mmHg")
            print(f"  Oxygen Saturation: {visit[6]} %")

#######################################################################################################

def displayStats(patients, patientId=0):
    """
    Prints the average of each vital sign for all patients or for the specified patient.

    patients: A dictionary of patient IDs, where each patient has a list of visits.tfc
    patientId: The ID of the patient to display vital signs for. If 0, vital signs will be displayed for all patients.
    """
    avgTem = 0
    avgHr = 0
    avgResRate = 0
    avgSysRate = 0
    avgDisRate = 0
    avgOxySat = 0
    numData = 0
    try:
        #if patient ID(user input) is 0, it prints the average vital signs for all patients
        if int(patientId) == 0:
            for patientNumber in patients:
                for visit in patients[patientNumber]:
                    avgTem += visit[1]                     #avg vital signs was 0, and it adds up the data for all visits.
                    avgHr += visit[2]                      #its in a for loop so it will add from all visits
                    avgResRate += visit[3]
                    avgSysRate += visit[4]
                    avgDisRate += visit[5]
                    avgOxySat += visit[6]
                    numData += 1
            if numData>0:                 #numData is number of data. to find average vital signs, I divide total vital signs from all visits
                print("Vital Signs for All Patients:")   #with the number of data.
                print(f"  Average Temperature: {float(avgTem/numData):.2f} C")
                print(f"  Average Heart Rate: {float(avgHr/numData):.2f} bpm")
                print(f"  Average Respiratory Rate: {float(avgResRate/numData):.2f} bpm")
                print(f"  Average Systolic Blood Pressure: {float(avgSysRate/numData):.2f} mmHg")
                print(f"  Average Diastolic Blood Pressure: {float(avgDisRate/numData):.2f} mmHg")
                print(f"  Average Oxygen Saturation: {float(avgOxySat/numData):.2f} %")
        #if user inputed a patient ID not in dictionary it will print 'no data found...'
        elif int(patientId) not in patients:
            print(f"No data found for patient with ID {patientId}.")
        else:
            for visit in patients[int(patientId)]:   #for a specific patient it print average vital signs from all their visits
                avgTem += visit[1]
                avgHr += visit[2]
                avgResRate += visit[3]
                avgSysRate += visit[4]
                avgDisRate += visit[5]
                avgOxySat += visit[6]
                numData += 1
            print(f"Vital Signs for Patient {patientId}:")
            print(f"  Average Temperature: {float(avgTem/numData):.2f} C")
            print(f"  Average Heart Rate: {float(avgHr/numData):.2f} bpm")
            print(f"  Average Respiratory Rate: {float(avgResRate/numData):.2f} bpm")
            print(f"  Average Systolic Blood Pressure: {float(avgSysRate/numData):.2f} mmHg")
            print(f"  Average Diastolic Blood Pressure: {float(avgDisRate/numData):.2f} mmHg")
            print(f"  Average Oxygen Saturation: {float(avgOxySat/numData):.2f} %")
    #making sure that user input is not some random word (has to be integer)
    except ValueError:
        print("Error:", "'patientId' should be an integer.")


#######################################################################################################

def addPatientData(patients, patientId, date, temp, hr, rr, sbp, dbp, spo2, fileName):
    """
    Adds new patient data to the patient list.

    patients: The dictionary of patient IDs, where each patient has a list of visits, to add data to.
    patientId: The ID of the patient to add data for.
    date: The date of the patient visit in the format 'yyyy-mm-dd'.
    temp: The patient's body temperature.
    hr: The patient's heart rate.
    rr: The patient's respiratory rate.
    sbp: The patient's systolic blood pressure.
    dbp: The patient's diastolic blood pressure.
    spo2: The patient's oxygen saturation level.
    fileName: The name of the file to append new data to.
    """
    #making sure that the new ID entered will be greater than 0.
    if patientId > 0:
        # if the date entered is not this format, it prints invalid date
        if not re.search("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", date):
            print("Invalid date format. Please enter date in the format 'yyyy-mm-dd'.")
        else:
            #append to file, split by '-' so I can seperate the date into components: year, month, day
            infile = open(fileName, 'a')
            dateList = date.split("-")
#change from str to int so following if statement works.
            year = int(dateList[0])
            month = int(dateList[1])
            day = int(dateList[2])
            if year < 1900 or not 1 <= month <= 12 or not 1 <= day <= 31:
                print("Invalid date. Please enter a valid date.")
                return
#makes sure that user input vital signs are within range.
            try:
                if not (35.0 <= temp <= 42.0):
                    raise ValueError("Invalid temperature. Please enter a temperature between 35.0 and 42.0 Celsius.")
                if not (30 <= hr <= 180):
                    raise ValueError("Invalid heart rate. Please enter a heart rate between 30 and 180 bpm.")
                if not (5 <= rr <= 40):
                    raise ValueError("Invalid respiratory rate. Please enter a respiratory rate between 5 and 40 bpm.")
                if not (70 <= sbp <= 200):
                    raise ValueError(
                        "Invalid systolic blood pressure. Please enter a systolic blood pressure between 70 and 200 mmHg.")
                if not (40 <= dbp <= 120):
                    raise ValueError(
                        "Invalid diastolic blood pressure. Please enter a diastolic blood pressure between 40 and 120 bpm.")
                if not (70 <= spo2 <= 100):
                    raise ValueError("Invalid oxygen saturation. Please enter an oxygen saturation between 70 and 100%.")
                #if the user inputed ID is not in the dictionary then it makes a new list for that key. Appends corresponding data.
                if patientId not in patients:
                    patients[patientId] = []
                    patients[patientId].append([date, temp, hr, rr, sbp, dbp, spo2])
                else:
                    patients[patientId].append([date, temp, hr, rr, sbp, dbp, spo2])
                infile.write(f"\n{patientId},{date},{temp},{hr},{rr},{sbp},{dbp},{spo2}")
                print(f"Visit is saved successfully for Patient # {patientId}")
            except ValueError as exception:
                print(str(exception))
            finally:
                infile.close()

    else:
        print("patient ID has to be greater than 0.")

###########################################################################################################


def findVisitsByDate(patients, year=None, month=None):
    """
    Find visits by year, month, or both.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    year: The year to filter by.
    month: The month to filter by.
    return: A list of tuples containing patient ID and visit that match the filter.
    """
    visits = []
    #year has to be none or right value, same for month
    if (year is None or year > 1900) and (month is None or 1 <= month <= 12):
        for patientId in patients:
            #for each patient ID's visit
            for visit in patients[patientId]:
                if re.search("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", visit[0]):
                    dateList = visit[0].split("-")
                    oldYear = int(dateList[0])
                    oldMonth = int(dateList[1])
                    if oldYear >= 1900 or 1 <= oldMonth <= 12:
                        if year is not None and month is not None:
                            if year == oldYear and month == oldMonth:
                                visits.append((patientId, visit))
                        elif year is not None and month is None:
                            if year == oldYear:
                                visits.append((patientId, visit))
                        elif year is None and month is None:
                            visits.append((patientId, visit))
    return visits

########################################################################################################

def findPatientsWhoNeedFollowUp(patients):
    """
    Find patients who need follow-up visits based on abnormal vital signs.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    return: A list of patient IDs that need follow-up visits to to abnormal health stats.
    """
    #blank list for followup patients
    followup_patients = []
    for patientId in patients:
        for visit in patients[patientId]:
            #corresponding vital values needs follow up
            if visit[2] > 100 or visit[2] < 60 or visit[4] > 140 or visit[5] > 90 or visit[6] < 90:
                if patientId not in followup_patients:
                    followup_patients.append(patientId)
    return followup_patients

########################################################################################################


def deleteAllVisitsOfPatient(patients, patientId, filename):
    """
    Delete all visits of a particular patient.

    patients: The dictionary of patient IDs, where each patient has a list of visits, to delete data from.
    patientId: The ID of the patient to delete data for.
    filename: The name of the file to save the updated patient data.
    return: None
    """
    #blank str set
    data = ""
    if patientId not in patients.keys():
        print(f"No data found for patient with ID {patientId}.")
    else:
        patients.pop(patientId)
        # open file for writing
        outputFile = open(filename, 'w')
        for patientNumber in patients:
            for visit in patients[patientNumber]:
                data += str(patientNumber)+","
                for index in visit:
                    data+=str(index)+","
                data = data[:-1]
                data+="\n"
        outputFile.write(data)
        print(f"Data for patient {patientId} has been deleted.")
        outputFile.close()

#########################################################################################################


def main():
    patients=readPatientsFromFile("patients.txt")

    while True:
        print("\n\nWelcome to the Health Information System\n\n")
        print("1. Display all patient data")
        print("2. Display patient data by ID")
        print("3. Add patient data")
        print("4. Display patient statistics")
        print("5. Find visits by year, month, or both")
        print("6. Find patients who need follow-up")
        print("7. Delete all visits of a particular patient")
        print("8. Quit\n")

        choice = input("Enter your choice (1-8): ")
        if choice == '1':
            displayPatientData(patients)
        elif choice == '2':
            patientID = int(input("Enter patient ID: "))
            displayPatientData(patients, patientID)
        elif choice == '3':
            patientID = int(input("Enter patient ID: "))
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                temp = float(input("Enter temperature (Celsius): "))
                hr = int(input("Enter heart rate (bpm): "))
                rr = int(input("Enter respiratory rate (breaths per minute): "))
                sbp = int(input("Enter systolic blood pressure (mmHg): "))
                dbp = int(input("Enter diastolic blood pressure (mmHg): "))
                spo2 = int(input("Enter oxygen saturation (%): "))
                addPatientData(patients, patientID, date, temp, hr, rr, sbp, dbp, spo2, 'patients.txt')
            except ValueError:
                print("Invalid input. Please enter valid data.")
        elif choice == '4':
            patientID = input("Enter patient ID (or '0' for all patients): ")
            displayStats(patients, patientID)
        elif choice == '5':
            year = input("Enter year (YYYY) (or 0 for all years): ")
            month = input("Enter month (MM) (or 0 for all months): ")
            visits = findVisitsByDate(patients, int(year) if year != '0' else None,
                                      int(month) if month != '0' else None)
            if visits:
                for visit in visits:
                    print("Patient ID:", visit[0])
                    print(" Visit Date:", visit[1][0])
                    print("  Temperature:", "%.2f" % visit[1][1], "C")
                    print("  Heart Rate:", visit[1][2], "bpm")
                    print("  Respiratory Rate:", visit[1][3], "bpm")
                    print("  Systolic Blood Pressure:", visit[1][4], "mmHg")
                    print("  Diastolic Blood Pressure:", visit[1][5], "mmHg")
                    print("  Oxygen Saturation:", visit[1][6], "%")
            else:
                print("No visits found for the specified year/month.")
        elif choice == '6':
            followup_patients = findPatientsWhoNeedFollowUp(patients)
            if followup_patients:
                print("Patients who need follow-up visits:")
                for patientId in followup_patients:
                    print(patientId)
            else:
                print("No patients found who need follow-up visits.")
        elif choice == '7':
            patientID = input("Enter patient ID: ")
            deleteAllVisitsOfPatient(patients, int(patientID), "patients.txt")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main()
