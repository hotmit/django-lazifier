from datetime import datetime
import pprint
import inspect
from os import path
from collections import OrderedDict
from django.db.models.query import QuerySet
from django.conf import settings
import json
import os
import re
import pytz
import shutil
from django_lazifier.utils.builtin_types.datetime import Dt
from django_lazifier.utils.builtin_types.dict import Dct
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.json.json_encoder import JsonEncoder

try:
    from django.db.models.query import ValuesQuerySet
except Exception as ex:
    ValuesQuerySet = None


def log_exception(exception):
    if settings and settings.DEBUG:
        p('Exception: %s' % exception)

# region [ Print Function ]
def d(obj, header='', indent=2, **kwargs):
    """
    Var dumps

    :param obj: the object you want to print
    :param indent: indent the json output
    :param header: the text in front of the printout of the object
    :param kwargs: any custom argument to mark the name or key related to the object
    """
    custom_param = ''
    if kwargs:
        custom_param = ' (%s)' % ', '.join(['{}={}'.format(k, v) for k, v in kwargs.items()])

    if type(obj) is str or type(obj) is int or type(obj) is float:
        if header:
            print('{}{} -> {}'.format(header, custom_param, str(obj)))
        else:
            print(str(obj))
        return

    if not isinstance(obj, list) and not isinstance(obj, dict):
        obj = Obj.get_dict(obj)

    if header:
        print('{}{} -> '.format(header, custom_param))
    print(json.dumps(obj, cls=JsonEncoder, skipkeys=True, indent=indent))


def p(*args, **kwargs):
    """
    Pretty print the object for debug
    :param kwargs:
    :param args:
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


# region [ Input & Output ]
class IOFunc:
    """
    General IO function. eg. File reading/writing
    """
    TZ_UTC = pytz.utc
    TZ_LOG = pytz.timezone('America/New_York')

    @classmethod
    def get_abs_path(cls, relative_root, relative_path):
        """
        Get the absolute path of the file

        :param relative_root: the reference root of the relative path
        :param relative_path: the relative path to the root
        :rtype: str
        """
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
        Write text to a file (overwrite if file already exist)

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
    def move_file(cls, src_file, target_folder, overwrite=True):
        """
        Move file to target folder

        :param src_file:
        :param target_folder:
        :param overwrite:
        :rtype: str
        :return: return the location of the new path
        """
        IOFunc.create_directories(target_folder)
        file_name = os.path.basename(src_file)

        target_file = os.path.join(target_folder, file_name)

        if IOFunc.file_exist(target_file) and overwrite:
            os.remove(target_file)

        os.rename(src_file, target_file)
        return target_file

    @classmethod
    def remove_directory(cls, folder_path):
        """
        Remove folder (it doesn't have to be emptied)

        :param folder_path:
        :return:
        """
        try:
            shutil.rmtree(folder_path)
            return True
        except Exception as ex:
            return False

    @classmethod
    def remove_file(cls, file_path):
        """
        Remove file

        :param file_path: full file path
        :rtype: bool
        """

        if cls.file_exist(file_path):
            try:
                os.remove(file_path)
            except Exception as ex:
                return False
        return True

    @classmethod
    def rename_directory(cls, old, dst):
        """
        Rename a directory.

        :param old: full path src
        :param dst: full path destination
        :return:
        """
        try:
            os.rename(old, dst)
            return True
        except Exception as ex:
            return False

    @classmethod
    def write_log(cls, log_file_path, log_text, log_max_size=5, **kwargs):
        """
        Write log to file

        :param log_file_path: full file path
        :param log_text: the text content
        :param log_max_size: max size(in mb) of log file before move log file to .bak
        :param kwargs: any key, value item you want to append to the text field
        """
        try:
            if isinstance(log_text, Exception):
                try:
                    frames = inspect.getouterframes(inspect.currentframe())
                    frame, filename, line_number, function_name, lines, index = frames[1]

                    if function_name == 'write_log' and len(frames) > 2:
                        frame, filename, line_number, function_name, lines, index = frames[2]

                    log_text = 'Exception: {msg} ({filename}, {function_name}()::{line_number})'\
                        .format(msg=str(log_text), filename=path.basename(filename),
                                function_name=function_name, line_number=line_number)
                except Exception as ex:
                    print('IOFunc.write_log(): ' + ex.__str__())

            if kwargs:
                if log_text:
                    log_text = '. '.join([str(log_text), Dct.to_string(kwargs)])
                else:
                    log_text = Dct.to_string(kwargs)

            dir_path = os.path.dirname(log_file_path)
            cls.create_directories(dir_path)

            now = datetime.utcnow()
            utc_now = Dt.replace_tzinfo(now, cls.TZ_UTC)
            log_tz_time = utc_now.astimezone(cls.TZ_LOG)

            log_text = '{date:%Y-%m-%d %H:%M:%S %Z%z}\t{content}\n'.format(date=log_tz_time, content=log_text)

            if cls.file_exist(log_file_path):
                max_size_in_byte = log_max_size * 1048576
                if os.path.getsize(log_file_path) > max_size_in_byte:
                    bak_file_path = log_file_path + '.bak'
                    cls.remove_file(bak_file_path)
                    os.rename(log_file_path, bak_file_path)

            cls.append_file(log_file_path, log_text)
        except Exception as ex:
            print('IOFunc.write_log(): ' + ex.__str__())
# endregion
