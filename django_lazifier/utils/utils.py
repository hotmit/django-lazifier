import pprint
import inspect
from os import path
from collections import OrderedDict
from django.db.models.query import QuerySet
from django.conf import settings
import json
import os
import re

try:
    from django.db.models.query import ValuesQuerySet
except Exception as ex:
    ValuesQuerySet = None


def log_exception(exception):
    if settings and settings.DEBUG:
        p('Exception: %s' % exception)

# region [ Print Function ]
def p(*args, **kwargs):
    """
    Pretty print the object for debug
    :param obj:
    :return:
    """
    (frame, filename, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

    print(':: [%s] => %s:%s' % (path.basename(filename), function_name, line_number))
    if not args:
        pass

    first = True
    for obj in args:
        if obj is None:
            print('None')

        if first and isinstance(obj, str) and len(args) > 1:
            print('%s: ' % obj)
            first = False
            continue

        first = False

        if isinstance(obj, QuerySet) or isinstance(obj, list) or \
                (ValuesQuerySet is not None and isinstance(obj, ValuesQuerySet)):
            result = '[ len=%s\n' % len(obj)
            index = 0
            for o in obj:
                o = pprint.pformat(o, indent=1, compact=False).strip()
                result += '    [%s] %s,\n' % (index, o)
                index += 1
            result += ']\n'
            print(result)
        elif isinstance(obj, dict) or type(obj) == OrderedDict:
            result = '{ len=%s\n' % len(obj)
            index = 0
            for k, o in obj.items():
                o = pprint.pformat(o, indent=1, compact=False).strip()
                result += '    [%s] \'%s\': %s,\n' % (index, k, o)
                index += 1
            result += '}\n'
            print(result)
        else:
            opts = {
                'indent': 1,
            }
            opts.update(kwargs)
            pprint.pprint(obj, **opts)
# endregion


# region [ IOFunc ]
class IOFunc:
    @classmethod
    def get_abs_path(cls, relative_root, relative_path):
        rel_dir = path.dirname(path.abspath(relative_root))
        return path.join(rel_dir, relative_path)

    @classmethod
    def file_exist(cls, file_path):
        """
        Test to see if the file exist (only file, not directory).

        :param file_path: file path
        :return: bool
        """
        return os.path.isfile(file_path)  # this test for exist and path is not a dir

    @classmethod
    def create_directories(cls, folder_path: str, mode=0o777, exist_ok=True):
        """
        Create all the folder recursively.

        :param folder_path:
        :param mode:
        :param exist_ok:
        :return:
        """
        os.makedirs(folder_path, mode, exist_ok)

    @classmethod
    def directory_exist(cls, folder_path):
        """
        Test to see if the directory exist

        :param folder_path:
        :return:
        """
        return os.path.isdir(folder_path)

    @classmethod
    def write_file(cls, file_path, content):
        """
        Write text to a file
        :param file_path:
        :param content:
        :return: bool
        """
        try:
            with open(file_path, 'w') as f:
                f.write(content)
        except:
            return False

        return True

    @classmethod
    def append_file(cls, file_path, content):
        """
        Append content to existing file.

        :param file_path: file path
        :param content: the string
        :return: bool
        """
        try:
            with open(file_path, 'a') as f:
                f.write(content)
        except:
            return False

        return True

    @classmethod
    def read_file(cls, file_path, default_value=''):
        """
        Read file content

        :param file_path:
        :type default_value: str | None
        :param default_value:
        :return:
        """
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except IOError:
            return default_value

    @classmethod
    def read_lines(cls, file_path):
        """
        Get all lines in the specified file

        :param file_path:
        :return:
        """
        try:
            with open(file_path) as f:
                result = f.readlines()
        except IOError:
            return []

        return result

    @classmethod
    def read_json(cls, file_path, default_value=None):
        """
        Read the file and parse the content for json object

        :param file_path:
        :param default_value:
        :return:
        """
        txt = IOFunc.read_file(file_path, None)

        if not txt:
            return default_value

        try:
            return json.loads(txt)
        except ValueError as ex:
            print('Error: %s' % ex)
            return default_value

    @classmethod
    def file_list(cls, folder_path, regex_filter=None, include_path=True, recursive=False):
        """
        Get the list of file inside a directory.

        :param folder_path: folder path
        :param regex_filter: regex to match the file name, None to get all files.
        :param include_path: append the root to the file name (ie return full path)
        :param recursive: search main and sub directories
        :return: list of string
        """
        result = []
        if not IOFunc.directory_exist(folder_path):
            return result

        if not recursive:
            result = os.listdir(folder_path)
            if regex_filter:
                result = [f for f in result if re.search(regex_filter, f, re.I) is not None]
            if include_path:
                result = [os.path.join(folder_path, f) for f in result]
            return result

        # recursive
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                file_name = f
                if not regex_filter or re.search(regex_filter, file_name, re.I):
                    if include_path:
                        file_name = os.path.join(root, file_name)
                    result.append(file_name)
        return result

    @classmethod
    def sort_file_list_by_mtime(cls, file_list: list, ascending=True, root_path=None):
        """
        Sort list of file by the modification time.

        :param file_list: list of file, relative or absolute path (if relative it requires root_path)
        :param ascending: True to sort oldest to newest, else newest to oldest
        :param root_path: if files in file_list is not absolute path, use this folder as the parent
        :return: sorted list by age
        """
        reverse = not ascending
        return sorted(file_list,
                      key=lambda f: os.path.getmtime(f)
                      if not root_path
                      else os.path.getmtime(os.path.join(root_path, f)),
                      reverse=reverse)

    @classmethod
    def sort_file_list_by_ctime(cls, file_list: list, ascending=True, root_path=None):
        """
        Sort list of file by the creation time.

        :param file_list: list of file, relative or absolute path (if relative it requires root_path)
        :param ascending: True to sort oldest to newest, else newest to oldest
        :param root_path: if files in file_list is not absolute path, use this folder as the parent
        :return: sorted list by age
        """
        reverse = not ascending
        return sorted(file_list,
                      key=lambda f: os.path.getctime(f)
                      if not root_path
                      else os.path.getctime(os.path.join(root_path, f)),
                      reverse=reverse)

    @classmethod
    def move_file(cls, src_file, target_folder):
        """
        Move file to target folder

        :param src_file:
        :param target_folder:
        :return:
        """
        IOFunc.create_directories(target_folder)
        file_name = os.path.basename(src_file)

        os.rename(src_file, os.path.join(target_folder, file_name))

# endregion
