# Info: #
# Pre-first version
# ===================================

import zipfile, os, zlib

# Change:
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
        return self.username
    def __repr__(self):
        return self.username
    
    def get_folder_info(self, folder_type):
        try:
            update_file = open('{}/{}.txt'.format(self.path, folder_type), 'r')
            data = update_file.read()
            update_file.close()
            return 'SCS', data
        except:
            return 'WTF', 'WTF'
        
    def set_folder_info(self, folder_type, info):
        try:
            update_file = open('{}/{}.txt'.format(self.path, folder_type), 'w')
            update_file.write(info)
            update_file.close()
            return 'SCS'
        except:
            return 'WTF'
        
    def get_file(self, folder_type, file_name):
        try:
            archive = zipfile.ZipFile(self.path+'/single.zip', 'w', compression=zipfile.ZIP_DEFLATED)
            archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_name), file_name)
            archive.close()
            archive = open(self.path+'/single.zip', 'rb')
            data = archive.read()
            archive.close()
            return 'SCS', data
        except:
            return 'WTF', 'WTF'
        
    def write_to_file(self, folder_type, file_name, data):
        try:
            target_file = open('{}/{}/{}'.format(self.path, folder_type, file_name), 'wb')
            target_file.write(data)
            target_file.close()
            return 'SCS'
        except:
            return 'WTF'
            
    def get_folder(self, folder_type):
        try:
            archive = zipfile.ZipFile(self.path+'/folder.zip', 'w')
            for root, dirs, files in os.walk('{}/{}'.format(self.path, folder_type)):
                for f in files:
                    archive.write(os.path.join(root, f), os.path.join(root.lstrip('{}/{}'.format(self.path, folder_type)), f))
            archive.close()
            archive = open(self.path+'/folder.zip', 'rb')
            data = archive.read()
            archive.close()
            return 'SCS', data
        except:
            return 'WTF', 'WTF'


'''
Exciting. Satisfying. Period.
.
'''
