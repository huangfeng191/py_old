import web

def get_session_value(key, prefix=''):
    sess = web.ctx.session
    key = key + prefix

    return sess.get(key, {})


def set_session_value(key, value, prefix=''):
    sess = web.ctx.session
    key = key + prefix
    sess[key] = value


