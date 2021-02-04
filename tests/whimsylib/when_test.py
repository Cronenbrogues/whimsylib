import unittest
from unittest.mock import call
from unittest.mock import Mock

from whimsylib.globals import G
from whimsylib import when


class WhenTest(unittest.TestCase):
    def setUp(self):
        self._rubadub = Mock()

        @when.when("put the LOTION on LOCATION")
        @when.when("put the LOTION", location="the skin")
        def put_the_lotion(lotion, location):
            self._rubadub.dub(lotion, location)

    def tearDown(self):
        when._CommandHandler._COMMANDS.clear()

    def test_register_with_bad_arguments(self):
        with self.assertRaises(when._InvalidCommand):

            @when.when("gets the HOSE")
            def gets_the_hose():
                pass

    def test_register_with_bad_capitalization(self):
        with self.assertRaises(when._InvalidCommand):

            @when.when("gEtS the HOSE")
            def gets_the_hose():
                pass

    def test_register_with_initial_majuscule(self):
        with self.assertRaises(when._InvalidCommand):

            @when.when("HOSE")
            def hose():
                pass

    def test_handle(self):
        when.handle("put the vaseline on the salty hollow of the bended knee")
        self._rubadub.dub.assert_called_once_with(
            "vaseline", "the salty hollow of the bended knee"
        )

    def test_handle_default(self):
        when.handle("put the vaseline")
        self._rubadub.dub.assert_called_once_with("vaseline", "the skin")

    def test_handle_ignores_case(self):
        when.handle("PUT THE LOTION ON THE SKIN")
        self._rubadub.dub.assert_called_once_with("lotion", "the skin")


class PollTest:
    def setUp():
        self._mock_parent = Mock()
        self._mock_parent.pre = Mock()
        G.add_event(self._mock_parent.pre, "pre")
        self._mock_parent.post = Mock()
        G.add_event(self._mock_parent.post, "post")

    def tearDown():
        G.reset()

    def test_poll_before(self):
        @when.poll(poll_before=True, poll_after=False)
        def wrapped():
            self._mock_parent.mid()

        self._mock_parent.assert_has_calls([call.pre.execute(), call.mid()])

    def test_poll_after(self):
        @when.poll(poll_before=False, poll_after=True)
        def wrapped():
            self._mock_parent.mid()

        self._mock_parent.assert_has_calls([call.mid(), call.post.execute()])

    def test_poll_before_and_after_by_default(self):
        @when.poll()
        def wrapped():
            self._mock_parent.mid()

        self._mock_parent.assert_has_calls(
            [call.pre.execute(), call.mid(), call.post.execute()]
        )
