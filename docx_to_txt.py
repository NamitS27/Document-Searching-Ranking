import sys
import fitz
import cloudconvert

def converttotxt(filenames):
    print("CONVERTING .........")
    final_files = []
    for i in filenames:
        api = cloudconvert.Api(
            '2R83XvhTuELfut2PvQbv0rRgPRSlTGA2wICqnQRUdnJL7YVua17xrHHpufJzqQtC')
        process = api.convert({
            'inputformat': 'docx',
            'outputformat': 'txt',
            'input': 'upload',
            'file': open(i, 'rb')
        })
        process.wait()  # wait until conversion finished
        txt_file_name = i[:len(i)-5]+".txt"
        process.download(txt_file_name)
        final_files.append(txt_file_name)
    return final_files