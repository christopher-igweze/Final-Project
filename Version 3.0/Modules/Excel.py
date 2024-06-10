from py import test
from Modules import dbMgr, rnd
from Modules.DBMgr import Instructor, MeetingTime
from Modules.Schedule import finalSchedule
import pandas as pd

def output_schedule():
    sheets = ["mon", "tue", "wed", "thur", "fri"]
    classes = finalSchedule()
    roomsobjects = dbMgr.get_rooms()
    rooms = [i.get_number() for i in roomsobjects]
    rooms.sort()
    thedata = {}
    times = [1,2,3,4,5,6,7,8,9,10]

    for day in sheets:
        mydata = []
        daylist = [lecture for lecture in classes if lecture.get_meetingTime().get_sub() == day]
        columns = ["Room/Time", "8:00am - 9:00am", '9:00am - 10:00am', '10:00am - 11:00am', '11:00am - 12:00pm', '12:00pm - 1:00pm', '1:00pm - 2:00pm', '3:00pm - 4:00pm', '4:00pm - 5:00pm', '5:00pm - 6:00pm', '6:00pm - 7:00pm']
        for room in rooms:
            row = []
            row.append(room)
            roomlist = [lecture for lecture in daylist if lecture.get_room().get_number() == room]
            j = 0
            length = len(roomlist)
            for i in range(len(times)):
                if length < 1:
                    row.append("")
                else:
                    if int(roomlist[j].get_meetingTime().get_id()[2:]) == times[i]:
                        row.append(str(roomlist[j].get_course().get_name()))
                        j+=1
                        length-=1
                    else:
                        row.append("")
            mydata.append(row)
        times = [x + 10 for x in times]
        thedata[day] = pd.DataFrame(mydata, columns=columns)
    with pd.ExcelWriter('C:/Users/USER/Documents/Important Files/Final Project/Version 3.0/sheets/final_timetable.xlsx', engine='openpyxl') as writer:
        for day in sheets:
            thedata[day].to_excel(writer, sheet_name=day, index=False)

    print("Excel workbook 'final_timetable.xlsx' has been created successfully with multiple sheets.")
