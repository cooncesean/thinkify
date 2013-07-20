class Tag(object):
    " Model representation of an RFID Tag. "
    def __init__(self, epc_id, frequency=None, slot=None, imag=None,
                 qmag=None, decoded=None, timestamp=None):
        self.epc_id = epc_id
        self.frequency = frequency
        self.slot = slot
        self.imag = imag
        self.qmag = qmag
        self.decoded = decoded
        self.timestamp = timestamp
