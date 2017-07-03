# Copyright 2017 Ashish Shekar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

from googleapiclient.discovery import build
from pkgutil import iter_modules 
import xml.etree.ElementTree as ET

# constants
WORKING_VALUES_DIR = None

# var related to goslate
DEF_CONFIG_XML_PATH = '/config.xml'
DEF_STRINGS_XML_PATH = None
DEF_LANG = None

# commands
CMD_INSTALL_TRANSLATE = 'pip install --upgrade google-api-python-client'
CMD_CLEAR = 'clear'

# string name array
string_name_array = []

# packages
PKG_TRANSLATE = 'googleapiclient'

def main():

	os.system(CMD_CLEAR)

	# check if googleapiclient is installed
	if not is_pkg_present(PKG_TRANSLATE):
		os.system(CMD_INSTALL_TRANSLATE)
	else:
		print "module(googleapiclient) present - Moving on!"

	# ask path of strings.xml
	DEF_STRINGS_XML_PATH = raw_input('Drag and drop [strings.xml] to translate : ')

	# ask which language you want to translate it to
	DEF_LANG = raw_input('Which language you want to translate it to ? [Two character abbreviation] : ')

	# first we need to tidy up our build env 
	# setup some folders and all
	WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

	# create_folder(WORKING_DIR)

	# now folder is created parse xml
	tree = ET.parse(DEF_STRINGS_XML_PATH)
	root = tree.getroot()

	for child in root:
		# string_name_array.append(child.text)
		translate(get_api_key(WORKING_DIR), DEF_LANG, child.text)



def translate(api_key, lang, text):
	service = build('translate', 'v2',
            developerKey=api_key)
	print(service.translations().list(
      source='en',
      target=lang,
      q=text
    ).execute())


# create values folder for your language
def create_folder(my_dir):
	
	WORKING_VALUES_DIR = get_lang_dir()

	if not os.path.exists(WORKING_VALUES_DIR):
		os.makedirs(WORKING_VALUES_DIR)
		print "created new folder for translations"

# even creating a folder is a drag - for example OS specific slashes
def get_lang_dir(my_dir):
	if sys.platform == 'darwin' or sys.platform == 'linux2':
		return str(my_dir + "/" + "values-" + DEF_LANG)
	else:
		return my_dir + "\\" + "values-" + DEF_LANG

def is_pkg_present(pkg_name):
	return pkg_name in (name for loader, name, ispkg in iter_modules())

def get_api_key(my_dir):
	tree = ET.parse(my_dir + DEF_CONFIG_XML_PATH)
	root = tree.getroot()

	for child in root:
		if child.get('name') == 'key':
			return child.text


if __name__ == '__main__':
	main()