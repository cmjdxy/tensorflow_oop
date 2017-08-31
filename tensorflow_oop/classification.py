import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
include_dir = os.path.join(script_dir, '../')
if include_dir not in sys.path:
    sys.path.append(include_dir)
from tensorflow_oop.neural_network import *

class TFClassifier(TFNeuralNetwork):

    """
    Classification model with Cross entropy loss function.
    """

    __slots__ = TFNeuralNetwork.__slots__ + ['probabilities']

    def initialize(self,
                   inputs_shape,
                   targets_shape,
                   outputsshape,
                   inputs_type=tf.float32,
                   targets_type=tf.float32,
                   outputstype=tf.float32,
                   reset=True,
                   **kwargs):
        """Initialize model.

        Arguments:
            inputs_shape -- shape of inputs layer
            targets_shape -- shape of targets layer
            outputsshape -- shape of outputs layer
            inputs_type -- type of inputs layer
            targets_type -- type of targets layer
            outputstype -- type of outputs layer
            reset -- indicator of clearing default graph
            kwargs -- dictionary of keyword arguments

        """
        super(TFClassifier, self).initialize(inputs_shape,
                                             outputsshape,
                                             inputs_type=inputs_type,
                                             outputstype=outputstype,
                                             reset=reset,
                                             **kwargs)

        # Add probability operation
        self.probabilities = tf.nn.softmax(self.outputs)

        # Add accuracy metric
        def accuracy_function(targets, outputs):
            correct_prediction = tf.equal(tf.argmax(targets, 1), tf.argmax(outputs, 1))
            return tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        self.add_metric('accuracy', accuracy_function)

    def loss_function(self, targets, outputs, **kwargs):
        """Cross entropy."""
        return tf.losses.softmax_cross_entropy(labels_placeholder, outputs) 

    @check_inputs_values
    def probabilities(self, inputs_values):
        """Get probabilites."""
        return self.sess.run(self.probabilities, feed_dict={
            self.inputs: inputs_values,
        })

    @check_inputs_values
    def classify(self, inputs_values):
        """Best prediction."""
        return self.sess.run(tf.argmax(self.probabilities, 1), feed_dict={
            self.inputs: inputs_values,
        })
