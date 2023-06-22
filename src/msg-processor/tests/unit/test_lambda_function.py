import pytest


from lambda_function import process_event


class TestMessageProcessor:
    event = {"Detail": "Event details."}

    def test_process_event(self):
        process_event(self.event)
