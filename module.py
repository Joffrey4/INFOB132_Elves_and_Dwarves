# coding=utf-8
import wave
import time
import random

import pickle
import socket
# ======================================PYAUDIO & WAVE=============================================================
# PyAudio : Python Bindings for PortAudio.

# Copyright (c) 2006 Hubert Pham

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
PyAudio provides Python bindings for PortAudio, the cross-platform
audio I/O library. With PyAudio, you can easily use Python to play and
record audio on a variety of platforms.  PyAudio is inspired by:

* pyPortAudio/fastaudio: Python bindings for PortAudio v18 API.
* tkSnack: cross-platform sound toolkit for Tcl/Tk and Python.

.. include:: ../sphinx/examples.rst

Overview
--------

**Classes**
  :py:class:`PyAudio`, :py:class:`Stream`

.. only:: pamac

   **Host Specific Classes**
     :py:class:`PaMacCoreStreamInfo`

**Stream Conversion Convenience Functions**
  :py:func:`get_sample_size`, :py:func:`get_format_from_width`

**PortAudio version**
  :py:func:`get_portaudio_version`, :py:func:`get_portaudio_version_text`

.. |PaSampleFormat| replace:: :ref:`PortAudio Sample Format <PaSampleFormat>`
.. _PaSampleFormat:

**Portaudio Sample Formats**
  :py:data:`paFloat32`, :py:data:`paInt32`, :py:data:`paInt24`,
  :py:data:`paInt16`, :py:data:`paInt8`, :py:data:`paUInt8`,
  :py:data:`paCustomFormat`

.. |PaHostAPI| replace:: :ref:`PortAudio Host API <PaHostAPI>`
.. _PaHostAPI:

**PortAudio Host APIs**
  :py:data:`paInDevelopment`, :py:data:`paDirectSound`, :py:data:`paMME`,
  :py:data:`paASIO`, :py:data:`paSoundManager`, :py:data:`paCoreAudio`,
  :py:data:`paOSS`, :py:data:`paALSA`, :py:data:`paAL`, :py:data:`paBeOS`,
  :py:data:`paWDMKS`, :py:data:`paJACK`, :py:data:`paWASAPI`,
  :py:data:`paNoDevice`

.. |PaErrorCode| replace:: :ref:`PortAudio Error Code <PaErrorCode>`
.. _PaErrorCode:

**PortAudio Error Codes**
  :py:data:`paNoError`, :py:data:`paNotInitialized`,
  :py:data:`paUnanticipatedHostError`, :py:data:`paInvalidChannelCount`,
  :py:data:`paInvalidSampleRate`, :py:data:`paInvalidDevice`,
  :py:data:`paInvalidFlag`, :py:data:`paSampleFormatNotSupported`,
  :py:data:`paBadIODeviceCombination`, :py:data:`paInsufficientMemory`,
  :py:data:`paBufferTooBig`, :py:data:`paBufferTooSmall`,
  :py:data:`paNullCallback`, :py:data:`paBadStreamPtr`,
  :py:data:`paTimedOut`, :py:data:`paInternalError`,
  :py:data:`paDeviceUnavailable`,
  :py:data:`paIncompatibleHostApiSpecificStreamInfo`,
  :py:data:`paStreamIsStopped`, :py:data:`paStreamIsNotStopped`,
  :py:data:`paInputOverflowed`, :py:data:`paOutputUnderflowed`,
  :py:data:`paHostApiNotFound`, :py:data:`paInvalidHostApi`,
  :py:data:`paCanNotReadFromACallbackStream`,
  :py:data:`paCanNotWriteToACallbackStream`,
  :py:data:`paCanNotReadFromAnOutputOnlyStream`,
  :py:data:`paCanNotWriteToAnInputOnlyStream`,
  :py:data:`paIncompatibleStreamHostApi`

.. |PaCallbackReturnCodes| replace:: :ref:`PortAudio Callback Return Code <PaCallbackReturnCodes>`
.. _PaCallbackReturnCodes:

**PortAudio Callback Return Codes**
  :py:data:`paContinue`, :py:data:`paComplete`, :py:data:`paAbort`

.. |PaCallbackFlags| replace:: :ref:`PortAutio Callback Flag <PaCallbackFlags>`
.. _PaCallbackFlags:

**PortAudio Callback Flags**
  :py:data:`paInputUnderflow`, :py:data:`paInputOverflow`,
  :py:data:`paOutputUnderflow`, :py:data:`paOutputOverflow`,
  :py:data:`paPrimingOutput`
