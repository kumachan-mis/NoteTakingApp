#!/usr/local/bin/python3
from os import path


class PathData:
    def __init__(self, is_new, pdf_path='', file_path=''):
        super().__init__()
        self.is_new = is_new
        self.pdf_path = pdf_path
        self.file_path = file_path
        self.image_dir_path = ''
        self.file_name = ''
        self.set_pdf_image_dir_path(pdf_path)
        self.set_file_path_name(file_path)

    def set_pdf_image_dir_path(self, pdf_path):
        if pdf_path == '':
            return

        self.pdf_path = pdf_path
        filename = path.splitext(path.split(self.pdf_path)[1])[0]
        self.image_dir_path = path.join('../images', filename)

    def set_file_path_name(self, file_path):
        if file_path == '':
            return

        self.file_path = file_path
        self.file_name = path.splitext(path.split(self.file_path)[1])[0]