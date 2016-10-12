# deepharmony


Deep Harmony is a machine learning project for creating harmonies based on a given melody.

Using LSTM neural networks to produce accompaniments for melodies. Developed for a music practicum class at WPI.

Currently, Deep Harmony is learning to mimic the behavior of Bach Chorales created by [David Cope](http://artsites.ucsc.edu/faculty/cope/).

Deep Harmony is written in [Python 3.5](https://www.python.org) and uses the [Keras](https://keras.io Keras) machine learning library.

## Dependencies:
* [Jupyter Notebook](http://jupyter.org), an interactive programming environment and editor (necessary for using the .ipynb files)
* Python 3.5, and the following libraries:
* numpy and matplotlib, for numerical computation and graphical plotting.
    * [music21](http://web.mit.edu/music21), for processing music data
    * [tqdm](https://pypi.python.org/pypi/tqdm), for nice progress bars
    * [Keras](https://keras.io), a deep learning library. We recommend installing it with the Theano backend, but the code should work with the TensorFlow backend as well.
* musescore 2+, for allowing music21 to render music as pictures

Jupyter Notebook, Python, Numpy, and Matplotlib are all packaged together in [Anaconda](https://www.continuum.io/downloads), and we recommend installing them that way.
