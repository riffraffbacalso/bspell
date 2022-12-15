from io import BytesIO
from string import ascii_lowercase
import re

from pytest_mock import MockerFixture
from pytest_httpx import HTTPXMock, IteratorStream
import pytest

from words import (
    Words,
    ALT_WORDS_PATH,
    OS_WORDS_PATH,
    OPTED_URL,
    CHIRICO_URL,
    TAR_MEMBERS,
)
from tests.params_words import *


def test_OS_reads_share_dict(mocker: MockerFixture):
    mock_fileinput = mocker.patch("fileinput.input")
    Words.get_words("OS")
    mock_fileinput.assert_called_once_with(OS_WORDS_PATH)


@pytest.mark.parametrize("lines,words", OS_PARAMS.values(), ids=OS_PARAMS.keys())
def test_OS_formats_words(mocker: MockerFixture, lines: list[str], words: list[str]):
    mocker.patch("fileinput.input", return_value=lines)
    assert [word for word in Words.get_words("OS")] == words


def test_create_dir(mocker: MockerFixture):
    mocker.patch("os.path.exists", return_value=False)
    mock_mkdir = mocker.patch("os.mkdir")
    mocker.patch("os.listdir", return_value=[".words"])
    mocker.patch("fileinput.input")
    Words.get_words("")
    mock_mkdir.assert_called_once_with(ALT_WORDS_PATH)


@pytest.mark.parametrize("word_src", ALT_WS_PARAMS.values(), ids=ALT_WS_PARAMS.keys())
def test_create_alt(mocker: MockerFixture, word_src: str):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=[])
    mock_open = mocker.patch("builtins.open")
    mock_req = mocker.patch(f"words.Words.request_{word_src}_words")
    mocker.patch("words.file_gen")
    Words.get_words(word_src)
    mock_open.assert_called_once_with(f"{ALT_WORDS_PATH}/{word_src}.words", "w")
    mock_req.assert_called_once()


def test_OPTED_requests(httpx_mock: HTTPXMock):
    for char in ascii_lowercase:
        httpx_mock.add_response(
            url=f"{OPTED_URL}{char}.html",
            stream=IteratorStream(
                [
                    b"<BODY>\n",
                    b"</BODY>",
                ]
            ),
        )
    Words.request_OPTED_words()
    reqs = httpx_mock.get_requests()
    assert len(reqs) == 26
    for req in reqs:
        assert req.method == "GET"
        assert re.match(rf"{re.escape(OPTED_URL)}[a-z].html", str(req.url))


@pytest.mark.parametrize("word,fn,defn", OPTED_PARAMS.values(), ids=OPTED_PARAMS.keys())
def test_OPTED_parse(httpx_mock: HTTPXMock, word: str, fn: str, defn: str):
    url_pattern = re.compile(rf"{re.escape(OPTED_URL)}[a-z].html")
    httpx_mock.add_response(
        url=url_pattern,
        stream=IteratorStream(
            [
                b"<BODY>\n",
                f"<P><B>{word}</B></P> (<I>{fn}</I>) {defn}\n".encode(),
                f"<P><B>{word}</B></P> (<I>{fn}</I>) {defn}\n".encode(),
                b"</BODY>\n",
            ]
        ),
    )
    assert [word for word in Words.request_OPTED_words()] == [word.lower()] * (
        26 if len(word) >= 4 else 0
    )


@pytest.mark.parametrize("data,words", TAR_PARAMS.values(), ids=TAR_PARAMS.keys())
def test_chirico(
    mocker: MockerFixture, httpx_mock: HTTPXMock, data: str, words: list[str]
):
    httpx_mock.add_response(url=CHIRICO_URL)
    mock_tar_open = mocker.patch("tarfile.open")
    mock_tar_context = mock_tar_open.return_value
    mock_tar = mock_tar_context.__enter__.return_value
    mock_tar.extractfile = mocker.Mock(return_value=BytesIO(data.encode("latin-1")))
    chirico_gen = Words.request_chirico_words()
    reqs = httpx_mock.get_requests()
    assert len(reqs) == 1 and reqs[0].method == "GET" and reqs[0].url == CHIRICO_URL
    assert mock_tar.extractfile.mock_calls == [mocker.call(tar) for tar in TAR_MEMBERS]
    assert [word for word in chirico_gen] == words


@pytest.mark.parametrize("word_src", ALT_WS_PARAMS.values(), ids=ALT_WS_PARAMS.keys())
def test_file_gen_used(mocker: MockerFixture, word_src: str):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=[])
    mock_file = mocker.patch("builtins.open").return_value
    mock_gen = mocker.patch(f"words.Words.request_{word_src}_words")
    mock_file_gen = mocker.patch("words.file_gen")
    Words.get_words(word_src)
    mock_file_gen.assert_called_once_with(mock_gen(), mock_file)


@pytest.mark.parametrize("word_src", ALT_WS_PARAMS.values(), ids=ALT_WS_PARAMS.keys())
def test_alt_reads_file(mocker: MockerFixture, word_src: str):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=[f"{word_src}.words"])
    mock_fileinput = mocker.patch("fileinput.input")
    Words.get_words(word_src)
    mock_fileinput.assert_called_once_with(f"{ALT_WORDS_PATH}/{word_src}.words")


@pytest.mark.parametrize("word_src", ALT_WS_PARAMS.values(), ids=ALT_WS_PARAMS.keys())
def test_alt_strip_lines(mocker: MockerFixture, word_src: str):
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.listdir", return_value=[f"{word_src}.words"])
    mocker.patch("fileinput.input", return_value=["q\n", "w", "e\n"])
    assert [word for word in Words.get_words(word_src)] == ["q", "w", "e"]
