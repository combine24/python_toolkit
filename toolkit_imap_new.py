import imaplib
import getpass
import email
import datetime
import re

class Imap():
	"""docstring for Imap"""
	def __init__(self, EMAIL_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD):
		self.con = imaplib.IMAP4_SSL(EMAIL_SERVER, port = 993)

		try:
			rv, data = self.con.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
		except imaplib.IMAP4.error:
			print ("LOGIN FAILED!!! ")
			raise
		else:
			print(rv, data)

	def __enter__(self):
		return self

	def __exit__(self,Type, value, traceback):  
		'''
		Executed after "with"
		'''
		print('Close the imap connection')
		self.con.close()

	def get_mail_folder(self):
		rv, mailboxes = self.con.list()
		if rv == 'OK':
			# print("mailboxes:")
			# print(mailboxes)

			# get inbox alias
			print(mailboxes)
			g = lambda i: re.compile(r'(?<=" )(.*)', re.IGNORECASE).findall(i.decode('utf-8'))[0]
			return list(map(g, mailboxes))
			
	def set_mail_read(self, mail_num):
		'''
		Mark mail as read/unread
		'''
		self.con.store(mail_num, '+FLAGS', '\\Seen')
		# Mark as unread
		# self.con.store(mail_num, '-FLAGS', '\\Seen')
	
	def delete_mail(self, mail_num):
		print("Delete mail {}".format(self.get_mail_subject(mail_num)))
		self.con.store(mail_num, '+FLAGS', '\\Deleted')
		self.con.expunge()

	def get_mail_subject(self, mail_num):
		rv, mail_data_bin = self.con.fetch(mail_num, '(RFC822)')
		if rv != 'OK':
			print("ERROR getting message", num)
			return
		# Fetch again if the mail not fetched
		mail_data_raw = mail_data_bin[0][1].decode('utf-8','ignore').replace('\r\n', '\n')
		self.email_message = email.message_from_string(mail_data_raw)
		return self.email_message['Subject']

	def get_mail_num(self, mailFolder):
		'''
		Fetch the mail index in a mail folder
		'''
		# mailFolder = '"{}"'.format(mailFolder)
		print("Processing mailbox {}...\n".format(mailFolder))
		rv, data = self.con.select(mailFolder)
		if rv != 'OK':
			print("ERROR: Unable to open mailbox ", rv)
			return
		rv, data = self.con.search(None, "ALL")
		return data[0].split()

	def empty_mail_folder(self, mailFolder):
		rev_list = imap.get_mail_num(mailbox)
		for mail_num in rev_list:
			# Always delete the first mail
			imap.delete_mail(rev_list[0])

	def walk_mail_folder(self, mailFolder):
		rv, data = self.con.select(mailFolder)
		if rv != 'OK':
			print("ERROR: Unable to open mailbox ", rv)
			return
		print("Processing mailbox {}...\n".format(mailFolder))
		rv, data = self.con.search(None, "ALL")
		
		print(data)
		print('-'*90)
		for mail_num in data[0].split():
			rv, mail_data_bin = self.con.fetch(mail_num, '(RFC822)')
			if rv != 'OK':
				print("ERROR getting message", num)
				return
			# mail_data_raw = mail_data_bin[0][1].decode('utf-8').replace('\r\n', '\n')
			# print(mail_data_raw)
			# self.email_message = email.message_from_string(mail_data_raw)
			print(self.email_message['Subject'])
			# print(email.utils.parseaddr(self.email_message['To']))
			# print(self.email_message.items())
			print('x'*90)
	
	def mark_all_mail_read(self):
		for mailbox in self.get_mail_folder():
			for mail_num in self.get_mail_num(mailbox):
				self.set_mail_read(mail_num)


if __name__ == '__main__':
	config = {
	'EMAIL_SERVER' : 'imap.126.com',
	'EMAIL_ACCOUNT' : 'qqxxxxxx@126.com',
	'EMAIL_PASSWORD' : 'xxxxxxxx'
	}

	with Imap(**config) as imap:
		print(imap.get_mail_folder())
		# imap.walk_mail_folder('&XfJT0ZAB-')
		# imap.mark_all_mail_read()
		for mailbox in imap.get_mail_folder():
		# mailbox = 'Raspberry pi booted'
			imap.empty_mail_folder(mailbox)