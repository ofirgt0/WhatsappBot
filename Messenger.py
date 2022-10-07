from typing import List
import requests
import json
import os
# Get new Auth TOKEN
# https://developers.facebook.com/apps/1914132042109760/whatsapp-business/wa-dev-console/?business_id=543237437287046

META_AUTH_TOKEN = 'EAAKkiM6wG4kBADqgvyR1t1x1VBenlP2W2EpOedOlGG8CuE2ZBrnQOu267dw8srstGtRtymMsnT9300YAkWq62L1e8ZCaRX9LTdfGdsCoo1LZBOSasiQgSljtXts6kQvuAADmKxvDtMkzy9EgAnle3Y9CMAOmgDlQbMQd5MxGojnJ6jhKIGZAOIprSsl2zW9Eq1WRXOtbuAZDZD'#os.environ['META_AUTH_TOKEN']
META_PHONE_ID = '104919479023325'#os.environ['META_PHONE_ID']
PHONE_NUMBER = '972502113342'#os.environ['PHONE_NUMBER']

BASE_URL = 'https://graph.facebook.com/v13.0/' + META_PHONE_ID + '/'


class List_button: 
	"""_summary: Button object used for list messages

	"""
	def __init__(self, btn_id: str, title: str, description: str):
		"""_summary_ Constructor for List_button

		Args:
			btn_id (string): used to identify the button (for parsing with webhook)
			title (string): title of the button
			description (string): description of the button
		"""
		self.btn_id = btn_id
		self.title = title
		self.description = description


class Reply_button:  # button reply message of "interactive message"
	"""_summary_ Button object with that sending automatic reply when clicked
	"""
	def __init__(self, btn_id: str, title: str):
		"""_summary_ Constructor for Reply_button

		Args:
			btn_id (string): used to identify the button (for parsing with webhook)
			title (string): title of the button
		"""
		self.btn_id = btn_id
		self.title = title


class Section:  # Section of title and buttons in "interactive message"
	"""_summary_ Section object used for interactive messages composed from title and buttons
	"""
	def __init__(self, title: str, buttons: List[List_button]):
		"""_summary_ Constructor for Section

		Args:
			title (string): title of the section
			buttons (List[List_button]): list of buttons to be displayed in the section
		"""
		self.title = title
		self.buttons = buttons


class Location:
	"""_summary_ Location object used for sending messages with location
	"""
	def __init__(self, latitude: float, longitude: float, name: str = None, address: str = None):
		"""_summary_

		Args:
			latitude (float): latitude of the location
			longitude (float): longitude of the location
			name (string, optional): name of the location. Defaults to None.
			address (string, optional): address of the location. Defaults to None.
		"""
		self.longitude = latitude
		self.latitude = longitude
		self.name = name
		self.address = address

#https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#supported-media-types

