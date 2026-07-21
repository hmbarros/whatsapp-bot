import subprocess
import time
import requests
import pandas as pd
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class open_chrome_with_auth:
    def __init__(self):
        CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        PROFILE_PATH = r"C:\PerfilPersonalizado"
        path =  'teste.xlsx'

        # Abre o Chrome em modo de depuração
        subprocess.Popen([
            CHROME_PATH,
            "--remote-debugging-port=9222",
            f"--user-data-dir={PROFILE_PATH}"
        ])

        # Aguarda o DevTools ficar disponível
        for _ in range(20):
            try:
                requests.get("http://127.0.0.1:9222/json/version", timeout=1)
                break
            except:
                time.sleep(1)
        else:
            raise Exception("Chrome não abriu a porta 9222.")

        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        self.driver = webdriver.Chrome(options=options)

        self.driver.get("https://web.whatsapp.com/")

        while not self.driver.find_elements(
            By.XPATH,
            "//input[@aria-label='Pesquisar ou começar uma nova conversa']"
        ):
            print("Aguardando leitura do QR Code...")
            time.sleep(5)
        
        print('WhatsApp Acessado')

        self.gerenciar_excel(path)

    def gerenciar_excel(self, archive_path):
        self.df = pd.read_excel(archive_path, dtype=str, sheet_name='Pastores')
        self.tratar_telefone()

        message = (
            "Prs IPB - PESQUISA IMPORTANTE.\n\nFavor respondê-la. Muito agradecido!\n\n"
            "https://forms.gle/91WKN9FKHqc59oM29"
        ).replace(' ', '%20').replace('\n', '%0A')

        contador = 0
        N = 10
        for index, row in self.df.iterrows():

            if pd.notna(row["Envio"]) and row["Envio"].strip() != "":
                continue
    
            resultado = self.enviar_mensagens(
                contato=row["CELULAR"],
                nome=row["NOME"],
                mensagem=message
            )
            self.df.at[index, "Envio"] = resultado

            self.salva_excel(archive_path)

            contador += 1

            if contador % N == 0:
                tempo = random.randint(10, 60)  # entre 30 e 90 segundos
                print(f"Pausa de {tempo}s após {contador} envios...")
                time.sleep(tempo)

    def enviar_mensagens(self, contato, nome, mensagem):
        self.driver.get(f"https://web.whatsapp.com/send?phone=+55{contato}&text={mensagem}")

        contato_existente = self.confere_existencia_contato()

        if contato_existente:
            time.sleep(4)
            # botao_enviar = WebDriverWait(self.driver, 20).until(
            #     EC.element_to_be_clickable(
            #         (By.XPATH, "//button[@aria-label='Enviar']")
            #     )
            # )

            # botao_enviar.click()

            #Testando
            campo = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'div[data-testid="conversation-compose-box-input"]')
                )
            )

            campo.click()
            campo.send_keys(Keys.CONTROL, "a")
            campo.send_keys(Keys.BACKSPACE)

            time.sleep(2)
            return "Enviado"
                        

        else:
            return "Não enviado"

    def tratar_telefone(self):
        self.df['CELULAR'] = self.df['CELULAR'].str.replace(r'\D', '', regex=True)

    def confere_existencia_contato(self):
        inicio = time.time()

        while time.time() - inicio < 5:

            # Número inexistente
            if self.driver.find_elements(
                By.XPATH,
                "//div[@data-testid='popup-contents' and contains(., 'não está no WhatsApp')]"
            ):
                return False

            # Conversa carregou
            if self.driver.find_elements(
                By.XPATH,
                "//div[@contenteditable='true'][@data-tab='10']"
            ):
                return True

            time.sleep(0.1)

        return None
    
    def salva_excel(self, archive_path):
        self.df.to_excel(archive_path, sheet_name="Pastores", index=False)



if __name__ == "__main__":
    open_chrome_with_auth()