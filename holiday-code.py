import datetime
import json
import os
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:      #Holiday class
    
    name: str
    date: datetime.datetime
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date})"
                   
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
        self.innerHolidays = []
           
    def addHoliday(self,holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        try:
            #holidayObj is a Holiday object
            verify = Holiday(holidayObj.name, holidayObj.date)
            self.innerHolidays.append(verify)
            # print(f"Successfully added holiday {holidayObj}.")
            return 0
        except TypeError:
            #holidayObj is not a Holiday object
            print("Error: that is not a Holiday object.")
            return 1
        except:
            #something else went wrong
            print("Error: an unknown error occurred.")
            return 1
        return 1

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        for i in self.innerHolidays:                        #search list of holidays
            if i.name == HolidayName and i.date == Date:    #if matching name and date are found
                return i                                    #return the holiday object
        return None                                         #otherwise, return None

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        toRemove = self.findHoliday(HolidayName, Date)      #find the holiday
        if toRemove != None:                                #if found
            self.innerHolidays.remove(toRemove)             #remove it
            # print(f"Successfully removed {toRemove}")
        else:                                               #otherwise, tell user to try again
            print(f"Could not find a holiday '{HolidayName}' on {Date}.")
        
    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        try:
            f = open(filelocation, "rt")                    #try to open a json file
        except:                                             #error out if it isn't found
            print(f"Failed to open file '{filelocation}'. Check the file name and try again.")
            return 1
        
        json_raw = f.read()                     #read the json file
        try:
            json_form = json.loads(json_raw)    #try to convert the text to a dictionary
        except:                                 #tell user if the formatting is wrong and error out
            print(f"'{filelocation}' is not a valid JSON file. Check the file's formatting and try again.")
            return 1
            
        try:                                    #try to read the list inside the json object
            dict_lst = json_form['holidays']
        except:                                 #tell user if formatting is wrong, and how to correct it
            print(f"'{filelocation}' is not correctly formatted. Make sure it consists of the following format:")
            print("{'Holidays': [{'name': <name>, 'date': <YYYY-MM-DD>}, ...]")
            return 1
        for i in dict_lst:                      #for each dictionary object in the list:
            newHoliday = Holiday(i["name"],datetime.datetime.fromisoformat(i["date"]))  #create a Holiday instance with the info
            added = self.addHoliday(newHoliday)     #add it to the list
            if added == 1:                          #if something goes wrong
                print(f"Error adding holiday '{newHoliday}'")   #error out
                return 1
        f.close()       #all done
        return 0

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        f = open(filelocation,"wt")             #open file - we're writing, so we don't need to check if it exists
        list_len = len(self.innerHolidays)      #get length of holiday list for later
        f.write('{\n "holidays" : [\n')         #write "header" of json file
        for i in self.innerHolidays:            #for each object in the holiday list:
            f.write("\t {\n")                           #construct a json object with the holiday info
            f.write(f'\t\t "name": "{i.name}",\n')
            f.write(f'\t\t "date": "{i.date}"\n')
            f.write("\t }")
            if self.innerHolidays.index(i) < list_len-1:
                f.write(",\n")
            else:
                f.write("\n ]\n")
        f.write('}')
        print(f"Successfully wrote all holidays to {filelocation}.")
        f.close()
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions. 
        years = ["2020","2021","2022","2023","2024"]    #years and month codes for URLs and holiday date string construction
        months = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}

        for i in years:     #for each year
            url = f"https://www.timeanddate.com/holidays/us/{i}"    #construct the url for that year
            response = requests.get(url)
            if response.status_code != 200:                         #if response is anything other than HTTP 200 ('OK')
                print("Error connecting to www.timeanddate.com")    #error out
                return 1
            html_raw = response.text    #get raw HTML from webpage
            
            soup = BeautifulSoup(html_raw, 'html.parser')   #put the HTML into BeautifulSoup's HTML parser
            holiday_table = soup.find('tbody')              #get to the body of the table where the data is
            for row in holiday_table.find_all('tr'):        #for each row in the table:
                if 'hol_' not in row.get('id'):             #if it's not one of the rows that appears at the beginning of each month:
                    date_tag = row.find('th')           #find the tag with the date in it
                    date_text = date_tag.string         #extract the raw string from the tag
                    date_month = date_text[0:3]         #extract the 3-letter month code
                    date_month = months[date_month]     #convert it to number code based on above dictionary
                    date_day = date_text[-2:].strip()   #extract the 2-digit day
                    if len(date_day) == 1:              #if day is only 1 digit (eg. '2')
                        date_day = f"0{date_day}"       #convert it to 2-digit format (eg. '02')
                    combined_date = f"{i}-{date_month}-{date_day}"  #create ISO formatted date string
                    iso_date = datetime.datetime.fromisoformat(combined_date)   #convert string to date
                    
                    name_tag = row.find('a')            #find the tag with the holiday name
                    name_text = name_tag.string         #extract the string from the tag
                    
                    if self.findHoliday(name_text, iso_date) == None:  #if new holiday is not in the list
                        new_holiday = Holiday(name_text, iso_date)
                        self.addHoliday(new_holiday)                        #add it to the list
        
        # print("Successfully scraped holiday data for 2020-2024")
        return 0

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)      #'nuff said
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        if week_number < 1 or week_number > 52:         #if week is outside of valid range:
            print("Error: week outside of valid range") #error out
            return None
        year_filter = list(filter(lambda n: n.date.year == year, self.innerHolidays))   #filter to holidays with given year
        week_filter = list(filter(lambda n: n.date.isocalendar().week == week_number, year_filter)) #filter to holidays with given week in the year
        return week_filter

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        for i in holidayList:
            print(str(i))

    def getWeather(self):   #due to the way my chosen weather API works, I can't use a week number to get weather for that static week, only a 'rolling' week
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        try:        #try to connect to the OpenWeather API
            url = "https://api.openweathermap.org/data/2.5/onecall?lat=44.97&lon=-93.26&exclude=current,minutely,hourly,alerts&units=imperial&appid=7bdf08f87f2b42a9e8956f9905feb0d3"
            response = requests.get(url)
        except:         #error out if it fails...
            print("Failed to connect to OpenWeather")
            return None
            
        if response.status_code != 200:     #...or if it's a bad response
            print("Failed to connect to OpenWeather")
            return None
        
        dates = []      #list for dates
        today = datetime.datetime.today()   #get today's date
        dates.append(today)                 #put it in the list
        newday = today + datetime.timedelta(days=1)     #get tomorrow's date
        for i in range(2,8):        #for the rest of the days in the week ahead
            dates.append(newday)    #append the new day
            newday += datetime.timedelta(days=1)    #get the day after
        
        weather_json = response.json()              #get json data from API
        weather_lst_raw = weather_json['daily']     #trim it down to the 7-day forecast
        weather_lst = []        #list to store condensed weather info
        for i in range(7):      #for each day in the week:
            high = weather_lst_raw[i]["temp"]["max"]    #get high temp
            low = weather_lst_raw[i]["temp"]["min"]     #get low temp
            wind = weather_lst_raw[i]["wind_speed"]     #get wind speed
            clouds = weather_lst_raw[i]["clouds"]       #get cloudiness
            precip = weather_lst_raw[i]["pop"]          #get chance of precipitation
            weather_dict = {                            #put 'em all in a dictionary
                "date" : dates[i],
                "weather" : {
                    "high" : high,
                    "low" : low,
                    "wind_speed" : wind,
                    "cloudiness" : clouds,
                    "precipitation" : precip * 100
                }
            }
            weather_lst.append(weather_dict)            #append the dictionary to the list
        return weather_lst

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        thisyear = datetime.datetime.today().isocalendar().year         #get current year
        thisweek = datetime.datetime.today().isocalendar().week         #get current week
        holidays_lst = self.filter_holidays_by_week(thisyear,thisweek)  #get filtered list of holidays
        if holidays_lst == None:        #if filter failed, error out
            print("Error retrieving holidays")
            return None
        elif holidays_lst == []:        #if no holidays this week, tell the user
            print("There are no holidays this week.")
            return 0
        else:                           #else, display the holidays
            self.displayHolidaysInWeek(holidays_lst)
        weather = input("Would you like to view this week's weather? y or n: ").lower()     #ask to see weather
        if weather == 'y':      #if yes
            weather_lst = self.getWeather()     #get weather
            if weather_lst != None:             #if getting weather doesn't fail
                for i in weather_lst:           #for each day
                    print(i["date"])            #print the date, followed by weather info
                    print(f"\tHigh temp: {i['weather']['high']} degrees F")
                    print(f"\tLow temp: {i['weather']['low']} degrees F")
                    print(f"\tWind Speed: {i['weather']['wind_speed']} mph")
                    print(f"\tCloudiness: {i['weather']['cloudiness']}%")
                    print(f"\tChance of precipitation: {i['weather']['precipitation']}%")
        return 0

