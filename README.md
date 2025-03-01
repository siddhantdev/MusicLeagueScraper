# Music League Scraper

Simple python code to scrape [Music League](https://musicleague.com/) website for some data.

## Dependencies:

The python packages `selenium` and `bs4` are required to run the programs. Additionally `geckodriver` needs to be on `PATH`.

## Running

Run any particular file with:

```
python3 file_name.py
```

The programs take a URL as input. A browser window will open which requires you
to sign in to Spotify and give permission. The functions for each file are:

| File   | Function    |
|--------------- | --------------- |
| `get_all_songs.py`   | Get all the songs submitted in a league grouped by round name, with information about: artist, album, how many votes the song recieved, who submitted the song    |
| `get_all_upvotes.py` | Get the spotify URIs for every song that each person in the league has voted for |
| `get_round_songs.py` | Same as `get_all_songs.py` but for a single round |
| `get_round_upvotes.py` | Same as `get_all_upvotes.py` but for a single round |

