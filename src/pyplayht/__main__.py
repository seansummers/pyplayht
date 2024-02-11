"""Basic CLI runner that takes text on stdin and streams wav data on stdout."""

import fileinput
import io
import sys
import textwrap
from contextlib import redirect_stdout

from . import GrpcTts

LINE_LIMIT = 6
SOFT_CHARACTER_MAX = 350
HARD_CHARACTER_MAX = 500

__wrapper = textwrap.TextWrapper(
    width=HARD_CHARACTER_MAX,
    expand_tabs=False,
    replace_whitespace=True,
    fix_sentence_endings=True,
    break_long_words=False,
    drop_whitespace=True,
    break_on_hyphens=False,
    max_lines=LINE_LIMIT,
)
# noinspection PyProtectedMember
__chunk_splitter = __wrapper._split_chunks

SENTENCE_END_SEARCH = __wrapper.sentence_end_re.search
WHITESPACE_TRANS = {}.fromkeys(__wrapper.unicode_whitespace_trans)


def ensure_limits(
    line: str, sentence_threshold=SOFT_CHARACTER_MAX, word_threshold=HARD_CHARACTER_MAX
) -> list[str]:
    """Given a line, split it by sentences if it is over length sentence_threshold.
    If it is still over, split it by word_threshold if it is still over length word_threshold.

    :param line: Line of text with sentence punctuation.
    :param sentence_threshold: Length to begin splitting by sentences.
    :param word_threshold: Length to begin splitting by words.
    :returns list[str]: Lines of text split by sentences.

    >>>
    """
    chunks = (
        chunk for chunk in __chunk_splitter(line) if chunk.translate(WHITESPACE_TRANS)
    )
    return chunks
    line_count = 0
    while line_count < min(max_lines, LINE_LIMIT):
        for line in texts:
            line_count += 1
            if len(line) > SOFT_CHARACTER_MAX:
                for line in break_by_sentence(line):
                    line_count += 1
                    if len(line) > HARD_CHARACTER_MAX:
                        for line in break_by_words(new_line):
                            line_count += 1
                            lines_to_speek.append(line) + 1


def turn_batch(tts: GrpcTts, texts: io.TextIOBase | list[str], output: io.BytesIO):
    """Using tts, parse the iterable of text lines (file object or other iterable), and produce bytes into the binary output file.
    Reads up to max_lines (no more than LINE_LIMIT) of max_characters per line.
    Breaks up lines longer than SOFT_CHARACTER_MAX at sentence endings, or 500 at word endings.


    :param tts: GrpcTts client instance
    :param texts: Text file stream
    :param output:  Binary file stream
    :return: None
    """
    for line in ensure_limits(texts):
        GrpcTts()


def pipeline_batch(tts: GrpcTts):
    """Pipeline TTS: read in lines of text until EOF, push out bytes"""
    with open(sys.stdout.fileno(), "wb", closefd=False) as stdout_b:
        for line in fileinput.input(encoding="utf-8"):
            for tts_response in tts([line]):
                stdout_b.write(tts_response.data)
                stdout_b.flush()


def main():
    """Main CLI runner. STDIN for text, STDOUT for WAV bytestream."""
    tts = GrpcTts.default()
    pipeline_batch(tts)


main()
