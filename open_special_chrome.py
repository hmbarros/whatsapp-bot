import subprocess
import time
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

    def enviar_mensagens(self, contato, nome, mensagem):
        self.driver.get(f"https://web.whatsapp.com/send?phone={contato}&text={mensagem}")

        contato_existente = self.confere_existencia_contato()

        if contato_existente:
            botao_enviar = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Enviar']")
                )
            )

            botao_enviar.click()

            time.sleep(2)
            return "Enviado"
                        

        else:
            return "Não enviado"

    def tratar_telefone(self):
        self.df['CELULAR'] = self.df['CELULAR'].str.replace(r'\D', '', regex=True)

    def confere_existencia_contato(self):
        # 1 - Aguarda aparecer a mensagem da criptografia
        while not self.driver.find_elements(
            By.XPATH,
            "//div[contains(., 'Protegida com a criptografia de ponta a ponta')]"
        ):
            time.sleep(0.1)

        # 2 - Aguarda ela desaparecer
        while self.driver.find_elements(
            By.XPATH,
            "//div[contains(., 'Protegida com a criptografia de ponta a ponta')]"
        ):
            time.sleep(0.1)

        # 3 - Depois que sumiu, espera até 3 segundos pelo logo do WhatsApp
        inicio = time.time()

        while time.time() - inicio < 3:

            if self.driver.find_elements(
                By.XPATH,
                "//span[@data-testid='wa-wordmark-refreshed']"
            ):
                return True

            time.sleep(0.1)

        return False
    
    def salva_excel(self, archive_path):
        self.df.to_excel(archive_path, sheet_name="Pastores", index=False)



if __name__ == "__main__":
    open_chrome_with_auth()