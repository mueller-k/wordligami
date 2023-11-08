from lambda_function import (
    convert_wordle_board_to_db_format,
    decode_message,
    get_wordligami_result,
    message_contains_wordle_submission,
    parse_message,
)


class TestMessageProcessor:
    def test_validate_message_text(self):
        valid_message = decode_message("Wordle 843 4/6*\n\n🟩⬛🟩⬛⬛\n🟩🟨🟩⬛⬛\n🟩⬛🟩⬛🟩\n🟩🟩🟩🟩🟩")
        invalid_message = decode_message(
            "Werdle 843 4/6*\n\n🟩⬛🟩⬛⬛\n🟩🟨🟩⬛⬛\n🟩⬛🟩⬛🟩\n🟩🟩🟩🟩🟩"
        )
        invalid_message_2 = "2 Kyle 2 Wordle"
        assert message_contains_wordle_submission(valid_message)
        assert not message_contains_wordle_submission(invalid_message)
        assert not message_contains_wordle_submission(invalid_message_2)

    def test_convert_wordle_board_to_db_format(self):
        wordle_board = [
            decode_message(row) for row in ["🟩⬛🟩⬛⬛", "🟩🟨🟩⬛⬛", "🟩⬛🟩⬛🟩", "🟩🟩🟩🟩🟩"]
        ]
        wordle_board_db_format = convert_wordle_board_to_db_format(wordle_board)
        assert wordle_board_db_format == "gwgwwgygwwgwgwgggggg"

    def test_process_message(self):
        assert 1

    def test_parse_message(self):
        wordle_board_message_1 = "Wordle 869 4/6*\n\n⬛🟨🟩⬛🟩\n⬛⬛🟩🟩🟩\n⬛🟩🟩🟩🟩\n🟩🟩🟩🟩🟩"
        wordle_board_message_2 = "Wordle 872 4/6*\n\n⬛🟨🟩⬛🟩\n⬛⬛🟩🟩🟩\n⬛🟩🟩🟩🟩\n🟩🟩🟩🟩🟩wboviewj"

        board_1, board_number_1 = parse_message(decode_message(wordle_board_message_1))
        board_2, board_number_2 = parse_message(decode_message(wordle_board_message_2))

        expected_board_1 = [
            "\\u2b1b\\U0001f7e8\\U0001f7e9\\u2b1b\\U0001f7e9",
            "\\u2b1b\\u2b1b\\U0001f7e9\\U0001f7e9\\U0001f7e9",
            "\\u2b1b\\U0001f7e9\\U0001f7e9\\U0001f7e9\\U0001f7e9",
            "\\U0001f7e9\\U0001f7e9\\U0001f7e9\\U0001f7e9\\U0001f7e9",
        ]

        assert board_1 == expected_board_1
        assert board_number_1 == "869"
        assert board_2 == expected_board_1
        assert board_number_2 == "872"

    def test_get_wordligami_result(self):
        wordle_board = [
            decode_message(row) for row in ["🟩⬛🟩⬛⬛", "🟩🟨🟩⬛⬛", "🟩⬛🟩⬛🟩", "🟩🟩🟩🟩🟩"]
        ]

        result = get_wordligami_result(wordle_board)
        assert result == {
            "matches": [
                {
                    "board": "gwgwwgygwwgwgwgggggg",
                    "board_number": "843",
                    "user_id": "57821028",
                }
            ],
            "wordligami": False,
        }
