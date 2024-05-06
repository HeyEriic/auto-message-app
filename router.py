import time
from selenium import webdriver
from message import send_message_to_contact
from flask import redirect, render_template, request, url_for
from read_document import read_excel_and_save_to_database
from database.db import count_contacts, count_contacts_with_message_sent_true, get_contacts, update_all_contacts_message_sent_false

def create_routes(app):
	@app.route("/")
	def upload_file():
		num_contacts = count_contacts()
		contacts_sent_true = count_contacts_with_message_sent_true()
		contacts_sent_false = num_contacts - contacts_sent_true
		
		return render_template('upload.html', contacts_count=num_contacts, contacts_sent_true=contacts_sent_true, contacts_sent_false=contacts_sent_false)

	@app.route('/process_file', methods=['POST'])
	def process_file():
		file = request.files['file']
		if file.filename == '':
				return redirect(url_for('upload_file'))

		read_excel_and_save_to_database(file)

		return redirect(url_for('upload_file'))

	@app.route('/send_message', methods=['GET', 'POST'])
	def send_message():
		if request.method == 'POST':
			num_contacts = int(request.form['num_contacts'])
			message = request.form['message']

			# Iniciar o navegador Chrome
			driver = webdriver.Chrome()

			# Carregar o WhatsApp Web
			driver.get("https://web.whatsapp.com")
			print("Por favor, escaneie o código QR com seu telefone.")
			time.sleep(20)

			# Iterar sobre os contatos e enviar mensagens
			contacts = get_contacts()[:num_contacts]
			for contact in contacts:
				contact_id, contact_name, contact_number, message_sent = contact
			
				# Verificar se o número de contato está vazio
				if not contact_number:
					print(f"Número de contato vazio para {contact_name}, pulando para o próximo contato.")
					continue
					
				if message_sent == True:
					print(f"Mensagem já enviada para {contact_name}.")
					continue

				send_message_to_contact(driver, contact_id, contact_name, contact_number, message)

			# Fechar o navegador
			driver.quit()

			return redirect(url_for('upload_file'))
		else:
			# Verificar se há contatos no banco de dados
			num_contacts = count_contacts()
			contacts_sent_true = count_contacts_with_message_sent_true()
			contacts_sent_false = num_contacts - contacts_sent_true

			return render_template('upload.html', num_contacts=num_contacts, contacts_sent_true=contacts_sent_true, contacts_sent_false=contacts_sent_false)
			
	@app.route('/reset_message_sent', methods=['POST'])
	def reset_message_sent():
			update_all_contacts_message_sent_false()
			
			return redirect(url_for('upload_file'))
