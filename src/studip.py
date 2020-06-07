#!/bin/env python3
import time
import os
import argparse

from tqdm import tqdm
import requests as req
from requests.auth import HTTPBasicAuth


class Crawler:

    def __init__(self, db):
        self.CHUNK_SIZE = None
        self.STUDIP_DOMAIN = None
        self.USER = None
        self.db = db

    def create_dir(self, dir):
        if not os.path.exists(dir):
            print('creating folder', dir)
            os.mkdir(dir)

    def get_uid(self):
        url = self.STUDIP_DOMAIN + '/api.php/user/'
        rsp = req.get(url, auth=self.USER)
        user_id = rsp.json()['user_id']
        return user_id

    def get_curr_semester(self):
        url = self.STUDIP_DOMAIN + '/api.php/semesters/'
        rsp = req.get(url, auth=self.USER)
        curr_time = int(str(int(time.time())))
        semesters = rsp.json()['collection']
        for sem_uri in semesters:
            semester = semesters[sem_uri]
            sem_begin = semester['begin']
            sem_end = semester['end']
            if sem_begin < curr_time < sem_end:
                return sem_uri
        return 0

    def get_ordered_semesters(self):
        url = self.STUDIP_DOMAIN + '/api.php/semesters/'
        rsp = req.get(url, auth=self.USER)
        semesters = rsp.json()['collection']
        order_sems = []
        for sem_uri in semesters:
            order_sems.append(sem_uri)
        return order_sems

    def get_curr_courses(self, user_id, semester):
        url = self.STUDIP_DOMAIN + '/api.php/user/' + user_id + '/courses'
        rsp = req.get(url, auth=self.USER)
        ord_sems = self.get_ordered_semesters()
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

    def get_top_folder(self, course):
        url = self.STUDIP_DOMAIN + '/api.php/course/' + course + '/top_folder'
        rsp = req.get(url, auth=self.USER)
        top_folder = rsp.json()
        tf_id = top_folder['id']
        return(tf_id)

    def get_docs(self, folder):
        url = self.STUDIP_DOMAIN + '/api.php/folder/' + folder
        rsp = req.get(url, auth=self.USER)
        docs = rsp.json()['file_refs']
        res_docs = []
        for doc in docs:
            doc_id = doc['id']
            res_docs.append(doc_id)
        return(res_docs)

    def download(self, doc):
        url1 = self.STUDIP_DOMAIN + '/api.php/file/' + doc
        rsp1 = req.get(url1, auth=self.USER)
        doc_name = rsp1.json()['name']
        doc_chdate = rsp1.json()['chdate']
        last_dl = self.db.get_last_file_dl(doc)
        if last_dl == None or last_dl < doc_chdate:
            print('downloading ', doc_name)
            url2 = self.STUDIP_DOMAIN + '/api.php/file/' + doc + '/download'
            rsp2 = req.get(url2, auth=self.USER, stream=True)
            total_size = int(rsp2.headers.get('content-length', 0))
            progbar = tqdm(total=total_size, unit='iB', unit_scale=True)
            with open(doc_name, 'wb') as doc_file:
                for chunk in rsp2.iter_content(self.CHUNK_SIZE):
                    progbar.update(len(chunk))
                    doc_file.write(chunk)
            self.db.set_last_file_dl(str(doc), str(int(time.time())))

    def get_subdirs(self, folder):
        url = self.STUDIP_DOMAIN + '/api.php/folder/' + folder
        rsp = req.get(url, auth=self.USER)
        subdirs = rsp.json()['subfolders']
        docs = rsp.json()['file_refs']
        res_subdirs = {}
        for subdir in subdirs:
            sub_id = subdir['id']
            sub_name = subdir['name']
            res_subdirs[sub_id] = sub_name
        return res_subdirs

    def download_folder(self, folder):
        docs = self.get_docs(folder)
        for doc in docs:
            print('found doc ', doc)
            self.download(doc)

    def download_folder_rec(self, folder, base_dir):
        print('folder ', folder)
        self.create_dir(base_dir)
        self.download_folder(folder)
        subdirs = self.get_subdirs(folder)
        os.chdir(base_dir)
        for subdir in subdirs:
            subdir_name = subdirs[subdir].replace('/', '-')
            subdir_path = os.path.join(base_dir, subdir_name)
            print(subdir_path)
            self.create_dir(subdir_path)
            os.chdir(subdir_path)
            self.download_folder_rec(subdir, subdir_path)

    def download_course(self, course, base_dir):
        print('course ', course)
        self.create_dir(base_dir)
        os.chdir(base_dir)
        root = self.get_top_folder(course)
        self.download_folder_rec(root, base_dir)

    def download_curr_courses(self, base_dir):
        print('Start downloading all current courses')
        self.create_dir(base_dir)
        curr_courses = self.get_curr_courses(
            self.get_uid(), self.get_curr_semester())
        os.chdir(base_dir)
        for course in curr_courses:
            print('course is ', curr_courses[course])
            course_name = curr_courses[course].replace('/', '-')
            path = os.path.join(base_dir, course_name)
            self.download_course(course, path)
