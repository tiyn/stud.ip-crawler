# Stud.IP Crawler

This is a program that downloads all files available for a given Stud.IP user.
It only downloads and searches through the courses in the current semester.
If you run the program again it only downloads files that have changed since the last time running it.

## Features/To-Dos

[x] Downloads files of given users active semester via commandline
    [x] Keeping file structure of Stud.IP
    [x] Specify username
    [x] Specify password
    [x] Specify stud.ip-url
    [x] Specify output directory
    [x] Specify chunk size to download big files
[x] Only download files after given date
    [x] Save and read download date
    [x] Possible reset of download date
[ ] Incremental file download
    [ ] Indexing

## Installation

- `git clone https://github.com/tiyn/studip-crawler`
- `cd studip-crawler`
- `pip3install -r requirements` - install dependencies

## Usage

Just run the file via `python3 crawler.py [options]`.
Alternatively to `python3 crawler.py` you can give yourself permissions using `chmod +x crawler.py [options]` and
run it with `./crawler.py [options]`.
There are several options required to work.
Run `python3 crawler.py -h` for a help menu and see which ones are important for you.

## Tested StudIP instances

- Carl von Ossietzky Universität Oldenburg
