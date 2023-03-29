from zipfile import ZipFile


def extract_zipfile(_zipfile: ZipFile, *selected_filenames):
    """
    This function help us to get specific files object based on specific file name

    This function look for all the selected_filenames items inside the _zipfile. if someone is fully matched then return
    the filename with the content otherwise pass
    :param _zipfile: Which zipfile object we want to use
    :param selected_filenames: List of selected file names as args
    :return: Return a generator of filename and file object
    """

    for filename in selected_filenames:
        if filename in _zipfile.namelist():
            with _zipfile.open(name=filename, mode='r') as zipfile_content:
                yield filename, zipfile_content
        else:
            pass
