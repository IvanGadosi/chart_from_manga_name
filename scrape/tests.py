from main import MangaGraph, _install_driver
import unittest
import requests
import warnings


@unittest.skipUnless(requests.get("https://manganato.com/").status_code == requests.codes.ok, "Manganato must be online")
class TestMangaGraph(unittest.TestCase):
	def setUp(self):
		self.manga=MangaGraph("Apotheosis")
		self.manga.find_manga()
		warnings.filterwarnings("ignore", message="unclosed", category=ResourceWarning)

	def test_searched_manga_page(self):
		self.assertIn(self.manga.name, self.manga.driver.title)
		self.assertIn("manganato.com/", self.manga.driver.current_url)

	def test_img_src(self):
		self.manga.get_manga_image()
		self.assertIn("https://avt.", self.manga.img_src)

	def test_searched_manga_views(self):
		self.manga.get_manga_data()
		self.assertIs(type(self.manga.manga_views), int)
		self.assertTrue(self.manga.manga_views>=0)

	def test_other_manga_page(self):
		self.manga.get_other_data()
		self.assertTrue(len(self.manga.other_manga_dict)<= 10)
		self.assertIn("Advanced Search", self.manga.driver.title)
		self.assertIn("topview", self.manga.driver.current_url)

	def tearDown(self):
		self.manga.driver.close()
		

if __name__ == '__main__':
	_install_driver()
	unittest.main(argv=[''],verbosity=2)