class Media:
	"""_summary_ Media object used for sending media messages"""	
	def __init__(self, type: str, link: str = None, filename: str = None):
		"""_summary_ Constructor for Media object

		Args:
			type (string): type of the media (image, video, audio, document)
			link (string, optional): direct link to media. Defaults to None.
			filename (string, optional): path to file on local machine. Defaults to None.

		Raises:
			Exception: if both link and filename are None
		"""
		self.type = type
		if not link and not filename:
			raise Exception('Either link or filename must be provided')

		if link:
			self.link = link
		else:
			self.filename = filename
			self.set_mime_type()
			self.uploadMedia()

 
	def set_mime_type(self):
		"""_summary_ Set mime type of the media based on the file extension
		"""
		if self.filename.split('.')[-1] == 'png':
			self.mime_type = 'image/png'
		elif self.filename.split('.')[-1] == 'pdf':
			self.mime_type = 'application/pdf'
		elif self.filename.split('.')[-1] == 'mp4':
			self.mime_type = 'video/mp4'
		elif self.filename.split('.')[-1] == 'mp3':
			self.mime_type = 'audio/mp3'
		elif self.filename.split('.')[-1] == 'wav':
			self.mime_type = 'audio/wav'
		elif self.filename.split('.')[-1] == 'ogg':
			self.mime_type = 'audio/ogg'
		elif self.filename.split('.')[-1] == 'webm':
			self.mime_type = 'video/webm'
		elif self.filename.split('.')[-1] == 'gif':
			self.mime_type = 'image/gif'
		elif self.filename.split('.')[-1] == 'jpeg':
			self.mime_type = 'image/jpeg'
		elif self.filename.split('.')[-1] == 'jpg':
			self.mime_type = 'image/jpg'
		elif self.filename.split('.')[-1] == 'webp':
			self.mime_type = 'image/webp'
		else:
			self.mime_type = 'raw'
   
	def uploadMedia(self):
		"""_summary_ Upload media to facebook servers and set object id to the one got back from the server
		"""
		url = BASE_URL + 'media'

		payload = {'messaging_product': 'whatsapp'}
		files = [
			('file', (self.filename.split('\\')[-1], open(self.filename, 'rb'), self.mime_type))
		]
		headers = {
			'Authorization': 'Bearer ' + META_AUTH_TOKEN
		}

		# TBD: handle error if upload failed (500)
		response = requests.request('POST', url, headers=headers, data=payload, files=files)

		# Parse response to get id
		response_json = json.loads(response.text)
		self.id = response_json['id']

	def toPayload(self):
		"""_summary_ Convert media object to payload as json

		Returns:
			{dict}: payload as json format
		"""
		payload = {}
		if hasattr(self, 'id'):  # if id is provided, use it to send media
			payload['media'] = {'id': self.id}
		else:  # Use link to send media
			payload['media'] = {'link': self.link}

		return payload


class Contact_address:
	"""_summary_ Contact address object used for Contact object
	"""
	def __init__(self, street: str = None, city: str = None, state: str = None, zipcode: str = None, country: str = None, country_code: str = None, type: str = None):
		"""_summary_

		Args:
			street (string, optional): Street number and name. Defaults to None.
			city (string, optional): City name. Defaults to None.
			state (string, optional): State abbreviation. Defaults to None.
			zipcode (string, optional): ZIP code. Defaults to None.
			country (string, optional):  Full country name. Defaults to None.
			country_code (string, optional): Two-letter country abbreviation. Defaults to None.
			type (string, optional): Standard values are HOME and WORK. Defaults to None.
		"""
		self.street = street
		self.city = city
		self.state = state
		self.zipcode = zipcode
		self.country = country
		self.country_code = country_code
		self.type = type

	def toPayload(self):
		"""_summary_ Convert contact address object to payload as json

		Returns:
			{dict} : payload as json format
		"""
		if not self.street and not self.city and not self.state and not self.zipcode and not self.country and not self.country_code and not self.type:
			return None
		payload = {}
		if self.street:
			payload['street'] = self.street
		if self.city:
			payload['city'] = self.city
		if self.state:
			payload['state'] = self.state
		if self.zipcode:
			payload['zip'] = self.zipcode
		if self.country:
			payload['country'] = self.country
		if self.country_code:
			payload['country_code'] = self.country_code
		if self.type:
			payload['type'] = self.type
		return payload


class Contact_name:
	"""_summary_ Contact name object used for Contact object
	"""
	def __init__(self, formatted_name: str , first_name: str = None, last_name: str = None, middle_name: str = None, prefix: str = None, suffix: str = None):
		"""_summary_
  
		Args:
			formatted_name (string):  Full name, as it normally appears.
			first_name (string, optional): First name. Defaults to None.
			last_name (string, optional): Last name. Defaults to None.
			middle_name (string, optional): Middle name. Defaults to None.
			prefix (string, optional): Name prefix. Defaults to None.
			suffix (string, optional): Name suffix. Defaults to None.
  		"""
		self.formatted_name = formatted_name
		self.first_name = first_name
		self.last_name = last_name
		self.middle_name = middle_name
		self.prefix = prefix
		self.suffix = suffix

	def toPayload(self):
		"""_summary_ Convert contact name object to payload as json

		Returns:
			{dict} : payload as json format
		"""
		payload = {"formatted_name": self.formatted_name}
		if self.first_name is not None:
			payload["first_name"] = self.first_name
		if self.last_name is not None:
			payload["last_name"] = self.last_name
		if self.middle_name is not None:
			payload["middle_name"] = self.middle_name
		if self.prefix is not None:
			payload["prefix"] = self.prefix
		if self.suffix is not None:
			payload["suffix"] = self.suffix
		return payload


