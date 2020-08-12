import h5py
import os 

class HDF5DatasetWriter:
    def __init__(self, dims, outputPath, dataKey="images",bufSize=1000):
    # verify that file doesnt exist
        if os.path.exists(outputPath):
            raise ValueError("Specified path to HDF5 file already exists",
                outputPath)
    
    # initialize HDF5 database
        self.db = h5py.File(outputPath, 'w')
        self.data = self.db.create_dataset(dataKey, dims, dtype="float")
        self.labels = self.db.create_dataset("labels", (dims[0],), dtype="int")

        # create buffer
        self.buffer = {"data": [], "labels": []}
        self.bufSize = bufSize
        self.startIdx = 0

    def add(self, rows, labels):
        # add data to buffer, if buffer is full flush it to 
        # the database
        self.buffer["data"].extend(rows)
        self.buffer["labels"].extend(labels)

        if len(self.buffer["data"]) >= self.bufSize:
            self.flush()


    def flush(self):
        # calculate the inserting range to hdf5 database for the buffer 
        endIdx = self.startIdx + len(self.buffer["data"])
        self.data[self.startIdx:endIdx] = self.buffer["data"]
        self.labels[self.startIdx:endIdx] = self.buffer["labels"]
        
        # update start and reset buffer
        self.startIdx = endIdx
        self.buffer = {"data": [], "labels": []}

    def storeClassLabels(self, classLabels):
        # create a dataset to store the actual class label names,
        # then store the class labels
        dt = h5py.special_dtype(vlen=str)
        labelSet = self.db.create_dataset("label_names",
            (len(classLabels),), dtype=dt)
        labelSet[:] = classLabels

    def close(self):
        if len(self.buffer["data"]) > 0:
            self.flush()
        self.db.close()