# ------------------------------------------
#
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------

import numpy as np
import tensorflow.keras as keras


class DataGenerator(keras.utils.Sequence):
    def __init__(self, ids_in_set, labels, samples_dir, batch_size=32, three_d=True, n_channels=1, categorise=True,
                 n_classes=1, shuffle=True):

        self.batch_size = batch_size
        self.three_d = three_d
        self.labels = labels
        self.ids_in_set = ids_in_set
        self.n_channels = n_channels
        self.categorise = categorise
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.samples_dir = samples_dir
        self.on_epoch_end()
        np.random.seed(1)

    def __len__(self):
        return int(np.floor(len(self.ids_in_set) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        batch_lower = index * self.batch_size
        batch_upper = batch_lower + self.batch_size
        indexes = self.indexes[batch_lower:batch_upper]

        # Get selected ids
        ids_in_set_temp = [self.ids_in_set[k] for k in indexes]

        # Generate data from ids
        X, y = self.__data_generation(ids_in_set_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        no_of_ids = len(self.ids_in_set)
        self.indexes = np.arange(no_of_ids)
        if self.shuffle:
            # inds = np.arange(no_of_ids).reshape(-1, self.batch_size)
            np.random.shuffle(self.indexes)
            # self.indexes = inds.flatten()
            # print(self.indexes)

    def __data_generation(self, ids_in_set_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Find the size of this batch
        first_id = ids_in_set_temp[0]
        #first_sample = np.load(self.samples_dir + '/' + first_id + '-sample.npy')
        first_sample = np.load(self.samples_dir + '/' + first_id + '-sample.npy').astype(float)

        # Initialization
        if self.three_d:
            X = np.empty((self.batch_size, *first_sample.shape, self.n_channels))
            #y = np.empty((self.batch_size, *first_sample.shape, self.n_classes), dtype=int)
            y = np.empty((self.batch_size, *first_sample.shape, self.n_classes), dtype=float)
        else:
            X = np.empty((self.batch_size, *first_sample.shape[-2:], self.n_channels))
            #y = np.empty((self.batch_size, *first_sample.shape[-2:], self.n_classes), dtype=int)
            y = np.empty((self.batch_size, *first_sample.shape[-2:], self.n_classes), dtype=float)

        # Generate data
        for i, ID in enumerate(ids_in_set_temp):
            # Store sample
            sample = np.load(self.samples_dir + '/' + ID + '-sample.npy')

            # Store values
            label_id = self.labels[ID]
            labelling = np.load(self.samples_dir + '/' + label_id + '.npy')

            if self.three_d:
                X[i, ] = np.expand_dims(sample, axis=-1)
            else:
                X[i, ] = np.transpose(sample, (1, 2, 0))

            if self.categorise:
                categorical_labelling = keras.utils.to_categorical(labelling, self.n_classes)
                y[i, ] = categorical_labelling
            else:
                # print(np.unique(labelling))
                y[i, ] = np.expand_dims(labelling, axis=-1)

        return X, y
