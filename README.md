# UG2Gcal

Easily convert your raw college schedule from BAAK into a readable format for Google Calendar! This tool takes in your copied schedule from BAAK or a `.txt` file and transforms it into a `.csv` file that can be imported into Google Calendar. Please note that you have to set reoccurring schedule manually since .csv files can't do reoccurring schedule

## Features
- **Automatically formats your schedule** into a Google Calendar-friendly `.csv` file
- **Improves readability** by standardizing course names, times, and lecturer
- **Quick and easy Google Calendar import**

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TheXploler/UG2GCal.git
   cd UG2GCal
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
    ```bash
   python ug2gcal.py
   ```

## Usage

### Option 1: Copy and Paste Schedule
1. Copy your schedule from BAAK
2. Select manual input
3. Paste your schedule into the input field
4. Pick a start date and an file output location and hit process
5. Import the `.csv` file into Google Calendar and you're done! 🚀

### Option 2: Use a `.txt` File
1. Save your copied schedule as a `.txt` file.
2. Select file input
3. Select the `.txt` file
4. Pick a start date and an file output location and hit process
5. Import the `.csv` file into Google Calendar and you're done! 🚀

## Importing to Google Calendar
1. Open **Google Calendar**
2. Click on the **Settings (⚙️) > Import & export**
3. Select **Import**, then upload the generated `.csv` file
4. Click **Import** and your schedule will appear in Google Calendar

## Contribution
Feel free to contribute! Fork the repo, make your changes, and submit a pull request

## License
This project is licensed under the MIT License