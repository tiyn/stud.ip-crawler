import os
import logging as log

from studip import Studip


class Crawler:

    def __init__(self, studip):
        self.studip = studip

    def download_folder(self, folder):
        docs = self.studip.get_docs(folder)
        for doc in docs:
            log.info('found doc ' + doc)
            self.studip.download(doc)

    def download_folder_rec(self, folder, base_dir):
        log.info('crawling folder ' + folder)
        self.create_dir(base_dir)
        self.download_folder(folder)
        subdirs = self.studip.get_subdirs(folder)
        os.chdir(base_dir)
        for subdir in subdirs:
            subdir_name = subdirs[subdir].replace('/', '-')
            subdir_path = os.path.join(base_dir, subdir_name)
            log.debug(subdir_path)
            self.create_dir(subdir_path)
            os.chdir(subdir_path)
            self.download_folder_rec(subdir, subdir_path)

    def download_course(self, course, base_dir):
        log.info('crawling course ' + course)
        self.create_dir(base_dir)
        os.chdir(base_dir)
        root = self.studip.get_top_folder(course)
        self.download_folder_rec(root, base_dir)

    def download_curr_courses(self, base_dir):
        log.info('Start crawling all current courses')
        self.create_dir(base_dir)
        curr_courses = self.studip.get_curr_courses(
            self.studip.get_uid(), self.studip.get_curr_semester())
        os.chdir(base_dir)
        for course in curr_courses:
            log.debug('course is ' + curr_courses[course])
            course_name = curr_courses[course].replace('/', '-')
            path = os.path.join(base_dir, course_name)
            self.download_course(course, path)

    def create_dir(self, dir):
        if not os.path.exists(dir):
            log.info('creating folder' + dir)
            os.mkdir(dir)