"""

__author__ = "Hubert Pham"
__version__ = "0.2.9"
__docformat__ = "restructuredtext en"

import sys

# attempt to import PortAudio
try:
    import _portaudio as pa
except ImportError:
    print("Could not import the PyAudio C module '_portaudio'.")
    raise

############################################################
# GLOBALS
############################################################

##### PaSampleFormat Sample Formats #####

paFloat32      = pa.paFloat32      #: 32 bit float
paInt32        = pa.paInt32        #: 32 bit int
paInt24        = pa.paInt24        #: 24 bit int
paInt16        = pa.paInt16        #: 16 bit int
paInt8         = pa.paInt8         #: 8 bit int
paUInt8        = pa.paUInt8        #: 8 bit unsigned int
paCustomFormat = pa.paCustomFormat #: a custom data format

###### HostAPI TypeId #####

paInDevelopment = pa.paInDevelopment #: Still in development
paDirectSound   = pa.paDirectSound   #: DirectSound (Windows only)
paMME           = pa.paMME           #: Multimedia Extension (Windows only)
paASIO          = pa.paASIO          #: Steinberg Audio Stream Input/Output
paSoundManager  = pa.paSoundManager  #: SoundManager (OSX only)
paCoreAudio     = pa.paCoreAudio     #: CoreAudio (OSX only)
paOSS           = pa.paOSS           #: Open Sound System (Linux only)
paALSA          = pa.paALSA          #: Advanced Linux Sound Architecture (Linux only)
paAL            = pa.paAL            #: Open Audio Library
paBeOS          = pa.paBeOS          #: BeOS Sound System
paWDMKS         = pa.paWDMKS         #: Windows Driver Model (Windows only)
paJACK          = pa.paJACK          #: JACK Audio Connection Kit
paWASAPI        = pa.paWASAPI        #: Windows Vista Audio stack architecture
paNoDevice      = pa.paNoDevice      #: Not actually an audio device

###### portaudio error codes #####

paNoError                               = pa.paNoError
paNotInitialized                        = pa.paNotInitialized
paUnanticipatedHostError                = pa.paUnanticipatedHostError
paInvalidChannelCount                   = pa.paInvalidChannelCount
paInvalidSampleRate                     = pa.paInvalidSampleRate
paInvalidDevice                         = pa.paInvalidDevice
paInvalidFlag                           = pa.paInvalidFlag
paSampleFormatNotSupported              = pa.paSampleFormatNotSupported
paBadIODeviceCombination                = pa.paBadIODeviceCombination
paInsufficientMemory                    = pa.paInsufficientMemory
paBufferTooBig                          = pa.paBufferTooBig
paBufferTooSmall                        = pa.paBufferTooSmall
paNullCallback                          = pa.paNullCallback
paBadStreamPtr                          = pa.paBadStreamPtr
paTimedOut                              = pa.paTimedOut
paInternalError                         = pa.paInternalError
paDeviceUnavailable                     = pa.paDeviceUnavailable
paIncompatibleHostApiSpecificStreamInfo = pa.paIncompatibleHostApiSpecificStreamInfo
paStreamIsStopped                       = pa.paStreamIsStopped
paStreamIsNotStopped                    = pa.paStreamIsNotStopped
paInputOverflowed                       = pa.paInputOverflowed
paOutputUnderflowed                     = pa.paOutputUnderflowed
paHostApiNotFound                       = pa.paHostApiNotFound
paInvalidHostApi                        = pa.paInvalidHostApi
paCanNotReadFromACallbackStream         = pa.paCanNotReadFromACallbackStream
paCanNotWriteToACallbackStream          = pa.paCanNotWriteToACallbackStream
paCanNotReadFromAnOutputOnlyStream      = pa.paCanNotReadFromAnOutputOnlyStream
paCanNotWriteToAnInputOnlyStream        = pa.paCanNotWriteToAnInputOnlyStream
paIncompatibleStreamHostApi             = pa.paIncompatibleStreamHostApi

###### portaudio callback return codes ######

paContinue = pa.paContinue #: There is more audio data to come
paComplete = pa.paComplete #: This was the last block of audio data
paAbort    = pa.paAbort    #: An error ocurred, stop playback/recording

###### portaudio callback flags ######

paInputUnderflow  = pa.paInputUnderflow  #: Buffer underflow in input
paInputOverflow   = pa.paInputOverflow   #: Buffer overflow in input
paOutputUnderflow = pa.paOutputUnderflow #: Buffer underflow in output
paOutputOverflow  = pa.paOutputOverflow  #: Buffer overflow in output
paPrimingOutput   = pa.paPrimingOutput   #: Just priming, not playing yet

############################################################
# Convenience Functions
############################################################

def get_sample_size(format):
    """
    Returns the size (in bytes) for the specified
    sample *format*.

    :param format: A |PaSampleFormat| constant.
    :raises ValueError: on invalid specified `format`.
    :rtype: integer
    """

    return pa.get_sample_size(format)

def get_format_from_width(width, unsigned=True):
    """
    Returns a PortAudio format constant for the specified *width*.

    :param width: The desired sample width in bytes (1, 2, 3, or 4)
    :param unsigned: For 1 byte width, specifies signed or unsigned format.

    :raises ValueError: when invalid *width*
    :rtype: A |PaSampleFormat| constant
    """

    if width == 1:
        if unsigned:
            return paUInt8
        else:
            return paInt8
    elif width == 2:
        return paInt16
    elif width == 3:
        return paInt24
    elif width == 4:
        return paFloat32
    else:
        raise ValueError("Invalid width: %d" % width)


############################################################
# Versioning
############################################################

def get_portaudio_version():
    """
    Returns portaudio version.

    :rtype: string
    """

    return pa.get_version()

def get_portaudio_version_text():
    """
    Returns PortAudio version as a text string.

    :rtype: string
    """

    return pa.get_version_text()

############################################################
# Wrapper around _portaudio Stream (Internal)
############################################################

# Note: See PyAudio class below for main export.

class Stream:
    """
    PortAudio Stream Wrapper. Use :py:func:`PyAudio.open` to make a new
    :py:class:`Stream`.

    **Opening and Closing**
      :py:func:`__init__`, :py:func:`close`

    **Stream Info**
      :py:func:`get_input_latency`, :py:func:`get_output_latency`,
      :py:func:`get_time`, :py:func:`get_cpu_load`

    **Stream Management**
      :py:func:`start_stream`, :py:func:`stop_stream`, :py:func:`is_active`,
      :py:func:`is_stopped`

    **Input Output**
      :py:func:`write`, :py:func:`read`, :py:func:`get_read_available`,
      :py:func:`get_write_available`
    """

    def __init__(self,
                 PA_manager,
                 rate,
                 channels,
                 format,
                 input=False,
                 output=False,
                 input_device_index=None,
                 output_device_index=None,
                 frames_per_buffer=1024,
                 start=True,
                 input_host_api_specific_stream_info=None,
                 output_host_api_specific_stream_info=None,
                 stream_callback=None):
        """
        Initialize a stream; this should be called by
        :py:func:`PyAudio.open`. A stream can either be input, output,
        or both.

        :param PA_manager: A reference to the managing :py:class:`PyAudio`
            instance
        :param rate: Sampling rate
        :param channels: Number of channels
        :param format: Sampling size and format. See |PaSampleFormat|.
        :param input: Specifies whether this is an input stream.
            Defaults to ``False``.
        :param output: Specifies whether this is an output stream.
            Defaults to ``False``.
        :param input_device_index: Index of Input Device to use.
            Unspecified (or ``None``) uses default device.
            Ignored if `input` is ``False``.
        :param output_device_index:
            Index of Output Device to use.
            Unspecified (or ``None``) uses the default device.
            Ignored if `output` is ``False``.
        :param frames_per_buffer: Specifies the number of frames per buffer.
        :param start: Start the stream running immediately.
            Defaults to ``True``. In general, there is no reason to set
            this to ``False``.
        :param input_host_api_specific_stream_info: Specifies a host API
            specific stream information data structure for input.

            .. only:: pamac

               See :py:class:`PaMacCoreStreamInfo`.

        :param output_host_api_specific_stream_info: Specifies a host API
            specific stream information data structure for output.

            .. only:: pamac

               See :py:class:`PaMacCoreStreamInfo`.

        :param stream_callback: Specifies a callback function for
            *non-blocking* (callback) operation.  Default is
            ``None``, which indicates *blocking* operation (i.e.,
            :py:func:`Stream.read` and :py:func:`Stream.write`).  To use
            non-blocking operation, specify a callback that conforms
            to the following signature:

            .. code-block:: python

               callback(in_data,      # recorded data if input=True; else None
                        frame_count,  # number of frames
                        time_info,    # dictionary
                        status_flags) # PaCallbackFlags

            ``time_info`` is a dictionary with the following keys:
            ``input_buffer_adc_time``, ``current_time``, and
            ``output_buffer_dac_time``; see the PortAudio
            documentation for their meanings.  ``status_flags`` is one
            of |PaCallbackFlags|.

            The callback must return a tuple:

            .. code-block:: python

                (out_data, flag)

            ``out_data`` is a byte array whose length should be the
            (``frame_count * channels * bytes-per-channel``) if
            ``output=True`` or ``None`` if ``output=False``.  ``flag``
            must be either :py:data:`paContinue`, :py:data:`paComplete` or
            :py:data:`paAbort` (one of |PaCallbackReturnCodes|).
            When ``output=True`` and ``out_data`` does not contain at
            least ``frame_count`` frames, :py:data:`paComplete` is
            assumed for ``flag``.

            **Note:** ``stream_callback`` is called in a separate
            thread (from the main thread).  Exceptions that occur in
            the ``stream_callback`` will:

            1. print a traceback on standard error to aid debugging,
            2. queue the exception to be thrown (at some point) in
               the main thread, and
            3. return `paAbort` to PortAudio to stop the stream.

            **Note:** Do not call :py:func:`Stream.read` or
            :py:func:`Stream.write` if using non-blocking operation.

            **See:** PortAudio's callback signature for additional
            details: http://portaudio.com/docs/v19-doxydocs/portaudio_8h.html#a8a60fb2a5ec9cbade3f54a9c978e2710

        :raise ValueError: Neither input nor output are set True.
        """

        # no stupidity allowed
        if not (input or output):
            raise ValueError("Must specify an input or output " + "stream.")

        # remember parent
        self._parent = PA_manager

        # remember if we are an: input, output (or both)
        self._is_input = input
        self._is_output = output

        # are we running?
        self._is_running = start

        # remember some parameters
        self._rate = rate
        self._channels = channels
        self._format = format
        self._frames_per_buffer = frames_per_buffer

        arguments = {
            'rate' : rate,
            'channels' : channels,
            'format' : format,
            'input' : input,
            'output' : output,
            'input_device_index' : input_device_index,
            'output_device_index' : output_device_index,
            'frames_per_buffer' : frames_per_buffer}

        if input_host_api_specific_stream_info:
            _l = input_host_api_specific_stream_info
            arguments[
                'input_host_api_specific_stream_info'
                ] = _l._get_host_api_stream_object()

        if output_host_api_specific_stream_info:
            _l = output_host_api_specific_stream_info
            arguments[
                'output_host_api_specific_stream_info'
                ] = _l._get_host_api_stream_object()

        if stream_callback:
            arguments['stream_callback'] = stream_callback

        # calling pa.open returns a stream object
        self._stream = pa.open(**arguments)

        self._input_latency = self._stream.inputLatency
        self._output_latency = self._stream.outputLatency

        if self._is_running:
            pa.start_stream(self._stream)

    def close(self):
        """ Close the stream """

        pa.close(self._stream)

        self._is_running = False

        self._parent._remove_stream(self)


    ############################################################
    # Stream Info
    ############################################################

    def get_input_latency(self):
        """
        Return the input latency.

        :rtype: float
        """

        return self._stream.inputLatency

    def get_output_latency(self):
        """
        Return the input latency.

        :rtype: float
        """

        return self._stream.outputLatency

    def get_time(self):
        """
        Return stream time.

        :rtype: float
        """

        return pa.get_stream_time(self._stream)

    def get_cpu_load(self):
        """
        Return the CPU load.  This is always 0.0 for the
        blocking API.

        :rtype: float
        """

        return pa.get_stream_cpu_load(self._stream)


    ############################################################
    # Stream Management
    ############################################################

    def start_stream(self):
        """ Start the stream. """

        if self._is_running:
            return

        pa.start_stream(self._stream)
        self._is_running = True

    def stop_stream(self):
        """
        Stop the stream. Once the stream is stopped, one may not call
        write or read.  Call :py:func:`start_stream` to resume the
        stream.
        """

        if not self._is_running:
            return

        pa.stop_stream(self._stream)
        self._is_running = False

    def is_active(self):
        """
        Returns whether the stream is active.

        :rtype: bool
        """

        return pa.is_stream_active(self._stream)

    def is_stopped(self):
        """
        Returns whether the stream is stopped.

        :rtype: bool
        """

        return pa.is_stream_stopped(self._stream)


    ############################################################
    # Reading/Writing
    ############################################################

    def write(self, frames, num_frames=None,
              exception_on_underflow=False):

        """
        Write samples to the stream.  Do not call when using
        *non-blocking* mode.

        :param frames:
           The frames of data.
        :param num_frames:
           The number of frames to write.
           Defaults to None, in which this value will be
           automatically computed.
        :param exception_on_underflow:
           Specifies whether an IOError exception should be thrown
           (or silently ignored) on buffer underflow. Defaults
           to False for improved performance, especially on
           slower platforms.

        :raises IOError: if the stream is not an output stream
           or if the write operation was unsuccessful.

        :rtype: `None`
        """

        if not self._is_output:
            raise IOError("Not output stream",
                          paCanNotWriteToAnInputOnlyStream)

        if num_frames == None:
            # determine how many frames to read
            width = get_sample_size(self._format)
            num_frames = int(len(frames) / (self._channels * width))
            #print len(frames), self._channels, self._width, num_frames

        pa.write_stream(self._stream, frames, num_frames,
                        exception_on_underflow)


    def read(self, num_frames, exception_on_overflow=True):
        """
        Read samples from the stream.  Do not call when using
        *non-blocking* mode.

        :param num_frames: The number of frames to read.
        :param exception_on_overflow:
           Specifies whether an IOError exception should be thrown
           (or silently ignored) on input buffer overflow. Defaults
           to True.
        :raises IOError: if stream is not an input stream
          or if the read operation was unsuccessful.
        :rtype: string
        """

        if not self._is_input:
            raise IOError("Not input stream",
                          paCanNotReadFromAnOutputOnlyStream)

        return pa.read_stream(self._stream, num_frames, exception_on_overflow)

    def get_read_available(self):
        """
        Return the number of frames that can be read without waiting.

        :rtype: integer
        """

        return pa.get_stream_read_available(self._stream)


    def get_write_available(self):
        """
        Return the number of frames that can be written without
        waiting.

        :rtype: integer

        """

        return pa.get_stream_write_available(self._stream)



############################################################
# Main Export
############################################################

class PyAudio:

    """
    Python interface to PortAudio. Provides methods to:
     - initialize and terminate PortAudio
     - open and close streams
     - query and inspect the available PortAudio Host APIs
     - query and inspect the available PortAudio audio
       devices

    Use this class to open and close streams.

    **Stream Management**
      :py:func:`open`, :py:func:`close`

    **Host API**
      :py:func:`get_host_api_count`, :py:func:`get_default_host_api_info`,
      :py:func:`get_host_api_info_by_type`,
      :py:func:`get_host_api_info_by_index`,
      :py:func:`get_device_info_by_host_api_device_index`

    **Device API**
      :py:func:`get_device_count`, :py:func:`is_format_supported`,
      :py:func:`get_default_input_device_info`,
      :py:func:`get_default_output_device_info`,
      :py:func:`get_device_info_by_index`

    **Stream Format Conversion**
      :py:func:`get_sample_size`, :py:func:`get_format_from_width`

    **Details**
    """

    ############################################################
    # Initialization and Termination
    ############################################################

    def __init__(self):
        """Initialize PortAudio."""

        pa.initialize()
        self._streams = set()

    def terminate(self):
        """
        Terminate PortAudio.

        :attention: Be sure to call this method for every instance of
          this object to release PortAudio resources.
        """

        for stream in self._streams.copy():
            stream.close()

        self._streams = set()

        pa.terminate()


    ############################################################
    # Stream Format
    ############################################################

    def get_sample_size(self, format):
        """
        Returns the size (in bytes) for the specified
        sample `format` (a |PaSampleFormat| constant).

        :param format: A |PaSampleFormat| constant.
        :raises ValueError: Invalid specified `format`.
        :rtype: integer
        """

        return pa.get_sample_size(format)

    def get_format_from_width(self, width, unsigned=True):
        """
        Returns a PortAudio format constant for the specified `width`.

        :param width: The desired sample width in bytes (1, 2, 3, or 4)
        :param unsigned: For 1 byte width, specifies signed or unsigned format.

        :raises ValueError: for invalid `width`
        :rtype: A |PaSampleFormat| constant.
        """

        if width == 1:
            if unsigned:
                return paUInt8
            else:
                return paInt8
        elif width == 2:
            return paInt16
        elif width == 3:
            return paInt24
        elif width == 4:
            return paFloat32
        else:
            raise ValueError("Invalid width: %d" % width)


    ############################################################
    # Stream Factory
    ############################################################

    def open(self, *args, **kwargs):
        """
        Open a new stream. See constructor for
        :py:func:`Stream.__init__` for parameter details.

        :returns: A new :py:class:`Stream`
        """

        stream = Stream(self, *args, **kwargs)
        self._streams.add(stream)
        return stream

    def close(self, stream):
        """
        Close a stream. Typically use :py:func:`Stream.close` instead.

        :param stream: An instance of the :py:class:`Stream` object.
        :raises ValueError: if stream does not exist.
        """

        if stream not in self._streams:
            raise ValueError("Stream `%s' not found" % str(stream))

        stream.close()

    def _remove_stream(self, stream):
        """
        Internal method. Removes a stream.

        :param stream: An instance of the :py:class:`Stream` object.
        """

        if stream in self._streams:
            self._streams.remove(stream)


    ############################################################
    # Host API Inspection
    ############################################################

    def get_host_api_count(self):
        """
        Return the number of available PortAudio Host APIs.

        :rtype: integer
        """

        return pa.get_host_api_count()

    def get_default_host_api_info(self):
        """
        Return a dictionary containing the default Host API
        parameters. The keys of the dictionary mirror the data fields
        of PortAudio's ``PaHostApiInfo`` structure.

        :raises IOError: if no default input device is available
        :rtype: dict
        """

        defaultHostApiIndex = pa.get_default_host_api()
        return self.get_host_api_info_by_index(defaultHostApiIndex)

    def get_host_api_info_by_type(self, host_api_type):
        """
        Return a dictionary containing the Host API parameters for the
        host API specified by the `host_api_type`. The keys of the
        dictionary mirror the data fields of PortAudio's ``PaHostApiInfo``
        structure.

        :param host_api_type: The desired |PaHostAPI|
        :raises IOError: for invalid `host_api_type`
        :rtype: dict
        """

        index = pa.host_api_type_id_to_host_api_index(host_api_type)
        return self.get_host_api_info_by_index(index)

    def get_host_api_info_by_index(self, host_api_index):
        """
        Return a dictionary containing the Host API parameters for the
        host API specified by the `host_api_index`. The keys of the
        dictionary mirror the data fields of PortAudio's ``PaHostApiInfo``
        structure.

        :param host_api_index: The host api index
        :raises IOError: for invalid `host_api_index`
        :rtype: dict
        """

        return self._make_host_api_dictionary(
            host_api_index,
            pa.get_host_api_info(host_api_index)
            )

    def get_device_info_by_host_api_device_index(self,
                                                 host_api_index,
                                                 host_api_device_index):
        """
        Return a dictionary containing the Device parameters for a
        given Host API's n'th device. The keys of the dictionary
        mirror the data fields of PortAudio's ``PaDeviceInfo`` structure.

        :param host_api_index: The Host API index number
        :param host_api_device_index: The n'th device of the host API
        :raises IOError: for invalid indices
        :rtype: dict
        """

        long_method_name = pa.host_api_device_index_to_device_index
        device_index = long_method_name(host_api_index,
                                        host_api_device_index)
        return self.get_device_info_by_index(device_index)

    def _make_host_api_dictionary(self, index, host_api_struct):
        """
        Internal method to create Host API dictionary that mirrors
        PortAudio's ``PaHostApiInfo`` structure.

        :rtype: dict
        """

        return {'index' : index,
                'structVersion' : host_api_struct.structVersion,
                'type' : host_api_struct.type,
                'name' : host_api_struct.name,
                'deviceCount' : host_api_struct.deviceCount,
                'defaultInputDevice' : host_api_struct.defaultInputDevice,
                'defaultOutputDevice' : host_api_struct.defaultOutputDevice}


    ############################################################
    # Device Inspection
    ############################################################

    def get_device_count(self):
        """
        Return the number of PortAudio Host APIs.

        :rtype: integer
        """

        return pa.get_device_count()

    def is_format_supported(self, rate,
                            input_device=None,
                            input_channels=None,
                            input_format=None,
                            output_device=None,
                            output_channels=None,
                            output_format=None):
        """
        Check to see if specified device configuration
        is supported. Returns True if the configuration
        is supported; throws a ValueError exception otherwise.

        :param rate:
           Specifies the desired rate (in Hz)
        :param input_device:
           The input device index. Specify ``None`` (default) for
           half-duplex output-only streams.
        :param input_channels:
           The desired number of input channels. Ignored if
           `input_device` is not specified (or ``None``).
        :param input_format:
           PortAudio sample format constant defined
           in this module
        :param output_device:
           The output device index. Specify ``None`` (default) for
           half-duplex input-only streams.
        :param output_channels:
           The desired number of output channels. Ignored if
           `input_device` is not specified (or ``None``).
        :param output_format:
           |PaSampleFormat| constant.

        :rtype: bool
        :raises ValueError: tuple containing (error string, |PaErrorCode|).
        """

        if input_device == None and output_device == None:
            raise ValueError("must specify stream format for input, " +\
                             "output, or both", paInvalidDevice);

        kwargs = {}

        if input_device != None:
            kwargs['input_device'] = input_device
            kwargs['input_channels'] = input_channels
            kwargs['input_format'] = input_format

        if output_device != None:
            kwargs['output_device'] = output_device
            kwargs['output_channels'] = output_channels
            kwargs['output_format'] = output_format

        return pa.is_format_supported(rate, **kwargs)

    def get_default_input_device_info(self):
        """
        Return the default input Device parameters as a
        dictionary. The keys of the dictionary mirror the data fields
        of PortAudio's ``PaDeviceInfo`` structure.

        :raises IOError: No default input device available.
        :rtype: dict
        """

        device_index = pa.get_default_input_device()
        return self.get_device_info_by_index(device_index)

    def get_default_output_device_info(self):
        """
        Return the default output Device parameters as a
        dictionary. The keys of the dictionary mirror the data fields
        of PortAudio's ``PaDeviceInfo`` structure.

        :raises IOError: No default output device available.
        :rtype: dict
        """

        device_index = pa.get_default_output_device()
        return self.get_device_info_by_index(device_index)


    def get_device_info_by_index(self, device_index):
        """
        Return the Device parameters for device specified in
        `device_index` as a dictionary. The keys of the dictionary
        mirror the data fields of PortAudio's ``PaDeviceInfo``
        structure.

        :param device_index: The device index
        :raises IOError: Invalid `device_index`.
        :rtype: dict
        """

        return self._make_device_info_dictionary(
            device_index,
            pa.get_device_info(device_index)
            )

    def _make_device_info_dictionary(self, index, device_info):
        """
        Internal method to create Device Info dictionary that mirrors
        PortAudio's ``PaDeviceInfo`` structure.

        :rtype: dict
        """

        device_name = device_info.name

        # Attempt to decode device_name
        for codec in ["utf-8", "cp1252"]:
            try:
                device_name = device_name.decode(codec)
                break
            except:
                pass

        # If we fail to decode, we return the raw bytes and let the caller
        # deal with the encoding.
        return {'index' : index,
                'structVersion' : device_info.structVersion,
                'name' : device_name,
                'hostApi' : device_info.hostApi,
                'maxInputChannels' : device_info.maxInputChannels,
                'maxOutputChannels' : device_info.maxOutputChannels,
                'defaultLowInputLatency' :
                device_info.defaultLowInputLatency,
                'defaultLowOutputLatency' :
                device_info.defaultLowOutputLatency,
                'defaultHighInputLatency' :
                device_info.defaultHighInputLatency,
                'defaultHighOutputLatency' :
                device_info.defaultHighOutputLatency,
                'defaultSampleRate' :
                device_info.defaultSampleRate
                }


######################################################################
# Host Specific Stream Info
######################################################################

try:
    paMacCoreStreamInfo = pa.paMacCoreStreamInfo
except AttributeError:
    pass
else:
    class PaMacCoreStreamInfo:
        """
        Mac OS X-only: PaMacCoreStreamInfo is a PortAudio Host API
        Specific Stream Info data structure for specifying Mac OS
        X-only settings. Instantiate this class (if desired) and pass
        the instance as the argument in :py:func:`PyAudio.open` to parameters
        ``input_host_api_specific_stream_info`` or
        ``output_host_api_specific_stream_info``.
        (See :py:func:`Stream.__init__`.)

        :note: Mac OS X only.

        .. |PaMacCoreFlags| replace:: :ref:`PortAudio Mac Core Flags <PaMacCoreFlags>`
        .. _PaMacCoreFlags:

        **PortAudio Mac Core Flags**
          :py:data:`paMacCoreChangeDeviceParameters`,
          :py:data:`paMacCoreFailIfConversionRequired`,
          :py:data:`paMacCoreConversionQualityMin`,
          :py:data:`paMacCoreConversionQualityMedium`,
          :py:data:`paMacCoreConversionQualityLow`,
          :py:data:`paMacCoreConversionQualityHigh`,
          :py:data:`paMacCoreConversionQualityMax`,
          :py:data:`paMacCorePlayNice`,
          :py:data:`paMacCorePro`,
          :py:data:`paMacCoreMinimizeCPUButPlayNice`,
          :py:data:`paMacCoreMinimizeCPU`

        **Settings**
          :py:func:`get_flags`, :py:func:`get_channel_map`
        """

        paMacCoreChangeDeviceParameters   = pa.paMacCoreChangeDeviceParameters
        paMacCoreFailIfConversionRequired = pa.paMacCoreFailIfConversionRequired
        paMacCoreConversionQualityMin     = pa.paMacCoreConversionQualityMin
        paMacCoreConversionQualityMedium  = pa.paMacCoreConversionQualityMedium
        paMacCoreConversionQualityLow     = pa.paMacCoreConversionQualityLow
        paMacCoreConversionQualityHigh    = pa.paMacCoreConversionQualityHigh
        paMacCoreConversionQualityMax     = pa.paMacCoreConversionQualityMax
        paMacCorePlayNice                 = pa.paMacCorePlayNice
        paMacCorePro                      = pa.paMacCorePro
        paMacCoreMinimizeCPUButPlayNice   = pa.paMacCoreMinimizeCPUButPlayNice
        paMacCoreMinimizeCPU              = pa.paMacCoreMinimizeCPU

        def __init__(self, flags=None, channel_map=None):
            """
            Initialize with flags and channel_map. See PortAudio
            documentation for more details on these parameters; they are
            passed almost verbatim to the PortAudio library.

            :param flags: |PaMacCoreFlags| OR'ed together.
                See :py:class:`PaMacCoreStreamInfo`.
            :param channel_map: An array describing the channel mapping.
                See PortAudio documentation for usage.
            """

            kwargs = {"flags" : flags,
                      "channel_map" : channel_map}

            if flags == None:
                del kwargs["flags"]
            if channel_map == None:
                del kwargs["channel_map"]

            self._paMacCoreStreamInfo = paMacCoreStreamInfo(**kwargs)

        def get_flags(self):
            """
            Return the flags set at instantiation.

            :rtype: integer
            """

            return self._paMacCoreStreamInfo.flags

        def get_channel_map(self):
            """
            Return the channel map set at instantiation.

            :rtype: tuple or None
            """

            return self._paMacCoreStreamInfo.channel_map

        def _get_host_api_stream_object(self):
            """Private method."""

            return self._paMacCoreStreamInfo


# ======================================COLORAMA=============================================================

import re
import sys
import os
import atexit
import contextlib

orig_stdout = None
orig_stderr = None

wrapped_stdout = None
wrapped_stderr = None

atexit_done = False

class WinColor(object):
    BLACK   = 0
    BLUE    = 1
    GREEN   = 2
    CYAN    = 3
    RED     = 4
    MAGENTA = 5
    YELLOW  = 6
    GREY    = 7

# from wincon.h
class WinStyle(object):
    NORMAL              = 0x00 # dim text, dim background
    BRIGHT              = 0x08 # bright text, dim background
    BRIGHT_BACKGROUND   = 0x80 # dim text, bright background

class WinTerm(object):

    def __init__(self):
        self._default = GetConsoleScreenBufferInfo(STDOUT).wAttributes
        self.set_attrs(self._default)
        self._default_fore = self._fore
        self._default_back = self._back
        self._default_style = self._style
        # In order to emulate LIGHT_EX in windows, we borrow the BRIGHT style.
        # So that LIGHT_EX colors and BRIGHT style do not clobber each other,
        # we track them separately, since LIGHT_EX is overwritten by Fore/Back
        # and BRIGHT is overwritten by Style codes.
        self._light = 0

    def get_attrs(self):
        return self._fore + self._back * 16 + (self._style | self._light)

    def set_attrs(self, value):
        self._fore = value & 7
        self._back = (value >> 4) & 7
        self._style = value & (WinStyle.BRIGHT | WinStyle.BRIGHT_BACKGROUND)

    def reset_all(self, on_stderr=None):
        self.set_attrs(self._default)
        self.set_console(attrs=self._default)

    def fore(self, fore=None, light=False, on_stderr=False):
        if fore is None:
            fore = self._default_fore
        self._fore = fore
        # Emulate LIGHT_EX with BRIGHT Style
        if light:
            self._light |= WinStyle.BRIGHT
        else:
            self._light &= ~WinStyle.BRIGHT
        self.set_console(on_stderr=on_stderr)

    def back(self, back=None, light=False, on_stderr=False):
        if back is None:
            back = self._default_back
        self._back = back
        # Emulate LIGHT_EX with BRIGHT_BACKGROUND Style
        if light:
            self._light |= WinStyle.BRIGHT_BACKGROUND
        else:
            self._light &= ~WinStyle.BRIGHT_BACKGROUND
        self.set_console(on_stderr=on_stderr)

    def style(self, style=None, on_stderr=False):
        if style is None:
            style = self._default_style
        self._style = style
        self.set_console(on_stderr=on_stderr)

    def set_console(self, attrs=None, on_stderr=False):
        if attrs is None:
            attrs = self.get_attrs()
        handle = STDOUT
        if on_stderr:
            handle = STDERR
        SetConsoleTextAttribute(handle, attrs)

    def get_position(self, handle):
        position = GetConsoleScreenBufferInfo(handle).dwCursorPosition
        # Because Windows coordinates are 0-based,
        # and SetConsoleCursorPosition expects 1-based.
        position.X += 1
        position.Y += 1
        return position

    def set_cursor_position(self, position=None, on_stderr=False):
        if position is None:
            # I'm not currently tracking the position, so there is no default.
            # position = self.get_position()
            return
        handle = STDOUT
        if on_stderr:
            handle = STDERR
        SetConsoleCursorPosition(handle, position)

    def cursor_adjust(self, x, y, on_stderr=False):
        handle = STDOUT
        if on_stderr:
            handle = STDERR
        position = self.get_position(handle)
        adjusted_position = (position.Y + y, position.X + x)
        SetConsoleCursorPosition(handle, adjusted_position, adjust=False)

    def erase_screen(self, mode=0, on_stderr=False):
        # 0 should clear from the cursor to the end of the screen.
        # 1 should clear from the cursor to the beginning of the screen.
        # 2 should clear the entire screen, and move cursor to (1,1)
        handle = STDOUT
        if on_stderr:
            handle = STDERR
        csbi = GetConsoleScreenBufferInfo(handle)
        # get the number of character cells in the current buffer
        cells_in_screen = csbi.dwSize.X * csbi.dwSize.Y
        # get number of character cells before current cursor position
        cells_before_cursor = csbi.dwSize.X * csbi.dwCursorPosition.Y + csbi.dwCursorPosition.X
        if mode == 0:
            from_coord = csbi.dwCursorPosition
            cells_to_erase = cells_in_screen - cells_before_cursor
        if mode == 1:
            from_coord = COORD(0, 0)
            cells_to_erase = cells_before_cursor
        elif mode == 2:
            from_coord = COORD(0, 0)
            cells_to_erase = cells_in_screen
        # fill the entire screen with blanks
        FillConsoleOutputCharacter(handle, ' ', cells_to_erase, from_coord)
        # now set the buffer's attributes accordingly
        FillConsoleOutputAttribute(handle, self.get_attrs(), cells_to_erase, from_coord)
        if mode == 2:
            # put the cursor where needed
            SetConsoleCursorPosition(handle, (1, 1))

    def erase_line(self, mode=0, on_stderr=False):
        # 0 should clear from the cursor to the end of the line.
        # 1 should clear from the cursor to the beginning of the line.
        # 2 should clear the entire line.
        handle = STDOUT
        if on_stderr:
            handle = STDERR
        csbi = GetConsoleScreenBufferInfo(handle)
        if mode == 0:
            from_coord = csbi.dwCursorPosition
            cells_to_erase = csbi.dwSize.X - csbi.dwCursorPosition.X
        if mode == 1:
            from_coord = COORD(0, csbi.dwCursorPosition.Y)
            cells_to_erase = csbi.dwCursorPosition.X
        elif mode == 2:
            from_coord = COORD(0, csbi.dwCursorPosition.Y)
            cells_to_erase = csbi.dwSize.X
        # fill the entire screen with blanks
        FillConsoleOutputCharacter(handle, ' ', cells_to_erase, from_coord)
        # now set the buffer's attributes accordingly
        FillConsoleOutputAttribute(handle, self.get_attrs(), cells_to_erase, from_coord)

    def set_title(self, title):
        SetConsoleTitle(title)

def reset_all():
    if AnsiToWin32 is not None:    # Issue #74: objects might become None at exit
        AnsiToWin32(orig_stdout).reset_all()


def init(autoreset=False, convert=None, strip=None, wrap=True):

    if not wrap and any([autoreset, convert, strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')

    global wrapped_stdout, wrapped_stderr
    global orig_stdout, orig_stderr

    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    if sys.stdout is None:
        wrapped_stdout = None
    else:
        sys.stdout = wrapped_stdout = \
            wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    if sys.stderr is None:
        wrapped_stderr = None
    else:
        sys.stderr = wrapped_stderr = \
            wrap_stream(orig_stderr, convert, strip, autoreset, wrap)

    global atexit_done
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def deinit():
    if orig_stdout is not None:
        sys.stdout = orig_stdout
    if orig_stderr is not None:
        sys.stderr = orig_stderr


@contextlib.contextmanager
def colorama_text(*args, **kwargs):
    init(*args, **kwargs)
    try:
        yield
    finally:
        deinit()


def reinit():
    if wrapped_stdout is not None:
        sys.stdout = wrapped_stdout
    if wrapped_stderr is not None:
        sys.stderr = wrapped_stderr


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream,
            convert=convert, strip=strip, autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream

winterm = None
if winterm is not None:
    winterm = WinTerm()


def is_stream_closed(stream):
    return not hasattr(stream, 'closed') or stream.closed


def is_a_tty(stream):
    return hasattr(stream, 'isatty') and stream.isatty()


class StreamWrapper(object):
    '''
    Wraps a stream (such as stdout), acting as a transparent proxy for all
    attribute access apart from method 'write()', which is delegated to our
    Converter instance.
    '''
    def __init__(self, wrapped, converter):
        # double-underscore everything to prevent clashes with names of
        # attributes on the wrapped stream object.
        self.__wrapped = wrapped
        self.__convertor = converter

    def __getattr__(self, name):
        return getattr(self.__wrapped, name)

    def write(self, text):
        self.__convertor.write(text)


class AnsiToWin32(object):
    '''
    Implements a 'write()' method which, on Windows, will strip ANSI character
    sequences from the text, and if outputting to a tty, will convert them into
    win32 function calls.
    '''
    ANSI_CSI_RE = re.compile('\001?\033\[((?:\d|;)*)([a-zA-Z])\002?')     # Control Sequence Introducer
    ANSI_OSC_RE = re.compile('\001?\033\]((?:.|;)*?)(\x07)\002?')         # Operating System Command

    def __init__(self, wrapped, convert=None, strip=None, autoreset=False):
        # The wrapped stream (normally sys.stdout or sys.stderr)
        self.wrapped = wrapped

        # should we reset colors to defaults after every .write()
        self.autoreset = autoreset

        # create the proxy wrapping our output stream
        self.stream = StreamWrapper(wrapped, self)

        on_windows = os.name == 'nt'
        # We test if the WinAPI works, because even if we are on Windows
        # we may be using a terminal that doesn't support the WinAPI
        # (e.g. Cygwin Terminal). In this case it's up to the terminal
        # to support the ANSI codes.
        conversion_supported = on_windows and winapi_test()

        # should we strip ANSI sequences from our output?
        if strip is None:
            strip = conversion_supported or (not is_stream_closed(wrapped) and not is_a_tty(wrapped))
        self.strip = strip

        # should we should convert ANSI sequences into win32 calls?
        if convert is None:
            convert = conversion_supported and not is_stream_closed(wrapped) and is_a_tty(wrapped)
        self.convert = convert

        # dict of ansi codes to win32 functions and parameters
        self.win32_calls = self.get_win32_calls()

        # are we wrapping stderr?
        self.on_stderr = self.wrapped is sys.stderr

    def should_wrap(self):
        '''
        True if this class is actually needed. If false, then the output
        stream will not be affected, nor will win32 calls be issued, so
        wrapping stdout is not actually required. This will generally be
        False on non-Windows platforms, unless optional functionality like
        autoreset has been requested using kwargs to init()
        '''
        return self.convert or self.strip or self.autoreset

    def get_win32_calls(self):
        if self.convert and winterm:
            return {
                AnsiStyle.RESET_ALL: (winterm.reset_all, ),
                AnsiStyle.BRIGHT: (winterm.style, WinStyle.BRIGHT),
                AnsiStyle.DIM: (winterm.style, WinStyle.NORMAL),
                AnsiStyle.NORMAL: (winterm.style, WinStyle.NORMAL),
                AnsiFore.BLACK: (winterm.fore, WinColor.BLACK),
                AnsiFore.RED: (winterm.fore, WinColor.RED),
                AnsiFore.GREEN: (winterm.fore, WinColor.GREEN),
                AnsiFore.YELLOW: (winterm.fore, WinColor.YELLOW),
                AnsiFore.BLUE: (winterm.fore, WinColor.BLUE),
                AnsiFore.MAGENTA: (winterm.fore, WinColor.MAGENTA),
                AnsiFore.CYAN: (winterm.fore, WinColor.CYAN),
                AnsiFore.WHITE: (winterm.fore, WinColor.GREY),
                AnsiFore.RESET: (winterm.fore, ),
                AnsiFore.LIGHTBLACK_EX: (winterm.fore, WinColor.BLACK, True),
                AnsiFore.LIGHTRED_EX: (winterm.fore, WinColor.RED, True),
                AnsiFore.LIGHTGREEN_EX: (winterm.fore, WinColor.GREEN, True),
                AnsiFore.LIGHTYELLOW_EX: (winterm.fore, WinColor.YELLOW, True),
                AnsiFore.LIGHTBLUE_EX: (winterm.fore, WinColor.BLUE, True),
                AnsiFore.LIGHTMAGENTA_EX: (winterm.fore, WinColor.MAGENTA, True),
                AnsiFore.LIGHTCYAN_EX: (winterm.fore, WinColor.CYAN, True),
                AnsiFore.LIGHTWHITE_EX: (winterm.fore, WinColor.GREY, True),
                AnsiBack.BLACK: (winterm.back, WinColor.BLACK),
                AnsiBack.RED: (winterm.back, WinColor.RED),
                AnsiBack.GREEN: (winterm.back, WinColor.GREEN),
                AnsiBack.YELLOW: (winterm.back, WinColor.YELLOW),
                AnsiBack.BLUE: (winterm.back, WinColor.BLUE),
                AnsiBack.MAGENTA: (winterm.back, WinColor.MAGENTA),
                AnsiBack.CYAN: (winterm.back, WinColor.CYAN),
                AnsiBack.WHITE: (winterm.back, WinColor.GREY),
                AnsiBack.RESET: (winterm.back, ),
                AnsiBack.LIGHTBLACK_EX: (winterm.back, WinColor.BLACK, True),
                AnsiBack.LIGHTRED_EX: (winterm.back, WinColor.RED, True),
                AnsiBack.LIGHTGREEN_EX: (winterm.back, WinColor.GREEN, True),
                AnsiBack.LIGHTYELLOW_EX: (winterm.back, WinColor.YELLOW, True),
                AnsiBack.LIGHTBLUE_EX: (winterm.back, WinColor.BLUE, True),
                AnsiBack.LIGHTMAGENTA_EX: (winterm.back, WinColor.MAGENTA, True),
                AnsiBack.LIGHTCYAN_EX: (winterm.back, WinColor.CYAN, True),
                AnsiBack.LIGHTWHITE_EX: (winterm.back, WinColor.GREY, True),
            }
        return dict()

    def write(self, text):
        if self.strip or self.convert:
            self.write_and_convert(text)
        else:
            self.wrapped.write(text)
            self.wrapped.flush()
        if self.autoreset:
            self.reset_all()


    def reset_all(self):
        if self.convert:
            self.call_win32('m', (0,))
        elif not self.strip and not is_stream_closed(self.wrapped):
            self.wrapped.write(Style.RESET_ALL)


    def write_and_convert(self, text):
        '''
        Write the given text to our wrapped stream, stripping any ANSI
        sequences from the text, and optionally converting them into win32
        calls.
        '''
        cursor = 0
        text = self.convert_osc(text)
        for match in self.ANSI_CSI_RE.finditer(text):
            start, end = match.span()
            self.write_plain_text(text, cursor, start)
            self.convert_ansi(*match.groups())
            cursor = end
        self.write_plain_text(text, cursor, len(text))


    def write_plain_text(self, text, start, end):
        if start < end:
            self.wrapped.write(text[start:end])
            self.wrapped.flush()


    def convert_ansi(self, paramstring, command):
        if self.convert:
            params = self.extract_params(command, paramstring)
            self.call_win32(command, params)


    def extract_params(self, command, paramstring):
        if command in 'Hf':
            params = tuple(int(p) if len(p) != 0 else 1 for p in paramstring.split(';'))
            while len(params) < 2:
                # defaults:
                params = params + (1,)
        else:
            params = tuple(int(p) for p in paramstring.split(';') if len(p) != 0)
            if len(params) == 0:
                # defaults:
                if command in 'JKm':
                    params = (0,)
                elif command in 'ABCD':
                    params = (1,)

        return params


    def call_win32(self, command, params):
        if command == 'm':
            for param in params:
                if param in self.win32_calls:
                    func_args = self.win32_calls[param]
                    func = func_args[0]
                    args = func_args[1:]
                    kwargs = dict(on_stderr=self.on_stderr)
                    func(*args, **kwargs)
        elif command in 'J':
            winterm.erase_screen(params[0], on_stderr=self.on_stderr)
        elif command in 'K':
            winterm.erase_line(params[0], on_stderr=self.on_stderr)
        elif command in 'Hf':     # cursor position - absolute
            winterm.set_cursor_position(params, on_stderr=self.on_stderr)
        elif command in 'ABCD':   # cursor position - relative
            n = params[0]
            # A - up, B - down, C - forward, D - back
            x, y = {'A': (0, -n), 'B': (0, n), 'C': (n, 0), 'D': (-n, 0)}[command]
            winterm.cursor_adjust(x, y, on_stderr=self.on_stderr)


    def convert_osc(self, text):
        for match in self.ANSI_OSC_RE.finditer(text):
            start, end = match.span()
            text = text[:start] + text[end:]
            paramstring, command = match.groups()
            if command in '\x07':       # \x07 = BEL
                params = paramstring.split(";")
                # 0 - change title and icon (we will only change title)
                # 1 - change icon (we don't support this)
                # 2 - change title
                if params[0] in '02':
                    winterm.set_title(params[1])
        return text

CSI = '\033['
OSC = '\033]'
BEL = '\007'


def code_to_chars(code):
    return CSI + str(code) + 'm'

def set_title(title):
    return OSC + '2;' + title + BEL

def clear_screen(mode=2):
    return CSI + str(mode) + 'J'

def clear_line(mode=2):
    return CSI + str(mode) + 'K'


class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class AnsiCursor(object):
    def UP(self, n=1):
        return CSI + str(n) + 'A'
    def DOWN(self, n=1):
        return CSI + str(n) + 'B'
    def FORWARD(self, n=1):
        return CSI + str(n) + 'C'
    def BACK(self, n=1):
        return CSI + str(n) + 'D'
    def POS(self, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'


class AnsiFore(AnsiCodes):
    BLACK           = 30
    RED             = 31
    GREEN           = 32
    YELLOW          = 33
    BLUE            = 34
    MAGENTA         = 35
    CYAN            = 36
    WHITE           = 37
    RESET           = 39

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX   = 90
    LIGHTRED_EX     = 91
    LIGHTGREEN_EX   = 92
    LIGHTYELLOW_EX  = 93
    LIGHTBLUE_EX    = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX    = 96
    LIGHTWHITE_EX   = 97


class AnsiBack(AnsiCodes):
    BLACK           = 40
    RED             = 41
    GREEN           = 42
    YELLOW          = 43
    BLUE            = 44
    MAGENTA         = 45
    CYAN            = 46
    WHITE           = 47
    RESET           = 49

    # These are fairly well supported, but not part of the standard.
    LIGHTBLACK_EX   = 100
    LIGHTRED_EX     = 101
    LIGHTGREEN_EX   = 102
    LIGHTYELLOW_EX  = 103
    LIGHTBLUE_EX    = 104
    LIGHTMAGENTA_EX = 105
    LIGHTCYAN_EX    = 106
    LIGHTWHITE_EX   = 107


class AnsiStyle(AnsiCodes):
    BRIGHT    = 1
    DIM       = 2
    NORMAL    = 22
    RESET_ALL = 0

Fore   = AnsiFore()
Back   = AnsiBack()
Style  = AnsiStyle()
Cursor = AnsiCursor()

STDOUT = -11
STDERR = -12

try:
    import ctypes
    from ctypes import LibraryLoader
    windll = LibraryLoader(ctypes.WinDLL)
    from ctypes import wintypes
except (AttributeError, ImportError):
    windll = None
    SetConsoleTextAttribute = lambda *_: None
    winapi_test = lambda *_: None
else:
    from ctypes import byref, Structure, c_char, POINTER

    COORD = wintypes._COORD

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("dwSize", COORD),
            ("dwCursorPosition", COORD),
            ("wAttributes", wintypes.WORD),
            ("srWindow", wintypes.SMALL_RECT),
            ("dwMaximumWindowSize", COORD),
        ]
        def __str__(self):
            return '(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)' % (
                self.dwSize.Y, self.dwSize.X
                , self.dwCursorPosition.Y, self.dwCursorPosition.X
                , self.wAttributes
                , self.srWindow.Top, self.srWindow.Left, self.srWindow.Bottom, self.srWindow.Right
                , self.dwMaximumWindowSize.Y, self.dwMaximumWindowSize.X
            )

    _GetStdHandle = windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [
        wintypes.DWORD,
    ]
    _GetStdHandle.restype = wintypes.HANDLE

    _GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
    _GetConsoleScreenBufferInfo.argtypes = [
        wintypes.HANDLE,
        POINTER(CONSOLE_SCREEN_BUFFER_INFO),
    ]
    _GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    _SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    _SetConsoleTextAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD,
    ]
    _SetConsoleTextAttribute.restype = wintypes.BOOL

    _SetConsoleCursorPosition = windll.kernel32.SetConsoleCursorPosition
    _SetConsoleCursorPosition.argtypes = [
        wintypes.HANDLE,
        COORD,
    ]
    _SetConsoleCursorPosition.restype = wintypes.BOOL

    _FillConsoleOutputCharacterA = windll.kernel32.FillConsoleOutputCharacterA
    _FillConsoleOutputCharacterA.argtypes = [
        wintypes.HANDLE,
        c_char,
        wintypes.DWORD,
        COORD,
        POINTER(wintypes.DWORD),
    ]
    _FillConsoleOutputCharacterA.restype = wintypes.BOOL

    _FillConsoleOutputAttribute = windll.kernel32.FillConsoleOutputAttribute
    _FillConsoleOutputAttribute.argtypes = [
        wintypes.HANDLE,
        wintypes.WORD,
        wintypes.DWORD,
        COORD,
        POINTER(wintypes.DWORD),
    ]
    _FillConsoleOutputAttribute.restype = wintypes.BOOL

    _SetConsoleTitleW = windll.kernel32.SetConsoleTitleA
    _SetConsoleTitleW.argtypes = [
        wintypes.LPCSTR
    ]
    _SetConsoleTitleW.restype = wintypes.BOOL

    handles = {
        STDOUT: _GetStdHandle(STDOUT),
        STDERR: _GetStdHandle(STDERR),
    }

    def winapi_test():
        handle = handles[STDOUT]
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        success = _GetConsoleScreenBufferInfo(
            handle, byref(csbi))
        return bool(success)

    def GetConsoleScreenBufferInfo(stream_id=STDOUT):
        handle = handles[stream_id]
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        success = _GetConsoleScreenBufferInfo(
            handle, byref(csbi))
        return csbi

    def SetConsoleTextAttribute(stream_id, attrs):
        handle = handles[stream_id]
        return _SetConsoleTextAttribute(handle, attrs)

    def SetConsoleCursorPosition(stream_id, position, adjust=True):
        position = COORD(*position)
        # If the position is out of range, do nothing.
        if position.Y <= 0 or position.X <= 0:
            return
        # Adjust for Windows' SetConsoleCursorPosition:
        #    1. being 0-based, while ANSI is 1-based.
        #    2. expecting (x,y), while ANSI uses (y,x).
        adjusted_position = COORD(position.Y - 1, position.X - 1)
        if adjust:
            # Adjust for viewport's scroll position
            sr = GetConsoleScreenBufferInfo(STDOUT).srWindow
            adjusted_position.Y += sr.Top
            adjusted_position.X += sr.Left
        # Resume normal processing
        handle = handles[stream_id]
        return _SetConsoleCursorPosition(handle, adjusted_position)

    def FillConsoleOutputCharacter(stream_id, char, length, start):
        handle = handles[stream_id]
        char = c_char(char.encode())
        length = wintypes.DWORD(length)
        num_written = wintypes.DWORD(0)
        # Note that this is hard-coded for ANSI (vs wide) bytes.
        success = _FillConsoleOutputCharacterA(
            handle, char, length, start, byref(num_written))
        return num_written.value

    def FillConsoleOutputAttribute(stream_id, attr, length, start):
        ''' FillConsoleOutputAttribute( hConsole, csbi.wAttributes, dwConSize, coordScreen, &cCharsWritten )'''
        handle = handles[stream_id]
        attribute = wintypes.WORD(attr)
        length = wintypes.DWORD(length)
        num_written = wintypes.DWORD(0)
        # Note that this is hard-coded for ANSI (vs wide) bytes.
        return _FillConsoleOutputAttribute(
            handle, attribute, length, start, byref(num_written))

    def SetConsoleTitle(title):
        return _SetConsoleTitleW(title)

# ===================================================================================================

def get_IP():
    """Returns the IP of the computer where get_IP is called.

    Returns
    -------
    computer_IP: IP of the computer where get_IP is called (str)

    Notes
    -----
    If you have no internet connection, your IP will be 127.0.0.1.
    This IP address refers to the local host, i.e. your computer.

    """

    return socket.gethostbyname(socket.gethostname())


def connect_to_player(player_id, remote_IP='25.68.218.220', verbose=False):
    """Initialise communication with remote player.

    Parameters
    ----------
    player_id: player id of the remote player, 1 or 2 (int)
    remote_IP: IP of the computer where remote player is (str, optional)
    verbose: True only if connection progress must be displayed (bool, optional)

    Returns
    -------
    connection: sockets to receive/send orders (tuple)

    Notes
    -----
    Initialisation can take several seconds.  The function only
    returns after connection has been initialised by both players.

    Use the default value of remote_IP if the remote player is running on
    the same machine.  Otherwise, indicate the IP where the other player
    is running with remote_IP.  On most systems, the IP of a computer
    can be obtained by calling the get_IP function on that computer.

    """

    # init verbose display
    if verbose:
        print '\n-------------------------------------------------------------'

    # open socket (as server) to receive orders
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    if remote_IP == '127.0.0.1':
        local_IP = '127.0.0.1'
    else:
        local_IP = get_IP()
    local_port = 42000 + (3-player_id)

    if verbose:
        print 'binding on %s:%d to receive orders from player %d...' % (local_IP, local_port, player_id)
    socket_in.bind((local_IP, local_port))

    socket_in.listen(1)
    if verbose:
        print '   done -> now waiting for a connection on %s:%d\n' % (local_IP, local_port)

    # open client socket used to send orders
    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    remote_port = 42000 + player_id

    connected = False
    msg_shown = False
    while not connected:
        try:
            if verbose and not msg_shown:
                print 'connecting on %s:%d to send orders to player %d...' % (remote_IP, remote_port, player_id)
            socket_out.connect((remote_IP, remote_port))
            connected = True
            if verbose:
                print '   done -> now sending orders to player %d on %s:%d' % (player_id, remote_IP, remote_port)
        except:
            if verbose and not msg_shown:
                print '   connection failed -> will try again every 100 msec...'
            time.sleep(.1)

            msg_shown = True

    if verbose:
        print

    # accept connection to the server socket to receive orders from remote player
    print 'sutck on accept'
    socket_in, remote_address = socket_in.accept()
    if verbose:
        print 'now listening to orders from player %d' % (player_id)

    # end verbose display
    if verbose:
        print '\nconnection to remote player %d successful\n-------------------------------------------------------------\n' % player_id

    # return sockets for further use
    return (socket_in, socket_out)


def disconnect_from_player(connection):
    """End communication with remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # shutdown sockets
    socket_in.shutdown(socket.SHUT_RDWR)
    socket_out.shutdown(socket.SHUT_RDWR)

    # close sockets
    socket_in.close()
    socket_out.close()


