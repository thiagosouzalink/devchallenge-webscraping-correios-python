from time import sleep
import sys

from selenium.webdriver import Firefox
from selenium.common.exceptions import (NoSuchElementException,      
                                       ElementNotInteractableException)

from cep.busca_cep import (buscar_cep, 
                           verificar_resultados, 
                           obter_endereco, 
                           realizar_nova_busca, 
                           mostrar_resultado_cep)


# Obtém CEP(s) para serem buscados
print("Informe um ou mais CEPs para serem consultados.")
print("Use virgula ou espaço em branco para separar cada CEP.")
ceps = input("Informe o(s) CEP(s): ")
lista_cep = ceps.replace(',', ' ').split()

# Acessa o site
url = "https://www.correios.com.br/"
browser = Firefox()
browser.get(url)

# Verifica se há pelo menos um cep inserido
if not lista_cep:
    print("Você não digitou nenhum CEP.")
    print("Busca finalizada sem sucesso.")
    sys.exit()

# Realiza a busca automatizada do primeiro CEP
try:
    sleep(3)
    buscar_cep(browser, lista_cep[0])
except NoSuchElementException as e:
    print("Erro: Houve um erro ao carregar a página.")
    print("Busca finalizada sem sucesso.")
else:
    browser.switch_to.window(browser.window_handles[1])

    sleep(5) #
    status, msg = verificar_resultados(browser, lista_cep[0])
    resultado = mostrar_resultado_cep(browser, status, msg)

    # Veriifca se há mais CEPs para serem buscados
    if len(lista_cep) > 1:
        for cep in lista_cep[1:]:
            try:
                realizar_nova_busca(browser, cep)
            except NoSuchElementException as e:
                print("Erro: Houve um erro ao carregar a página.")
                print("Busca encerrada.")
                print(resultado)
                sys.exit()
            except ElementNotInteractableException as e:
                print("Erro: Houve um erro ao carregar a página.")
                print("Busca encerrada.")
                print(resultado)
                sys.exit()
            else:
                sleep(5)
                status, msg = verificar_resultados(browser, cep)
                resultado += mostrar_resultado_cep(browser, status, msg)
    
    # Mostra resultados da busca
    print(resultado)

# Aguarda 5 segundos e fecha o browser
sleep(5)
browser.quit()  
