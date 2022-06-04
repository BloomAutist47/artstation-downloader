# Script Written by Bloom
# Github: https://github.com/BloomAutist47

import os
import json
import cloudscraper

# Place Name Here
artstation_user = ""

# Scraper
scraper = cloudscraper.create_scraper()

# Script Vars
user_id = ""
master_list = []

def get_user_id():
    global user_id
    response = scraper.get(f"https://www.artstation.com/users/{artstation_user}/quick.json")
    if response.status_code == 404:
        print("> Artist does not exists")
        return False
    data = json.loads(response.text)
    user_id = data['id']
    return True

def getMasterList():
    global master_list
    global artstation_user
    global user_id

    for num in range(0,5):
        response = scraper.get(f"https://www.artstation.com/users/{artstation_user}/projects.json?page={num}&user_id={user_id}").text
        data = json.loads(response)['data']
        
        if master_list != [] and  data == []:
            break
        master_list += data;
        print("  get page: ", num)

def download_images():
    global master_list
    global artstation_user
    
    hash_list = []
    
    image_location = f"download/{artstation_user}-images"
    
    os.makedirs(f"{image_location}/", exist_ok=True)
    
    for item in master_list:
        hash_id = item["hash_id"]

        # Checks if downloaded already
        if hash_id in hash_list: continue
            
        # Get individual post data json
        response = scraper.get(f"https://www.artstation.com/projects/{hash_id}.json").text

        # Gets the image assets only
        image_datas = json.loads(response)['assets']
        
        print(f"  Hash ID: {hash_id} Url: https://www.artstation.com/artwork/{hash_id}")
        
        # Download each image individually
        for image in image_datas:
            # Filename
            filename = f"{artstation_user}-{hash_id}-{image['id']}.jpg"
            file_exists = os.path.exists(f"{image_location}/" + filename)
            if file_exists:
                print("    Downloaded Already: ", filename)
                continue

            # Gets raw image
            image_response = scraper.get(image['image_url'] + "&dl=1")
           
            # Saves to folder
            file = open(f"{image_location}/{filename}", "wb")
            file.write(image_response.content)
            file.close()
            
            print("    Done: ", filename, " Url: ", image['image_url'])

        hash_list.append(hash_id)
        print("")

    # Get Download Count
    os.makedirs(f"{image_location}/", exist_ok=True)
    dir_path = f"{image_location}/"
    count = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
    print(f"> Downloaded: {count} images\n")

# Menu
print("> Artstation Downloader v.0.1 by Bloom Autist")
print("> Github: https://github.com/BloomAutist47/")
print("")

while True:
    artstation_user = input('> Enter artist name: ')
    artstation_user = artstation_user.strip().lower()
    if artstation_user == "":
        continue

    print("\n> Getting User ID")
    valid = get_user_id()
    if not valid:
        continue
    break

# Body
print("\n> Getting Master List")
getMasterList()

print("\n> Downloading All Art station images\n")
download_images()

# Exit
x = input('> Enter any key to exit...')



