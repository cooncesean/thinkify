import math


class Tag(object):
    " Model representation of an RFID Tag. "
    def __init__(self, epc_id, frequency=None, slot=None, imag=None,
                 qmag=None, iq_decoded=None, timestamp=None, id_prefix=None):
        self.epc_id = epc_id
        self.frequency = frequency and int(frequency) or None
        self.slot = slot and int(slot, 16) or None
        self.i_magnitude = imag and int(imag, 16) or 0
        self.q_magnitude = qmag and int(qmag, 16) or 0
        self.iq_decoded = iq_decoded
        self.timestamp = timestamp and int(timestamp, 16) or None
        self.trunc_id = id_prefix and epc_id.replace(id_prefix, '') or epc_id

    @property
    def signal_strength(self):
        """
        Return a calculation of signal strength for the given tag. Only
        possible if the I and Q (magnitudes) are set on the Tag instance.
        You can use these fields to calculate an overall signal strength
        for the read that can give you some indication of the range of the
        tag to the antenna.
        """
        high_rssi = 10
        delta_rssi = abs(self.i_magnitude - self.q_magnitude)
        return 2 * high_rssi + 10 * math.log(1 + 10 ** (-delta_rssi / 10.0))
