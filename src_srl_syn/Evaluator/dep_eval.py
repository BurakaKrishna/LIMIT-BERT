__author__ = 'max'

import re
import numpy as np

def is_uni_punctuation(word):
    match = re.match("^[^\w\s]+$]", word, flags=re.UNICODE)
    return match is not None


def is_punctuation(word, pos, punct_set=None):
    if punct_set is None:
        return is_uni_punctuation(word)
    else:
        return pos in punct_set or pos == 'PU' # for chinese


def eval(batch_size, words, postags, heads_pred, types_pred, heads, types,
         punct_set=None, symbolic_root=False):
    ucorr = 0.
    lcorr = 0.
    total = 0.
    ucomplete_match = 0.
    lcomplete_match = 0.

    ucorr_nopunc = 0.
    lcorr_nopunc = 0.
    total_nopunc = 0.
    ucomplete_match_nopunc = 0.
    lcomplete_match_nopunc = 0.

    corr_root = 0.
    total_root = 0.
    start = 1 if symbolic_root else 0
    for i in range(batch_size):
        ucm = 1.
        lcm = 1.
        ucm_nopunc = 1.
        lcm_nopunc = 1.
        #assert len(heads[i]) == len(heads_pred[i])
        for j in range(start, len(heads[i])):
            word = words[i][j]

            pos = postags[i][j]

            total += 1
            if int(heads[i][j]) == int(heads_pred[i][j]):
                ucorr += 1
                if types[i][j] == types_pred[i][j]:
                    lcorr += 1
                else:
                    lcm = 0
            else:
                ucm = 0
                lcm = 0

            if not is_punctuation(word, pos, punct_set):
                total_nopunc += 1
                if int(heads[i][j]) == int(heads_pred[i][j]):
                    ucorr_nopunc += 1
                    if types[i][j] == types_pred[i][j]:
                        lcorr_nopunc += 1
                    else:
                        lcm_nopunc = 0
                else:
                    ucm_nopunc = 0
                    lcm_nopunc = 0

            if int(heads_pred[i][j]) == 0:
                total_root += 1
                corr_root += 1 if int(heads[i][j]) == 0 else 0

        ucomplete_match += ucm
        lcomplete_match += lcm
        ucomplete_match_nopunc += ucm_nopunc
        lcomplete_match_nopunc += lcm_nopunc

    print(
        'W. Punct: ucorr: %d, lcorr: %d, total: %d, uas: %.4f%%, las: %.4f%%, ucm: %.4f%%, lcm: %.4f%%' % (
            ucorr, lcorr, total, ucorr * 100 / total, lcorr * 100 / total,
            ucomplete_match * 100 / batch_size, lcomplete_match * 100 / batch_size))
    print(
        'Wo Punct: ucorr: %d, lcorr: %d, total: %d, uas: %.4f%%, las: %.4f%%, ucm: %.4f%%, lcm: %.4f%%' % (
            ucorr_nopunc, lcorr_nopunc, total_nopunc,
            ucorr_nopunc * 100 / total_nopunc,
            lcorr_nopunc * 100 / total_nopunc,
            ucomplete_match_nopunc * 100 / batch_size, lcomplete_match_nopunc * 100 / batch_size))
    print('Root: corr: %d, total: %d, acc: %.4f%%' % (
        corr_root, total_root, corr_root * 100 / total_root))

    uas = ucorr_nopunc * 100 / total_nopunc
    las = lcorr_nopunc * 100 / total_nopunc

    return uas, las

