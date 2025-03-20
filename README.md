# Road Test Booking Bot

This is a Selenium-based bot that automates the process of checking for earlier road test appointments on the ICBC website. If an earlier appointment is found, the bot sends an email notification.

## Features

- Logs into the ICBC appointment system using credentials from a `.env` file
- Checks for an earlier available road test appointment
- Sends an email notification if an earlier appointment is found
- Runs periodically (e.g., every 10 minutes)

## Prerequisites

- Python 3.11.4
- Google Chrome browser
- ChromeDriver (matching the installed Chrome version)
- A Gmail account for email notifications

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/codingpog/Road-Test-Booking-Bot.git
   cd Road-Test-Booking-Bot
   ```

2. Create a virtual environment for Windows (optional but recommended):

   ```sh
   python -m venv .venv     # Create the virtual environment
   Set-ExecutionPolicy Unrestricted -Scope Process  # Temporarily allow PowerShell scripts to run in the current session
   .venv\Scripts\activate.PS1  # Activate virtual environment in PowerShell
   ```

3. Install dependencies:

   ```sh
   pip install selenium
   ```

   ```sh
   pip install python-dotenv
   ```

   ```sh
   pip install python-dateutil
   ```

   ```sh
   pip install yagmail
   ```

   ```sh
   pip install schedule
   ```

4. Set up your `.env` file with the following format:

   ```ini
   LAST_NAME=YourLastName
   LICENSE_NUMBER=YourLicenseNumber
   KEYWORD=YourKeyword
   EMAIL=your-email@gmail.com
   PASSWORD=your-app-password (set up app password in Gmail first)
   ```

   **⚠️ Important:** Do not share your `.env` file or push it to GitHub.

5. Download and place `chromedriver.exe` in the project folder. Ensure it matches your Chrome version.

## Usage

Run the script to check for earlier appointments:

```sh
python main.py
```
