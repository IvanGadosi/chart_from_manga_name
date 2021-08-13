from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep

import geckodriver_autoinstaller
import matplotlib.pyplot as plt

from PIL import Image
import requests
from io import BytesIO


class MangaGraph:
	"""
	Finds and prints searched manga data and image in
	comparison with other titles with the same genre
	"""
	def __init__(self, name):
		self.name=name
		self.manga_views=0
		self.other_manga_dict={}
		self.img_src=""

		options=Options()
		options.add_argument("--headless")
		self.driver=webdriver.Firefox(options=options)

		self.manga_names_list=[]
		self.manga_views_list=[]

	def __str__(self):
		return self.name
	
	def find_manga(self):
		self.driver.get("https://manganato.com/")

		self.driver.find_element_by_id("search-story").send_keys("{}".format(self.name))
		self.driver.find_element_by_id("search-story").send_keys(Keys.ENTER)
		sleep(3)
		self.driver.find_element_by_css_selector("div.search-story-item:nth-child(1) > a:nth-child(1)").click()

	def get_manga_image(self):
		self.img_src=self.driver.find_element_by_css_selector(".info-image > img:nth-child(1)").get_attribute("src")

	def get_manga_data(self):
		self.manga_views=int(self.driver.find_element_by_css_selector \
		(".story-info-right-extent > p:nth-child(2) > span:nth-child(2)").text.replace(",", ""))

	def get_other_data(self):
		self.driver.find_element_by_css_selector \
		(".variations-tableInfo > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > a:nth-child(1)").click()
		self.driver.find_element_by_css_selector(".advanced-search-tool-title").click()
		self.driver.find_element_by_css_selector(".advanced-search-tool-orderby-content > option:nth-child(2)").click()
		self.driver.find_element_by_css_selector(".advanced-search-tool-apply").click()

		for i in range(10):
			other_managa_name=self.driver.find_element_by_css_selector \
			("div.content-genres-item:nth-child({}) > div:nth-child(2) > h3:nth-child(1) > a:nth-child(1)" \
			.format(i+1)).get_attribute("title")
			if other_managa_name != self.name:
				other_managa_views=self.driver.find_element_by_css_selector \
				("div.content-genres-item:nth-child({}) > div:nth-child(2) > p:nth-child(3) > span:nth-child(1)" \
				.format(i+1)).text
				self.other_manga_dict[other_managa_name]=int(other_managa_views.replace(",", ""))

	def create_graph(self):
		short_name=lambda x: x if len(x)<=15 else x[:15]+"..."
		self.manga_names_list.append(short_name(self.name))
		self.manga_views_list.append(self.manga_views)

		for key, value in self.other_manga_dict.items():
			self.manga_names_list.append(short_name(key))
			self.manga_views_list.append(value)

		custom_explode=[0 for _ in range(len(self.manga_names_list)-1)]
		custom_explode.insert(0, 0.3)
		fig = plt.figure()
		plt.subplots_adjust(left=0.4)
		plt.pie(self.manga_views_list, explode=custom_explode)
		plt.legend(self.manga_names_list, loc='upper center', bbox_to_anchor=(0.2, 0.1),
          ncol=3, fancybox=True, shadow=True)
		response = requests.get(self.img_src)
		img = Image.open(BytesIO(response.content))
		img.thumbnail((256,256),Image.ANTIALIAS)
		fig.figimage(img, 40, fig.bbox.ymax - img.size[1]-80)
		plt.show()
		self.driver.close()


def _install_driver():
	geckodriver_autoinstaller.install()
	with open("geckodriver.log", "w") as f:
		pass

def main():
	print("Installing driver...")
	_install_driver()

	manga=MangaGraph("Apotheosis")
	print("Looking for {}...".format(manga.name))
	manga.find_manga()
	print("Getting manga image...")
	manga.get_manga_image()
	print("Getting manga data...")
	manga.get_manga_data()
	print("Getting additional data for comparison...")
	manga.get_other_data()
	print("Ploting graph...")
	manga.create_graph()


if __name__ == "__main__":
	main()
