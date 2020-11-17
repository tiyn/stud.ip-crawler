import time
import logging as log

#from tqdm import tqdm
import requests as req
from requests.auth import HTTPBasicAuth
import json


class Studip:

    def __init__(self, chunk_size, domain, user, db):
        self.CHUNK_SIZE = chunk_size
        self.DOMAIN = domain
        self.USER = user
        self.db = db

    def auth_req(self, url):
        """Creates a request for a user.

        Parameter:
        url(string): URL to send the request to

        Returns:
        string: request
        """
        url = self.DOMAIN + url
        return req.get(url, auth=self.USER)

    def get_uid(self):
        """Get the user id of the user specified in the object.

        Returns:
        string: user id
        """
        rsp = self.auth_req('/api.php/user/')
        user_id = rsp.json()['user_id']
        return user_id

    def get_curr_semester(self):
        """Get the current semester of the studip instance specified in the object.

        Returns:
        string: id for current semester
        """
        rsp = self.auth_req('/api.php/semesters/')
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
        """Get the a list of semesters of studip instance specified in the object.

        Returns:
        list(string): all semesters of the user
        """
        rsp = self.auth_req('/api.php/semesters/')
        semesters = rsp.json()['collection']
        order_sems = []
        for sem_uri in semesters:
            order_sems.append(sem_uri)
        return order_sems

    def get_curr_courses(self, user_id, semester):
        """Get the a list of semesters of studip instance specified in the object.

        Returns:
        string: id of the current semester
        """
        rsp = self.auth_req('/api.php/user/' + user_id + '/courses?limit=1000')
        ord_sems = self.get_ordered_semesters()
        courses = rsp.json()['collection']
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
                log.info(course_title + " will be downloaded")
                course_id = course['course_id']
                course_list[course_id] = course_title
        return course_list

    def get_top_folder(self, course):
        """Retrieves the top folder id of a given course.

        Parameters:
        course (string): course to get the top folder of

        Returns:
        string: id of the top folder
        """
        rsp = self.auth_req('/api.php/course/' + course + '/top_folder')
        top_folder = rsp.json()
        tf_id = top_folder['id']
        return(tf_id)

    def get_docs(self, folder):
        """Get all the documents of a given folder.

        Parameters:
        folder(string): id of the folder to get documents of

        Returns:
        list(string): ids of the documents
        """
        rsp = self.auth_req('/api.php/folder/' + folder)
        res_docs = []
        try:
            docs = rsp.json()['file_refs']
        except ValueError:
            return res_docs
        for doc in docs:
            try:
                doc_id = doc['id']
                res_docs.append(doc_id)
            except KeyError:
                return res_docs
        return(res_docs)

    def download(self, doc):
        """Download a document.

        Parameters:
        doc (string): id of the document to download
        """
        rsp1 = self.auth_req('/api.php/file/' + doc)
        doc_name = rsp1.json()['name']
        doc_chdate = rsp1.json()['chdate']
        last_dl = self.db.get_last_file_dl(doc)
        if last_dl == None or last_dl < doc_chdate:
            rsp2 = self.auth_req('/api.php/file/' + doc + '/download')
            log.info('downloading ' + doc_name)
            try:
                with open(doc_name, 'wb') as doc_file:
                    for chunk in rsp2.iter_content(self.CHUNK_SIZE):
                        doc_file.write(chunk)
                self.db.set_last_file_dl(str(doc), str(int(time.time())))
            except OSError:
                log.warning("Error while writing to the file " + doc_name)

    def get_subdirs(self, folder):
        """Get all the subdirectories of a given folder.

        Parameters:
        folder(string): id of the folder to get subdirectories of

        Returns:
        list(string): ids of the subdirectories
        """
        res_subdirs = {}
        rsp = self.auth_req('/api.php/folder/' + folder)
        try:
            subdirs = rsp.json()['subfolders']
        except ValueError:
            return res_subdirs
        for subdir in subdirs:
            try:
                sub_id = subdir['id']
                sub_name = subdir['name']
                res_subdirs[sub_id] = sub_name
            except KeyError:
                return res_subdirs
        return res_subdirs
