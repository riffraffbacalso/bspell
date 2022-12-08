from pytest_mock import MockerFixture
import pytest

from solve import solve_bee
from tests.params_solve import *

@pytest.mark.parametrize("word_src", WS_PARAMS.values(), ids=WS_PARAMS.keys())
def test_use_word_src(mocker: MockerFixture, word_src: str):
    mock_get_words = mocker.patch("words.Words.get_words")
    solve_bee("problem", word_src)
    mock_get_words.assert_called_once_with(word_src)


@pytest.mark.parametrize("word_list,answers", WL_PARAMS.values(), ids=WL_PARAMS.keys())
def test_valid_words(mocker: MockerFixture, word_list: list[str], answers: list[str]):
    mocker.patch("words.Words.get_words", return_value=word_list)
    assert solve_bee("qwertyu", "") == answers
