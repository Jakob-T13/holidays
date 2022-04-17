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
class Holiday:
    
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
        
    def __eq__(self,other):
        for i in self.innerHolidays:
            if i not in other.innerHolidays:
                return False
        return True
   
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
        for i in self.innerHolidays:
            if i.name == HolidayName and i.date == Date:
                return i
        return None

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        toRemove = self.findHoliday(HolidayName, Date)
        if toRemove != None:
            self.innerHolidays.remove(toRemove)
            # print(f"Successfully removed {toRemove}")
        else:
            print(f"Could not find a holiday '{HolidayName}' on {Date}.")
        
    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        try:
            f = open(filelocation, "rt")
        except:
            print(f"Failed to open file '{filelocation}'. Check the file name and try again.")
            return 1
        
        json_raw = f.read()
        try:
            json_form = json.loads(json_raw)
        except:
            print(f"'{filelocation}' is not a valid JSON file. Check the file's formatting and try again.")
            return 1
            
        try:
            dict_lst = json_form['holidays']
        except:
            print(f"'{filelocation}' is not correctly formatted. Make sure it consists of the following format:")
            print("{'Holidays': [{'name': <name>, 'date': <ISO date>}, ...]")
            return 1
        for i in dict_lst:
            newHoliday = Holiday(i["name"],datetime.datetime.fromisoformat(i["date"]))
            added = self.addHoliday(newHoliday)
            if added == 1:
                print(f"Error adding holiday '{newHoliday}'")
                return 1
        # print(f"Successfully added holidays from {filelocation}")
        f.close()
        return 0

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        f = open(filelocation,"wt")
        list_len = len(self.innerHolidays)
        f.write('{\n "holidays" : [\n')
        for i in self.innerHolidays:
            f.write("\t {\n")
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
        years = ["2020","2021","2022","2023","2024"]
        months = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}

        for i in years:
            url = f"https://www.timeanddate.com/holidays/us/{i}"
            response = requests.get(url)
            if response.status_code != 200:
                print("Error connecting to www.timeanddate.com")
                return 1
            html_raw = response.text
            
            soup = BeautifulSoup(html_raw, 'html.parser')
            holiday_table = soup.find('tbody')
            for row in holiday_table.find_all('tr'):
                if 'hol_' not in row.get('id'):
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
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        # if year < 2020 or year > 2024:
            # print("Error: year outside of valid range")
            # return None
        if week_number < 1 or week_number > 52:
            print("Error: week outside of valid range")
            return None
        year_filter = list(filter(lambda n: n.date.year == year, self.innerHolidays))
        week_filter = list(filter(lambda n: n.date.isocalendar().week == week_number, year_filter))
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
        try:
            url = "https://api.openweathermap.org/data/2.5/onecall?lat=44.97&lon=-93.26&exclude=current,minutely,hourly,alerts&units=imperial&appid=7bdf08f87f2b42a9e8956f9905feb0d3"
            response = requests.get(url)
        except:
            print("Failed to connect to OpenWeather")
            return None
        
        dates = []
        today = datetime.datetime.today()
        dates.append(today)
        newday = today + datetime.timedelta(days=1)
        for i in range(2,8):
            dates.append(newday)
            newday += datetime.timedelta(days=1)
            
        print(dates)
        
        weather_json = response.json()
        weather_lst_raw = weather_json['daily']
        weather_lst = []
        for i in range(7):
            high = weather_lst_raw[i]["temp"]["max"]
            low = weather_lst_raw[i]["temp"]["min"]
            wind = weather_lst_raw[i]["wind_speed"]
            clouds = weather_lst_raw[i]["clouds"]
            precip = weather_lst_raw[i]["pop"]
            weather_dict = {
                "date" : dates[i],
                "weather" : {
                    "high" : high,
                    "low" : low,
                    "wind_speed" : wind,
                    "cloudiness" : clouds,
                    "precipitation" : precip * 100
                }
            }
            weather_lst.append(weather_dict)
        return weather_lst

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        thisyear = datetime.datetime.today().isocalendar().year
        thisweek = datetime.datetime.today().isocalendar().week
        holidays_lst = self.filter_holidays_by_week(thisyear,thisweek)
        if holidays_lst == None:
            print("Error retrieving holidays")
            return None
        elif holidays_lst == []:
            print("There are no holidays this week.")
            return 0
        else:
            self.displayHolidaysInWeek(holidays_lst)
        weather = input("Would you like to view this week's weather? y or n: ").lower()
        if weather == 'y':
            weather_lst = self.getWeather()
            if weather_lst != None:
                for i in weather_lst:
                    print(i["date"])
                    print(f"\tHigh temp: {i['weather']['high']} degrees F")
                    print(f"\tLow temp: {i['weather']['low']} degrees F")
                    print(f"\tWind Speed: {i['weather']['wind_speed']} mph")
                    print(f"\tCloudiness: {i['weather']['cloudiness']}%")
                    print(f"\tChance of precipitation: {i['weather']['precipitation']}%")
        return 0

