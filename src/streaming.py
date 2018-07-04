# a little change from transcribe_streaming_indefinite.py(Copyright 2017 Google Inc),
# a sample usage of Google Cloud Speech API

# [START import_libraries]
from __future__ import division

import collections
import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.api_core import exceptions

import streaming_mic
from PyQt5.QtCore import QThread,pyqtSignal
# [END import_libraries]


def duration_to_secs(duration):
    return duration.seconds + (duration.nanos / float(1e9))


class ResumableMicrophoneStream(streaming_mic.MicrophoneStream):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk_size, max_replay_secs=5):
        super(ResumableMicrophoneStream, self).__init__(rate, chunk_size)
        self._max_replay_secs = max_replay_secs

        # Some useful numbers
        # 2 bytes in 16 bit samples
        self._bytes_per_sample = 2 * self._num_channels
        self._bytes_per_second = self._rate * self._bytes_per_sample

        self._bytes_per_chunk = (self._chunk_size * self._bytes_per_sample)
        self._chunks_per_second = (
                self._bytes_per_second // self._bytes_per_chunk)
        self._untranscribed = collections.deque(
                maxlen=self._max_replay_secs * self._chunks_per_second)

    def on_transcribe(self, end_time):
        while self._untranscribed and end_time > self._untranscribed[0][1]:
            self._untranscribed.popleft()

    def generator(self, resume=False):
        total_bytes_sent = 0
        if resume:
            # Make a copy, in case on_transcribe is called while yielding them
            catchup = list(self._untranscribed)
            # Yield all the untranscribed chunks first
            for chunk, _ in catchup:
                yield chunk

        for byte_data in super(ResumableMicrophoneStream, self).generator():
            # Populate the replay buffer of untranscribed audio bytes
            total_bytes_sent += len(byte_data)
            chunk_end_time = total_bytes_sent / self._bytes_per_second
            self._untranscribed.append((byte_data, chunk_end_time))

            yield byte_data


class SimulatedMicrophoneStream(ResumableMicrophoneStream):
    def __init__(self, audio_src, *args, **kwargs):
        super(SimulatedMicrophoneStream, self).__init__(*args, **kwargs)
        self._audio_src = audio_src

    def _delayed(self, get_data):
        total_bytes_read = 0
        start_time = time.time()

        chunk = get_data(self._bytes_per_chunk)

        while chunk and not self.closed:
            total_bytes_read += len(chunk)
            expected_yield_time = start_time + (
                    total_bytes_read / self._bytes_per_second)
            now = time.time()
            if expected_yield_time > now:
                time.sleep(expected_yield_time - now)

            yield chunk

            chunk = get_data(self._bytes_per_chunk)

    def __exit__(self, type, value, traceback):
        self.closed = True


class StreamingThread(QThread):

    streaming_result = pyqtSignal(str)
    final_result = pyqtSignal(str)

    @staticmethod
    def __record_keeper(responses, stream):
        """Calls the stream's on_transcribe callback for each final response.
        Args:
            responses - a generator of responses. The responses must already be
                filtered for ones with results and alternatives.
            stream - a ResumableMicrophoneStream.
        """
        for r in responses:
            result = r.results[0]
            if result.is_final:
                top_alternative = result.alternatives[0]
                # Keep track of what transcripts we've received, so we can resume
                # intelligently when we hit the deadline
                stream.on_transcribe(duration_to_secs(
                        top_alternative.words[-1].end_time))
            yield r

    def __emit_streaming_result(self, responses, stream):
        """Iterates through server responses and prints them.
        Same as in transcribe_streaming_mic, but keeps track of when a sent
        audio_chunk has been transcribed.
        """
        try:
            with_results = (r for r in responses if (
                    r.results and r.results[0].alternatives))
            streaming_mic.emit_streaming_result(
                StreamingThread.__record_keeper(with_results, stream), thread=self)
        except exceptions.InvalidArgument:
            pass
        except exceptions.ServiceUnavailable:
            self.streaming_result.emit('オフラインのため, 音声認識結果は表示されません')
            self.quit()

    def __do_streaming(self, sample_rate):
        # See http://g.co/cloud/speech/docs/languages
        # for a list of supported languages.
        language_code = 'ja-JP'  # a BCP-47 language tag

        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            max_alternatives=1,
            enable_word_time_offsets=True)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)
        mic_manager = ResumableMicrophoneStream(
                sample_rate, int(sample_rate / 10))

        with mic_manager as stream:
            resume = False
            while True:
                self.audio_generator = stream.generator(resume=resume)
                self.requests = (types.StreamingRecognizeRequest(audio_content=content)
                            for content in self.audio_generator)

                self.responses = client.streaming_recognize(streaming_config, self.requests)

                try:
                    # Now, put the transcription responses to use.
                    self.__emit_streaming_result(self.responses, stream)
                    break
                except (exceptions.OutOfRange, exceptions.InvalidArgument) as e:
                    if not ('maximum allowed stream duration' in e.message or
                            'deadline too short' in e.message):
                        raise
                    resume = True

    def run(self):
        self.__do_streaming(44100)