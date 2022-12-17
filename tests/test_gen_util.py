from pytest_mock import MockerFixture
import pytest

from gen_util import file_iter
from tests.params_gen_util import *


@pytest.mark.parametrize("words", FILE_PARAMS.values(), ids=FILE_PARAMS.keys())
def test_write_and_yield(mocker: MockerFixture, words: list[str]):
    mock_file = mocker.Mock()
    mock_file.write = mocker.Mock()
    mock_file.close = mocker.Mock()
    word_gen = file_iter(lambda: (word for word in words), mock_file)
    assert [word for word in word_gen] == words
    assert mock_file.write.mock_calls == [mocker.call(f"{word}\n") for word in words]
    mock_file.close.assert_called_once()
