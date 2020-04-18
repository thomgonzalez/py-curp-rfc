# -*- coding: utf-8 -*-
import datetime
from .utils import (
	ENT_FED, WORDS, to_upper,
	remove_names, search_vowel, search_consonant
)


class BaseGenerator(object):
	"""class Base Generator"""
	def generate(self):
		raise NotImplementedError('No implement.')

	def parse(self, complete_name, last_name, mother_last_name=None, city=None,
		state_code=None):
		if city is not None:
			self.city = to_upper(city)
		if state_code is not None:
			self.state_code = to_upper(state_code)
		if mother_last_name is not None:
			self.mother_last_name = to_upper(mother_last_name)
		self.complete_name = to_upper(complete_name)
		self.complete_name = remove_names(self.complete_name)
		self.last_name = to_upper(last_name)
		
	def data_fiscal(self, complete_name, last_name, mother_last_name, birth_date):
		birth_date = self.parse_date(birth_date)

		first_name = self.remove_precisions(self.complete_name)
		last_name = self.remove_precisions(self.last_name)
		mother_last_name = self.remove_precisions(self.mother_last_name)

		last_name = self.remove_articles(last_name)
		if len(last_name) is 1 or len(last_name) is 2:
			initials = self.initials_name_comp(first_name, last_name, mother_last_name)
		else:
			initials = self.initials_name(first_name, last_name, mother_last_name)
		print(initials)

		completename = self.verify_words(initials)
		
		return '%s%s' % (completename, birth_date)
		
	def initials_name(self, first_name, last_name, mother_last_name):
		"""Rule 1 - The key is integrated with the following data:

		1.- The first letter of the father's last name and the next first vowel of the same.
		2.- The first letter of the mother's last name.
		3.- The first letter of the name.
		"""
		
		ini_last_name = last_name[0:1]
		last_name_vowel = search_vowel(last_name)
		ini_mothlast_name = self.get_ini_mothlast_name(mother_last_name)
		ini_first_name = first_name[0:1]

		# Rule 5
		# When the paternal or maternal surname are composed, the first word that corresponds
		# to any of them will be taken for the classification.
		# Dolores San Martín Dávalos SADD-180812
		# Mario Sánchez de la Barquera Gómez SAGM-190224
		# Antonio Jiménez Ponce de León JIPA-170808

		initials = '%s%s%s%s' % (
			ini_last_name, 
			last_name_vowel, 
			ini_mothlast_name, 
			ini_first_name
		)
		return initials

	def remove_precisions(self, phrase):
		""" Rule 3 - When the initial letter of any of the surnames or first names is composed,
		only its initial will be noted. In Ch la C and in Ll la L.

		For example:
			Manuel Chávez González CAGM-240618
			Felipe Camargo Llamas CALF-450228
			Charles Kennedy Truman KETC-511012
		"""
		letters = phrase[0:2]
		data = phrase[2:len(phrase)]
		
		if letters == 'CH':
			phrase = 'C%s' % data
		elif letters == 'LL':
			phrase = 'L%s' % data
		return phrase


	def remove_articles(self, last_name):
		"""
		Replace all the occurrences of string in list by AA in the main list 
		"""
		toBeReplaces = ['DE', 'DEL', 'LA','LOS', 'LAS', 'Y', 'MC', 'MAC', 'VON', 'VAN', 'DE LA']
		# Iterate over the strings to be replaced
		for elem in toBeReplaces :
			# Check if string is in the main string
			if elem in last_name :
				# Replace the string
				last_name = last_name.replace(elem, '').strip()
		return last_name 



	def get_ini_mothlast_name(self, mother_last_name):
		"""	The first letter of the mother's last name.
		"""
		return 'X' if mother_last_name is None else mother_last_name[0:1]


	def initials_name_comp(self, first_name, last_name, mother_last_name):
		"""Rule 4 - In cases where the paternal surname of the natural person
			is made up of one or two letters, the password will be formed as follows:

			1.- The first letter of the paternal surname.
			2.- The first letter of the mother's last name.
			3.- The first and second letters of the name.

		For example:
			Alvaro de la O Lozano 	OLAL-401201
			Ernesto Ek Rivera 	ERER-071120
		"""
		ini_last_name = last_name[0:1]
		ini_mthlast_name = self.get_ini_mothlast_name(mother_last_name)
		data = "{}{}{}".format(ini_last_name, ini_mthlast_name, first_name[0:2])
	 	return data  


	def verify_words(self, rfc):
		for item in WORDS:
			if item == rfc:
				rfc = 'XXXX'
				break
		return rfc

	def parse_date(self, birthdate):
		"""Rule 2 - The taxpayer's date of birth will be noted below, in the following order:

		1. Year: The last two figures will be taken, writing them in Arabic numerals.
		2.- Month: The month of birth will be taken in its order number, in a calendar year,
			writing it with Arabic numbers.
		3.- Day: It will be written in Arabic numerals.

		Args:
			birthdate: The first parameter.

		Returns:
		As a result we will have the numerical expression: 070401
		"""
		try:
			dtype = type(birthdate)
			if birthdate is None:
				birthdate = datetime.datetime.today()
			else:
				if not (dtype is datetime.datetime or dtype is datetime.date):
					birthdate = datetime.datetime.strptime(birthdate, '%d-%m-%Y').date()
			
			year = str(birthdate.year)
			year = year[2:4]
			# When in the year, month or day, of the date of birth, only one figure appears,
			# a ZERO will be put before it.
			month = str(birthdate.month).zfill(2)
			day = str(birthdate.day).zfill(2)
			return '%s%s%s' % (year, month, day)
		except Exception as exc:
			raise str(exc)

	def city_search(self, name_city):
		data = ''	
		for key, value in ENT_FED.items():
			if key == name_city:
				data = value
		return data

	def get_consonante(self, word):
		return search_consonant(word)

	def get_year(self, str_date):
		"""Get year of birth date."""
		try:
			if str_date is None:
				date = datetime.datetime.today()
			else:
				date = datetime.datetime.strptime(str_date, '%d-%m-%Y').date()
			return date.year
		except Exception as exc:
			raise str(exc)

	def current_year(self):
		return datetime.datetime.now().year
		