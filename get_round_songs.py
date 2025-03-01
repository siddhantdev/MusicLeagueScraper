import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def process_link(driver):
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

url = input()
driver = webdriver.Firefox()
driver.get(url)
wait = WebDriverWait(driver, 3600)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5.card-title")))
time.sleep(5)
process_link(driver)
driver.quit()