def notify_remote_orders(connection, orders):
    """Notifies orders of the local player to a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)
    orders: orders of the local player (str)

    Raises
    ------
    IOError: if remote player cannot be reached

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # deal with null orders (empty string)
    if orders == '':
        orders = 'null'

    # send orders
    try:
        socket_out.sendall(orders)
    except:
        raise IOError, 'remote player cannot be reached'


def get_remote_orders(connection):
    """Returns orders from a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)

    Returns
    ----------
    player_orders: orders given by remote player (str)

    Raises
    ------
    IOError: if remote player cannot be reached

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # receive orders
    try:
        orders = socket_in.recv(4096)
    except:
        raise IOError, 'remote player cannot be reached'

    # deal with null orders
    if orders == 'null':
        orders = ''

    return orders



#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================

def start_game(remote=1, pc_id = 1, player1='player 1', player2='player_2', map_size=7, file_name=None, sound=False, clear=False):
    """Start the entire game.
    Parameters:
    -----------
    player1: Name of the first player or IA (optional, str).
    player2: Name of the second player or IA (optional, str).
    map_size: Size of the map that players wanted to play with (optional, int).
    file_name: File of the name to load if necessary (optional, str).
    sound: Activate the sound or not (optional, bool).
    clear: Activate the "clear_output" of the notebook. Game looks more realistic, but do not work properly on each computer (optional, bool).
    Notes:
    ------
    It is the main function that gonna call the other functions.
    map_size must be contained between 7 and 30
    file_name load a game only if the game was saved earlier
    Version:
    -------
    specification: Laurent Emilie & Maroit Jonathan v.1 (10/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey v.1(21/03/16)
    """
    # Creation of the database or load it.
    if file_name:
        data_map = load_data_map()
    else:
        data_map = create_data_map(remote, map_size, player1, player2, clear)
        data_ia = create_data_ia(map_size, remote)
    remote2 = False
    # If we play versus another ia, connect to her.
    if remote2:
        #IP = '138.48.160.1' + str(pc_id)
        connection = connect_to_player(remote, '127.0.0.1')
        print 'connected'
    else:
        connection = None

    # Diplay introduction event and the map.
    play_event(sound,"","","intro")

    # Run de game turn by turn
    continue_game = True
    while continue_game:
        display_map(data_map, clear)
        data_map = choose_action(data_map, connection, data_ia)
        save_data_map(data_map)
        continue_game, loser, winner = is_not_game_ended(data_map)

    # Once the game is finished, disconnect from the other player.
    if remote2:
        disconnect_from_player(connection)

    # Display the game-over event (versus IA).
    if player1 == 'IA' or player2 == 'IA':
        player = "loser"
        play_event(sound,player1,player, 'game_over')
    # Display the win event (versus real player).
    else:
        player ="winner"
        play_event(sound,player1,player, 'win')