def user_add_holiday(menu,hlist):       #UI for adding holidays
    os.system('cls')
    print(menu[2])
    hname = input("Holiday: ")      #ask for holiday name
    valid_date = True
    while valid_date:
        hdate = input("Date (YYYY-MM-DD): ")    #ask for holiday date in ISO format
        try:
            hfdate = datetime.datetime.fromisoformat(hdate)     #try to convert datestring to a date
            valid_date = False
        except:
            print("Error: invalid date. Please try again.")     #tell user to try again if it fails
    if hlist.findHoliday(hname, hfdate) == None:    #if the holiday isn't already in the list:
        new_holiday = Holiday(hname,hfdate)         #create the Holiday object
        hlist.addHoliday(new_holiday)               #add it to the list
        print("Success:")
        print(f"{str(new_holiday)} has been added to the holiday list.")
    else:                                           #else:
        print("Failure:")                           #tell user it's already in the list
        print("That holiday is already in the holiday list.")
    input("Press Enter to continue...")
    
def user_remove_holiday(menu,hlist):    #UI for removing holidays
    os.system('cls')
    print(menu[3])
    valid_holiday = True
    while valid_holiday:
        hname = input("Holiday Name: ")                 #ask for holiday name
        hdate = input("Holiday Date (YYYY-MM-DD): ")    #ask for holiday date
        try:
            hfdate = datetime.datetime.fromisoformat(hdate)     #try to convert datestring to date
            if hlist.findHoliday(hname, hfdate) != None:        #if the holiday is found
                hlist.removeHoliday(hname, hfdate)              #remove it
                print(f"Successfully removed {hname} ({hdate}) from the holiday list.")
            else:                                               #if it's not found, go back to main menu
                print("Error: Could not find that holiday. Check the name and date, and try again.")
            valid_holiday = False
        except:     #if conversion fails, try again
            print("Error: invalid date. Please try again.")
    input("Press Enter to continue...")
    
