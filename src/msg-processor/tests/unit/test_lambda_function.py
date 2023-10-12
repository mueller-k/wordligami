# import pytest


from lambda_function import valid_message_text, convert_wordle_board_to_db_format


class TestMessageProcessor:
    def test_validate_message_text(self):
        valid_message = "Wordle 843 4/6*\n\n🟩⬛🟩⬛⬛\n🟩🟨🟩⬛⬛\n🟩⬛🟩⬛🟩\n🟩🟩🟩🟩🟩"
        invalid_message = "Werdle 843 4/6*\n\n🟩⬛🟩⬛⬛\n🟩🟨🟩⬛⬛\n🟩⬛🟩⬛🟩\n🟩🟩🟩🟩🟩"
        assert valid_message_text(valid_message)
        assert not valid_message_text(invalid_message)

    def test_convert_wordle_board_to_db_format(self):
        wordle_board_raw = ["🟩⬛🟩⬛⬛", "🟩🟨🟩⬛⬛", "🟩⬛🟩⬛🟩", "🟩🟩🟩🟩🟩"]
        wordle_board_db_format = convert_wordle_board_to_db_format(wordle_board_raw)
        assert wordle_board_db_format == "gwgwwgygwwgwgwgggggg"
    
    def test_process_message(self):
        message = ""
        assert 1

