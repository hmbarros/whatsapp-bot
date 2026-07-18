import easyocr

pessoa = 'errado'
leitor = easyocr.Reader(['pt'])
resultado = leitor.readtext(f'{pessoa}.png', detail=0)

if any("não está no WhatsApp" in s for s in resultado):
    print(f'A pessoa {pessoa} não tem este nº no Whatsapp')