def display_event(player,player_name,event,count_line):
    """Display screen which representst the actualy situation with the name of the concerned player
    Parameters:
    -----------
    player: tells if player 1 or player 2 concerned player (str)
    player_name: name of the user to display (str)
    event : the event who represent the situation ,introduction , game over, winner screen (str)

    Version:
    -------
    specification: Maroit Jonathan and Laurent Emilie (v.1 16/02/16)
    implementation: Maroit Jonathan (v.1 16/02/16)
    """
    if len(str(player_name))< 9:
        player_name = str(player_name)+((9-(len(str(player_name))))*' ')
    player_name = player_name[0:9]
    color_player= Back.RED
    if player == 'player1':
        color_player= Back.BLUE
    
    if event=='intro' :   
    
        l0='█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'
        l1='██████████████████████████████████████████████████████++████████++███████████████████████████████████████████████████████'
        l2='███████+++█████████████████++██████████+++████████████++███++█████+++███████████████++███████████████++██████████++██████'
        l3='+++++++███++++++++++████;████:++██+++██+++██++++++++++++++++++++++███+++++++████████++███████+++██+++██+++++++█████+++██+'
        l4='+++++++***++*****+++++++++++++++++***+++++++**++++++++**+++++***++++++++++++++***++++++++++++***++:++++++***++***++++++++'
        l5='**+++██████**████*****+++*******************++*******;███*******++***████*++**+++*******+++*******+++**████:*******+++++*'
        l6='*****██:::**:::██********::*******;::************::**██:██******::***██*██*******************:::******██*:::*************'
        l7='*****██;,::,:::██:::*██**██**:████;:::█████;,,::;**::██:██:::***::***██::██:;██**;██::████:**██:*██::*██::::::█████:::,:*'
        l8='::;:;██::::::::██::::██::██::██::██::██:::::::::::::::███::::::::::::██::██::██:█:██:::::██::██:███:::██:::::██::;:::::::'
        l9=':::::█████:::::██::::██::██::██::██::██::::::::::::::██::::::::::::::██;:██::██:█:██:::::██::███:::::██████::██::::::::::'
        l10=':::::██::::::::██::::██::██::██████:::████:::::::::,,██:████:::::::::██,:██::██:█;██:;█████::██:::::::██::::::████:::::::'
        l11=':::::██:::::,,,██::::██,,██::██:,,:::::,,██:::,,,::,,██,,██::::::::::██::██,:██:█:██:██:,██::██:,,::::██:,,,:::::██,,,:::'
        l12=',,:::██:::,,,,,██:::.,████,,,██:,,,,,,,::██:::,,,,,,,██,,██,,,,,::,,,██,██,,,,██:██,:██,,██,,██,::,,,:██,,,,,,:::██,,,,,:'
        l13=',,,,,██████,,██████,,,,██,,,,,████,,,█████,,,,,,,,,,,,███,██,,,,,,,,,████,,,,,██,██,,,█████,,██,,,,,,,██,,,,,█████,,:,,,,'
        l14=',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'
        l15=',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,' 
        la1=Back.WHITE+Fore.BLACK+'                   GROUPE 42 : EMILIE LAURENT, JOFFREY BIENVENU, JONATHAN MAROIT ET SYLVAIN PIRLOT                       '  
    
    
    
    
        line_list = [l0,l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,la1]
        if count_line < len(line_list):
            print Fore.RED+ Back.BLACK+line_list[count_line]
         
    
    
    elif event=='game_over':
        d0=(Fore.BLACK+Back.WHITE)+'                                                        '+('The loser is: '+player_name)+'                                                   '
        d1='██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'
        d2='███████████████████████████████████████        ████████████████████████████████████        ███████████████████████████████████████'
        d3='███████████████████████████████████████        ████████████████████████████████████        ███████████████████████████████████████'
        d4='███████████████████████████████████████████████    ████                    ████    ███████████████████████████████████████████████'
        d5='███████████████████████████████████████████████    ████                    ████    ███████████████████████████████████████████████'
        d6='███████████████████████████████████████████████████                            ███████████████████████████████████████████████████'
        d7='███████████████████████████████████████████████████    ████████    ████████    ███████████████████████████████████████████████████'
        d8='███████████████████████████████████████████████████    ████████    ████████    ███████████████████████████████████████████████████'
        d9='███████████████████████████████████████████████████    ████████    ████████    ███████████████████████████████████████████████████'
        d10='███████████████████████████████████████████████████    ████            ████    ███████████████████████████████████████████████████'
        d11='███████████████████████████████████████████████████    ████            ████    ███████████████████████████████████████████████████'
        d12='███████████████████████████████████████████████████            ████            ███████████████████████████████████████████████████'
        d13='███████████████████████████████████████████████████            ████            ███████████████████████████████████████████████████'
        d14='███████████████████████████████████████████████    ████                    ████    ███████████████████████████████████████████████'
        d15='███████████████████████████████████████████████    ████                    ████    ███████████████████████████████████████████████'
        d16='███████████████████████████████████████        ████████    ████    ████    ████████        ███████████████████████████████████████'
        d17='███████████████████████████████████████        ████████    ████    ████    ████████        ███████████████████████████████████████'
        d18='██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████'
        d19=(Fore.BLACK+Back.WHITE)+'                                                                                                                                  '
        death_list=[d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18]
        if count_line < len(death_list):
            print (Fore.BLACK+color_player+death_list[count_line])
        
         
    elif event == 'win':
        
        w0=Back.BLACK+Fore.WHITE+'                                                               THE                                                                '
        wa='                                                                                                                                  '
        w1='               ██ █ ██       █           ██   ██  ████   ██   ██ ██   ██ ██████  █████                          █████             '
        w2='              █████████     ███          ██   ██   ██    ██   ██ ██   ██ ██      ██  ██         █            ███  █               ' 
        w3='              ███ █ ███      █           ██   ██   ██    ███  ██ ███  ██ ██      ██  ██        █ █         ██    █                '
        w4='               ██ █ ██       █           ██ █ ██   ██    ████ ██ ████ ██ ██      ██  ██       █ █ █      ██     █                 '
        w5='                █ █ █        █           ██ █ ██   ██    ██ ████ ██ ████ █████   █████          █       █      █                  '
        w6='                  █          █           ██ █ ██   ██    ██  ███ ██  ███ ██      ██ ██          █       █      █                  '
        w7='                  █          █            ██ ██    ██    ██   ██ ██   ██ ██      ██  ██         █       █     █                   '
        w8='                  █      █████████        ██ ██    ██    ██   ██ ██   ██ ██      ██  ██        ███       █    █                   '
        w9='                 ███     █████████        ██ ██   ████   ██   ██ ██   ██ ██████  ██  ██       ██ ██       ██ █                    '
        wb='                  █          █                                                                █   █         ████                  ' 
        wb1='                                                                                                                                  '
        w10=Back.BLACK+Fore.WHITE+'                                                               IS                                                                 '
        w11=(Back.BLACK+Fore.WHITE)+'                                                            '+player_name+'                                                             '                                 
        win_list=[w0,wa,w1,w2,w3,w4,w5,w6,w7,w8,w9,wb,wb1,w10,w11]
        if count_line < len(win_list):
            print (Fore.BLACK+color_player+win_list[count_line]) 

                

