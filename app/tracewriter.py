'''
TraceWriter - writes bacterio traces to .btf file
'''

from datetime import datetime


class TraceWriter(object):
    '''
    TraceWriter - writes bacterio traces to .btf file
    '''
    __slots__ = ('_file')
    
    def __init__(self, config):
        '''
        'config' is bacterio config.Config object
        '''
        dt = datetime.now()
        fileName = '%s_%04d%02d%02d-%02d-%02d-%02d.btf' % (config.miscParams.traceFilePrefix, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        self._file = open(fileName, 'w')
        self._file.write(repr(config.fieldParams)+'\n')
        self._file.write(repr(config.modelParams)+'\n')
        self._file.write('\nStep\tBacteria\tPredators\n')
    
    def write(self, step, numBacteria, numPredators):
        '''
        Writes one trace row
        '''
        self._file.write(str(step)+'\t'+str(numBacteria)+'\t'+str(numPredators)+'\n')
        
    def __del__(self):
        self._file.close()
