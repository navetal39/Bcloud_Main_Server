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
            data = update_file.read()
            update_file.close()
            if data == '':
                data = 'EMPTY'
            return 'SCS', data # If the folder is empty the client sends 'Empty' rather than '', just so there won't be problems...
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'
        
    def set_folder_info(self, folder_type, info):
        try:
            update_file = open('{}/{}.txt'.format(self.path, folder_type), 'w')
            if info != 'EMPTY':
                update_file.write(info)
            else: # If the folder is empty the client sends 'Empty' rather than '', just so there won't be problems...
                update_file.write('')
            update_file.close()
            return 'SCS'
        except Exception, error:
            print 'ERROR', error
            return 'WTF'

    def get_files(self, folder_type, files):
        try:
            archive = zipfile.ZipFile(self.path+'/files.zip', 'w', compression = zipfile.ZIP_DEFLATED)
            for file_name in files:
                archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_name), file_name)
            archive.close()
            archive = open(self.path+'/files.zip', 'rb')
            data = archive.read()
            archive.close()
            return 'SCS', data
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'

    def delete_file(self, folder_type, file_name):
        try:
            os.remove('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_name))
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
            updated_files.write(data)
            updated_files.close()
            updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'r')
            updated_files.extract_all('{}/{}'.format(self.path, folder_type))
            updated_files.close()
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
