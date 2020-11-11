# Stud.IP Crawler

![stud.ip-crawler-logo](studip_crawler.png)

This is a program that downloads all files available for a given Stud.IP user.
It only downloads and searches through the courses in the current semester.
If you run the program again it only downloads files that have changed since
the last time running it.

## Features/To-Dos

- [x] Downloads files of given users active semester via commandline
  - [x] Keeping file structure of Stud.IP
  - [x] Specify username
  - [x] Specify password
  - [x] Specify Stud.IP-URL
  - [x] Specify output directory
  - [x] Specify chunk size to download big files
  - [x] Specify all important database variables
- [x] Only download files after given date
  - [x] Save and read download date
  - [x] Possible reset of download date
- [x] Incremental file download
  - [x] Store id and chdate of downloaded files
- [x] Logging
  - [x] Console log
  - [x] Log file
  - [x] Specify log level
- [x] Docker
  - [x] DockerHub image
  - [x] Docker-compose with db

### Errors and workarounds

- [ ] If filename is too long it currently gets skipped
- [ ] Filenames get sometimes displayed wrong (probably utf8 problems)

## Installation

- create an instance of a mysql database
- `git clone https://github.com/tiyn/studip-crawler`
- `cd studip-crawler/src/`
- `pip3install -r requirements` - install dependencies

## Usage

Just run the file via `python3 run.py [options]`.
Alternatively to `python3 run.py` you can give yourself permissions using
`chmod +x run.py [options]` and
run it with `./run.py [options]`.
There are several options required to work.
Run `python3 run.py -h` for a help menu and see which ones are important for you.

### Docker

#### Environment-variables

Set the following variables with the -e tag.
| Name | Usage | Default |
| ---- |------ | ------- |
| `USER` | username on the studip server | `admin` |
| `PSWD` | password on the studip server | `admin` |
| `URL` | url of the studip server | `admin` |
| `HOST` | ip of the mysql instance to connect | `mysql` |
| `DB_USER` | username of the mysql instance to connect | `root` |
| `DB_PSWD` | password of the mysql instance to connect | `root` |
| `INTERVAl` | update interval in seconds | `86400` |

#### Volumes

Set the following volumes with the -v tag.
| Volume-Name | Container mount | Description |
| ----------- | --------------- | ----------------------------------- |
| `studip_data` | `/studip/src/data` | directory for studip files to be saved to |

#### docker-compose.yml

Copy `docker-compose.yml` and change it to your needs.
Then run `docker-compose up`.

## Tested StudIP instances

- Carl von Ossietzky Universität Oldenburg
