import os
from suffix_tree import SuffixTree

# def remove_empty_lines(filename):
#     with open(filename) as in_file, open(filename, 'r+') as out_file:
#         out_file.writelines(line for line in in_file if line.strip())
#         out_file.truncate()

def checkTitle(filename):
    with open(filename,'r',encoding="utf8") as ff:
        line = ff.readline()
        linecheck = ff.readline()
        if linecheck == "\n":
            return True
        else:
            return False


def addTitle(filename):
    string = filename[0:len(filename)-4]+"\n\n"
    with open(filename,'r',encoding="utf8") as f:
        with open('newfile.txt','w',encoding="utf8") as f2:
            f2.write(string)
            f2.write(f.read())
    os.remove(filename)
    os.rename('newfile.txt',filename)


# def appendLine(filename):
#     string = ""
#     with open(filename, 'r') as fp:
#         for i in fp.readline():
#             line = i.strip()
#             string += line + ' '
#     with open(filename, 'w+') as ff:
#         ff.write(string+"\n")

def mergeFiles(filenames):
    os.remove("output.txt")  # change the path according to your pc
    with open("output.txt", 'a+',encoding="utf8") as ff:
        for i in range(len(filenames)):
            with open(filenames[i], 'r',encoding="utf8") as fp:
                for j in fp.readlines():
                    ff.write(j)
            ff.write("\n\n\n")


def create_dataset(filenames):
    data = []
    ind = 1
    count = 1
    for j in filenames:
        temp = []
        y = ""
        with open(j, "r",encoding="utf8") as f:
            fl = f.readline()
            temp.append(count)
            temp.append(fl.strip())
            f.readline()
            for line in f:
                line = line.strip()
                y += line + ' '
            temp.append(y)
        count = count + 1
        data.append(temp)
    return data


# def processOutput(file,filenames):
#     ind = 1
#     ind3 = 0
#     indlist = []
#     with open(file,'r') as fp:
#         for i in fp.readlines():
#             line = i.strip()
#             if ind<len(filenames):
#                 if line == filenames[ind][0:len(filenames[ind])-4]:
#                     ind = ind+1
#                     indlist.append(ind3)
#             ind3 = ind3+1
#     print(indlist)
#
#     for i in range(len(indlist)):
#         with open(file,'r') as fp:
#             contents = fp.readlines()
#         contents.insert(indlist[i]+2*i,"\n\n")
#         with open(file,'w') as ff:
#             contents = "".join(contents)
#             ff.write(contents)

def make_suffix_tree(filename):
    final = []
    string = ''
    title = ''
    flag = 0
    with open(filename, "r",encoding="utf8") as f:
        for i in f.readlines():
            line = i.strip()
            if len(line) == 0:
                flag = flag - 1
                continue
            elif flag == 0 and len(line) != 0:  # It is a title
                final.append(SuffixTree(string, title, False))
                string = ''
                title = line
                flag = 2
                continue
            elif flag == 1 and len(line) != 0:  # Content
                flag = 2
                string += line + ' '
            elif flag == 2:
                string += line + ' '
    final.append(SuffixTree(string, title, False))
    return final

def clean_file(filename):
    def is_all_whitespace(line):
        for char in line:
            if char != ' ' and char != '\n':
                return False
        return True

    with open(filename, 'r',encoding="utf8") as file:
        file_out = []
        for line in file:
            if is_all_whitespace(line):
                line = '\n'
            file_out.append(line)

    while file_out[-1] == '\n': 
        file_out.pop(-1)

    if file_out[-1][-1] == "\n":
        file_out[-1] = file_out[-1][:-1]
    
    with open(filename, 'w',encoding="utf8") as file:
        file.write(''.join(file_out))


def processFiles(filenames):
    
    for j in range(len(filenames)):
        if not checkTitle(filenames[j]):
            addTitle(filenames[j])
        clean_file(filenames[j])

    mergeFiles(filenames)
    data = create_dataset(filenames)
    final = make_suffix_tree("output.txt")
    return final, data

# filenames = ["test1.txt","test2.txt","test3.txt"]
# for j in range(len(filenames)):
#     if not checkTitle(filenames[j]):
#         addTitle(filenames[j])