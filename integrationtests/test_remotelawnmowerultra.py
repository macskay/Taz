__author__ = 'Max'

from unittest import TestCase
from integrationtests.remotelawnmowerultra import CommandProcessor


class TestRemoteLawnMowerUltra(TestCase):
    def test_string_match_is_looking_at_gnomes(self):
        processor = CommandProcessor()
        self.assertTrue(processor.is_looking_at_gnomes("look at gnome"))
        self.assertTrue(processor.is_looking_at_gnomes("look at gnomes"))
        self.assertTrue(processor.is_looking_at_gnomes("look gnomes"))

    def test_string_match_is_looking_at_tools(self):
        processor = CommandProcessor()
        self.assertTrue(processor.is_looking_at_tools("look at tools"))
        self.assertTrue(processor.is_looking_at_tools("look at pile of tools"))
        self.assertTrue(processor.is_looking_at_tools("look tool"))
        self.assertTrue(processor.is_looking_at_tools("look at tool"))
        self.assertTrue(processor.is_looking_at_tools("look at pile"))
        self.assertTrue(processor.is_looking_at_tools("look pile"))

