import serial
import time

from thinkify.tag import Tag


class ThinkifyReader(object):
    """
    Wrapper for the Thinkify TR-200 RFID Reader API.

    Usage:
        >>> from thinkify.reader import ThinkifyReader
        >>> reader = ThinkifyReader('/dev/tty.usbmodem1411')
        >>> reader.get_version()
        VERSION=2.2.3
        >>> tag_list = reader.get_tags()
        >>> [tag.epc_id for tag in tag_list]
        <epc_id_1>
        <epc_id_2>
        ....
    """
    def __init__(self, port, baudrate=115200, tag_id_prefix=None):
        """
        Initalizes an connection to a connected (via USB) ThinkifyReader
        TR-200 and abstracts common commands to get and set data to/from the
        device.

        Params:
            @port (str) => The path to the modem on disk. On a Mac/Linux
            this should be somewhere in /dev/, typically the
            path is: `/dev/tty.usbmodem1411` but can vary based
            on your configuration.

            @baudrate (int) => An optional argument allowing one to override
            the default `115200`.

            @tag_id_prefix (str) => Optional string prefix for similar tags.
            It allows the developer to parse the `epc_id` when  instantiating
            new `Tag` objects and provides access to the truncated Tag id using
            the `Tag.trunc_id` property.
        """
        self.port = port
        self.baudrate = baudrate
        self.tag_id_prefix = tag_id_prefix
        self.serial = serial.Serial(port, baudrate)
        self.serial.flushInput()

    def _format_response(self, response):
        " Trim response cruft. "
        return response.replace('\r\n\r\nREADY>', '')

    def _issue_command(self, command):
        """
        Util method to issue any command passed to the method to the reader.
        This method is used by a number of public methods on the class and
        may be used issue whatever you'd like to the reader given the
        documentation here: http://bit.ly/1dKFJ5x
        """
        # Issue the read command to the device
        self.serial.write('%s\r' % command)

        # Need to wait for just a bit to get a round trip response
        time.sleep(.1)

        # Read and format the response from the device
        response = self.serial.read(self.serial.inWaiting())
        return response

    def get_version(self):
        " Returns the firmware version on the device. "
        response = self._issue_command('v')
        return self._format_response(response)

    # TAG READING METHODS ####################################################
    # These methods attempt to read tags using the current settings on the
    # device.
    ##########################################################################
    def get_tags(self, print_response=False):
        """
        Runs a single `ping` checking for any and all tags within the reader's
        read current range and returns a list of `Tag` objects with their
        respective epc_ids (tag ids).
        """
        start = time.time()
        response = self._issue_command('t')
        response = self._format_response(response)
        if print_response:
            print response

        # Instantiate a list of Tag objects for each line of the response
        tag_list = []
        for response_line in response.split('\r\n'):
            if response_line.startswith('TAG='):
                tag_list.append(Tag(response_line.replace('TAG=', '')))
        print 'time: ', time.time() - start
        return tag_list

    def get_tags_with_epc_data(self, print_response=False):
        " Similar to `get_tags()` but returns each Tag's entire `epc` data. "
        self._issue_command('ix1')
        response = self._issue_command('t')
        if print_response:
            print self._format_response(response)
        self._issue_command('ix0')

        # Instantiate a list of Tag objects
        tag_list = []
        for response_line in response.split('\r\n'):
            if response_line.startswith('TAG='):
                tag_parts = response_line.replace('TAG=', '').split(' ')
                t = Tag(
                        tag_parts[0],           # Tag ID
                        tag_parts[1],           # Frequency
                        tag_parts[2],           # Slot
                        tag_parts[3],           # I magnitude
                        tag_parts[4],           # Q magnitude
                        tag_parts[5],           # Decoded
                        tag_parts[6],           # Timestamp of read
                        self.tag_id_prefix,
                    )
                tag_list.append(t)
        return tag_list

    def get_closest_tag(self):
        " Return the closest Tag instance. "
        start = time.time()
        tag_list = self.get_tags_with_epc_data()
        closest_tag = None
        if len(tag_list) >= 1:
            tag_list.sort(key=lambda x: x.signal_strength, reverse=True)
            closest_tag = tag_list[0]
        print 'time: ', time.time() - start
        return closest_tag

    def get_most_recent_tag_indefinitely(self):
        """
        Return the last properly formatted tag after issuing a `t6` command.
        The `t6` command sets the reader to loop indefinitely and streams
        tag data (as soon as it is found) back to the serial port.

        This function listens for valid tag data and returns a Tag instance
        given the most recent (valid) Tag ID.
        """
        self._issue_command('t6')
        while True:
            data = self.serial.read(self.serial.inWaiting())
            # print 'data', data, len(data), time.time()
            if self.tag_id_prefix and data and len(data) > len(self.tag_id_prefix) + 10:
                try:
                    epc_id = data.split('TAG=')[1].split(' ')[0]
                    self._issue_command(' \r')
                    self.serial.flushInput()
                    return Tag(epc_id, id_prefix=self.tag_id_prefix)
                except IndexError:
                    print 'IndexError', data

    # AMPLIFIER (ANTENNA) METHODS ############################################
    # Used to set and get the parameters tha control the characteristics of
    # the amplifier in the base band receiver.
    ##########################################################################
    def get_amplifier_settings(self):
        " Returns the current amplifier settings on the antenna. "
        response = self._issue_command('a')
        return self._format_response(response)

    def set_amplifier_gain(self, gain_code):
        """
        Sets the amplifier's gain on the antenna.

        Params:
            @gain_code (int) => The id of the gain you want to tune the
            antenna to. The list of valid gain codes can be found in
            `view_gain_codes()`.
        """
        if gain_code not in range(0, 6):
            raise Exception("""
                The gain code `%d` is invalid. Valid gains must be an integer
                between 0-6. Check the `view_gain_codes()` method for more
                info on valid codes.
            """ % gain)
        self.serial.write('ag%d\r' % gain_code)

    def view_gain_codes(self):
        " Return a list of valid `gain` codes for the device. "
        print 'Gain Codes And Their Corresponding Values:'
        print 'Value\tGain'
        print '--------------'
        print '%d\t%s' % (0, '0dB')
        print '%d\t%s' % (1, '-9dB')
        print '%d\t%s' % (2, '-6dB')
        print '%d\t%s' % (3, '-3dB')
        print '%d\t%s' % (4, '+3dB')
        print '%d\t%s' % (5, '+6dB')
        print '%d\t%s' % (6, '+9dB')

    def set_amplifier_mixer_amplification_control(self, value):
        """
        Toggle the device's 10dB mixer amplifcation control.

        Params:
            @value (bool) => Toggle value. True turns the mixer amp on
            while False turns it off.
        """
        self.serial.write('am%d\r' % (value and 1 or 0))

    # INVENTORY METHODS ######################################################
    # Used to set and get the parameters that control the flow of the Gen2
    # anti-collision algorithm. Modifications to the default parameters may
    # be helpful in cases where there are a large number of tags in the field
    # or when it is desirable to increase the number of redundant reads for
    # a given tag.
    ##########################################################################
    def get_inventory_settings(self):
        " Return the current inventory settings on the device. "
        response = self._issue_command('i')
        return self._format_response(response)
