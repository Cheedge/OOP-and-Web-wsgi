from ftplib import FTP
import os

# file info
remote_file_name = 'GitHub-Mark.zip'
local_file_name = remote_file_name
remote_dir = '.'
url_add = f'https://github-media-downloads.s3.amazonaws.com/'

# fetch remote_file
remote_file = FTP(remote_file_name)
