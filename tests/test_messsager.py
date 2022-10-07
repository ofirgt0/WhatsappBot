# Workaround to import Messenger
from re import T
import sys
import os
from this import d

import pytest
sys.path.append('../')
from Messenger import *


PHONE_NUMBER = os.environ['PHONE_NUMBER']

class TestClass:
	
	def test_sanity(self):
		x = "this"
		assert "h" in x, 'Sanity Test Failed'

	# Test Objects classes
	def test_list_button(self):
		try:
			btn = List_button('SECTION_1_ROW_1_ID', 'titleMe', 'dicsc1')
		except:
			assert False, 'Invalid List-Button Class Use'
		assert True


	def test_reply_button(self):
		try:
			btn = Reply_button('SECTION_1_ROW_1_ID', 'titleMe')
		except:
			assert False, 'Invalid Reply-Button Class Use'
		assert True
  
	def test_location(self):
		try:
			loc = Location(1.0, 1.0, name='LocationName', address='LocationAddress')
		except:
			assert False, 'Invalid Location Class Use'
		assert True

	def test_media_link(self):
		try:
			media = Media('imageLink', 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png')
		except:
			assert False, 'Invalid Media-link Class Use'
		assert True
  
	def test_media_file(self):
		try:
			media = Media('imageFile', 'tests/test.png')
		except:
			assert False, 'Invalid Media-file Class Use'
		assert True
  
	def test_media_invalid(self):
		try:
			media = Media('imageFile')
		except:
			assert True
			return
		assert False, 'Invalid Media-invalid arguments Class Use'

	def test_section(self):
		try:
			bnt1 = List_button('SECTION_1_ROW_1_ID', 'titleMe', 'dicsc1')
			bnt2 = List_button('SECTION_1_ROW_2_ID', 'titleMe', 'dicsc2')
			Section('Section1', [bnt1, bnt2])
		except:
			assert False, 'Invalid Section Class Use'
		assert True
		
	# Test Sends functions
	@pytest.mark.enable_socket
	def test_send_message(self):
		try:
			response = send_message(phone_number=PHONE_NUMBER, body="Test Message")
			if json.loads(response)['messages'][0]['id']:
				assert True
			else:
				assert False, 'Invalid respond from send message'
		except:
			assert False, 'Send Message Error (probably invalid auth key)'
   
	@pytest.mark.enable_socket
	def test_send_list_message(self):
		try:
			response = send_list_message(phone_number=PHONE_NUMBER, body="Test list message", button_text="Test button", sections=[Section('Section1', [List_button('SECTION_1_ROW_1_ID', 'titleMe', 'dicsc1'), List_button('SECTION_1_ROW_2_ID', 'titleMe', 'dicsc2')])])
			if json.loads(response)['messages'][0]['id']:
				assert True
			else:
				assert False, 'Invalid respond from send message'
		except:
			assert False, 'Send Message list Error (probably invalid auth key)'
   
	@pytest.mark.enable_socket
	def test_send_reply_message(self):
		try:
			bnt1 = Reply_button('SECTION_2_ROW_1_ID', 'titleMe1')
			bnt2 = Reply_button('SECTION_2_ROW_2_ID', 'titleMe2')
			send_reply_message(phone_number=PHONE_NUMBER, body="Test reply message", buttons=[bnt1, bnt2], header='headerit')
		except:
			assert False, 'Send Message reply Error (probably invalid auth key)'
		assert True

	@pytest.mark.enable_socket
	def test_send_location_message(self):
		try:
			loc = Location(latitude=32.061312, longitude=34.791438, name='Hichal Menore', address='Tel Aviv')
			send_location_message(phone_number=PHONE_NUMBER, location=loc)
		except:
			assert False, 'Send Message location Error (probably invalid auth key)'
		assert True

	@pytest.mark.enable_socket
	def test_send_contact_message(self):
		try:
			address1 = Contact_address(street='street', city='city', country='country', zipcode='zip')
			address2 = Contact_address(street='street1', city='city1', country='country1', country_code='country_code')

			email1 = Contact_email(email='asdsad@sda.com')
			email2 = Contact_email(email='2')

			name1 = Contact_name(formatted_name='Omry Zur', first_name='first1', last_name='last1')

			organization1 = Contact_org(department='dep1', title='title1', company='company1')

			phone1 = Contact_phone(phone='0000000001')
			phone2 = Contact_phone(phone='2000000001')

			url1 = Contact_url(url='www.google.com')
			url2 = Contact_url(url='www.google.com', type='work')

			new_contact = Contact(addresses=[address1, address2], emails=[email1, email2], name=name1, org=organization1, phones=[phone1,phone2], urls=[url1, url2])

			send_contacts_message(phone_number=PHONE_NUMBER, contacts=[new_contact])
		except:
			assert False, 'Send Message contact Error (probably invalid auth key)'
		assert True
	
	@pytest.mark.enable_socket
	def test_send_media_message_link(self):
			# PDF test
		try:
			media_document = Media(type='document', link=r'https://example-files.online-convert.com/document/pdf/example.pdf')
			send_media_message(phone_number=PHONE_NUMBER, media=media_document)
		except:
			assert False, 'Send Message media link Error (PDF) (probably invalid auth key)'
		
  		# Video test
		try:
			media_video = Media(type='video', link=r'https://example-files.online-convert.com/video/mp4/example.mp4')
			send_media_message(phone_number=PHONE_NUMBER, media=media_video)
		except:
			assert False, 'Send Message media link Error (Video) (probably invalid auth key)'

		# Sticker test
		try:
			media_sticker = Media(type='sticker', link=r'https://raw.githubusercontent.com/viztushar/stickers-internet/master/emojis2.webp')
			send_media_message(phone_number=PHONE_NUMBER, media=media_sticker)
		except:
			assert False, 'Send Message media link Error (Sticker) (probably invalid auth key)'
	
	@pytest.mark.enable_socket
	def test_send_media_message_file(self):
			# PDF test
		try: #os.path.join
			media_document = Media(type='document', filename=os.path.join('test_files','test.pdf'))
			send_media_message(phone_number=PHONE_NUMBER, media=media_document)
		except:
			assert False, 'Send Message media link Error (PDF) (probably invalid auth key)'
		
		# Video test
		try:
			media_video = Media(type='video', filename=os.path.join('test_files','test.mp4'))
			send_media_message(phone_number=PHONE_NUMBER, media=media_video)
		except:
			assert False, 'Send Message media link Error (Video) (probably invalid auth key)'

		# Sticker test
		try:
			media_sticker = Media(type='sticker', filename=os.path.join('test_files','test.webp'))
			send_media_message(phone_number=PHONE_NUMBER, media=media_sticker)
		except:
			assert False, 'Send Message media link Error (Sticker) (probably invalid auth key)'
