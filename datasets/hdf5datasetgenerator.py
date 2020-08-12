from keras.utils import np_utils
import numpy as np
import h5py

class HDF5DatasetGenerator:
    def __init__(self, dbPath, batchSize, preprocessors=None,
        aug=None, binarize=True, classes=2):
        
        self.db = h5py.File(dbPath,"r")
        self.numImages = self.db["labels"].shape[0]

        self.batchSize = batchSize
        self.preprocessors = preprocessors
        self.aug = aug
        self.binarize = binarize
        self.classes = classes

    def generator(self, passes=np.inf):
        epochs = 0

        while epochs < passes:
            for i in  np.arange(0, self.numImages, self.batchSize):
                # read batch
                images = self.db["images"][i:i+self.batchSize]
                labels = self.db["labels"][i:i+self.batchSize]

                # process labels
                if self.binarize:
                    labels = np_utils.to_categorical(labels,
                        num_classes=self.classes)

                # process images
                if self.preprocessors is not None:
                    procImages = []
                    for image in images:
                        # apply all preprocessors to each image
                        for p in self.preprocessors:
                            image = p.preprocess(image)
                        procImages.append(image)
                    images = np.array(procImages)
                
                # perform batch augmentation
                if self.aug is not None:
                    (images, labels) = next(self.aug.flow(images,
                        labels, self.batchSize))

                # yield results
                yield (images, labels)

            epochs += 1

    def close(self):
        self.db.close()