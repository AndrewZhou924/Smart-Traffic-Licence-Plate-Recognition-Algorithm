import pickle as pkl

# gen alphabet via label
# alphabet_set = set()
# infofiles = ['infofiles/infofile_selfcollect.txt','infofiles/infofile_train_public.txt']
# for infofile in infofiles:
#     f = open(infofile)
#     content = f.readlines()
#     f.close()
#     for line in content:
#         if len(line.strip())>0:
#             if len(line.strip().split('\t'))!=2:
#                 print(line)
#             else:
#                 fname,label = line.strip().split('\t')
#                 for ch in label:
#                     alphabet_set.add(ch)
#
# alphabet_list = sorted(list(alphabet_set))
# pkl.dump(alphabet_list,open('alphabet.pkl','wb'))

# alphabet_list = pkl.load(open('alphabet.pkl', 'rb'))
# alphabet = [ord(ch) for ch in alphabet_list]
# alphabet_v2 = alphabet
# print(alphabet_v2)
alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
               'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O', "皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽",
               "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青",
               "宁", "新", "警", "学"]
alphabet_v2 = [ord(ch) for ch in alphabet_list]
alphabet = alphabet_v2