def play_event(sound,player,player_name,event):
    """Play a selected sound 
    Parameters:
    -----------
    sound: argument who active or desactive the sound, true or false (bool)
    sound_name:the name of the sound file that will be played (str)
    Versions:
    ---------
    spécification: Maroit Jonathan (v.1 17/02/16)
    implémentation: Maroit Jonathan(v.1 17/02/16)
    """ 
    if sound:
        sound_name = event+'.wav'
        chunk = 1024
        wf = wave.open(sound_name, 'rb')
        p = PyAudio()
        
        
        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)
        
        data = wf.readframes(chunk)
        written = False
        time_count = 0
        count_line = 0
        
        while data != '':
            time_count += 1
            if time_count == 18:
                time_count = 0
                display_event(player,player_name,event,count_line)
                count_line += 1
            stream.write(data)
            data = wf.readframes(chunk)
        
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
    else : 
        for count_line in range(20):
            display_event(player,player_name,event,count_line)
            time.sleep(0.5)
    time.sleep(2)
    
def display_map(data_map, clear):
    """Display the map of the game.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)
    clear: Activate the "clear_output" of the notebook. Game looks more realistic (bool)

    Version:
    --------
    specification: Laurent Emilie v.1 (12/02/16)
    implementation: Bienvenu Joffrey v.3 (01/04/16)
    """
    # if clear:
        #clear_output()

    # Check which player have to play and define displaying constants.
    player = 'player' + str((data_map['main_turn'] % 2) + 1)
    ennemy = 'player' + str(2 - (data_map['main_turn'] % 2))
    ui_color = data_map[player + 'info'][0]

    data_cell = {'ui_color': ui_color}

    # Generate the units to be displayed.
    for i in range(1, data_map['map_size'] + 1):
        for j in range(1, data_map['map_size'] + 1):

            # Coloration black/white of the cells.
            background_cell = ''
            if (i + j) % 2 == 0:
                background_cell = Back.WHITE

            if (i, j) in data_map['player1']:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = data_map['player1'][(i, j)][1] + background_cell + ' ☻' + str(data_map['player1'][(i, j)][0]) + (str(data_map['player1'][(i, j)][2]) + ' ')[:2]
            elif (i, j) in data_map['player2']:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = data_map['player2'][(i, j)][1] + background_cell + ' ☻' + str(data_map['player2'][(i, j)][0]) + (str(data_map['player2'][(i, j)][2]) + ' ')[:2]
            else:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = background_cell + (' ' * 5)

    # Generate the statistics to be displayed.
    player1_cell = data_map[player].keys()
    cell1_couter = 0
    player2_cell = data_map[ennemy].keys()
    cell2_couter = 0
    unit_name = {'E': 'Elf', 'D': 'Dwarf'}

    for i in range(1, 5):
        for j in range(1, 3):
            if len(player1_cell) > cell1_couter:
                data_cell['stat' + str(i) + str(j)] = (('0' + str(player1_cell[cell1_couter][0]))[-2:] + '-' + ('0' + str(player1_cell[cell1_couter][1]))[-2:] + ' ' + unit_name[data_map[player][player1_cell[cell1_couter]][0]] + ' hp: ' + str(data_map[player][player1_cell[cell1_couter]][2]) + ' ' * 20)[:20]
                cell1_couter += 1
            else:
                data_cell['stat' + str(i) + str(j)] = ' ' * 20
        for j in range(3, 5):
            if len(player2_cell) > cell2_couter:
                data_cell['stat' + str(i) + str(j)] = (('0' + str(player2_cell[cell2_couter][0]))[-2:] + '-' + ('0' + str(player2_cell[cell2_couter][1]))[-2:] + ' ' + unit_name[data_map[ennemy][player2_cell[cell2_couter]][0]] + ' hp: ' + str(data_map[ennemy][player2_cell[cell2_couter]][2]) + ' ' * 20)[:20]
                cell2_couter += 1
            else:
                data_cell['stat' + str(i) + str(j)] = ' ' * 20

    # Generate the title of the map to be displayed.
    data_cell['turn'] = str(data_map['main_turn']/2 + 1)
    data_cell['playername'] = data_map[player + 'info'][1]
    data_cell['blank'] = ((data_map['map_size'] * 5) - 19 - len(data_cell['turn']) - len(data_cell['playername'])) * ' '

    # Print the top of the UI.
    for line in data_map['data_ui']:
        print line % data_cell

