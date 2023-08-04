import os
import unittest

if 'test_url' in os.environ:
    url = os.environ['test_url']
else:
    url = '/youtube.com/c/ABCNews/live'
sample = '474011'


class TestCases(unittest.TestCase):

    def probe(self, args, count):
        '''Make actual query to the service. Redefined in child class'''
        pass

    def test_video(self):
        '''Get video stream by implicit parameter'''
        args = url
        self.assertTrue(self.probe(args, len(sample)//2).hex() == sample)

    def test_formats(self):
        '''Check for available formats (worst ... best)'''
        args = url + '?--list-formats'
        self.assertTrue('Available formats for ' in self.probe(args, None).decode())

    def test_help(self):
        '''Pull out long help message'''
        args = '?--help'
        self.assertTrue('Usage: yt-dlp ' in self.probe(args, None).decode())
