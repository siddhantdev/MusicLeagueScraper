import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def spotify_url_to_uri(url: str) -> str:
    import re
    
    pattern = r'https://open\.spotify\.com/(track|album|artist|playlist)/([a-zA-Z0-9]{22})'
    
    match = re.match(pattern, url)
    
    if not match:
        raise ValueError("Invalid Spotify URL format.")
    
    spotify_type = match.group(1)
    spotify_id = match.group(2)
    
    return f"spotify:{spotify_type}:{spotify_id}"

class Song:
    def Song(self):
        self.url = ""
        self.submitted_by = ""
        self.num_votes = 0
        self.voters = []

    def __str__(self) -> str:
        return f"{self.url}\n{self.submitted_by}\t{self.num_votes}\n{','.join(self.voters)}\n"

def process_link(link, driver):
    driver.get(link)
    time.sleep(10)
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

url = input("Enter Music League URL: ")
driver = webdriver.Firefox()
driver.get(url)
wait = WebDriverWait(driver, 3600)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5.card-title")))
time.sleep(5)
html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
elements = soup.find_all('h5', class_='card-title')

rounds = []

for element in elements:
    rounds.append(element.text)

links = soup.find_all('a', class_='stretched-link')

links_list = []
for i, link in enumerate(links):
    curr_link = str(link['href'])
    if (curr_link.startswith("/l/") and not("create" in curr_link)):
        links_list.append(curr_link)

data = list(zip(rounds, links_list))

songs_by_person = {}

for link in links_list:
    curr_link = "https://app.musicleague.com" + link
    songs = process_link(curr_link, driver)
    for song in songs:
        for person in song.voters:
            if person not in songs_by_person:
                songs_by_person[person] = []
            songs_by_person[person].append(song.url)

for key, value in songs_by_person.items():
    print(key)
    for url in value:
        print(spotify_url_to_uri(url), end=',')

driver.quit()
