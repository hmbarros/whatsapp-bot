import pandas as pd
from sender import SendPersonalizedMessage

class message_sender:
    def __init__(self, arquive_path):
        self.df = pd.read_excel(arquive_path, dtype=str, sheet_name='Pastores')
        self.tratar_telefone()

        print(self.df.head(20))

        message = (
            "Boa noite, pastor, tudo bem?\n\n"
            "Consegui caminhar com o programa para fazer o envio de mensagens aos pastores da listagem que o senhor compartilhou.\n\n"
            "Agora preciso apenas de um texto padrão que o senhor deseja enviar para cada pastor. "
            "Ele pode conter o nome do pastor no meio da mensagem porque eu consigo personalizá-lo do meu lado. Com esse texto, vamos conseguir fazer um teste final e calcular quanto tempo será necessário para concluir todo o envio."
            "Como são muitos pastores, existe a possibilidade de precisarmos realizar os disparos ao longo de alguns finais de semana ou por vários dias, "
            "para evitar que o WhatsApp bloqueie o número.\n\n"
            "De qualquer forma, o programa tem funcionado muito bem. Agora só precisamos alinhar a mensagem e estimar o tempo necessário para finalizar todos os envios.\n\n"
            "Inclusive, esta própria mensagem já foi enviada pelo bot. Ela aparenta ter sido enviada por mim, mas, na verdade, foi o programa que a enviou em meu lugar.\n\nAbraços"
        )

        # self.send_message('19999844586', message, 'Elisa')
        # self.send_message('19998016329', message, 'Otávio')
        self.send_message('19991073927', message, 'Noidy')


    def tratar_telefone(self):
        self.df['CELULAR'] = self.df['CELULAR'].str.replace(r'\D', '', regex=True)


    def send_message(self, celphone, message, name=None):
        service = SendPersonalizedMessage(sender="whatsapp")

        service.send(
            celphone,
            message,
            name,
        )


if __name__ == "__main__":
    path = 'ENDEEREÇO DOS PASTORES DA IPB - Rev Juarez 020626 - Whatsapp.xlsx'
    sender = message_sender(path)