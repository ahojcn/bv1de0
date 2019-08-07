import random

from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
from django.http.response import HttpResponse


def get_verify_code_img(request, h=25, w=100, font_size=23):
    """
    生成验证码
    :param font_size: 字体大小
    :param w: 验证码的宽度
    :param h: 验证码的高度
    :param request: 客户端发来的请求
    :return: 图片数据
    """

    width = w
    height = h
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), 255)

    # 创建画面对象
    im = Image.new('RGB', (width, height), bg_color)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取 4 个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/font/LatienneSwaT.ttf', font_size)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verify_code'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回
    return HttpResponse(buf.getvalue(), 'image/png')