def ia_reflexion(data_ia, data_map, player):
    """Brain of the Artificial Intelligence.

    Parameters:
    -----------
    ia_data: the whole database (dict)

    Returns:
    --------
    data_ia: database for the ia (dict)
    data_map: database of the whole game (dict)
    player: tells which player is the ia (int)

    Versions:
    ---------
    specification: Bienvenu Joffrey & Laurent Emilie v.2 (28/04/16)
    implementation: Bienvenu Joffrey & Laurent Emilie v.3 (01/0516)
    """
    ia = 'player' + str(data_map['remote'])
    enemy = 'player' + str(3 - data_map['remote'])
    commands = {}

    new_positions = []
    moved_units = []

    for ia_unit in data_ia[ia]:
        unit_has_attacked = False
        unit_targets = []

        for enemy_unit in data_ia[enemy]:
            # Find each possible target for the Dwarves.
            if data_ia[ia][ia_unit][0] == 'D':
                if (ia_unit[0] - 1) <= enemy_unit[0] <= (ia_unit[0] + 1) and (ia_unit[1] - 1) <= enemy_unit[1] <= (ia_unit[1] + 1):
                    # Add the unit to the target list.
                    unit_targets.append(enemy_unit)

            # Find each possible target for the Elves - ATTACK
            else:
                for i in range(2):
                    if (ia_unit[0] - (1 + i)) <= enemy_unit[0] <= (ia_unit[0] + (1 + i)) and (ia_unit[1] - (1 + i)) <= enemy_unit[1] <= (ia_unit[1] + (1 + i)):
                        # Add the unit to the target list.
                        unit_targets.append(enemy_unit)

        # Find the weakest units.
        if unit_targets:
            target = unit_targets[0]
            for enemy_unit in unit_targets:
                if data_ia[enemy][enemy_unit][0] == 'D' or data_ia[enemy][enemy_unit][1] < data_ia[enemy][target][1]:
                    target = enemy_unit

            # Write the attack.
            commands[data_ia[ia][ia_unit][2]] = [ia_unit, ' -a-> ', target]
            unit_has_attacked = True

        # Find the weakest of all enemy's units - MOVE
        if not unit_has_attacked:
            target_list = data_ia[enemy].keys()
            target = target_list[0]

            for enemy_unit in data_ia[enemy]:
                if data_ia[enemy][enemy_unit][0] == 'D' or data_ia[enemy][enemy_unit][1] < data_ia[enemy][target][1]:
                    target = enemy_unit

            target_cell = [ia_unit[0], ia_unit[1]]
            # Move on Y axis
            if target and abs(ia_unit[1] - target[1]) > abs(ia_unit[0] - target[0]) and 1 <= ia_unit[0] <= data_map['map_size'] and 1 <= ia_unit[1] <= data_map['map_size']:
                if ia_unit[1] > target[1]:
                    target_cell[1] -= 1
                else:
                    target_cell[1] += 1
            # Move on X axis
            elif target and 1 <= ia_unit[0] <= data_map['map_size'] and 1 <= ia_unit[1] <= data_map['map_size']:
                if ia_unit[0] > target[0]:
                    target_cell[0] -= 1
                else:
                    target_cell[0] += 1

            new_target = False
            # Check if he can move on the targeted position.
            enemy_positions = data_ia[enemy].keys()
            ia_positions = data_ia[ia].keys()
            for units in moved_units:
                del ia_positions[ia_positions.index(units)]

            # If the units can't move, find another free cell.
            if target_cell in (new_positions or enemy_positions or ia_positions):
                new_target_cells = []
                for line in range(target_cell[0] - 1, target_cell[0] + 2):
                    for column in range(target_cell[1] - 1, target_cell[1] + 2):

                        # Append the possible free cell to the list.
                        if (line, column) not in (new_positions or enemy_positions or ia_positions):
                            new_target_cells.append((line, column))

                # Choose the nearest free cell.
                if new_target_cells:
                    new_target = new_target_cells[0]
                    for cell in new_target_cells:
                        if abs(ia_unit[0] - cell[0]) + abs(ia_unit[1] - cell[1]) < abs(ia_unit[0] - new_target[0]) + abs(ia_unit[1] - new_target[1]):
                            new_target = new_target_cells[new_target_cells.index(cell)]

            # Save the new target in the correct variable.
            if new_target:
                target_cell = new_target

            # Write the move
            if target_cell != ia_unit:
                commands[data_ia[ia][ia_unit][2]] = [ia_unit, ' -m-> ', target_cell]
                new_positions.append(target_cell)
                moved_units.append(ia_unit)

    return commands

