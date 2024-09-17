import xml.etree.ElementTree as ET
import pandas as pd


def parse_music_library(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the Tracks dictionary
    tracks_dict = root.find('./dict/key[.="Tracks"]/../dict')

    if tracks_dict is None:
        raise ValueError("Could not find Tracks dictionary in the XML file")

    # Initialize a list to store track data
    tracks_data = []

    # Iterate through each track
    for track in tracks_dict.findall('dict'):
        track_info = {}
        for i in range(0, len(track), 2):
            key = track[i].text
            value = track[i + 1]

            if value.tag == 'integer':
                track_info[key] = int(value.text)
            elif value.tag == 'string':
                track_info[key] = value.text
            elif value.tag == 'date':
                track_info[key] = value.text
            elif value.tag == 'true':
                track_info[key] = True
            elif value.tag == 'false':
                track_info[key] = False

        tracks_data.append(track_info)

    # Create a DataFrame
    df = pd.DataFrame(tracks_data)

    return df


# Usage
file_path = 'Library.xml'
music_df = parse_music_library(file_path)

# Display the first few rows of the DataFrame
print(music_df.head())

# Save the DataFrame to a CSV file (optional)
music_df.to_csv('music_library.csv', index=False)