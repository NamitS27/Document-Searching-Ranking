import re
from file_processing import processFiles
import filechooser as fc
from split_pdf import convert,highlight

filenames = fc.multfile()
fables, data = processFiles(filenames)
del fables[0]
n = len(fables)
print("Number of documents readed : ", n)


# Q1. Find all occurences of a query string
# Gives the indices at which the query string has occured. Zero based indexing is followed
def all_matches(query_string):
    flag = 0
    titlelist = []
    titleoccur = []
    for i in range(0, len(fables)):
        alloc = []
        index = fables[i].find_all_occurences(query_string)
        titlelist.append(fables[i].get_title())
        for j in index:
            if j != -1:
                flag += 1
                #print('Title : ' + fables[i].get_title() + '\t\t Position : ' + str(j))
                alloc.append([print_sentence(j, i), j])
        titleoccur.append(alloc)
    # if flag == 0:
    #     print('No Match Found!!!')
    return titlelist, titleoccur


# Q2. Find the 1st Occurence of a query string. If not found, Find the 1st occurence of the longest substring of query string
# Gives the Longest substring and the index of its 1st occurence for which match was found.
def first_substring_match(query_string, i):
    flag1 = 0
    start = 0
    end = len(query_string) - 1
    for j in range(0, len(query_string)):
        start = 0
        end = len(query_string) - j - 1
        for k in range(len(query_string) - j - 1, len(query_string)):
            substr = query_string[start:end + 1]
            index = fables[i].find_substring(substr)
            if index != -1:
                flag1 += 1
                ret_list = [substr, index]
                return ret_list
            else:
                start = start + 1
                end = end + 1

    return ['', -1]


# Q3. Find and rank all the documents corresponding to a query string by defining relevance
def rank_docs(query_string):
    """
    # Defining relevance as an integer storing a score.
    # If the whole substring is found as it is in a document(story), a score of 150 is assigned.
    # If all different words in the query are found, not necessarily non-stop, a score of 75 is assigned
    # If a substring of Query is found and if
      -> len(substring) >= 0.6*len(Query_string) score = 40
      -> Else discard the substring
    # If some words in the query are found, score gets added accordingly :  For each matched word in the query,
      -> if len(word) > 5  score += 10
      -> if len(word) > 2  score += 5
      -> if len(word) < 2  score += 1
    # If a word with len(word) > 2 has occured multiple times, score += n * 3, n being the number of times it has occured
    # The Documents are then sorted according to their relevance scores and the titles are printed """

    query_words = re.sub(r'[^a-zA-Z ]', '', query_string).split()
    scores = {}  # {Title : score}
    for i in range(0, len(fables)):
        if fables[i].find_substring(query_string) != -1:
            scores[fables[i].get_title()] = 150
        else:
            scores[fables[i].get_title()] = 0
            n = len(query_words)
            matches = []
            for word in query_words:
                index = fables[i].find_substring(word)
                if index != -1:
                    matches.append(word)
            if len(matches) == n:
                scores[fables[i].get_title()] += 75
            else:
                ret_list = first_substring_match(query_string, i)
                if len(ret_list[0]) > 0.6 * len(query_string):
                    scores[fables[i].get_title()] += 40
                    for word in matches:
                        if len(word) > 3:
                            scores[fables[i].get_title()] += 3 * \
                                (len(fables[i].find_all_occurences(word)) - 1)
                else:
                    for word in matches:
                        if len(word) > 5:
                            scores[fables[i].get_title()] += 5 * \
                                (len(fables[i].find_all_occurences(word)) - 1)
                            scores[fables[i].get_title()] += 10
                        elif len(word) > 2:
                            scores[fables[i].get_title()] += 3 * \
                                (len(fables[i].find_all_occurences(word)) - 1)
                            scores[fables[i].get_title()] += 5
                        else:
                            scores[fables[i].get_title()] += 1

    # Sort the dictionary according to their scores
    relevant_stories = sorted(scores.items(), key=lambda x: x[1])
    n = len(relevant_stories)
    for i in range(0, n):
        print("(Title , score) : ", relevant_stories[n - i - 1])


def print_sentence(index, i):
    if index == -1:
        return
    start = 0
    end = 0
    if index - 20 > 0:
        start = index - 20
    if index + 15 < len(data[i][2]):
        end = index + 20
    else:
        end = len(data[i][2]) - 1
    #print("Sentence : ", data[i][2][start:end])
    # print("\n")
    return data[i][2][start:end]


def findAll(titleL, matchlist, query_doc):
    ind = -1
    for i in range(len(titleL)):
        if query_doc == titleL[i]:
            ind = i
            break
    if ind == -1:
        print("No doc found")
        return False
    elif len(matchlist[ind]) == 0:
        print("No Match Found")
        return False
    else:
        k = 0
        print("Sentence : " +matchlist[ind][0][0], "\t| Pos. = ", matchlist[ind][0][1])
        print("Next Occurance ? (Press N) : ", end=" ")
        ch = input()
        while ch == 'n' or ch == 'p':
            if ch == 'n':
                if k < len(matchlist[ind])-1:
                    k = k+1
                    print("Sentence : " +matchlist[ind][k][0],
                          "\t| Pos. = ", matchlist[ind][k][1])
                else:
                    print("No further occurance found")
            else:
                if k > 0:
                    k = k-1
                    print(matchlist[ind][k][0],
                          "Pos. = ", matchlist[ind][k][1])
                else:
                    print("No more previous occurance")
            print("\nNext(n) / Previous(p) / Exit(e): ", end=" ")
            ch = input().lower()
        return True


# Main
ch = 'y'
while ch == "y" or ch == "Y":
    print("\n-----------------------------------------------------------------\n1. Find All occurences of a Query string \n2. Rank documents for the given Query string \n--------------------------------------------------------------------\nChoose from above")
    choice = int(input().strip())

    if choice == 1:
        print('Give a query string : ',end = "")
        query_string = input().strip()
        test1, test2 = all_matches(query_string)
        print("Enter the document in the which you want to find : ",end = "")
        file_q = input()
        if(findAll(test1, test2, file_q)):
            print("\n---------------------------------------------------------------\nHighlight Files ? (Y/N) : ",end = " ")
            chh = input()
            if chh.lower()=='y':
                file_pdf = []
                for i in filenames:
                    file_pdf.append(convert(i))
                for i in file_pdf:
                    highlight(i,query_string)

    # elif choice == 2:
    #     print('Give a query string : ')
    #     query_string = input().strip()
    #     for i in range(0, n):
    #         ret_list = first_substring_match(query_string, i)
    #         if ret_list[1] != -1:
    #             print('Title : {0:>18}\t\t\tPosition : {1:>4}\t\t\tSubstring : {2:>4}'.format(
    #                 fables[i].get_title(), str(ret_list[1]), ret_list[0]))
    #             print("Sentence : ", print_sentence(ret_list[1], i))

    elif choice == 2:
        print('Give a query string : ',end = "")
        query_string = input().strip()
        rank_docs(query_string)

    else:
        print("Wrong Input")

    print('\nContinue? (y/n)')
    ch = input().strip()