# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/5
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/5
# Version : 1.0

import misc.utils as utils
import time

import json

def getCycleToT(cycle,t=None):
    '''
    Args:
        cycle:  day month year week
        s:  str 字符串时间 ，None 是 现在

    Returns:

    '''
    o={
        "day":"%Y%m%d",
        "month":"%Y%m",
        "year":"%Y"
    }

    if not t:
        ti =int(time.time())
        if cycle =="week":
            t,_=utils.getFirstEndDayOfWeek(ti)
        else:
            t=utils.YMD(ti,o[cycle])
    return t

def contactToMethod(str,params={}):
    '''

    Args:
        str:  方法名
        params: 方法的 Object 参数

    Returns:
        待 eval 的 string 方法
    '''
    s=(str+"(**%s)")%json.dumps(params)
    return  s




def compressObject(obj):
    '''
    #  将多级object 对象 压缩成  一级用 . 区分的对象
    Args:
        obj: {"a":1,"b":{"c":1}}

    Returns:
        {"a":1,"b.c":1}

    '''
    def plusKey(base, key, val, compressed):
        base1 = base + key
        if type(val) == dict and len(val.keys()) > 0 and   "$" not in  val.keys()[0] :
            base1 = base1 + "."
            for k, v in val.items():
                plusKey(base1, k, v, compressed)

        else:
            compressed[base1] = val

    o = {}
    base = ""
    compressed = {}
    for k, v in obj.items():
        plusKey(base, k, v, compressed)

    return compressed


def equalObj(obj1={},obj2={}):
    i=cmp(obj1,obj2)
    if i==0:
        return True
    else:
        return False

def parseConditions(conditions=None):
    q = {}

    if conditions:

        for c in conditions:

            f = c.get('field')
            r = c.get('relation', 'and')
            o = c.get('operate', '')
            v = c.get('value')

            if f and o:

                a = None

                if r == 'and':
                    q['$and'] = q.get('$and', {})
                    a = q['$and']
                elif r == 'or':
                    q['$or'] = q.get('$or', {})
                    a = q['$or']

                if a is not None:
                    if f not in a: a[f] = {}

                    if o == 'like':
                        # a.append({f:{'$regex':v}})
                        a[f]['$regex'] = v
                    elif o == '=':
                        # a.append({f:v})
                        a[f] = v
                    elif o == '>=':
                        # a.append({f:{'$gte':v}})
                        a[f]['$gte'] = v
                    elif o == '>':
                        # a.append({f:{'$gt' :v}})
                        a[f]['$gt'] = v
                    elif o == '<=':
                        # a.append({f:{'$lte':v}})
                        a[f]['$lte'] = v
                    elif o == '<':
                        # a.append({f:{'$lt' :v}})
                        a[f]['$lt'] = v
                    elif o == 'nil':
                        # a.append({f:{'$exists':False}})
                        a[f]['$exists'] = False
                    elif o == '!=':
                        # a.append({f:{'$ne':v}})
                        a[f]['$ne'] = v
                    elif o == 'in':
                        # a.append({f:{'$in':v}})
                        a[f]['$in'] = v

    if '$and' in q and len(q.get('$and')) == 0:
        del q['$and']

    if '$or' in q and len(q.get('$or')) == 0:
        del q['$or']

    return q




def parse_conditions_CRUD(conditions=None):
    q = {}

    if conditions:

        for c in conditions:

            f = c.get('Field')
            r = c.get('Relation', 'and')
            o = c.get('Operate', '')
            v = c.get('Value')

            if f and o:

                a = None

                if r == 'and':
                    q['$and'] = q.get('$and', {})
                    a = q['$and']
                elif r == 'or':
                    q['$or'] = q.get('$or', {})
                    a = q['$or']

                if a is not None:
                    if f not in a: a[f] = {}

                    if o == 'like':
                        # a.append({f:{'$regex':v}})
                        a[f]['$regex'] = v
                    elif o == '=':
                        # a.append({f:v})
                        a[f] = v
                    elif o == '>=':
                        # a.append({f:{'$gte':v}})
                        a[f]['$gte'] = v
                    elif o == '>':
                        # a.append({f:{'$gt' :v}})
                        a[f]['$gt'] = v
                    elif o == '<=':
                        # a.append({f:{'$lte':v}})
                        a[f]['$lte'] = v
                    elif o == '<':
                        # a.append({f:{'$lt' :v}})
                        a[f]['$lt'] = v
                    elif o == 'nil':
                        # a.append({f:{'$exists':False}})
                        a[f]['$exists'] = False
                    elif o == '!=':
                        # a.append({f:{'$ne':v}})
                        a[f]['$ne'] = v
                    elif o == 'in':
                        # a.append({f:{'$in':v}})
                        a[f]['$in'] = v

    if '$and' in q and len(q.get('$and')) == 0:
        del q['$and']

    if '$or' in q and len(q.get('$or')) == 0:
        del q['$or']

    return q


def objBindType(type,o,data={}):
    o["type"]=type
    o[type]=data