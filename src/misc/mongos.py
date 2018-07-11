import web
import datetime
from bson.binary import Binary
from re import _pattern_type
import time

valid_key_types = set((str, unicode))
atomic_types = set((bool, int, long, float, str, unicode, type(None),
    _pattern_type, datetime.datetime))

def needs_encode(obj):
  
    obtype = type(obj)
    if obtype in atomic_types:
        return False
    if obtype is list:
        return any(needs_encode(i) for i in obj)
    if obtype is dict:
        return any(type(k) not in valid_key_types or needs_encode(v)
            for (k, v) in obj.iteritems())
    return True

class MongoStore(web.session.Store):
  
    def __init__(self, db, collection_name='sessions'):
      
        self.collection = db[collection_name]
        self.collection.ensure_index('atime')
    
    def encode(self, sessiondict):
        return dict((k, Binary(web.session.Store.encode(self, v)) if needs_encode(v) else v)
            for (k, v) in sessiondict.iteritems())

    def decode(self, sessiondict):
        return dict((k, web.session.Store.decode(self, v) if type(v) is Binary else v)
            for (k, v) in sessiondict.iteritems())

    def __contains__(self, sessionid):
        return bool(self.collection.find_one(sessionid, projection=[]))

    def __getitem__(self, sessionid):
      
        s = self.collection.find_one(sessionid)
        
        if not s:
            raise KeyError(sessionid)
        
        return self.decode(s['_data'])

    def __setitem__(self, sessionid, sessiondict):
      
        data = self.encode(sessiondict)
        self.collection.update({'_id':sessionid}, {'_data': data, 'atime': time.time()}, upsert=True)

    def __delitem__(self, sessionid):
        self.collection.remove(sessionid)
        
    def cleanup(self, timeout):
      
      cutoff = time.time() - timeout
      self.collection.remove({'atime': {'$lt': cutoff}})