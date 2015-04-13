__author__ = 'Rich Johnson'
'''
Write a python program to create and store the backups of both db_tweets and
db_streamT to S3. It also should have a capability of loading the backups if
necessary.
'''
# Standard Packages
import glob
import os
import os.path
import sys
# Installed Packages
import boto
from boto.s3.key import Key



def load(fm, to):
    """
    Loads a mongo database from S3 to the local computer

    All files in the S3 bucket are assumed to be valid database files and
    are therefore downloaded and inserted in to the database.
    Note: This function overwrites existing database files. Ensure you backup
    all database files as necessary for your needs.

    :param fm: An S3 bucket that contains the mongodb backup files
    :param to: A local directory to write the backup to
    :return: None
    """
    conn = boto.connect_s3()
    bucket = conn.get_bucket(fm)

    for key in bucket.list():
        try:
            key.get_contents_to_filename(os.path.join(to, key.key))
        except IOError:
            print "Check file write permissions"
            raise IOError


def backup(dbs, fm, to):
    """
    Backups a list of mongodb files from the local machine to S3
    :param dbs: a list containing the names of databases to backup
    :param fm: a local directory containing mongodb files
    :param to: an S3 bucket to store the backup mongodb files
    :return: None
    """
    conn = boto.connect_s3()
    if not conn.lookup(to):
        conn.create_bucket(to)
    bucket = conn.get_bucket(to)

    for db in dbs:
        for file in glob.glob(fm + os.sep + db + "*"):
            k = Key(bucket)
            k.key = os.path.split(file)[1]
            try:
                k.set_contents_from_filename(file)
            except IOError:
                print "Check file read permissions"
                raise IOError


if __name__ == '__main__':
    databases = ['db_tweets', 'db_streamT']
    s3loc = 'rj.w205a3'
    lcl = os.path.abspath("/home/rich/DBDATA/mongodb/")

    if not len(sys.argv) == 2:
        print len(sys.argv)
        print "usage: python part3.1.py <backup|load>"
    else:
        if sys.argv[1] == 'backup':
            backup(databases, lcl, s3loc)
        elif sys.argv[1] == 'load':
            load(s3loc, lcl)
        else:
            print "Improper usage: argv[1]: %s" (sys.argv[1],)
            print "usage: python part3.1.py <backup|load>"

