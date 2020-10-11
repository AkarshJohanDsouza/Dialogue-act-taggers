def check_speaker(each_utterence,features,speaker, tag_actor, prev_speaker):

    tokens_list = []
    position = []
    bi_grams = []
    big_grams_position = []
    tri_grams = []
    if speaker != prev_speaker and prev_speaker != None:
        features.append("SPEAKER_CHANGE")

    if prev_speaker == None:
        features.append("FIRST_UTTERANCE")

    if (not each_utterence.pos):
        features.append('NO_WORD')
        return features, each_utterence.speaker, each_utterence.act_tag
    for i, (token, pos) in enumerate(each_utterence.pos):
        if (i == 0):
            features.append('FIRST_TOKEN_' + token)
            features.append('FIRST_POS_' + pos)
        if (i == 1):
            features.append('FIRST_TOKEN_' + token)
            features.append('FIRST_POS_' + pos)
        if (i == len(each_utterence.pos) - 1):
            features.append('LAST_TOKEN_' + token)
            features.append('LAST_POS_' + pos)
        #     tokens.append("THIRDTOKEN_" + pos_tag.token)
        #     tokens.append("THIRDPOS_" + pos_tag.pos)
        # if token_index == num_tokens - 3:
        #     tokens.append("THIRDLASTTOKEN_" + pos_tag.token)
        #     tokens.append("THIRDLASTPOS_" + pos_tag.pos)
        if (i == len(each_utterence.pos) - 2):
            features.append('SECOND_TOLAST_TOKEN_' + token)
            features.append('SECOND_TOLAST_POS_' + pos)
        features.append('TOKEN_' + token)
        features.append('POS_' + pos)

        temp_features_list = zip(each_utterence.pos[:-1], each_utterence.pos[1:])
    for pos1, pos2 in temp_features_list:
        features.append("BIGRAM_{}_{}".format(pos1.token, pos2.token))
        features.append("BIGRAM_POS_{}_{}".format(pos1.pos, pos2.pos))
    return features, each_utterence.speaker, each_utterence.act_tag