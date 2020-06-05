#!/bin/env python3
import time
import os
import argparse

from tqdm import tqdm
import requests as req
from requests.auth import HTTPBasicAuth


def create_dir(dir):
    if not os.path.exists(dir):
        print('creating folder', dir)
        os.mkdir(dir)


def set_last_dl(time):
    last_dl_file = open('last_dl.txt', 'w')
    last_dl_file.write(str(time).split('.')[0])


def get_last_dl():
    try:
        last_dl_file = open('last_dl.txt', 'r')
        return int(last_dl_file.read())
    except:
        return None

parser = argparse.ArgumentParser(description='Download Files from StudIP.')
parser.add_argument('-o', '--output', type=str,
                    default='./data', help='path to output directory')
parser.add_argument('-u', '--user', type=str, help='studip username', required=True)
parser.add_argument('-p', '--passw', type=str, help='studip password', required=True)
parser.add_argument('-s', '--url', type=str, help='studip url', required=True)
parser.add_argument('-c', '--chunk', type=int, default=1024 *
                    1024, help='chunksize for downloading data')
parser.add_argument('-r', '--reset_dl_date', action='store_true')

args = parser.parse_args()

BASE_DIR = os.path.abspath(args.output)
CHUNK_SIZE = args.chunk
STUDIP_DOMAIN = args.url
USERNAME = args.user
PASSWORD = args.passw
USER = (USERNAME, PASSWORD)
if args.reset_dl_date:
    set_last_dl(None)
LAST_DOWNLOAD = get_last_dl()


def get_uid():
    url = STUDIP_DOMAIN + '/api.php/user/'
    rsp = req.get(url, auth=USER)
    user_id = rsp.json()['user_id']
    return user_id


def get_curr_semester():
    url = STUDIP_DOMAIN + '/api.php/semesters/'
    rsp = req.get(url, auth=USER)
    curr_time = int(str(time.time()).split('.')[0])
    semesters = rsp.json()['collection']
    for sem_uri in semesters:
        semester = semesters[sem_uri]
        sem_begin = semester['begin']
        sem_end = semester['end']
        if sem_begin < curr_time < sem_end:
            return sem_uri
    return 0


def get_ordered_semesters():
    url = STUDIP_DOMAIN + '/api.php/semesters/'
    rsp = req.get(url, auth=USER)
    semesters = rsp.json()['collection']
    order_sems = []
    for sem_uri in semesters:
        order_sems.append(sem_uri)
    return order_sems


def get_curr_courses(user_id, semester):
    url = STUDIP_DOMAIN + '/api.php/user/' + user_id + '/courses'
    rsp = req.get(url, auth=USER)
    ord_sems = get_ordered_semesters()
    courses = rsp.json()['collection']
    i = 0
    course_list = {}
    for course_uri in courses:
        course = courses[course_uri]
        start_sem = course['start_semester']
        if start_sem != None:
            start_ind = ord_sems.index(start_sem)
        else:
            start_ind = 100
        end_sem = course['end_semester']
        if end_sem != None:
            end_ind = ord_sems.index(end_sem)
        else:
            end_ind = 100
        curr_ind = ord_sems.index(semester)
        if start_ind <= curr_ind <= end_ind:
            course_title = course['title']
            course_id = course['course_id']
            course_list[course_id] = course_title
    return course_list


def get_top_folder(course):
    url = STUDIP_DOMAIN + '/api.php/course/' + course + '/top_folder'
    rsp = req.get(url, auth=USER)
    top_folder = rsp.json()
    tf_id = top_folder['id']
    return(tf_id)


def get_docs(folder):
    url = STUDIP_DOMAIN + '/api.php/folder/' + folder
    rsp = req.get(url, auth=USER)
    docs = rsp.json()['file_refs']
    res_docs = []
    for doc in docs:
        doc_id = doc['id']
        res_docs.append(doc_id)
    return(res_docs)


def download(doc, time):
    url1 = STUDIP_DOMAIN + '/api.php/file/' + doc
    rsp1 = req.get(url1, auth=USER)
    doc_name = rsp1.json()['name']
    doc_chdate = rsp1.json()['chdate']
    if time == None or time < doc_chdate:
        print('downloading ', doc_name)
        url2 = STUDIP_DOMAIN + '/api.php/file/' + doc + '/download'
        rsp2 = req.get(url2, auth=USER, stream=True)
        total_size = int(rsp2.headers.get('content-length', 0))
        progbar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(doc_name, 'wb') as doc:
            for chunk in rsp2.iter_content(CHUNK_SIZE):
                progbar.update(len(chunk))
                doc.write(chunk)


def get_subdirs(folder):
    url = STUDIP_DOMAIN + '/api.php/folder/' + folder
    rsp = req.get(url, auth=USER)
    subdirs = rsp.json()['subfolders']
    docs = rsp.json()['file_refs']
    res_subdirs = {}
    for subdir in subdirs:
        sub_id = subdir['id']
        sub_name = subdir['name']
        res_subdirs[sub_id] = sub_name
    return res_subdirs


def download_folder(folder, time):
    docs = get_docs(folder)
    for doc in docs:
        print('found doc ', doc)
        download(doc, time)


def download_folder_rec(folder, time, base_dir):
    print('folder ', folder)
    create_dir(base_dir)
    download_folder(folder, time)
    subdirs = get_subdirs(folder)
    os.chdir(base_dir)
    for subdir in subdirs:
        subdir_name = subdirs[subdir].replace('/', '-')
        subdir_path = os.path.join(base_dir, subdir_name)
        print(subdir_path)
        create_dir(subdir_path)
        os.chdir(subdir_path)
        download_folder_rec(subdir, time, subdir_path)


def download_course(course, time, base_dir):
    print('course ', course)
    create_dir(base_dir)
    os.chdir(base_dir)
    root = get_top_folder(course)
    download_folder_rec(root, time, base_dir)


def download_curr_courses(time, base_dir):
    print('Start downloading all current courses')
    create_dir(base_dir)
    curr_courses = get_curr_courses(get_uid(), get_curr_semester())
    os.chdir(base_dir)
    for course in curr_courses:
        print('course is ', curr_courses[course])
        course_name = curr_courses[course].replace('/', '-')
        path = os.path.join(base_dir, course_name)
        download_course(course, time, path)


download_curr_courses(LAST_DOWNLOAD, BASE_DIR)
set_last_dl(time.time())
