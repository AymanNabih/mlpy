import numpy as np

import mlpy.neuralNetwork.structure.activations as activations

class Layer(object):
    def __init__(self, bounds, size, prev, l_rate = 1, bias = False, label = "Layer"):
        assert isinstance(size, int) and size > 0
        assert isinstance(prev, Layer) or prev == None
        assert isinstance(bias, bool)
        assert isinstance(label, str)

        self.label = label
        self.size = size
        self.prev = prev
        self.l_rate = l_rate
        self.bias = bias

        self.result = np.zeros(size)
        self.error = None
        self.syn = None
        self.deltaWeights = None

        if not prev == None:
            prev.syn =  (bounds.maxBound - bounds.minBound) * np.random.random((self.prev.size + self.prev.bias, self.size)) + bounds.minBound

    def __str__(self):
        return ('======= Layer: {label} =======\n' +
                'Syn: \n' +
                '{syn}\n' +
                'Res: \n' +
                '{res}\n' +
                'Error: \n' +
                '{err}\n' +
                'Delta Weights: \n'+
                '{delta}\n').format(label=self.label,
                                           syn=self.syn, res=self.result, err=self.error, delta=self.deltaWeights)

    def propagate(self):
        if self.prev != None:
            if self.prev.bias:
                self.prev.result = self.addBias(self.prev.result)
            self.result = activations.nonlin(np.dot(self.prev.result, self.prev.syn))

        return self.result

    def calculateOutputDelta(self, target):
        self.error = target - self.result
        self.prev.deltaWeights = self.error * activations.nonlin(self.result, deriv=True)
        return self.error

    def backPropagate(self, delta):
        if not np.any(self.syn):
            return self.calculateOutputDelta(delta)
        elif not self.prev == None:
            self.error = self.deltaWeights.dot(self.syn.T)
            self.prev.deltaWeights = self.error * activations.nonlin(self.result, deriv=True)
            if self.bias:
                self.prev.deltaWeights = self.removeBias(self.prev.deltaWeights)
            return self.error

    def applyDeltaWeights(self):
        if np.any(self.syn):
            self.syn += self.l_rate * self.result.T.dot(self.deltaWeights)

    def addBias(self, arr):
        ones = np.ones((len(arr), 1))
        return np.append(arr, ones, axis=1)

    def removeBias(self, arr):
        return np.delete(arr, len(arr[0]) - 1, axis=1)

    def getWeights(self):
        weights = []
        if np.any(self.syn):
            for neuron in range(len(self.syn)):
                for synapse in range(len(self.syn[0])):
                    weights.append(self.syn[neuron][synapse])
        return weights


    def setWeights(self, weights):
        weightsClone = list(weights)
        if np.any(self.syn):
            for neuron in range(len(self.syn)):
                for synapse in range(len(self.syn[0])):
                    self.syn[neuron][synapse] = weightsClone.pop(0)
        return weightsClone