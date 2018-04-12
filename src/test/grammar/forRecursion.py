@path("/jiayuan/forcar/tree.json")
class JiayuanForcarTree(POST):
    def createst(self, item):
        r = OrderedDict()
        r['Type'] = 'L'
        r['Name'] = item['sn']
        r['ObjId'] = item['_id']
        r['Tel'] = item['phone']
        r['Icon'] = 'Station'
        return r
    @streecid
    @rolize
    def action(self, EndType='L', _cid=None, _scid=None, _role=None, Did=None, Type=None, *args, **kwArgs):


        def _build_tree(dep):
            _tree = webservice.api.view.createbiz(dep)
            for _dep in service.biz.deps.items(query={'cid': dep['cid'], 'pid': dep['_id']}):
                __tree = _build_tree(_dep)
                _tree['Children'].append(__tree)
            for _st in service.biz.cars.items(query={'cid': dep['cid'], 'dep': dep['_id']}):
                _tree['Children'].append(self.createst(_st))
            return _tree

        def build_tree(cid):
            query = {'cid': cid}
            if Did:
                query['_id'] = Did
            else:
                query['pid'] = '0'
            rs = OrderedDict([('Type', 'R'), ('Name', u'车辆构架'), ('ObjId', ''), ('Icon', 'Root'), ('Children', [])])
            for dep in service.biz.deps.items(query=query):
                rs['Children'].append(_build_tree(dep))
            return rs

        return build_tree(cid=_cid)