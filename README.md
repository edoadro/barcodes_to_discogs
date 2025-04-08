# Music Info Fetcher

This script reads a list of barcodes from a CSV file, fetches album and track details from the Discogs API, and saves the information into two separate CSV files.

## Disclaimer 
The script is designed to run with a list of barcodes extracted using this [barcode scanner app](https://apps.apple.com/it/app/barcode-scanners/id504201315?l=en-GB). 

**Adjust the script accordingly if you plan to get barcodes in a different way**

## Setup

1. **Install Python 3:**  
   Make sure you have Python 3 installed on your computer.

2. **Install Required Packages:**  
   Open your terminal (or command prompt) and run:

   ```bash
   pip install pandas requests numpy
   ```

## Configuration

1. **CSV File:**  
Create a file named `cd_barcodes.csv` in the same folder as the script.  
The file should have a column labeled `Code` with the barcode numbers. Again adjust the script to your specific needs.

2. **Discogs API Token:**  
You need a Discogs API token for the script to work.  
- Either set it as an environment variable named `DISCOGS_TOKEN`:
  ```
  export DISCOGS_TOKEN="your_discogs_token_here"
  ```
- Or, if the variable is not set, the script will ask you to enter the token when you run it.

## Running the Script

1. Open your terminal in the folder where the script is located.
2. Run the script by typing:

   ```bash
   python music_info_fetcher.py
   ```
   
3. The script will:
- Read the barcodes from `cd_barcodes.csv`
- Retrieve album and track details from Discogs for each barcode
- Save the album info to `albums.csv` and track info to `tracks.csv`

That's it! Follow these steps and the script will handle the rest.
