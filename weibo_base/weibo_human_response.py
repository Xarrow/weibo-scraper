# -*- coding=utf-8 -*-
"""
 @Author xuanji.zj
 @Email xuanji.zj@alibaba-inc.com
 @Time 2021/6/2 3:39 下午
 @desc  Add New Functions In weibo_human_response
 
"""


class RealTimeHotWordResponse(object):
    __slots__ = ['_sequence', '_desc', '_hot', '_url']

    def __init__(self, ):
        self._sequence = 0
        self._desc = ""
        self._hot = 0
        self._url = ""

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        self._sequence = sequence

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property
    def hot(self):
        return self._hot

    @hot.setter
    def hot(self, hot):
        self._hot = hot

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def __repr__(self):
        return "<RealTimeHotWordResponse sequence=%r,desc=%r,hot=%r,url=%r,>" % (
            self._sequence, self._desc, self._hot, self._url,)


def genPythonicGetterSetter(pclass):
    pclass_contructor = globals()[pclass]
    instance = pclass_contructor()
    ss = """\treturn "<""" + instance.__class__.__name__ + " "
    fields = ""
    field_value = ""
    for k in instance.__dict__:
        rk = k
        if k.startswith("_"):
            k = k[1:len(k)]

        print("@property")
        print("def " + k + "(self):")
        print("\treturn self." + rk)
        print("@" + k + ".setter")
        print("def " + k + "(self," + k + "):")
        print("\tself." + rk, "= " + k)
        fields += k + "=%r,"
        field_value += "self." + rk + ","

    print("def __repr__(self):")
    ss = ss + fields + '>"%' + "(" + field_value + ')'
    print(ss)


if __name__ == '__main__':
    genPythonicGetterSetter(RealTimeHotWordResponse.__name__)
