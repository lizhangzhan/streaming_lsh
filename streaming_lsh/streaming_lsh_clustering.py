'''
Created on Jun 25, 2011

@author: kykamath
'''
from classes import RandomGaussianUnitVector, VectorPermutation,\
    SignaturePermutationWithTrie, Cluster, UtilityMethods,\
    SignaturePermutationWithSortedList
from operator import itemgetter
from library.classes import TwoWayMap

class StreamingLSHClustering(object):
    def __init__(self, **clustering_settings):
        self.thresholdForDocumentToBeInACluster = clustering_settings['threshold_for_document_to_be_in_cluster']
        self.unitVector = RandomGaussianUnitVector(dimensions=clustering_settings['dimensions'], mu=0, sigma=1)
        self.vectorPermutations = VectorPermutation.getPermutations(clustering_settings['signature_length'], clustering_settings['dimensions'], self.unitVector)
        signatureType = clustering_settings.get('signature_type', 'signature_type_trie')
        if signatureType=='signature_type_trie': self.signaturePermutations = [SignaturePermutationWithTrie(clustering_settings['signature_length']) for i in range(clustering_settings['number_of_permutations'])]
        else: self.signaturePermutations = [SignaturePermutationWithSortedList(clustering_settings['signature_length']) for i in range(clustering_settings['number_of_permutations'])]
        self.phraseTextAndDimensionMap, self.clusters = TwoWayMap(), {}
        self.clustering_settings = clustering_settings
    
    def getClusterForDocument(self, document):
        UtilityMethods.updatePhraseTextAndDimensionsMap(document, self.phraseTextAndDimensionMap, **self.clustering_settings)
        document.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)
        predictedCluster = None
        possibleNearestNeighbors = reduce(lambda x,y:x.union(y), (permutation.getNearestDocuments(document) for permutation in self.signaturePermutations), set())
        if possibleNearestNeighbors: predictedCluster = max(((clusterId, self.clusters[clusterId].cosineSimilarity(document)) for clusterId in possibleNearestNeighbors), key=itemgetter(1))
        if predictedCluster and predictedCluster[1]>=self.thresholdForDocumentToBeInACluster:return predictedCluster[0]
    
    def getClusterAndUpdateExistingClusters(self, document):
        predictedCluster = self.getClusterForDocument(document)
        if predictedCluster!=None: self.clusters[predictedCluster].addDocument(document)
        else:
            newCluster = Cluster(document)
            newCluster.setSignatureUsingVectorPermutations(self.unitVector, self.vectorPermutations, self.phraseTextAndDimensionMap)
            for permutation in self.signaturePermutations: permutation.addDocument(newCluster)
            self.clusters[newCluster.clusterId] = newCluster
