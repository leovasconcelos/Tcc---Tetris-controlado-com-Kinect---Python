<h1>IFSP - Laboratório de Computação Aplicada - LABCOM3</h1>

<h2>Exemplos e desenvolvimento da integração Kinect - Python via OpenNI e NiTE</h2>

<h4>Ambiente de execução</h4>

<ul>
    <li>Baixar a libfreenect para compilar apenas o driver Freenect para a biblioteca OpenNI (o Freenect em si é instalável via repositório apt)<br>
        Repositório: <a href="https://github.com/OpenKinect/libfreenect/tree/master/OpenNI2-FreenectDriver">https://github.com/OpenKinect/libfreenect/tree/master/OpenNI2-FreenectDriver</a>
    </li>
    <li>Baixar a OpenNI e descompactar no diretório desejado. Copiar o driver compilado no passo anterior para a pasta <tt>Redist/OpenNI2/Drivers</tt> da instalação.
    </li>
    <li>Baixar a versão 2.0 da NiTE e descompactar no diretório desejado.
        Repositório: <a href="http://download.dahoo.fr/Ressources/openNi/NiTE%20v2.0/">http://download.dahoo.fr/Ressources/openNi/NiTE%20v2.0/</a>
    </li>
    <li>Testar as aplicações exemplo do NiTE (recomendado: <tt>Samples/Bin/SimpleUserTracker</tt>. Tudo deve estar funcionando neste momento!</li>
    <li>Instalar o wrapper Python para a OpenNI e NiTE atualizado disponível em <a href="https://github.com/severin-lemaignan/openni-python">https://github.com/severin-lemaignan/openni-python</a>. Baixar os arquivos e executar <tt>python setup.py</tt> na linha de comando.
    </li>

</ul>