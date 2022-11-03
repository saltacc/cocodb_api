import json

import requests
import mimetypes


class Database:
    _ACCEPTED_INSERT_TYPES = {'.png', '.jpg', '.jpeg', '.webp'}
    _QUERY_META_PATH = '/query/meta/'
    _QUERY_IMAGE_PATH = '/query/image/'
    _QUERY_TOTAL_PATH = '/query/total/'
    _INSERT_PATH = '/scrape/insert'

    '''
            Create an instance of the Database class

                    Parameters:
                            ip (str): server IP address
                            port (int): server port
                            source_name (str): the scraping source name
                            key (str): auth key
                            name (str): username

                    Keyword Arguments:
                            https (bool): use https

                    Returns:
                            database (Database): The created database
            '''

    def __init__(self, ip: str, port: int, source_name: str, key: str, name: str, https: bool = False):
        self._db_url = f"{'https' if https else 'http'}://{ip}:{port}"
        self._source_name = source_name
        self._base_data = {
            "source_name": source_name,
            "key": key,
            "name": name
        }

    '''
        Returns the entry metadata in a JSON file.

                Parameters:
                        entry_id (str): The ID of the entry

                Returns:
                        metadata (json): The metadata of the entry
        '''

    def get_entry_meta(self, entry_id):
        url = self._db_url + self._QUERY_META_PATH + self._source_name + '/' + str(entry_id)
        return json.loads(requests.get(url).text)

    '''
            Get the total amount of images for the current source
                    Returns:
                            count (int): The number of posts in DB for the source
            '''

    def get_entry_total(self):
        url = self._db_url + self._QUERY_TOTAL_PATH + self._source_name
        return int(requests.get(url).text)

    '''
            Returns the image

                    Parameters:
                            entry_id (str): The ID of the entry

                    Keyword Arguments:
                            return_image_ext (bool): return the image extension
                            stream (bool): return the file as a stream

                    Returns:
                            image (bytes): Image as bytes
                            stream (urllib3.response.HTTPResponse): Image stream if stream kwarg is True
                            ext (str): The file extension if return_image_ext kwarg is True
            '''

    def get_entry_image(self, entry_id, return_image_ext=False, stream=False):
        url = self._db_url + self._QUERY_IMAGE_PATH + self._source_name + '/' + str(entry_id)
        if stream:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise Exception(f'DB returned response code {response.status_code}')
            response.raw.decode_content = True
            if return_image_ext:
                return response.raw, mimetypes.guess_extension(response.headers['content-type'])
            return response.raw
        else:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f'DB returned response code {response.status_code}\nINFO: {response.content.decode()}')
            if return_image_ext:
                return response.content, mimetypes.guess_extension(response.headers['content-type'])
            return response.content

    '''
                Uploads an image to the DB

                        Parameters:
                                image (Union[bytes, urllib3.response.HTTPResponse]):
                                file_id (str): The ID of the entry
                                creation_date (int): UNIX timestamp of when the source image was uploaded
                                metadata (dict): A dictionary containing the image metadata
                '''

    def upload_image(self, image, filename, file_id, creation_date, metadata):
        url = self._db_url + self._INSERT_PATH
        # python doesn't implicitly copy
        data = self._base_data.copy()
        data = data | {
            "source_id": file_id,
            "creation_date": creation_date,
            "metadata": json.dumps(metadata)
        }
        response = requests.post(url, files={filename: image}, data=data)
        if 'ok' not in response.content.decode():
            raise Exception(f'Server returned:\n{response.content.decode()}')