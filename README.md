# Currently this is very much a WORK IN PROGRESS and does not yet fully work as intended.
# TUe Osiris Gradescrape
Who wants to log in to Osiris and click multiple links to get an overview of your grades? Who wants to constantly check Osiris to see if there are new grades posted online?

Well, I sure don't! Let this tool do it for you :-)

## Important note:
This tool has been written by me as a TU/e student. I am in no other way affiliated with the TU/e. Though Osiris is not a service made by the university, my code is designed to deal specifically with the TU/e login page design elements. Should your school/university also make use of Osiris, then it is possible a large part of this tool works for you and you might just have to fix the login-part. I have never tested this in other versions than what is used here.

## Overview
The tool takes your username and password, logs in to Osiris and fetches your grades. If set up properly, it can do so on a user-defined interval. Should new grades be found, it notifies the user by showing an interface with all the users grades in a sortable table.

Calling this tool on an interval is intended to be handled by the OS. For example through the Windows Task Scheduler.

## Dependencies
The following list is not complete, and will be updated in the future.

|library|Version|Description|
|-------|-------|-----------|
|PyQt5|5.x|QtWebkit is used as a headless browser to bypass the JavaScript login page|
|BeautifulSoup4 | 4.x | Used to scrape the pages and extract the data |

## Configuration
In order to use this tool, it of course needs access to your Osiris page. For this you need to do the follwing:
### ! Rename example_config.json to config.json and fill with your user data!

## Disclaimer
The code within this project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

## Changelog
TBA
