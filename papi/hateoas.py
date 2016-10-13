def decorate_item(item, parent_path, name=None, name_fn=None):
    if name is None:
        if name_fn is not None:
            name = name_fn(item)
    if not 'keys' in dir(item):
        item = { 'value': item }
    if item.get('_links') is None:
        item['_links'] = {}
    item['_links']['parent'] = '/' + '/'.join(parent_path)
    if name is not None:
        self_path = list(parent_path)
        self_path.append(name)
        item['_links']['self'] = '/' + '/'.join(self_path)
    return item

def decorate_list(items, parent_path, name_fn=None):
    return [ decorate_item(item, parent_path, name_fn=name_fn) for item in items ]

def decorate_dict(items, parent_path):
    return [ decorate_item(v, parent_path, k) for k, v in items.items() ]
