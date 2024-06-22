
import win32com.client
import hashlib
from glob import glob
import os
import sqlite3

def get_file_metadata(file, path, filename, metadata):    
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)

    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value
        
    file_metadata['Full_Path'] = file
    file_metadata['Path'] = path


    #with open(item, 'rb') as file_to_check:
    try:
        with open(file, 'rb') as file_to_check:
            data = file_to_check.read()    
            md5_returned = hashlib.md5(data).hexdigest()
            file_metadata['md5'] = md5_returned
    except:
        file_metadata['md5'] = "Error"
    return file_metadata
    

if __name__ == '__main__':    
    root_folder = 'G:\\My Drive\\'
    files = [f for f in glob('G:\\My Drive\\**', recursive=True) if os.path.isfile(f)]
    for file in files:    
        print(file)  
        path, filename = os.path.split(file)       
        metadata = ['Name', 'Size', 'Item_Type', 'Date_Modified', 'Date_Created']
        meta_data=(get_file_metadata(file, path, filename, metadata))       
        # insert into sqlite db
        con = sqlite3.connect("files_data.db")
        cur = con.cursor()
        columns = ', '.join(meta_data.keys())
        placeholders = ':'+', :'.join(meta_data.keys())
        query = 'INSERT INTO file_meta_data (%s) VALUES (%s)' % (columns, placeholders)        
        cur.execute(query, meta_data)
        con.commit()