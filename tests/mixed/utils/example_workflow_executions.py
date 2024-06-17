"""Class responsible for implementing default executions of atm workflows
 uses its default input files, returning dict which can be passed into
 REST request.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import os
from tests.gui.utils.generic import upload_workflow_path


class ExampleWorkflowExecutionInitialStoreContent:

    def __init__(self, resolve_file_id, upload_file, resolve_group_id=None):
        self.resolve_file_id = resolve_file_id
        self.upload_file = upload_file
        self.resolve_group_id = resolve_group_id

    @staticmethod
    def gather_input_files(workflow):
        return [f for f in os.listdir(upload_workflow_path(workflow)) if
                f != workflow + '.json']

    def bagit_uploader(self, input_file=None, dest_dir='space1/dir1'):
        input_files = self.gather_input_files(
            'bagit-uploader') if not input_file else input_file
        for file in input_files:
            path = upload_workflow_path('bagit-uploader') + '/' + file
            self.upload_file(path, file)
        file_paths = [f'{dest_dir.split("/")[0]}/{file}' for file in input_files]

        return [{
                'input-bagit-archives': {'fileId': self.resolve_file_id(path)},
                'destination-directory': {'fileId': self.resolve_file_id(dest_dir)}
        } for path in file_paths], input_files

    def detect_file_formats(self, input_file=None, space='space1'):
        input_files = self.gather_input_files(
            'detect-file-formats') if not input_file else input_file
        for file in input_files:
            path = upload_workflow_path('detect-file-formats') + '/' + file
            self.upload_file(path, file)
        file_paths = [f'{space}/{file}' for file in input_files]
        return [{
                'input-files': [{'fileId': self.resolve_file_id(path)}]
        } for path in file_paths], input_files

    def detect_file_mime_formats(self, input_file=None, space='space1'):
        input_files = self.gather_input_files(
            'detect-file-mime-formats') if not input_file else input_file
        for file in input_files:
            path = upload_workflow_path('detect-file-mime-formats') + '/' + file
            self.upload_file(path, file)
        file_paths = [f'{space}/{file}' for file in input_files]
        return [{
                'input-files': [{'fileId': self.resolve_file_id(path)}]
        } for path in file_paths], input_files

    def download_files(self, input_file=None, destination='space1/dir1'):
        input_files = self.gather_input_files(
            'download-files') if not input_file else input_file
        for file in input_files:
            path = upload_workflow_path('download-files') + '/' + file
            self.upload_file(path, file)
        file_paths = [f'{destination.split("/")[0]}/{file}' for file in input_files]
        return [{
                'fetch-files': [{'fileId': self.resolve_file_id(path)}],
                'destination': {'fileId': self.resolve_file_id(destination)}
        } for path in file_paths], input_files

    def calculate_checksums_mounted(self, input_file='space1/file1'):
        return [{
                'input-files': [{'fileId': self.resolve_file_id(input_file)}]
        }], [input_file]

    def calculate_checksums_rest(self, input_file='space1/file1'):
        return [{
            'input-files': [{'fileId': self.resolve_file_id(input_file)}]
        }], [input_file]

    def demo(self, input_file='space1/dir1'):
        return [{
            'input_files': [{'fileId': self.resolve_file_id(input_file)}]
        }], [input_file]

    def echo(self, input_file='space1/file1'):
        return [{
            'input': [{'fileId': self.resolve_file_id(input_file)}]
        }], [input_file]

    def initialize_eureka3D_project(self, parent_directory='space1/dir1',
                                    project_name='hello', group='group1'):
        return [{
                'Parent directory': {'fileId': self.resolve_file_id(parent_directory)},
                'Project name': project_name,
                'Managing groups': [{'groupId': self.resolve_group_id(group)}]
        }], []

    def substitute_placeholders_example(self, name='Tom'):
        return [{
            'input-store': {'name': name}
        }], []
