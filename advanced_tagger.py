from hw2_corpus_tool import get_data
import pycrfsuite
import sys
import os
import glob
import string

trainer = pycrfsuite.Trainer(verbose=True)
trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })


def getfilelabels(file):
    filelabels = []
    for i in range(len(file)):
        filelabels.append(file[i].act_tag)
    return filelabels

def featuresforfile(file):
    # firstsent = True
    flist = []
    act_tags = []
    #
    # sent1 = file.pop()
    prevspeaker = None

    for i in range(len(file)):

        # sent1 = file.pop()
        # prevspeaker = sent1.speaker
        sent1 = file[i]

        if i == 0:
            speakerchange = False
            firstutterance = True

        elif sent1.speaker != prevspeaker:
            speakerchange = True
            firstutterance = False
        else:
            speakerchange = False
            firstutterance = False

        prevspeaker = sent1.speaker
        features = [
            'speakerchange=%s' % speakerchange,
            'firstutterance=%s' % firstutterance
        ]



        tokens = []
        postags = []
        if sent1.pos == None or len(sent1.text) == 0:
            postags.extend(['pos=NO_WORD'])
            features.extend(postags)
            flist.append(features)
            act_tags.append(sent1.act_tag)
            continue
            # continue
        # prev = "FIRST"
        cnt = 0
        for tokenpos in sent1.pos:
            if cnt == 0:
                tokens.extend(['first_token='+tokenpos.token])
                tokens.extend(['first_pos=' + tokenpos.pos])
            cnt+=1
            # tokens.extend('prevtoken=TOKEN_' + prev)
            # prev = tokenpos.token
            tokens.extend(['token=TOKEN_' + tokenpos.token])
            postags.extend(['pos=POS_' + tokenpos.pos])
            # isdigit = False
            # ispunctutation = False
            # if tokenpos.token in string.digits:
            #     isdigit = True
            # if tokenpos.token in string.punctuation:
            #     ispunctutation = True
            # features.extend(
            #     [
            #         "ispunctuation=%s" %ispunctutation,
            #         # "isdigit=%s" %isdigit
            #         "wordlowercase=%s" %tokenpos.token.lower()
            #         # "allcaps=%s" %tokenpos.token.isupper()
            #     ]
            # )
        if len(sent1.pos) >0:
            features.extend(
                [
                    "last_token=%s" %sent1.pos[-1].token,
                    "last_pos=%s" %sent1.pos[-1].pos
                    # "text=%s" %sent1.text
                ]
            )
        if len(sent1.pos) > 3:
            features.extend(
                [
                    "second_last_token=%s" %sent1.pos[-2].token,
                    "second_last_pos=%s" %sent1.pos[-2].pos
                ]
            )
        tf_list = zip(sent1.pos[:-1], sent1.pos[1:])
        for pos1, pos2 in tf_list:
            features.append("BG_token_"+pos1.token + "_"+pos2.token)
            features.append("BG_pos_"+pos1.pos+"_"+pos2.pos)
        features.extend(tokens)
        features.extend(postags)
        flist.append(features)
        # print(features)
        act_tags.append(sent1.act_tag)

    trainer.append(flist, act_tags)
    return flist

datafilenames=list(get_data(sys.argv[1]))

for file in datafilenames:
    fof = featuresforfile(file)

trainer.train('model1')
# print(listOfCsvfiles)

#Testing

tagger = pycrfsuite.Tagger()
tagger.open('model1')

testfileslist = list(get_data(sys.argv[2]))

dialog_filenames = sorted(glob.glob(os.path.join(sys.argv[2], "*.csv")))
file_list=[]
for dialog_filename in dialog_filenames:
    head, tail = os.path.split(dialog_filename)
    file_list.append(tail)
counter=0

opfile = open(sys.argv[3], "w", encoding="latin1")

# num_pred = 0
# correctly_pred = 0
for file in testfileslist:

    X_test = [featuresforfile(file)]

    Y_pred = [tagger.tag(xseq) for xseq in X_test]
    Y_act = [getfilelabels(file)]
    # print('Test files')
    # print(X_test)
    # opfile.write("Filename= " + '"' + file_list[counter] + '"' + "\n")

    #calculate accuracy:


    # print(Y_pred)
    Y_pred = Y_pred[0]
    # Y_act = Y_act[0]
    # print(Y_act)
    # print("Ypred len",len(Y_pred))
    # print("Yact len", len(Y_act))
    for i in range(len(Y_pred)):

        # if Y_pred[i] == Y_act[i]:
        #     correctly_pred += 1
        # for label in each_flabel:
        opfile.write(Y_pred[i])
        opfile.write("\n")

        # num_pred +=1

    # counter = counter + 1

    opfile.write("\n")

# print("accuracy: ", correctly_pred / num_pred)