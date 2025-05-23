import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
def process_link(link, driver):
    driver.get(link)
    time.sleep(10)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    songs = soup.find_all('a', class_="text-purple")

    texts = soup.find_all('p', class_='card-text')

    votes = soup.find_all('p', class_="fw-semibold")

    people = soup.find_all('h6', class_="fw-semibold")

    if (len(songs) >= 2):
        songs = songs[1:]

    if (len(texts) >= 2):
        texts = texts[1:]

    artists = []
    albums = []
    for i in range(0, len(texts), 3):
        artists.append(texts[i].text)
        albums.append(texts[i + 1].text)

    songs = [song.text for song in songs]
    votes = [vote.text for vote in votes]
    people = [person.text for person in people]

    data = list(zip(songs, artists, albums, votes, people))
    for song in data:
        print("| ".join(song))
    print()

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

for round_name, link in data:
    print(round_name)
    curr_link = "https://app.musicleague.com" + link
    process_link(curr_link, driver)

driver.quit()
