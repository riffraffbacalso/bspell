from pytest_mock import MockerFixture
import pytest

from gen_util import file_gen
from tests.params_gen_util import *


@pytest.mark.parametrize("words", PRINT_PARAMS.values(), ids=PRINT_PARAMS.keys())
def test_write_and_yield(mocker: MockerFixture, words: list[str]):
    mock_file = mocker.Mock()
    mock_file.write = mocker.Mock()
    mock_file.close = mocker.Mock()
    word_gen = file_gen((word for word in words), mock_file)
    assert [word for word in word_gen] == words
    assert mock_file.write.mock_calls == [mocker.call(f"{word}\n") for word in words]
    mock_file.close.assert_called_once()
