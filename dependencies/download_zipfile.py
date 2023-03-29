from zipfile import ZipFile
from zipfile import BadZipfile
from requests import get
from io import BytesIO


def download_zipfile(file_url: str) -> ZipFile or None:
    """
    Download ZipFile function help us to download any valid zipfile from online.
    and return a valid ZipFile object of zipfile module.
    If we import a invalid zipfile path or url, then it will return None instead of Zipfile object
    :param file_url: Here we should put a valid zipfile url. For example: https://data.bus-data.dft.gov.uk/gtfs.zip
    :return: Zipfile object if no error found else return None
    """

    try:
        response = get(url=file_url, stream=True)  # get response form url

        total_length = response.headers.get('content-length')  # total size of the file
    except Exception as e:
        print(e)
        return None

    if not total_length:
        return None

    else:

        buffer = BytesIO()

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                buffer.write(chunk)
            else:
                pass

        buffer.seek(0)

        try:
            return ZipFile(file=buffer)
        except BadZipfile:
            return None