def user_add_holiday(menu,hlist):
    os.system('cls')
    print(menu[2])
    hname = input("Holiday: ")
    valid_date = True
    while valid_date:
        hdate = input("Date (YYYY-MM-DD): ")
        try:
            hfdate = datetime.datetime.fromisoformat(hdate)
            valid_date = False
        except:
            print("Error: invalid date. Please try again.")
    if hlist.findHoliday(hname, hfdate) == None:
        new_holiday = Holiday(hname,hfdate)
        hlist.addHoliday(new_holiday)
        print("Success:")
        print(f"{str(new_holiday)} has been added to the holiday list.")
    else:
        print("Failure:")
        print("That holiday is already in the holiday list.")
    input("Press Enter to continue...")
    
def user_remove_holiday(menu,hlist):
    os.system('cls')
    print(menu[3])
    valid_holiday = True
    while valid_holiday:
        hname = input("Holiday Name: ")
        hdate = input("Holiday Date (YYYY-MM-DD): ")
        try:
            hfdate = datetime.datetime.fromisoformat(hdate)
            if hlist.findHoliday(hname, hfdate) != None:
                hlist.removeHoliday(hname, hfdate)
                print(f"Successfully removed {hname} ({hdate}) from the holiday list.")
            else:
                print("Error: Could not find that holiday. Check the name and date, and try again.")
            valid_holiday = False
        except:
            print("Error: invalid date. Please try again.")
    input("Press Enter to continue...")
    
def user_save_holiday(menu,hlist):
    os.system('cls')
    print(menu[4])
    in_menu = True
    while in_menu:
        ui = input("Are you sure you want to save your changes? [y/n]: ").lower()
        if ui == 'y':
            hlist.save_to_json('holidays.json')
            in_menu = False
        elif ui == 'n':
            print("Holiday list file save canceled.")
            in_menu = False
        else:
            print("Please type 'y' or 'n'.")
    input("Press Enter to continue...")
    
def user_view_holiday(menu,hlist):
    os.system('cls')
    print(menu[5])
    valid_year = True
    while valid_year:
        year = input("Which year? [Leave blank for current year]: ")
        if year == '':
            year = datetime.datetime.today().isocalendar().year
        try:
            year = int(year)
            valid_year = False
        except:
            print("Error: invalid value for year. Please try again.")
    valid_week = True
    thisweek = False
    while valid_week:
        week = input("Which week? [1-52, leave blank for current week]: ")
        if week == '':
            thisweek = True
            week = datetime.datetime.today().isocalendar().week
        try:
            week = int(week)
            if week < 1 or week > 52:
                print("Error: invalid week number. Please try again.")
            else:
                valid_week = False
        except:
            print("Error: invalid value for week. Please try again.")
    
    print(f"These are the holidays for {year} week #{week}:")
    if thisweek:
        hlist.viewCurrentWeek()
    else:
        to_show = hlist.filter_holidays_by_week(year,week)
        if to_show == []:
            print("There are no holidays this week.")
        else:
            hlist.displayHolidaysInWeek(to_show)
    input("Press Enter to continue...")
    
def user_exit(menu):
    os.system('cls')
    print(menu[6])
    valid_input = True
    while valid_input:
        ui = input("Are you sure you want to exit? Any unsaved changes will be lost. [y/n] ").lower()
        if ui == 'y' or ui == 'n':
            valid_input = False
        else:
            print("Error: invalid input. Please try again.")
    if ui == 'y':
        print("Goodbye!")
        exit(0)
    else:
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
    menufile = open('menus.txt','rt')
    menutxt = menufile.read()
    menus = menutxt.split(';\n')
    menufile.close()
    print(menus[0])
    holidaylst = HolidayList()
    holidaylst.read_json('holidays.json')
    starting_lst = holidaylst
    first_len = holidaylst.numHolidays()
    print(f"There are {first_len} holidays stored in the system.")
    
    holidaylst.scrapeHolidays()
    second_len = holidaylst.numHolidays() - first_len
    print(f"An additional {second_len} holidays were scraped from timeanddate.com.")
    input("Press Enter to continue...")
    os.system('cls')
    
    is_running = True
    while is_running:
        print(menus[1])
        ui = input("@> ")
        if ui == '1':
            user_add_holiday(menus,holidaylst)
        elif ui == '2':
            user_remove_holiday(menus,holidaylst)
        elif ui == '3':
            user_save_holiday(menus,holidaylst)
        elif ui == '4':
            user_view_holiday(menus,holidaylst)
        elif ui == '5':
            user_exit(menus)
        else:
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





