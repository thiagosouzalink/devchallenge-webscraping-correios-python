from time import sleep

from selenium.common.exceptions import (NoSuchElementException,      
                                       ElementNotInteractableException)


def buscar_cep(browser, cep):
    """ Realiza a busca do CEP informado.
    
    Args:
        browser: Instâcia do browser.
        cep: CEP para ser buscado.
    """
    entrada_cep = browser.find_element_by_id("relaxation")
    boxes = browser.find_elements_by_class_name("card-mais-acessados")
    busca = boxes[1].find_element_by_class_name("bt-link-ic")
    sleep(1.5)
    entrada_cep.send_keys(cep)
    sleep(1.5)
    busca.click()


def verificar_resultados(browser, cep):
    """ Verifica o resultado da busca do CEP.

    Args:
        browser: Instâcia do browser.
        cep: CEP a ser buscado
    Returns:
        Tupla contendo como elementos, respectivamente: 
            bool: Informando se o resultado da verificação é válido 
                  para continuação da busca.
            str: Contendo mensagem de status da busca.
    """
    try:
        mensagem_resultado = browser.find_element_by_id("mensagem-resultado").text
    except NoSuchElementException as e:
        msg = "\nErro: Ocorreu um erro durante o processo de automatização"
        return (False, msg)
    else:
        if 'Não há dados' in mensagem_resultado:
            msg = f"CEP: {cep}"
            msg += "\nStatus: Nenhum resultado encontrado. "
            msg += "Insira um CEP válido e tente novamente"
            return (False, msg)
    
    try:
        table = browser.find_element_by_id("resultado-DNEC")
        tbody = table.find_element_by_tag_name("tbody")
        linhas_resultados = tbody.find_elements_by_tag_name("tr")
    except NoSuchElementException as e:
        msg = "\nErro: Ocorreu um erro durante o processo de automatização"
        return (False, msg)
    else:
        resultados_encontrados = len(linhas_resultados)
        if resultados_encontrados > 1:
            msg = f"CEP: {cep}"
            msg += "\nStatus: Vários resultados encontrados. "
            msg += "Filtre um CEP mais específico e tente novamente"
            return (False, msg)
    
        msg = f"CEP: {cep}"
        msg += "\nStatus: CEP encontrado."
        return (True, msg)


def obter_endereco(browser):
    """ Obtém informações do endereço encontrado resultado da busca do CEP.

    Args:
        browser: Instâcia do browser.
    Returns:
        Lista com informações da busca solicitada.
    """
    td_log = 'td[data-th="Logradouro/Nome"]'
    td_bairro = 'td[data-th="Bairro/Distrito"]'
    td_local = 'td[data-th="Localidade/UF"]'

    logradouro = browser.find_element_by_css_selector(td_log).text
    bairro = browser.find_element_by_css_selector(td_bairro).text
    localidade = browser.find_element_by_css_selector(td_local).text

    return [logradouro, bairro, localidade]


def realizar_nova_busca(browser, cep):
    """ Realiza uma nova busca de um CEP
    
    Args:
        browser: Instâcia do browser.
        cep: CEP a ser buscado.
    """
    btn_nova_busca = browser.find_element_by_id("btn_voltar")
    btn_nova_busca.click()
    
    sleep(3)
    cep_buscar = browser.find_element_by_name("endereco")
    buscar = browser.find_element_by_id("btn_pesquisar")
    sleep(1.5)
    cep_buscar.send_keys(cep)
    sleep(1.5)
    buscar.click()


def mostrar_resultado_cep(browser, status, msg):
    """ Obtém detalhe do resultado da busca do cEP.

    Args:
        browser: Instâcia do browser.
        status: status(validação) da busca.
        msg: Mensagem do status da busca.
    Returns:
        string com detalhes da busca
    """
    saida = "\n############### Dados do CEP Informado ###############\n"
    saida += msg
    if status:
        try:
            logradouro, bairro, localidade = obter_endereco(browser)
        except NoSuchElementException as e:
            saida += "\nOcorreu um erro durante o processo de automatização"
        else:
            sleep(1.5)
            saida += f"\nLogradouro/Nome: {logradouro}"
            saida += f"\nBairro/Distrito: {bairro}"
            saida += f"\nLocalidade/UF: {localidade}"
    saida += "\n######################################################\n"
    return saida