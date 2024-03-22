#link_details.py
import json

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def extract_details_from_link(unrestricted_link):
    config = load_config()
    CURRENT_SEASON = config['CURRENT_SEASON']
    CURRENT_EPISODE = config['CURRENT_EPISODE']
    catalog_type = "Series" if CURRENT_SEASON != "0" and CURRENT_EPISODE != "0" else "Movie"
    
    if catalog_type == "Series":
        season_episode = f"S{CURRENT_SEASON}E{CURRENT_EPISODE}"
        content_details = f"{catalog_type} | Video ID: {config.get('video_id', 'Unknown')} | {season_episode} | {unrestricted_link}"
    else:
        content_details = f"{catalog_type} | Video ID: {config.get('video_id', 'Unknown')} | {unrestricted_link}"
    return content_details

def save_unrestricted_link(unrestricted_link):
    content_details = extract_details_from_link(unrestricted_link)
    all_links = []
    found_index = -1

    try:
        with open('continue_watching.txt', 'r') as file:
            all_links = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pass

    video_id = content_details.split('|')[1].strip()
    season_episode = content_details.split('|')[2].strip() if "Series" in content_details else None

    for i, link in enumerate(all_links):
        existing_video_id = link.split('|')[1].strip()
        existing_season_episode = link.split('|')[2].strip() if "Series" in link else None
        
        if video_id == existing_video_id and (season_episode == existing_season_episode or season_episode is None):
            found_index = i
            break

    if found_index != -1:  # if a duplicate is found, overwrite it
        all_links[found_index] = content_details
    else:
        all_links.append(content_details)

    with open('continue_watching.txt', 'w') as file:
        for link in all_links:
            file.write(link + "\n")