class Contact_org:
	"""_summary_ Contact organization object used for Contact object
	"""
	def __init__(self, company: str = None, department: str = None, title: str = None):
		"""_summary_

		Args:
			company (string, optional): Name of the contact's company. Defaults to None.
			department (string, optional): Name of the contact's department. Defaults to None.
			title (string, optional): Contact's business title. Defaults to None.
		"""
		self.company = company
		self.department = department
		self.title = title

	def toPayload(self):
		"""_summary_ Convert contact org object to payload as json

		Returns:
			{dict} : payload as json format
		"""
		if not self.company and not self.department and not self.title:
			return None
		payload = {}
		if self.company:
			payload['company'] = self.company
		if self.department:
			payload['department'] = self.department
		if self.title:
			payload['title'] = self.title
		return payload


class Contact_phone:
	"""_summary_ Contact phone object used for Contact object
	"""
	def __init__(self, phone: str = None, type: str = None, wa_id: str = None):
		"""_summary_

		Args:
			phone (string, optional): Phone number, can be automatically populated with the `wa_id` value as a formatted phone number. Defaults to None.
			type (string, optional):  Standard Values are CELL, MAIN, IPHONE, HOME, and WORK. Defaults to None.
			wa_id (string, optional): WhatsApp ID. Defaults to None.
		"""
		self.phone = phone
		self.type = type
		self.wa_id = wa_id

	def toPayload(self):
		"""_summary_ Convert contact phone object to payload as json

		Returns:
			{dict} : payload as json format
		"""
		if not self.phone and not self.type and not self.wa_id:
			return None
		payload = {}
		if self.phone:
			payload['phone'] = self.phone
		if self.type:
			payload['type'] = self.type
		if self.wa_id:
			payload['wa_id'] = self.wa_id
		return payload


class Contact_url:
	"""_summary_ Contact url object used for Contact object
	"""
	def __init__(self, url: str = None, type: str = None):
		"""_summary_

		Args:
			url (string, optional): URL. Defaults to None.
			type (string, optional): Standard values are HOME and WORK. Defaults to None.
		"""
		self.url = url
		self.type = type

	def toPayload(self):
		"""_summary_ Convert contact url object to payload as json

		Returns:
			{dict} : payload as json format
		"""
		if not self.url and not self.type:
			return None
		payload = {}
		if self.url:
			payload['url'] = self.url
		if self.type:
			payload['type'] = self.type
		return payload


class Contact_email:
	"""_summary_ Contact email object used for Contact object
	"""
	def __init__(self, email: str = None, type: str = None):
		"""_summary_

		Args:
			email (string, optional):  Email address. Defaults to None.
			type (string, optional): Standard values are HOME and WORK. Defaults to None.
		"""
		self.email = email
		self.type = type

	def toPayload(self):
		"""_summary_ Convert contact email object to payload as json

		Returns:
			{dict} : payload as json format
		"""
		if not self.email and not self.type:
			return None
		payload = {}
		if self.email:
			payload['email'] = self.email
		if self.type:
			payload['type'] = self.type
		return payload


