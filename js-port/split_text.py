from typing import List, Optional
from pydantic import BaseModel
from .types import Tokenizer, should_continue
from .token_counter import token_counter
from .cancelled_error import CancelledError

ALPHANUMERIC_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
DEFAULT_SEPARATORS = [
    "\n## ",
    "\n### ",
    "\n#### ",
    "\n##### ",
    "\n###### ",
    "```\n\n",
    "\n\n***\n\n",
    "\n\n---\n\n",
    "\n\n___\n\n",
    "<table>",
    "\n\n",
    "\n",
    " "
]

class SplitTextArgs(BaseModel):
    text: str
    tokenizer: Tokenizer
    max_chunk_size: int
    separators: Optional[List[str]] = None
    should_continue: Optional[should_continue] = None

class TextChunk(BaseModel):
    text: str
    length: int
    start_pos: int
    end_pos: int


def split_text(args: SplitTextArgs) -> List[TextChunk]:
    text = args.text
    tokenizer = args.tokenizer
    max_chunk_size = args.max_chunk_size
    separators = args.separators or DEFAULT_SEPARATORS

    encode_tokens = tokenizer.encode_tokens
    count_tokens = token_counter(encode_tokens=encode_tokens, max_expected_tokens=max_chunk_size)

    def check_continue():
        if args.should_continue and not args.should_continue():
            raise CancelledError()

    def recursive_split(text: str, separators: List[str], start_pos: int) -> List[TextChunk]:
        chunks = []
        if text:
            parts = []
            separator = ''
            next_separators = separators[1:] if len(separators) > 1 else []
            if separators:
                separator = separators[0]
                parts = split_by_spaces(text) if separator == ' ' else text.split(separator)
            else:
                half = len(text) // 2
                parts = [text[:half], text[half:]]

            for i, part in enumerate(parts):
                check_continue()
                last_chunk = (i == len(parts) - 1)

                chunk = part
                end_pos = (start_pos + (len(chunk) - 1)) + (0 if last_chunk else len(separator))
                if not last_chunk:
                    chunk += separator

                if not contains_alphanumeric(chunk):
                    continue

                length = count_tokens(chunk)
                if length > max_chunk_size:
                    sub_chunks = recursive_split(chunk, next_separators, start_pos)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(TextChunk(text=chunk, length=length, start_pos=start_pos, end_pos=end_pos))

                start_pos = end_pos + 1

        return combine_chunks(chunks)

    def combine_chunks(chunks: List[TextChunk]) -> List[TextChunk]:
        combined_chunks = []
        current_chunk = None
        for chunk in chunks:
            check_continue()
            if current_chunk:
                length = current_chunk.length + chunk.length
                if length > max_chunk_size:
                    combined_chunks.append(current_chunk)
                    current_chunk = chunk
                else:
                    current_chunk.text += chunk.text
                    current_chunk.end_pos = chunk.end_pos
                    current_chunk.length += length
            else:
                current_chunk = chunk
        if current_chunk:
            combined_chunks.append(current_chunk)
        return combined_chunks

    def contains_alphanumeric(text: str) -> bool:
        return any(char in ALPHANUMERIC_CHARS for char in text)

    def split_by_spaces(text: str) -> List[str]:
        parts = []
        tokens = encode_tokens(text)
        while True:
            check_continue()
            if len(tokens) <= max_chunk_size:
                parts.append(tokenizer.decode_tokens(tokens))
                break
            else:
                span = tokens[:max_chunk_size]
                tokens = tokens[max_chunk_size:]
                parts.append(tokenizer.decode_tokens(span))
        return parts

    return recursive_split(text, separators, 0)
