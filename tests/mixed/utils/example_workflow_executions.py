"""Class responsible for implementing example executions of atm workflows
uses its example input files, returning dict which can be passed into
REST request.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import os
from collections.abc import Callable
from typing import Optional

from tests.conftest import JsonValue
from tests.gui.utils.generic import upload_workflow_path

type StoreContent = dict[str, JsonValue]
type InputFiles = list[str]
type ExecutionResult = tuple[list[StoreContent], InputFiles | list[InputFiles]]
type ResolveId = Callable[[str], str]
type UploadFile = Callable[[str, str], None]


class ExampleWorkflowExecutionInitialStoreContent:

    def __init__(
        self,
        resolve_file_id: ResolveId,
        upload_file: UploadFile,
        resolve_group_id: Optional[ResolveId] = None,
    ) -> None:
        self.resolve_file_id = resolve_file_id
        self.upload_file = upload_file
        self.resolve_group_id = resolve_group_id

    @staticmethod
    def gather_input_files(workflow: str) -> InputFiles:
        return [
            f
            for f in os.listdir(upload_workflow_path(workflow))
            if f != workflow + ".json"
        ]

    def bagit_uploader(
        self, input_file: Optional[InputFiles] = None, dest_dir: str = "space1/dir1"
    ) -> ExecutionResult:
        input_files = (
            self.gather_input_files("bagit-uploader") if not input_file else input_file
        )
        for file in input_files:
            path = upload_workflow_path("bagit-uploader") + "/" + file
            self.upload_file(path, file)
        file_paths = [f'{dest_dir.split("/")[0]}/{file}' for file in input_files]

        return [
            {
                "input-bagit-archives": {"fileId": self.resolve_file_id(path)},
                "destination-directory": {"fileId": self.resolve_file_id(dest_dir)},
            }
            for path in file_paths
        ], input_files

    def detect_file_formats(
        self, input_file: Optional[InputFiles] = None, space: str = "space1"
    ) -> ExecutionResult:
        input_files = (
            self.gather_input_files("detect-file-formats")
            if not input_file
            else input_file
        )
        for file in input_files:
            path = upload_workflow_path("detect-file-formats") + "/" + file
            self.upload_file(path, file)
        file_paths = [f"{space}/{file}" for file in input_files]
        return [
            {"input-files": [{"fileId": self.resolve_file_id(path)}]}
            for path in file_paths
        ], input_files

    def detect_file_mime_formats(
        self, input_file: Optional[InputFiles] = None, space: str = "space1"
    ) -> ExecutionResult:
        input_files = (
            self.gather_input_files("detect-file-mime-formats")
            if not input_file
            else input_file
        )
        for file in input_files:
            path = upload_workflow_path("detect-file-mime-formats") + "/" + file
            self.upload_file(path, file)
        file_paths = [f"{space}/{file}" for file in input_files]
        return [
            {"input-files": [{"fileId": self.resolve_file_id(path)}]}
            for path in file_paths
        ], input_files

    def download_files(
        self,
        input_file: Optional[InputFiles] = None,
        destination: str = "space1/dir1",
    ) -> ExecutionResult:
        input_files = (
            self.gather_input_files("download-files") if not input_file else input_file
        )
        for file in input_files:
            path = upload_workflow_path("download-files") + "/" + file
            self.upload_file(path, file)
        file_paths = [f'{destination.split("/")[0]}/{file}' for file in input_files]
        return [
            {
                "fetch-files": [{"fileId": self.resolve_file_id(path)}],
                "destination": {"fileId": self.resolve_file_id(destination)},
            }
            for path in file_paths
        ], input_files

    def calculate_checksums_mounted(
        self, input_file: str = "space1/file1"
    ) -> ExecutionResult:
        return [{"input-files": [{"fileId": self.resolve_file_id(input_file)}]}], [
            input_file
        ]

    def calculate_checksums_rest(
        self, input_file: str = "space1/file1"
    ) -> ExecutionResult:
        return [{"input-files": [{"fileId": self.resolve_file_id(input_file)}]}], [
            input_file
        ]

    def demo(self, input_file: str = "space1/dir1") -> ExecutionResult:
        return [{"input_files": [{"fileId": self.resolve_file_id(input_file)}]}], [
            input_file
        ]

    def echo(self, input_file: str = "space1/file1") -> ExecutionResult:
        return [{"input": [{"fileId": self.resolve_file_id(input_file)}]}], [input_file]

    def initialize_eureka3D_project(  # pylint: disable=invalid-name
        self,
        parent_directory: str = "space1/dir1",
        project_name: str = "hello",
        group: str = "group1",
    ) -> ExecutionResult:
        if self.resolve_group_id is None:
            raise RuntimeError("Group ID resolver is required for this workflow")
        return [
            {
                "Parent directory": {"fileId": self.resolve_file_id(parent_directory)},
                "Project name": project_name,
                "Managing groups": [{"groupId": self.resolve_group_id(group)}],
            }
        ], []

    def substitute_placeholders_example(self, name: str = "Tom") -> ExecutionResult:
        return [{"input-store": {"name": name}}], []

    def annotate_images(
        self, input_file: Optional[InputFiles] = None, space: str = "space1"
    ) -> ExecutionResult:
        input_files = (
            self.gather_input_files("annotate-images") if not input_file else input_file
        )
        for file in input_files:
            path = upload_workflow_path("annotate-images") + "/" + file
            self.upload_file(path, file)
        file_paths = [f"{space}/{file}" for file in input_files]

        return [
            {"Files to process": [{"fileId": self.resolve_file_id(path)}]}
            for path in file_paths
        ], [file_paths]
