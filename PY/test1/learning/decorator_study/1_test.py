#! /usr/bin/env python3
"""
an example showing how to use decorator
"""
import functools

def log(logorfunc='default_call'):
    """ produce a decorator taking a log string as para
    """
    def decorator(func):
        """ a decorator taking in a func and returning a wrapper func
        """
        @functools.wraps(func)
        def wrapper(*args, **kw):
            """ prints some log around the execution
                of the func taken in
            """
            print('begin %s %s():' % (acstr, func.__name__))
            ret = func(*args, **kw)
            print('end %s %s():' % (acstr, func.__name__))
            return ret  # need to return the return value of func here
        return wrapper

    if isinstance(logorfunc, str):  # check the para's type
        acstr = logorfunc
        return decorator
    else:
        acstr = 'void_call'
        return decorator(logorfunc)


@log('execute')
def now(s):
    """ prints some date info
    """
    print(s,'2017-1-11')
    return 'wo'
@log()
def now2():
    """ prints some date info
    """
    print('2017-1-12')


@log
def now3():
    """ prints some date info
    """
    print('2017-1-13')

print(now('qqq'))
# for f in (now, now2, now3):
#     f()
#     print("f's name is: %s\n" % f.__name__)