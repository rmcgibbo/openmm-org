from __future__ import print_function
import os
import boto
from boto.s3.key import Key

# The secret key is available as a secure environment variable
# on travis-ci to push the build documentation to Amazon S3.
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET_NAME = 'openmm.org'

bucket_name = AWS_ACCESS_KEY_ID.lower() + '-' + BUCKET_NAME
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(BUCKET_NAME)

def upload(path, root=None, prefix='', versioned=True):
    if root is None:
        root = path
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fn = os.path.join(dirpath, filename)
            k = Key(bucket)
            k.key = os.path.join(prefix, os.path.relpath(fn, root))
            print('Uploading', k.key, '...')
            k.set_contents_from_filename(fn)

upload('landing-page', versioned=False)