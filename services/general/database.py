
def files_to_dict(files):
    """Get response from db and define the

    :param files: files list from the db    
    """
    _files_json = list()
    for _file in files:
        """Add file to list"""
        _files_json.append(_file.to_dict())
    return _files_json
