# -*- coding:utf-8 -*-
# 图片压缩类

from __future__ import division


class ThumbnailTool(object):

    def avatar_thumbnail(self):
        pass

    # 按长边,指定缩放倍数等比例缩放
    @classmethod
    def constrain_thumbnail(cls, img, times=2):
        width, height = img.size
        # 按给定的倍数缩放
        img.thumbnail((width//times, height//times))
        return img

    # 将长边，按等比例缩放至指定大小
    @classmethod
    def constrain_len_thumbnail(cls, img, length):
        width, height = img.size
        if width > height:
            scale = width / height
            width = length
            height = width / scale
        else:
            scale = height / width
            height = length
            width = height / scale

        img.thumbnail((width, height))
        return img