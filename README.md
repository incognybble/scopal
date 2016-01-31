# scopal

This program is used to collect your own data from the Opal website https://www.opal.com.au/ .

While the website does allow you to download your own data in PDF, it isn't particularly useful if you want to do some analysis on the data. This code saves your data in CSV. Works in Firefox and Chrome. Default option is Firefox.

## Compatibility
* Windows - confirmed with both Firefox and Chrome.
* Linux - confirmed with Firefox.

## Requirements
* Python 2.7
* Selenium library https://pypi.python.org/pypi/selenium
* Firefox or Chrome and ChromeDriver https://sites.google.com/a/chromium.org/chromedriver/downloads
* Opal account with linked card

## Usage
If compiling the code into an executable and using Firefox, the webdriver files for the browser will need to be copied into the same folder as the executable. Webdriver files are webdriver.xpi and webdriver_prefs.json

If using Chrome, the ChromeDriver address needed to be in the system's PATH variable. I put the ChromeDriver executable in C:\Python27\Scripts

When the code is run, it will ask for several user inputs.
* username - your username to log into your Opal account. Cannot be blank.
* password - your password to log into your Opal account. Cannot be blank.
* card - the name of the card that the data is collected from. This field is optional, and is more useful when you have multiple cards linked to the same account.
* stop - the unique trip id where the code should stop collecting data. This field is optional, and is more useful if some data has been collected before. This saves you from having to recollect data.
* output file - the location and filename of the output file. This field is optional, and by default the output file is opal.csv
* browser - the browser you want to use. This field is optional. Firefox is the default.

Your username and password are not stored, and are just used to login to get the data. Consequently, each time you run the code, you will need to re-enter your details.

## Disclaimer
Opal and its associated trademarks are intellectual property of Transport for NSW and its subsidiaries. The author does not claim any responsibility for mistakes in the data.

This program is designed for personal use and to allow you to collect your own data. It is not intended for use in collecting other users' data.

## License
Copyright 2015 incognybble

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
