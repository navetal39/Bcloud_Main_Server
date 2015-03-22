# Info: #
# ===================================

import zipfile, os, zlib, sys
sys.path.append('../')
from COM import *


global ROOT
ROOT = "C:/Bcloud"

'''
To do:
1) Make 'Get Folder' ignore system files, etc.
'''

class User(object):
    def __init__(self, username):
        self.username = username
        self.path = "{root}/{name}".format(root = ROOT, name =self.username)
        
    def __str__(self):
        return "A user named {}".format(self.username)
    def __repr__(self):
        return "User:{}".format(self.username)
    
    def get_folder_info(self, folder_type):
        try:
            update_file = open('{}/{}.txt'.format(self.path, folder_type), 'r')
            print 'gfi: opened file'
            data = update_file.read()
            print 'gfi: read'
            update_file.close()
            print 'gfi: closed'
            if data == '':
                data = 'EMPTY'
            return 'SCS', data # If the folder is empty the client sends 'Empty' rather than '', just so there won't be problems...
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'
        
    def set_folder_info(self, folder_type, info):
        try:
            update_file = open('{}/{}.txt'.format(self.path, folder_type), 'w')
            print 'sfi: opened file'
            if info != 'EMPTY':
                update_file.write(info)
                print 'sfi: wrote info'
            else: # If the folder is empty the client sends 'Empty' rather than '', just so there won't be problems...
                update_file.write('')
                print 'sfi: wrote nothing'
            update_file.close()
            print 'sfi: closed file'
            return 'SCS'
        except Exception, error:
            print 'ERROR', error
            return 'WTF'

    def get_files(self, folder_type, files):
        try:
            archive = zipfile.ZipFile(self.path+'/files.zip', 'w', compression = zipfile.ZIP_DEFLATED)
            print 'get: opened archive'
            for file_name in files:
                archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_name), file_name)
                print 'get: added file'
            archive.close()
            print 'get: closed archive'
            archive = open(self.path+'/files.zip', 'rb')
            print 'get: opened archive to read'
            data = archive.read()
            print 'get: read'
            archive.close()
            print 'get: closed archive'
            return 'SCS', data
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'

    def delete_file(self, folder_type, file_name):
        try:
            os.remove('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_name))
            print 'del: removed file'
            return 'SCS'
        except WindowsError, error:
            if error.errno == 2:
                return 'SCS'
            else:
                return 'WTF'
        except:
            return 'WTF'
        
    def update_folder(self, folder_type, data):
        try:
            updated_files = open('{}/updated_files.zip'.format(self.path), 'wb')
            print 'set: opened archive to write'
            updated_files.write(data)
            print 'set: wrote'
            updated_files.close()
            print 'set: closed archive'
            updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'r')
            print 'set: opened archive to extract'
            updated_files.extractall('{}/{}'.format(self.path, folder_type))
            print 'set: extracted'
            updated_files.close()
            print 'set: closed archive again'
            return 'SCS'
        except:
            return 'WTF'
            
    def get_folder(self, folder_type):
        try:
            archive = zipfile.ZipFile(self.path+'/folder.zip', 'w', compression=zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk('{}/{}'.format(self.path, folder_type)):
                for f in files:
                    archive.write(os.path.join(root, f), os.path.join(root.lstrip('{}/{}'.format(self.path, folder_type)), f))
            archive.close()
            archive = open(self.path+'/folder.zip', 'rb')
            data = archive.read()
            archive.close()
            return 'SCS', data
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'


'''
Exciting. Satisfying. Period.
.
'''
