
import win32com.client
import hashlib

def get_file_metadata(path, filename, metadata):    
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)

    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value
        
    with open(path+'/'+filename, 'rb') as file_to_check:
        data = file_to_check.read()    
        md5_returned = hashlib.md5(data).hexdigest()
        file_metadata['md5'] = md5_returned
    return file_metadata


if __name__ == '__main__':
    folder = 'G:\\My Drive\\Property'
    filename = 'mortgage-letter.jpg'
    metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created']
    print(get_file_metadata(folder, filename, metadata))