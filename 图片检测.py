import imghdr

if __name__ == '__main__':
    with open('/home/ubuntu/Picture/1001887.jpg', 'rb') as f:
        # 1.检查文件的类型一般是对比文件的头部字节
        # content = f.read()
        # print(content)
        # 方式1： 设置第一个参数，传递文件路径、文件对象
        # type=imghdr.what(f)
        # print(type)
        # 方式2 ：设置第二个参数，传递二进制数据
        data_bytes = f.read()
        type = imghdr.what(None, data_bytes)
        print(type)
    # JPG  :  JFIF
    # PNG  ：
