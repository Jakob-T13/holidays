# Holidays
Python assessment involving scraping a web page for holidays, putting that information into objects, and displaying that information cleanly.

## Usage
Upon startup, the main program will open 'holidays.json' and read its data, then scrape holiday data from [timeanddate](https://www.timeanddate.com/holidays/us/). Following that, the user will be brought to an interactive main menu.

### Add Holiday
To add a holiday to the list, select the first option from the main menu. From there, the user is promped for a name and a date in ISO format (`YYYY-MM-DD`), allowing for retries if the date is incorrectly formatted. If the holiday name and date combination doesn't exist in the list, then the new holiday is added; otherwise, the user is informed of the duplicate entry. In either case, the user is then returned to the main menu.

### Remove Holiday
To remove a holiday from the list, select the second option from the main menu. The user will be prompted for a name and date, similar to if they were adding a holiday. If a matching holiday is found in the list, it will be removed; otherwise, the user is informed that no such holiday was found.

### Save to File
Saving to the `holidays.json` used in initialization is done through the third option in the main menu. The user will be prompted for confirmation, and then brought back to the main menu whether the file is saved or not.

### View Holidays Per Week
The fourth option in the main menu allows the user to input a year and week (or leave blank to get current year/week) and get the holidays for that week.
If the current week is selected (by leaving it blank, *not* manually choosing it), then the user will also be asked if they want to see weather information for the upcoming week. If so, then daily weather info for the next seven days will be shown, obtained from the [OpenWeatherMap API](https://openweathermap.org/api).