def user_save_holiday(menu,hlist):      #UI for saving to file
    os.system('cls')
    print(menu[4])
    in_menu = True
    while in_menu:
        ui = input("Are you sure you want to save your changes? [y/n]: ").lower()   #ask user if they're sure
        if ui == 'y':                           #if yes:
            hlist.save_to_json('holidays.json') #save to json file
            in_menu = False
        elif ui == 'n':                                 #if no:
            print("Holiday list file save canceled.")   #cancel out
            in_menu = False
        else:       #be strict with user input
            print("Please type 'y' or 'n'.")
    input("Press Enter to continue...")
    
def user_view_holiday(menu,hlist):      #UI for viewing holidays
    os.system('cls')
    print(menu[5])
    valid_year = True
    while valid_year:
        year = input("Which year? [Leave blank for current year]: ")    #ask for year
        if year == '':
            year = datetime.datetime.today().isocalendar().year         #get current year if blank
        try:
            year = int(year)        #try to convert year to int
            valid_year = False
        except:                     #try input again if it fails
            print("Error: invalid value for year. Please try again.")
    valid_week = True
    thisweek = False
    while valid_week:
        week = input("Which week? [1-52, leave blank for current week]: ")  #ask for week
        if week == '':
            thisweek = True
            week = datetime.datetime.today().isocalendar().week     #get current week if blank
        try:
            week = int(week)        #try to convert week to int
            if week < 1 or week > 52:   #try input again if outside valid range
                print("Error: invalid week number. Please try again.")
            else:
                valid_week = False
        except:                     #try input again if it fails
            print("Error: invalid value for week. Please try again.")
    
    print(f"These are the holidays for {year} week #{week}:")
    if thisweek:                #if using current week
        hlist.viewCurrentWeek() #use viewCurrentWeek which includes weather info
    else:                       #otherwise
        to_show = hlist.filter_holidays_by_week(year,week)  #filter list to given year and week
        if to_show == []:       #tell user if there are no holidays for the week
            print(f"There are no holidays in {year}, week {week}.")
        else:                   #otherwise, print the list of holidays
            hlist.displayHolidaysInWeek(to_show)
    input("Press Enter to continue...")
    
def user_exit(menu):        #UI to exit the program
    os.system('cls')
    print(menu[6])
    valid_input = True
    while valid_input:      #ask user if they're sure
        ui = input("Are you sure you want to exit? Any unsaved changes will be lost. [y/n] ").lower()
        if ui == 'y' or ui == 'n':
            valid_input = False
        else:       #be strict with input
            print("Error: invalid input. Please try again.")
    if ui == 'y':           #if yes
        print("Goodbye!")   #be polite
        os.system('cls')
        exit(0)             #exit cleanly
    else:                   #otherwise, go back
        input("Press Enter to return to the main menu...")

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    menufile = open('menus.txt','rt')   #open file with menus
    menutxt = menufile.read()           #read file text
    menus = menutxt.split(';\n')        #split text into list on delimiter
    menufile.close()                    #close the file
    os.system('cls')
    print(menus[0])                     #print the intro menu
    holidaylst = HolidayList()              #initialize HolidayList
    holidaylst.read_json('holidays.json')   #read json file into the HolidayList
    first_len = holidaylst.numHolidays()    #get original length of HolidayList
    print(f"There are {first_len} holidays stored in the system.")  #tell user how many holidays there are
    
    holidaylst.scrapeHolidays()             #scrape holidays
    second_len = holidaylst.numHolidays() - first_len   #get number of holidays scraped
    print(f"An additional {second_len} holidays were scraped from timeanddate.com.")    #tell user about them
    input("Press Enter to continue...")
    os.system('cls')
    
    is_running = True
    while is_running:
        print(menus[1])         #print main menu
        ui = input("@> ")
        if ui == '1':       #add holiday
            user_add_holiday(menus,holidaylst)
        elif ui == '2':     #remove holiday
            user_remove_holiday(menus,holidaylst)
        elif ui == '3':     #save to file
            user_save_holiday(menus,holidaylst)
        elif ui == '4':     #view holidays
            user_view_holiday(menus,holidaylst)
        elif ui == '5':     #exit
            user_exit(menus)
        else:               #try again
            print("Command not recognized.")
            input("Press Enter to continue...")
        os.system('cls')
    
    

if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





