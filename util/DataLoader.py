import numpy as np
import gzip

class DataLoader:

    # Read probability files: pairs of phrases/sentences with p(x), p(y), p(x|y) values
    def gzread_cpr(self, s, word_to_index):
        s1 = []
        p1 = []
        s2 = []
        p2 = []
        pr_x = []
        pr_y = []
        pr_xy = []
        cpr_xy = []
        l1 = []
        l2 = []
        labels = []
        max_length = 0
        for line in gzip.open(s):
            tokens = line.strip().split("\t")
            t1 = []
            p1.append(tokens[0])
            for a in tokens[0].split():
                if a in word_to_index:
                    t1.append(word_to_index[a])
                else:
                    t1.append(word_to_index['oov'])
            s1.append(t1)
            t2 = []
            p2.append(tokens[2])
            for a in tokens[2].split():
                if a in word_to_index:
                    t2.append(word_to_index[a])
                else:
                    t2.append(word_to_index['oov'])
            s2.append(t2)
            pr_x.append(float(tokens[1]))
            pr_y.append(float(tokens[3]))
            pr_xy.append(max(1e-20, float(tokens[4])))
            cpr_xy.append(max(1e-20, float(tokens[5])))
            l1.append(len(t1))
            l2.append(len(t2))
            max_length = max(max_length, len(t1))
            max_length = max(max_length, len(t2))
            if len(tokens) == 7: # has entailment label
                labels.append(tokens[6])
        return s1, s2, np.array(pr_x), np.array(pr_y), np.array(pr_xy), np.array(cpr_xy), np.array(l1), np.array(
            l2), max_length, p1, p2, labels

    def read_glove_vectors(self, file):
        matrix = []
        embedding_size = 0
        word_to_index = {}
        count = 0
        for line in gzip.open(file):
            tokens = line.strip().split()
            temp = []
            for t in tokens[1:]:
                temp.append(float(t))
            matrix.append(temp)
            word_to_index[tokens[0]] = count
            count += 1
            embedding_size = len(temp)
        # append vector for OOV
        np_matrix = np.array(matrix)
        oov_vector = np.random.uniform(-1.0, 1.0, [1, embedding_size])
        np_matrix = np.concatenate((np_matrix, oov_vector))
        word_to_index["oov"] = count
        return np_matrix, word_to_index

    def pad_tensor(self, data, maxlength):
        padded_data = []
        for idx, line in enumerate(data):
            temp_line = line[:]
            while len(temp_line) < maxlength:
                temp_line.append(0)
            while len(temp_line) > maxlength:
                del temp_line[-1]
            padded_data.append(temp_line)
        return np.array(padded_data)
