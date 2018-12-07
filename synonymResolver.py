from nltk.corpus import wordnet
from pprint import pprint as pp




class DisjointSet(object):

    def __init__(self):
        self.root = {}  # maps a member to the treeSet's root
        self.treeSet = {}
        self.treeSynSet = {}  # maps a treeSet root to the treeSet (which is a set)

    def __init__(self,wordList=[]):
        self.root = {}
        self.treeSet = {}
        self.treeSynSet = {}
        self.buildDsFromList(wordList)

    def getWordSynSet(self, word):
        word_synonyms = set('')
        for synset in wordnet.synsets(word):
            for lemma in synset.lemma_names():
                word_synonyms.add(lemma)
        return word_synonyms

    def add(self, a, b):
        roota = self.root.get(a)
        rootb = self.root.get(b)
        if roota is not None:
            if rootb is not None:
                if roota == rootb: return
                treeSeta = self.treeSet[roota]
                treeSetb = self.treeSet[rootb]
                treeSynSeta = self.treeSynSet[roota]
                treeSynSetb = self.treeSynSet[rootb]
                if len(treeSeta) < len(treeSetb):
                    a, roota, treeSeta, treeSynSeta, b, rootb, treeSetb, treeSynSetb = b, rootb, treeSetb, treeSynSetb, a, roota, treeSeta, treeSynSeta

                    treeSeta |= treeSetb
                    treeSynSeta |= treeSynSetb
                del self.treeSet[rootb]
                del self.treeSynSet[rootb]
                for k in treeSetb:
                    self.root[k] = roota
            else:
                self.treeSet[roota].add(b)
                self.treeSynSet[roota] |= self.getWordSynSet(b)
                self.root[b] = roota
        else:
            if rootb is not None:
                self.treeSet[rootb].add(a)
                self.treeSynSet[rootb] |= self.getWordSynSet(a)
                self.root[a] = rootb
            else:
                self.root[a] = self.root[b] = a
                self.treeSynSet[a] = self.getWordSynSet(a)
                self.treeSynSet[a] |= self.getWordSynSet(b)
                self.treeSet[a] = set([a, b])

    def checkConnection(self, a, b):
        roota = self.root.get(a)
        rootb = self.root.get(b)
        if roota is not None:
            treeSynSeta = self.treeSynSet[roota]
        else:
            treeSynSeta = self.getWordSynSet(a)

        if rootb is not None:
            treeSynSetb = self.treeSynSet[rootb]
        else:
            treeSynSetb = self.getWordSynSet(b)


        return len(treeSynSeta & treeSynSetb) > 0

    def checkNadd(self, a, b):
        if self.checkConnection(a, b):
            self.add(a, b)

    def buildDsFromList(self,wordList):
        for word1 in wordList:
            for word2 in wordList:
                self.checkNadd(word1, word2)


def sampleUsage():
    words = ["meow","cat","hot","spicy","cold","icy","frozen"]
    ds = DisjointSet(wordList=words)
    print("\n")
    pp(ds.root)
    print("\n")
    pp(ds.treeSet)


sampleUsage()