from pytest_mock import MockerFixture
import pytest

from args import get_args
from tests.params_args import *


@pytest.mark.parametrize("puzzle", P_PARAMS.values(), ids=P_PARAMS.keys())
def test_puzzle_store(mocker: MockerFixture, puzzle: str):
    mocker.patch("sys.argv", ["", puzzle])
    assert get_args().problem == puzzle


@pytest.mark.parametrize("word_src", WS_PARAMS.values(), ids=WS_PARAMS.keys())
def test_word_src_store(mocker: MockerFixture, word_src: str):
    mocker.patch("sys.argv", ["", "-w", word_src] if word_src else [""])
    assert get_args().word_src == word_src if word_src else "OS"


@pytest.mark.parametrize("puzzle", P_ERR_PARAMS.values(), ids=P_ERR_PARAMS.keys())
def test_puzzle_error(mocker: MockerFixture, puzzle: str):
    mocker.patch("sys.argv", ["", puzzle])
    mock_stderr = mocker.patch("sys.stderr")
    with pytest.raises(SystemExit, match="2"):
        get_args()
    assert f"'{puzzle}'" in mock_stderr.mock_calls[1].args[0]


@pytest.mark.parametrize("word_src", WS_ERR_PARAMS.values(), ids=WS_ERR_PARAMS.keys())
def test_word_src_error(mocker: MockerFixture, word_src: str):
    mocker.patch("sys.argv", ["", "-w", word_src])
    mock_stderr = mocker.patch("sys.stderr")
    with pytest.raises(SystemExit, match="2"):
        get_args()
    assert f"'{word_src}'" in mock_stderr.mock_calls[1].args[0]
