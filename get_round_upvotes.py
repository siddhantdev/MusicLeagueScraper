import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def spotify_url_to_uri(url: str) -> str:
    """
    Convert a Spotify URL to a Spotify URI.
    
    Args:
        url (str): A Spotify URL in one of these formats:
            - https://open.spotify.com/track/[id]
            - https://open.spotify.com/album/[id]
            - https://open.spotify.com/artist/[id]
            - https://open.spotify.com/playlist/[id]
            Can include additional query parameters
    
    Returns:
        str: A Spotify URI in the format 'spotify:[type]:[id]'
    
    Raises:
        ValueError: If the URL is not a valid Spotify URL or is in an unsupported format
    """
    import re
 
    # Pattern to match Spotify URLs
    pattern = r'https://open\.spotify\.com/(track|album|artist|playlist)/([a-zA-Z0-9]{22})'
    
    # Try to match the pattern
    match = re.match(pattern, url)
    
    if not match:
        raise ValueError(
            "Invalid Spotify URL format. URL must start with 'https://open.spotify.com/' "
            "and include a supported type (track/album/artist/playlist) followed by a 22-character ID"
        )
    
    # Extract the type and ID from the match
    spotify_type = match.group(1)
    spotify_id = match.group(2)
    
    # Construct and return the URI
    return f"spotify:{spotify_type}:{spotify_id}"

class Song:
    def Song(self):
        self.url = ""
        self.submitted_by = ""
        self.num_votes = 0
        self.voters = []

    def __str__(self) -> str:
        return f"{self.url}\n{self.submitted_by}\t{self.num_votes}\n{','.join(self.voters)}\n"

def process_link(driver):
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    songs = soup.find_all('a', class_="text-purple")
    votes = soup.find_all('p', class_="fw-semibold")
    people = soup.find_all('h6', class_="fw-semibold")


    matching_divs = [
        div for div in soup.find_all('div', class_='row')
        if len(div.find_all('div', class_=['col', 'col-auto'])) == 3 and div.find_parent('div', class_='card-footer')
    ]

    voters = [div.find('div', class_='col').find('b', class_="d-block") for div in matching_divs]

    if (len(songs) >= 2):
        songs = songs[1:]

    songs = [song.get("href") for song in songs]
    votes = [int(vote.text.split(' ')[0]) for vote in votes]
    people = [person.text for person in people]

    voters_by_song = []
    i = 0

    for song, nv in zip(songs, votes):
        curr = []
        for _ in range(0, nv):
            while voters[i] is None:
                i += 1
            curr.append(voters[i].text)
            i += 1
        voters_by_song.append(curr)            

    data = []

    for song, vote, person, sv in zip(songs, votes, people, voters_by_song):
        curr_song = Song()
        curr_song.url = song
        curr_song.submitted_by = person
        curr_song.num_votes = vote
        curr_song.voters = sv

        data.append(curr_song)

    return data

url = input("Enter Round URL: ")
driver = webdriver.Firefox()
driver.get(url)
wait = WebDriverWait(driver, 3600)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5.card-title")))
time.sleep(10)
songs_by_person = {}

songs = process_link(driver)

for song in songs:
    for person in song.voters:
        if person not in songs_by_person:
            songs_by_person[person] = []
        songs_by_person[person].append(song.url)

for key, value in songs_by_person.items():
    print(key)
    for i in range(len(value)):
        if i == len(value) - 1:
            print(spotify_url_to_uri(value[i]))
        else:
            print(spotify_url_to_uri(value[i]), end=',')

driver.quit()