def ia_action(data_map, data_ia, player):
    """The artificial intelligence of the game. Generate an instruction and return it.

    Parameters:
    -----------
    data_map: the whole database of the game (dict).
    data_ia: the ia identifier ('player1' or 'player2', string).
    player: the player identifier ('player1' or 'player2', string).

    Return:
    -------
    command: the instruction of the ia (string).

    Version:
    --------
    specification: Laurent Emilie and Bienvenu Joffrey v. 1 (02/03/16)
    implementation: Bienvenu Joffrey and Jonathan Maroit & Laurent Emilie v.4 (01/05/16)
    """
    raw_commands = ia_reflexion(data_ia, data_map, player)

    # Rewrite the command into a single string.
    string_commands = ''
    for key in raw_commands:
        string_commands += ('0' + str(raw_commands[key][0][0]))[-2:] + '_' + ('0' + str(raw_commands[key][0][1]))[-2:] + raw_commands[key][1] + ('0' + str(raw_commands[key][2][0]))[-2:] + '_' + ('0' + str(raw_commands[key][2][1]))[-2:] + '   '
    print string_commands
    return string_commands


def create_data_ia(map_size, id):
    """Create the ia database.

    Parameters:
    -----------
    map_size: the length of the board game, every unit add one unit to vertical axis and horizontal axis (int, optional)
    id: tells which player is the ia (int)

    Returns:
    --------
    data_ia: the ia database (dict).

    Versions:
    ---------
    specifications: Laurent Emilie v.1 (24/04/16)
    implementation: Laurent Emilie v.1 (24/04/16)
    """
    data_ia = {'player1': {},
               'player2': {},
               'main_turn': 1,
               'attack_turn': 0,
               'map_size': map_size,
               'id': id}


    order_unit = {}
    order_unit['if_left'] = [(2,3), (3,2), (1,3), (2,2), (3,1), (1,2), (2,1), (1,1)]
    order_unit['if_right'] = [(map_size -1, map_size -2), (map_size -2, map_size -1), (map_size, map_size -2), (map_size -1, map_size -1), (map_size -1, map_size -1), (map_size -2, map_size), (map_size, map_size-1), (map_size -1, map_size), (map_size, map_size)]

    print order_unit

    for i in range(2):
        for line in range(1, 4):
            for column in range(1, 4):
                unit = 'E'
                life = 4

                if line >= 2 and column >= 2:
                    unit = 'D'
                    life = 10

                if line + column != 6:
                    x_pos = abs(i * map_size - line + i)
                    y_pos = abs(i * map_size - column + i)

                    if i == 0:
                        unit_id = (order_unit['if_left'].index((x_pos,y_pos))) + 1
                        data_ia['player1'][(x_pos, y_pos)] = [unit, life, unit_id]
                    else:
                        unit_id = (order_unit['if_right'].index((x_pos,y_pos))) + 1
                        data_ia['player2'][(x_pos, y_pos)] = [unit, life, unit_id]

    return data_ia


def save_data_map(data_map):
    """Load a saved game.

    Parameters:
    -----------
    data_map_saved: name of the file to load (str)

    Version:
    --------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Pirlot Sylvain v.1 & Bienvenu Joffrey (21/03/16)
    """
    pickle.dump(data_map, open("save.p", "wb"))



def load_data_map():
    """Save the game.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)

    Version:
    --------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Pirlot Sylvain v.1 & Bienvenu Joffrey (21/03/16)
    """

    return pickle.load(open("save.p", "rb"))

def move_unit(data_map, start_coord, end_coord, player, enemy, data_ia):
    """Move an unit from a cell to another cell. And check if the move is legal.

    Parameters:
    -----------
    data_map: the whole database (dict)
    start_coord: coordinates at the origin of the movement (tuple)
    end_coord: coordinates at the destination of the movement (tuple)
    player: the player who is moving the unit (str)
    enemy: the other player (str)

    Returns:
    --------
    data_map: the database modified by the move (dict)

    Notes:
    ------
    The database will only change the coordinate of the units concerned.
    start_coord and end_coord will be tuple of int

    Version:
    --------
    specification: Laurent Emilie & Bienvenu Joffrey v.2 (17/02/16)
    implementation: Laurent Emilie & Bienvenu Joffrey v.2 (17/03/16)
    """

    # Check if there's a unit on the starting cell, and if the destination cell is free.
    if start_coord in data_map[player] and end_coord not in data_map[player]and end_coord not in data_map[enemy]:

        # Check if the move is rightful and save it.
        if start_coord[0] - 1 <= end_coord[0] <= start_coord[0] + 1 and start_coord[1] - 1 <= end_coord[1] <= start_coord[1] + 1:
            if data_map[player][start_coord][0] == 'E' or (sum(start_coord) - 1 <= sum(end_coord) <= sum(start_coord) + 1):
                data_map[player][end_coord] = data_map[player].pop(start_coord)
                data_ia[player][end_coord] = data_ia[player].pop(start_coord)
    return data_map, data_ia

def is_not_game_ended(data_map):
    """Check if the game is allow to continue.

    Parameter:
    ----------
    data_map: the whole database (dict)

    Returns:
    --------
    continue_game : boolean value who said if the game need to continue(bool).
    loser : the player who lose the game(str).
    winner : the player who won the game(str).

    Notes:
    ------
    The game stop when a player run out of unit or if 20 turn have been played without any attack.
    In this case, the player 1 win.

    Version:
    -------
    specification: Maroit Jonathan(v.1 21/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey (v.1.1 22/03/16)
    """

    continue_game = True
    loser = None
    winner = None

    # If a player has not any units, the other player win.
    for i in range(2):
        if not len(data_map['player' + str(i + 1)]) and continue_game:
            loser = 'player' + str(i + 1)
            winner = 'player' + str(3 - (i + 1))
            continue_game = False

    # If there's 20 turn without any attack, player1 loose and player2 win.
    if float(data_map['attack_turn']) / 2 > 19:
        loser = 'player1'
        winner = 'player2'
        continue_game = False

    return continue_game, loser, winner

