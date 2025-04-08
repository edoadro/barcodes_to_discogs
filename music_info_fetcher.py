import pandas as pd
import requests
import time
import numpy as np
import os
from getpass import getpass

import requests
import time
from typing import Tuple, List, Dict, Optional


def get_music_data(barcode: str, token: str, retries: int = 5, delay: int = 10) -> Tuple[Dict[str, Optional[str]], List[Dict[str, Optional[str]]]]:
    
    barcode_url = f"https://api.discogs.com/database/search?barcode={barcode}&token={token}"
    
    for i in range(retries):
        try:
            barcode_response = requests.get(barcode_url)
            barcode_response.raise_for_status()  # Check for HTTP errors
            barcode_data = barcode_response.json()  # Try to parse JSON
            break  # Exit the loop if successful
        except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError) as e:
            print(f"Attempt {i + 1} failed for barcode {barcode}: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    else:
        print(f"Failed to retrieve data for barcode {barcode} after {retries} attempts.")
        return {
            'barcode': barcode,
            'main_artist': None,
            'artists': None,
            'title': None,
            'complete_title': None,
            'country': None,
            'year': None,
            'genre': None,
            'style': None,
            'cover_image': None,
            'lowest_price': None,
        }, []

    if barcode_data['results'] == []:
        album = {
            'barcode': barcode,
            'main_artist': None,
            'artists': None,
            'title': None,
            'complete_title': None,
            'country': None,
            'year': None,
            'genre': None,
            'style': None,
            'cover_image': None,
            'lowest_price': None,
        }
        tracklist = []
    else:
        release_data = barcode_data['results'][0]
        
        release_id = release_data['id']
        release_url = f"https://api.discogs.com/releases/{release_id}?token={token}"
        
        for i in range(retries):
            try:
                id_response = requests.get(release_url)
                id_response.raise_for_status()  # Check for HTTP errors
                id_data = id_response.json()  # Try to parse JSON
                break  # Exit the loop if successful
            except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError) as e:
                print(f"Attempt {i + 1} failed for release {release_id}: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
        else:
            print(f"Failed to retrieve release data for release ID {release_id} after {retries} attempts.")
            return {
                'barcode': barcode,
                'main_artist': None,
                'artists': None,
                'title': None,
                'complete_title': release_data.get('title', None),
                'country': release_data.get('country', None),
                'year': None,
                'genre': release_data.get('genre', None),
                'style': release_data.get('style', None),
                'cover_image': release_data.get('cover_image', None),
                'lowest_price': None,
            }, []
        
        album = {
            'barcode': barcode,
            'main_artist': id_data.get('artists', [{}])[0].get('name', None),
            'artists': ', '.join([i.get('name', None) for i in id_data.get('artists', [])]),
            'title': id_data.get('title', None),
            'complete_title': release_data.get('title', None),
            'country': release_data.get('country', None),
            'year': id_data.get('year', None),
            'genre': release_data.get('genre', None),
            'style': release_data.get('style', None),
            'cover_image': release_data.get('cover_image', None),
            'lowest_price': id_data.get('lowest_price', None),
        }
            
        tracklist = [{
            'album_barcode': barcode,
            'position': index + 1,
            'title': i.get('title', None),
            'contributions': ', '.join([f"{artist.get('role', 'Composed by')} {artist.get('name', album.get('main_artist', 'Unknown'))}" for artist in i.get('extraartists', [{'role': 'Composed by', 'name': album.get('main_artist', 'Unknown')}])]),
            'contributors': ', '.join([artist.get('name', album.get('main_artist', 'Unknown')) for artist in i.get('extraartists', [{'role': 'Composed by', 'name': album.get('main_artist', 'Unknown')}])])
        } for index, i in enumerate(id_data.get('tracklist', []))]
    return album, tracklist

def main() -> None:
    #variables
    
    #try to ge t the token from the environment variable
    if 'DISCOGS_TOKEN' in os.environ:
        token = os.environ['DISCOGS_TOKEN']
    else:
        token = getpass('Enter your Discogs token (you can also set this as an envornment variable "DISCOGS_TOKEN"):')
        
    
    path = 'cd_barcodes.csv'

    #initial df (with barcodes) -> creation and preparation
    df_barcodes = pd.read_csv(path, skiprows= [0, 1, -2, -1])
    df_barcodes.drop(columns=['Timestamp', 'Date'], inplace= True)
    df_barcodes.dropna(subset=['Code'],  inplace= True)
    df_barcodes['Code'] = df_barcodes['Code'].astype(int).astype(str)
    barcodes_list = df_barcodes['Code'].to_list()
    
    #create lists to keep each dict with the info 
    album_data = []
    tracklist_data = []

    for code in barcodes_list:
        time.sleep(1)
        print(f"Getting data for barcode: {code}...")
        album, tracklist  = get_music_data(code, token)
        album_data.append(album)
        tracklist_data.extend(tracklist)
        print("Done✅")
        
        
    album_df = pd.DataFrame(album_data)
    tracklist_df = pd.DataFrame(tracklist_data)
    
    
    #export to 2 CSV files 
    print("Exporting data to CSV files...")
    
    album_df.to_csv('albums.csv', index=False)
    tracklist_df.to_csv('tracks.csv', index=False)

if __name__ == '__main__':
    main()
