import importlib
import unittest
from unittest.mock import call
from unittest.mock import Mock
from unittest.mock import patch

from whimsylib.globals import G
from whimsylib import when


class WhenTest(unittest.TestCase):
    def setUp(self):
        self._rubadub = Mock()

        @when.when("put the LOTION on LOCATION")
        @when.when("put the LOTION", location="the skin")
        def put_the_lotion(lotion, location):
            """Puts the LOTION directly on there."""
            self._rubadub.dub(lotion, location)

    def tearDown(self):
        importlib.reload(when)

    def test_register_with_insufficient_arguments(self):
        with self.assertRaises(when._InvalidCommand):

            @when.when("gets the HOSE")
            def gets_the_hose():
                pass

    def test_register_with_excess_arguments(self):
        with self.assertRaises(when._InvalidCommand):

            @when.when("gets nothin")
            def gets_the_hose(the_hose):
                pass

    def test_register_when_argument_aint_match_placeholder(self):
        with self.assertRaises(when._InvalidCommand):

            @when.when("gets the HOSE")
            def gets_the_hose(whose):
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

    def test_handle_different_order(self):
        it = Mock()

        @when.when("it does TOLD", this="you know what")
        @when.when("it does THIS whenever its TOLD")
        def what_it_does_whenever(this, told):
            it.does(this, told)

        when.handle("it does that whenever its instructed")
        it.does.assert_called_once_with("that", "instructed")

    def test_quit(self):
        with self.assertRaises(KeyboardInterrupt):
            when.handle("exit")

    def test_exit(self):
        with self.assertRaises(KeyboardInterrupt):
            when.handle("quit")

    @patch("whimsylib.when.say.insayne")
    def test_help_and_theys_always_help_exit_and_quit_commands(self, q_lazzarus):
        when.handle("help")
        # TODO: Sort; any_order=False.
        q_lazzarus.assert_has_calls(
            [
                call("help: Prints this help message."),
                call("put the LOTION on LOCATION: Puts the LOTION directly on there."),
                call("put the LOTION: Puts the LOTION directly on there."),
                call("quit"),
                call("exit"),
            ],
            any_order=True,
        )

    @patch("whimsylib.when.say.insayne")
    def test_help_without_a_docstring(self, q_lazzarus):
        @when.when("goodbye horses")
        def no_docstring():
            pass

        when.handle("help")
        q_lazzarus.assert_called_with("goodbye horses")


class PollTest(unittest.TestCase):
    def setUp(self):
        self._mock_parent = Mock()
        self._mock_parent.pre = Mock()
        G.add_event(self._mock_parent.pre, "pre")
        self._mock_parent.post = Mock()
        G.add_event(self._mock_parent.post, "post")

    def tearDown(self):
        G.reset()

    def test_poll_before(self):
        @when.poll(poll_before=True, poll_after=False)
        def wrapped():
            self._mock_parent.mid()

        wrapped()
        self._mock_parent.assert_has_calls([call.pre.execute(), call.mid()])

    def test_poll_after(self):
        @when.poll(poll_before=False, poll_after=True)
        def wrapped():
            self._mock_parent.mid()

        wrapped()
        self._mock_parent.assert_has_calls([call.mid(), call.post.execute()])

    def test_poll_before_and_after_by_default(self):
        @when.poll()
        def wrapped():
            self._mock_parent.mid()

        wrapped()
        self._mock_parent.assert_has_calls(
            [call.pre.execute(), call.mid(), call.post.execute()]
        )
