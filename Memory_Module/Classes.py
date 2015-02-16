# Info: #
# Pre-first version
# ===================================

# Change:
ROOT = "C:/Bcloud"

'''
To do:
EVERYTHING!
'''

class User(object):
    def __init__(self, username):
        self.username = username
        self.path = "{root}/{name}".format(root = ROOT, name =self.username)
    def __str__(self):
        return self.username
    def __repr__(self):
        return self.username
    def modify_memory(self, file_name, data):
        pass
    def get_folder_info(self, folder_type):
        pass
    def get_file(self, folder_type, file_name):
        pass
    def get_folder(self, folder_type):
        
'''
Exciting. Satisfying. Period.
.
'''