class Contact:
	"""_summary_ Contact object used for sending messages with contact card
	"""
	def __init__(self, name: Contact_name, addresses: List[Contact_address] = None, birthday: str = None, emails: List[Contact_email] = None, org: Contact_org = None, phones: List[Contact_phone] = None,
				 urls: List[Contact_url] = None):
		"""_summary_

		Args:
			name (Contact_name): Full contact name
			addresses (Contact_address, optional): Full contact address(es) [can be a list of Contact_address]. Defaults to None.
			birthday (string, optional): YYYY-MM-DD formatted string.. Defaults to None.
			emails (Contact_email, optional): Contact email address(es) [can be a list of Contact_emails]. Defaults to None.
			org (Contact_org, optional): Contact organization information. Defaults to None.
			phones (Contact_phone, optional): Contact phone number(s) [can be a list of Contact_phone]. Defaults to None.
			urls (Contact_url, optional): Contact URL(s) [can be a list of Contact_url]. Defaults to None.
		"""
		self.name = name
		self.addresses = addresses
		self.birthday = birthday
		self.emails = emails
		self.org = org
		self.phones = phones
		self.urls = urls

	def toPayload(self):
		"""_summary_ Convert contact object to payload as json

		Returns:
			{dict}: payload as json format
		"""
		payload = {'name': self.name.toPayload()}

		if self.addresses:
			if isinstance(self.addresses, list):
				payload['addresses'] = [address.toPayload() for address in self.addresses]
			else:
				payload['addresses'] = self.addresses.toPayload()

		if self.birthday:
			payload['birthday'] = self.birthday
		if self.emails:
			if isinstance(self.emails, list):
				payload['emails'] = [email.toPayload() for email in self.emails]
			else:
				payload['emails'] = self.emails.toPayload()

		if self.org:
			payload['org'] = self.org.toPayload()
		if self.phones:
			if isinstance(self.phones, list):
				payload['phones'] = [phone.toPayload() for phone in self.phones]
			else:
				payload['phones'] = self.phones.toPayload()
		if self.urls:
			if isinstance(self.urls, list):
				payload['urls'] = [url.toPayload() for url in self.urls]
			else:
				payload['urls'] = self.urls.toPayload()
		return payload


def send_message(phone_number: str, body: str):
	"""_summary_ Send message to phone number

	Args:
		phone_number (string): Phone number with country code
		body (string): Message body

	Returns:
		string: Response from API server
	"""
	url = BASE_URL + 'messages'

	payload = json.dumps({
		'messaging_product': 'whatsapp',
		'recipient_type': 'individual',
		'to': phone_number,
		'type': 'text',
		'text': {
			'preview_url': 'false',
			'body': body
		}
	})
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + META_AUTH_TOKEN
	}

	response = requests.request('POST', url, headers=headers, data=payload)

	return response.text


def send_list_message(phone_number: str, body: str, button_text: str, sections: List[Section], header: str = '', footer: str = ''):
	"""_summary_ Send message with list of buttons to phone number

	Args:
		phone_number (string): Phone number with country code
		body (string): Message body
		button_text (string): Text displayed on the button
		sections (List[Section]): List of sections
		header (str, optional): header text for message. Defaults to ''.
		footer (str, optional): footer text for message. Defaults to ''.

	Returns:
		string: Response from API server
	"""
	url = BASE_URL + 'messages'
	interactive_payload = {'interactive': {'type': 'list'}}

	# Add header if exist
	if header:
		interactive_payload['interactive']['header'] = {'type': 'text', 'text': header}

	# Add body to message
	interactive_payload['interactive']['body'] = {"text": body}

	# Add footer if exist
	if footer:
		interactive_payload['interactive']['footer'] = {'text': header}

	#
	interactive_payload['interactive']['action'] = {'button': button_text, 'sections': []}

	# Add the sections with the buttons
	section_id = 0
	for section in sections:
		interactive_payload['interactive']['action']['sections'].append({'title': section.title, 'rows': []})
		for button in section.buttons:
			interactive_payload['interactive']['action']['sections'][section_id]['rows'].append(
				{'id': button.btn_id, 'title': button.title, 'description': button.description})
		section_id += 1

	payload = json.dumps({
		'messaging_product': 'whatsapp',
		'recipient_type': 'individual',
		'to': phone_number,
		'type': 'interactive',
		'interactive': interactive_payload['interactive']
	})

	print(payload)

	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + META_AUTH_TOKEN
	}

	response = requests.request('POST', url, headers=headers, data=payload)

	return response.text


