# Info: #
# ===================================

import zipfile, os, zlib, sys
sys.path.append('../')
from COM import *


global ROOT
ROOT = "C:/Bcloud"


class User(object):
    def __init__(self, username):
        ''' Sets up a new user
        '''
        self.username = username
        self.path = "{root}/{name}".format(root = ROOT, name =self.username) # The path to the main directory of the user, used as a "shortcut"
        
    def __str__(self):
        ''' Used for debug
        '''
        return "A user named {}".format(self.username)
    def __repr__(self):
        ''' Used for debug
        '''
        return "User:{}".format(self.username)
    
    def get_folder_info(self, folder_type):
        ''' Gets the content of a folder's updates file - A text that contains the names of the files and the last time each was changed on the client's side.
        '''
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
        except IOError, e:
            if e.errno == 2: # IOError 2 means the path does not exist. Since we know that each client has these files, it means the client does not exist.
                return 'NNM', 'NNM'
            else:
                return 'WTF', 'WTF'
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'
        
    def set_folder_info(self, folder_type, info):
        ''' Updates the content of the folder's info file.
        '''
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
        ''' Gets the list of files given, all compressed into a zip file.
        '''
        try:
            # The first time we open the archive we do it using the "zipfile" module, and we do it to write files into the archive.
            archive = zipfile.ZipFile(self.path+'/files.zip', 'w', compression = zipfile.ZIP_DEFLATED)
            print 'get: opened archive'
            for file_name in files:
                archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_name), file_name) # Accesses the file with the full path, writes it into the archive with the relative path.
                print 'get: added file'
            archive.close()
            print 'get: closed archive'
            # The second time we open the archive we do it using the normal "open" function, and we do it to read the file's content as a bitestream.
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
        ''' deletes a specific file from a folder.
        '''
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
        ''' Gets an archive filled with updated files and folders, and extracts those into the given folder.
        '''
        try:
            # The first time we open the file we do it as a normal file in order to write the bitestream
            updated_files = open('{}/updated_files.zip'.format(self.path), 'wb')
            print 'set: opened archive to write'
            updated_files.write(data)
            print 'set: wrote'
            updated_files.close()
            print 'set: closed archive'
            # The second time we open the file we do it as a zipfile in order to access the "extractall" function
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
        ''' archives an entire folder and returns the content of the archive as a bitestream.
        '''
        try:
            # First opening as a zip archive
            archive = zipfile.ZipFile(self.path+'/folder.zip', 'w', compression=zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk('{}/{}'.format(self.path, folder_type)):
                for f in files:
                    archive.write(os.path.join(root, f), os.path.join(root[len('{}/{}'.format(self.path, folder_type)):], f)) # We write into the archive using the relative path, not the full one.
            archive.close()
            # Second opening as a normal file
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
