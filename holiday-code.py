import datetime
import json
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
   
    def addHoliday(holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        try:
            #holidayObj is a Holiday object
            verify = Holiday(holidayObj.name, holidayObj.date)
            self.innerHolidays.append(verify)
            print(f"Successfully added holiday {holidayObj}.")
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

    def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        for i in self.innerHolidays:
            if i.name == HolidayName and i.date = Date:
                return i
        return None

    def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        toRemove = findHoliday(HolidayName, Date)
        if toRemove != None:
            innerHolidays.remove(toRemove)
            print(f"Successfully removed {toRemove}")
        else:
            print(f"Could not find a holiday '{HolidayName}' on {Date}.")
        
    def read_json(filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        try:
            f = open(filelocation, "rt")
        except:
            print(f"Failed to open file '{filelocation}'. Check the file name and try again.")
            return 1
        
        json_raw = f.read()
        try:
            dict_lst = json.loads(json_raw)
        except:
            print(f"'{filelocation}' is not a valid JSON file. Check the file's formatting and try again.")
            return 1
        
        for i in dict_lst:
            newHoliday = Holiday(i["name"],datetime.fromisoformat(i["date"]))
            if addHoliday(newHoliday) == 1:
                print(f"Error adding holiday '{newHoliday}'")
                return 1
        print(f"Successfully added holidays from {filelocation}")
        f.close()
        return 0

    def save_to_json(filelocation):
        # Write out json file to selected file.
        f = open(filelocation,"wt")
        f.write("[\n")
        for i in self.innerHolidays:
            f.write("{\n\t")
            f.write(f'"name": "{i.name}",\n')
            f.write(f'"date": "{i.date}"\n')
            f.write("}")
            if self.innerHolidays.index(i) < len(self.innerHolidays):
                f.write(",\n")
            else:
                f.write("\n]")
        print(f"Successfully wrote all holidays to {filelocation}.")
        f.close()
        
    def scrapeHolidays():
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
            holiday_table = soup.find('table',attrs={'id':'holidays-table'})
            for row in holiday_table.find_all_next('tr',attrs={'class':'showrow'}):
                date_tag = row.find('th')           #find the tag with the date in it
                date_text = date_tag.string         #extract the raw string from the tag
                date_month = date_text[0:2]         #extract the 3-letter month code
                date_month = months[date_month]     #convert it to number code based on above dictionary
                date_day = date_text[-2:].strip()   #extract the 2-digit day
                if len(date_day) == 1:              #if day is only 1 digit (eg. '2')
                    date_day = f"0{date_day}"       #convert it to 2-digit format (eg. '02')
                combined_date = f"{i}-{date_month}-{date_day}"  #create formatted date
                
                name_tag = row.find('a')            #find the tag with the holiday name
                name_text = name_tag.string         #extract the string from the tag
                
                if findHoliday(name_text, combined_date) == None:   #if new holiday is not in the list
                    addHoliday(name_text, combined_date)            #add it to the list
        
        print("Successfully scraped holiday data for 2020-2024")
        return 0

    def numHolidays():
        # Return the total number of holidays in innerHolidays
        return len(innerHolidays)
    
    def filter_holidays_by_week(year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        if year < 2020 or year > 2024:
            print("Error: year outside of valid range")
            return None
        if week < 1 or week > 52:
            print("Error: week outside of valid range")
            return None
        year_filter = list(filter(lambda n: n.date.year == year, self.innerHolidays))
        week_filter = list(filter(lambda n: n.date.isocalendar().week == week_number, year_filter))
        return week_filter

    def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        for i in holidayList:
            print(str(i))

    def getWeather():
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
        
        weather_json = response.json()
        weather_lst_raw = weather_json['daily']
        weather_lst = []
        for i in weather_lst_raw:
            high = i["temp"]["max"]
            low = i["temp"]["min"]
            wind = i["wind_speed"]
            clouds = i["clouds"]
            precip = i["pop"]
            weather_dict = {
                "high" : high,
                "low" : low,
                "wind_speed" : wind
                "cloudiness" : f"{clouds}%"
                "precipitation" : f"{precip}%"
            }
            weather_lst.append(weather_dict)
        return weather_lst

    def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



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





