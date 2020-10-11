from hw2_corpus_tool import get_data
import pycrfsuite
import sys
import os
import glob

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
            # print("pos null")
            continue
            # continue
        for tokenpos in sent1.pos:
            tokens.extend(['token=' + tokenpos.token])
            postags.extend(['pos=' + tokenpos.pos])

        features.extend(tokens)
        features.extend(postags)
        flist.append(features)
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

tflist = list(get_data(sys.argv[2]))

dialog_filenames = sorted(glob.glob(os.path.join(sys.argv[2], "*.csv")))
file_list=[]
for dialog_filename in dialog_filenames:
    head, tail = os.path.split(dialog_filename)
    file_list.append(tail)
# counter=0

opfile = open(sys.argv[3], "w", encoding="latin1")

num_pred = 0
correctly_pred = 0
for file in tflist:

    x_test = [featuresforfile(file)]

    Y_pred = [tagger.tag(xseq) for xseq in x_test]
    # Y_act = [getfilelabels(file)]
    Y_pred = Y_pred[0]
    # Y_act = Y_act[0]
    for i in range(len(Y_pred)):

        if Y_pred[i] == Y_act[i]:
            correctly_pred += 1
        # for label in each_flabel:
        opfile.write(Y_pred[i])
        opfile.write("\n")

        num_pred +=1

    opfile.write("\n")

print("accuracy: ", correctly_pred / num_pred)