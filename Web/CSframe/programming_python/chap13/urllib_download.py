from urllib.request import urlopen
import os, getpass

# file info
remote_file_name = 'Octocats.zip'
url_add = f'https://github-media-downloads.s3.amazonaws.com/{remote_file_name}'
# remote_file_name = 'google-logo-icon-10.jpg'
# url_add = f'https://icon-library.com/images/google-logo-icon/{remote_file_name}'
print(url_add)
local_file_name = remote_file_name

# fetch(download)
remote_file = urlopen(url_add)

# remote file write to local file
local_file = open(local_file_name, 'wb')
print(f'download {remote_file_name} from {url_add}')
local_file.write(remote_file.read())
# read local file
# local_file.read()

# close files
local_file.close()
remote_file.close()