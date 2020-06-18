


def up_load_file(data):
    from qiniu import Auth, put_data

    access_key = 'Z3n7VHTzWjjTxiSQc1cLlvtjdBjdG6yIsRYXim54'
    secret_key = 'OuU8PaON7VxJYiO7ER_uS_MIsx-PkmkgckiEDBeN'

    q = Auth(access_key, secret_key)

    bucket_name = 'zhdsh35'

    key = None

    token = q.upload_token(bucket_name, key, 3600)

    # localfile = '/home/ubuntu/Picture'

    # ret,info = put_file(token,key,localfile)
    ret, info = put_data(token, key, data)
    if info.status_code == 200:
        return 'http://qc3o3ps8s.bkt.clouddn.com' + ret.get('key')
    else:
        raise BaseException(info.error)

    # print(info)
    # print(ret.get('key'))
    #


if __name__ == '__main__':
    with open('/home/ubuntu/Picture/1001887.jpg','rb') as f:
        file_bytes = f.read()

        fiel_url = up_load_file(file_bytes)
        print(fiel_url)