def send_reply_message(phone_number: str, body: str, buttons: List[Reply_button], header: str = '', footer: str = ''):
	"""_summary_ Send message with reply buttons to phone number

	Args:
		phone_number (str): Phone number with country code
		body (str): Message body
		buttons (List[Reply_button]): List of reply buttons
		header (str, optional): header text for message. Defaults to ''.
		footer (str, optional): footer text for message. Defaults to ''.

	Returns:
		str: Response from API server
	"""
	url = BASE_URL + 'messages'
	interactive_payload = {'interactive': {'type': 'button'}}

	# Add header if exist
	if header:
		interactive_payload['interactive']['header'] = {'type': 'text', 'text': header}

	# Add body to message
	interactive_payload['interactive']['body'] = {"text": body}

	# Add footer if exist
	if footer:
		interactive_payload['interactive']['footer'] = {'text': header}

	interactive_payload['interactive']['action'] = {'buttons': []}

	# Add the reply buttons
	for button in buttons:
		interactive_payload['interactive']['action']['buttons'].append({'type': 'reply', 'reply': {'id': button.btn_id,
																								   'title': button.title}})

	payload = json.dumps({
		'messaging_product': 'whatsapp',
		'recipient_type': 'individual',
		'to': phone_number,
		'type': 'interactive',
		'interactive': interactive_payload['interactive']
	})

	print(payload)

	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + META_AUTH_TOKEN
	}

	response = requests.request('POST', url, headers=headers, data=payload)

	return response.text


def send_location_message(phone_number: str, location: Location):
	"""_summary_ Send message with location to phone number

	Args:
		phone_number (str): Phone number with country code
		location (Location): Location object

	Returns:
		str: Response from API server
	"""
	url = BASE_URL + 'messages'

	location_payload = {'location': {'latitude': location.latitude, 'longitude': location.longitude}}
	if location.name:
		location_payload['location']['name'] = location.name
	if location.address:
		location_payload['location']['address'] = location.address

	payload = json.dumps({
		'messaging_product': 'whatsapp',
		'recipient_type': 'individual',
		'to': phone_number,
		'type': 'location',
		'location': location_payload['location']
	})
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + META_AUTH_TOKEN
	}

	response = requests.request('POST', url, headers=headers, data=payload)

	return response.text


def send_contacts_message(phone_number: str, contacts: List[Contact]):  # contacts: list of Contact
	"""_summary_ Send message with contacts to phone number

	Args:
		phone_number (str): Phone number with country code
		contacts (List[Contact]): List of contacts

	Returns:
		str: Response from API server
	"""
	url = BASE_URL + 'messages'

	contacts_paylaod = {'contacts': []}
	for contact in contacts:
		contacts_paylaod['contacts'].append(contact.toPayload())  # contact: Contact

	payload = json.dumps({
		'messaging_product': 'whatsapp',
		'recipient_type': 'individual',
		'to': phone_number,
		'type': 'contacts',
		'contacts': contacts_paylaod['contacts']
	})
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + META_AUTH_TOKEN
	}

	response = requests.request('POST', url, headers=headers, data=payload)

	return response.text


def send_media_message(phone_number: str, media: Media):
	"""_summary_ Send message with media to phone number

	Args:
		phone_number (str): Phone number with country code
		media (Media): Media object

	Returns:
		str: Response from API server
	"""
	url = BASE_URL + 'messages'

	# TBD: fix this to use payload from Media class
	media_payload = media.toPayload()

	payload = json.dumps({
		'messaging_product': 'whatsapp',
		'recipient_type': 'individual',
		'to': phone_number,
		'type': media.type,
		media.type: media_payload['media']
		#media.type: {
			# 'id': media.id
			#'link': 'https://i.imgur.com/dLSARUC.png'
		#}
	})
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + META_AUTH_TOKEN
	}

	response = requests.request('POST', url, headers=headers, data=payload)

	return response.text
	

def main():
    send_message(PHONE_NUMBER,'HEYYYY');

if __name__ == "__main__":
    main()