def create_data_ui(data_map, clear):
    """Generate the whole user's interface with the statistics.

    Parameters:
    -----------
    data_map: the whole database (dict)
    clear: Activate the "clear_output" of the notebook. Game looks more realistic (bool)

    Returns:
    --------
    data_ui: the user's interface to print (list)

    Versions:
    ---------
    specification: Laurent Emilie v.1 (15/03/16)
    implementation: Bienvenu Joffrey v.3.1 (24/03/16)
    """
    data_ui = [[]] * (16 + data_map['map_size'])

    # Initialisation of the displaying constants.
    grid_size = 5 * data_map['map_size']
    ui_color = '%(ui_color)s'

    margin = 5
    line_coloured = ui_color + ('█' * (117 + margin)) + Style.RESET_ALL
    if clear:
        margin = 9
        line_coloured = ui_color + ('█' * (121 + margin)) + Style.RESET_ALL


    border_black = Back.BLACK + '  ' + Style.RESET_ALL
    margin_left = ((20 - data_map['map_size']) * 5) / 2
    margin_right = ((20 - data_map['map_size']) * 5) - (((20 - data_map['map_size']) * 5) / 2)
    border_coloured_margin_left = ui_color + ('█' * (margin + margin_left)) + Style.RESET_ALL
    border_coloured_margin_right = ui_color + ('█' * (margin + margin_right)) + Style.RESET_ALL
    border_coloured_left = ui_color + ('█' * margin) + Style.RESET_ALL
    border_coloured_right = ui_color + ('█' * margin) + Style.RESET_ALL
    border_coloured_middle = ui_color + ('█' * 8) + Style.RESET_ALL

    border_white = ' ' * 2

    # Generate and save the top of the UI.
    for i in range(3):
        data_ui[i] = line_coloured

    # Generate and save the top of the grid.
    turn_message = 'Turn %(turn)s - %(playername)s, it\'s up to you ! %(blank)s'
    data_ui[3] = border_coloured_margin_left + Fore.WHITE + Back.BLACK + '  ' + turn_message + '  ' + Style.RESET_ALL + border_coloured_margin_right
    data_ui[4] = border_coloured_margin_left + border_black + ' ' * (grid_size + 8) + border_black + border_coloured_margin_right

    # Generate and save the architecture of the grid.
    for i in range(1, data_map['map_size'] + 1):
        data_ui[i + 4] = border_coloured_margin_left + border_black + Fore.BLACK + ' ' + ('0' + str(i))[-2:] + ' ' + Style.RESET_ALL
        for j in range(1, data_map['map_size'] + 1):
            data_ui[i + 4] += '%((' + str(i) + ',' + str(j) + '))5s' + Style.RESET_ALL
        data_ui[i + 4] += '    ' + border_black + border_coloured_margin_right

    # Generate and save the foot of the grid.
    data_ui[data_map['map_size'] + 5] = border_coloured_margin_left + border_black + Fore.BLACK + '   '
    for i in range(1, data_map['map_size'] + 1):
        data_ui[data_map['map_size'] + 5] += '  ' + ('0' + str(i))[-2:] + ' '
    data_ui[data_map['map_size'] + 5] += '     ' + border_black + border_coloured_margin_right

    data_ui[data_map['map_size'] + 6] = border_coloured_margin_left + Back.BLACK + (grid_size + 12) * ' ' + Style.RESET_ALL + border_coloured_margin_right

    # Generate and save the top of the statistics.
    data_ui[data_map['map_size'] + 7] = line_coloured

    data_ui[data_map['map_size'] + 8] = border_coloured_left + Fore.WHITE + Back.BLACK + '  Your units:' + (' ' * 39) + Style.RESET_ALL + border_coloured_middle
    data_ui[data_map['map_size'] + 8] += Fore.WHITE + Back.BLACK + '  Opponent\'s units:' + (' ' * 33) + Style.RESET_ALL + border_coloured_right

    # Generate and save the content of the statistics.
    for i in range(4):
        data_ui[data_map['map_size'] + 9 + i] = border_coloured_left + border_black + ' ' + border_white + Fore.BLACK + '%(stat' + str(i+1) + '1)s' + border_white + '%(stat' + str(i+1) + '2)s' + border_white + ' ' + border_black + border_coloured_middle
        data_ui[data_map['map_size'] + 9 + i] += border_black + ' ' + border_white + '%(stat' + str(i+1) + '3)s' + border_white + '%(stat' + str(i+1) + '4)s' + border_white + ' ' + border_black + border_coloured_right

    # Generate and save the foot of the statistics.
    data_ui[data_map['map_size'] + 13] = border_coloured_left + Back.BLACK + (' ' * 52) + Style.RESET_ALL + border_coloured_middle
    data_ui[data_map['map_size'] + 13] += Back.BLACK + (' ' * 52) + Style.RESET_ALL + border_coloured_right

    for i in range(2):
        data_ui[data_map['map_size'] + 14 + i] = line_coloured

    return data_ui

def create_data_map(remote, map_size=7, name_player1='A', name_player2='B', clear=False):
    """ Create a dictionary that the game will use as database with units at their initial places.

    Parameters:
    ----------
    map_size : the length of the board game, every unit add one unit to vertical axis and horizontal axis (int, optional).
    name_player1: name of the first player (str)
    name_player2: name of the second player (str)
    clear: if you want to activate the clear screen (bool)

    Returns:
    -------
    data_map : dictionary that contain information's of every cells of the board (dict).
    data_ui : list with data to display the ui (list of str).

    Notes:
    -----
    The game board is a square, the size must be a positive integer, minimum 7 and maximum 30 units,
    or the game will be stopped after 20 turns if nobody attack.

    Version:
    -------
    specification: Maroit Jonathan & Bienvenu Joffrey v.2 (04/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey & Laurent Emilie v.5 (23/03/16)
    """
    # Initialisation of variables
    data_map = {'player1': {},
                'player1info': [],
                'player2': {},
                'player2info': [],
                'main_turn': 1,
                'attack_turn': 0,
                'map_size': map_size,
                'remote': remote}

    # Place units to their initial positions.
    player_data = [Fore.BLUE, Fore.RED, name_player1, name_player2]
    for i in range(2):
        for line in range(1, 4):
            for column in range(1, 4):
                unit = 'E'
                life = 4

                if line >= 2 and column >= 2:
                    unit = 'D'
                    life = 10

                if line + column != 6:
                    x_pos = abs(i * map_size - line + i)
                    y_pos = abs(i * map_size - column + i)

                    data_map['player' + str(i + 1)][(x_pos, y_pos)] = [unit, player_data[i], life]
        data_map['player' + str(i + 1) + 'info'].extend([player_data[i], player_data[i + 2]])

    if not remote:
        # Randomize which player will start the game.
        number = random.randint(1, 2)
        if number == 1:
            data_map['player1info'][1] = name_player1
            data_map['player2info'][1] = name_player2
        else:
            data_map['player1info'][1] = name_player2
            data_map['player2info'][1] = name_player1

    data_map['data_ui'] = create_data_ui(data_map, clear)

    return data_map

def choose_action(data_map, connection, data_ia):
    """Ask and execute the instruction given by the players to move or attack units.

    Parameters:
    ----------
    data_map: the whole database (dict)

    Returns:
    -------
    data_map: the database changed by moves or attacks (dict)

    Notes:
    -----
    Instructions must be in one line, with format xx_xx -a-> xx_xx for an attack and xx_xx -m-> xx_xx for a movement.
    Each instruction must be spaced by 3 characters.

    Version:
    -------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Laurent Emilie v.3 (21/03/16)
    """
    player = 'player' + str((data_map['main_turn'] % 2) + 1)
    enemy = 'player' + str(2 - (data_map['main_turn'] % 2))
    if data_map['remote']:
        player = 'player' + str(data_map['remote'])
        enemy = 'player' + str(3 - data_map['remote'])

    # Tells whether IA or player's turn.
    # if (data_map['main_turn'] % 2) + 2 == data_map['remote'] or data_map['main_turn'] % 2 == data_map['remote'] or data_map[str(player + 'info')][1] == 'IA':
    if data_map['main_turn'] % 2 == data_map['remote'] % 2 or data_map[str(player + 'info')][1] == 'IA':
        game_instruction = ia_action(data_map, data_ia, player)
        #if data_map['remote']:
        #    notify_remote_orders(connection, game_instruction)
    else:
        if data_map['remote']:
            player = 'player' + str(3 - data_map['remote'])
            enemy = 'player' + str(data_map['remote'])
            game_instruction = get_remote_orders(connection)
        else:
            game_instruction = raw_input('Enter your commands in format xx_xx -a-> xx_xx or xx_xx -m-> xx_xx')

    # Split commands string by string.
    list_action = game_instruction.split()

    # grouper instruction par instructions
    list_action2 = []
    for instruction in range(0, len(list_action), 3):
        list_action2.append((list_action[instruction], list_action[instruction + 1], list_action[instruction + 2]))

    # Call attack_unit or move_unit in function of instruction.
    attack_counter = 0
    for i in range(len(list_action2)):
        if '-a->' in list_action2[i]:
            data_map, attacked, data_ia = attack_unit(data_map, (int(list_action2[i][0][:2]), int(list_action2[i][0][3:])),
                        (int(list_action2[i][2][:2]), int(list_action2[i][2][3:])), player, enemy, data_ia)
            attack_counter += attacked
        elif '-m->' in list_action2[i]:
            data_map, data_ia = move_unit(data_map, (int(list_action2[i][0][:2]), int(list_action2[i][0][3:])),
                      (int(list_action2[i][2][:2]), int(list_action2[i][2][3:])), player, enemy, data_ia)

    # Save if a player have attacked.
    if attack_counter:
        data_map['attack_turn'] = 0
    else:
        data_map['attack_turn'] += 1
    data_map['main_turn'] += 1

    return data_map

def attack_unit(data_map, attacker_coord, target_coord, player, enemy, data_ia):
    """Attack an adverse cell and check whether it is a legal attack.

    Parameters:
    -----------
    data_map: the whole database (dict)
    attacker_coord: coordinates of the attacker's pawn (tuple)
    target_coord: coordinates of the attacked's pawn (tuple)
    player: the player who is attacking (str)
    enemy: the other player (str)

    Returns:
    --------
    data_map: the database modified by the attack (dict)

    Notes:
    ------
    The database will only change by decrement unit's life and, eventually, decrementing the unit's number of the player.
    attacker_coord and attacked_coord will be tuple of int.

    Version:
    -------
    specification: Laurent Emilie & Bienvenu Joffrey v.2 (17/03/16)
    implementation: Bienvenu Joffrey v.1 (17/03/16)
    """
    damage = {'E': 1, 'D': 3}
    attacked = 0

    # Check if there's a unit on the attacker cell, and if the attacked cell is occupied.
    if attacker_coord in data_map[player] and target_coord in data_map[enemy]:

        # Check if the attack is rightful and save it.
        if attacker_coord[0] - 2 <= target_coord[0] <= attacker_coord[0] + 2 and attacker_coord[1] - 2 <= target_coord[1] <= attacker_coord[1] + 2:
            attacker_type = data_map[player][attacker_coord][0]
            if attacker_type == 'E' or (attacker_coord[0] - 1 <= target_coord[0] <= attacker_coord[0] + 1 and attacker_coord[1] - 1 <= target_coord[1] <= attacker_coord[1] + 1):

                # Decrement the heal point and delete the unit if their hp are equal or less than 0.
                data_map[enemy][target_coord][2] -= damage[attacker_type]
                if data_map[enemy][target_coord][2] <= 0:
                    del data_map[enemy][target_coord]

                data_ia[enemy][target_coord][1] -= damage[attacker_type]
                if data_ia[enemy][target_coord][1] <= 0:
                    del data_ia[enemy][target_coord]

                attacked = 1

    return data_map, attacked, data_ia