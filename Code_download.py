# Autor: Roger da Silva Machado

from ota_updater import Ota_updater
import utime
import network
import os

import ujson

class Code_download:
  #Classe utilizada para atualizar os codigos usando OTA e um repositorio privado do github 
  
  def download_update(self):
  
  #Metodo que primeiramente busca os dados necessarios no arquivo json, apos, se conseguir conexao com a internet,
  #verifica se eh necessario realizar o download de uma nova versao do codigo e apos realiza a atualizacao do codigo

    try:
      file = open('conf.json', 'r') #: le os dados do json
      file_json = ujson.loads(file.read())
      password_wifi = file_json['network']['password'] #: senha da rede wifi
      name_wifi = file_json['network']['ssid'] #: ssid da rede wifi
      token = file_json['git']['token'] #: token da conta do projeto do GitHub
      url = file_json['git']['url'] #: url do projeto do GitHub
      file.close()
      
      diretorio = 'src' #: diretorio que contem os codigos que serao baixados via ota
      
      o = Ota_updater(url, main_dir= diretorio, headers={'Authorization': 'token {}'.format(token)}) #: cria o objeto OTA com os dados do projeto privado do GitHub

      sta_if = network.WLAN(network.STA_IF)
      sta_if.active(True)

      data_download = ''
      data_update = ''

      for _ in range(10):
        sta_if.connect(name_wifi, password_wifi)
        utime.sleep(1)
        # se conectar na internet, atualiza o horario e verifica se tem que fazer download dos codigos e atualizar
        if sta_if.isconnected():
          settime() #: realiza a atualizacao do horario local
          download = o.download_updates_if_available()         

          update = o.apply_pending_updates_if_available()
          
          os.chdir(diretorio) #: redireciona o diretorio atual para o diretorio dos codigos

          return
        utime.sleep(11)
      # se chegou aqui eh porque nao conseguiu internet, entao eh necessario fazer o redirecionamento para a pasta onde esta os codigos
      os.chdir(diretorio) 

    except Exception as e: 
      if(os.getcwd() == '/'):
        # caso o diretorio atual seja o / eh realizado o redirecionamento para o diretorio dos codigos
        os.chdir(diretorio)     



