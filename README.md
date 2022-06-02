# scaff

Sistema para Cadastro, Auditorias, Fiscalizações e Análise de Fraudes.

Obs: sistema descartado.

## Desenvolvimento

Essa documentação é voltada para o Sistema operacional Windows e para a IDE Pycharm.

### Dependências
Antes de clonar a aplicação é necessário ter todas as dependêcias instaladas na máquina.

| Fonte           | Descrição                                                                                                  |
| :-------------- | :--------------------------------------------------------------------------------------------------------- |
| Python	      | [A linguagem de programação Python](http://www.python.org/getit/), v3.x                                    |
| PostgreSQL	  | [O Sistema de Banco de Dados PostgreSQL](http://www.postgresql.org/download/), v9.3 or newer               |
| pip	          | [Uma ferramenta para instalação e gerenciamento de pacotes Python](http://www.pip-installer.org/)          |
| virtualenv      | [O construtor do ambiente virtual Python](http://www.virtualenv.org/)                                      |
| Git             | [Um sistema de controle de versões](http://book.git-scm.com/2_installing_git.html)                         |
| Django          | [Um framework Python Web de alto nível, v2.2 ou mais nova](https://www.djangoproject.com/download/)        |
| Psycopg2        | [Adaptador PostgreSQL para Python](http://initd.org/psycopg/)                                              |

A instalação do Python, PostgreSQL e do Git são feitas a partir de um arquivo executável que pode ser baixado nos seus sites oficiais. 

#### Pip 
Para instalar o `pip` utilize a linha de comando:
```
python -m pip install -U pip
```
#### Virtualenv
Depois do Python, PostgreSQL, Git e Pip instalados na máquina, é hora de instalar as outras dependências no python.
As boas práticas de desenvolvimento em Pyhton dizem para sempre utilizar um ambiente virtual, dessa forma, você 
cria com container com as dependências do projeto naquele espaço apenas sem influenciar as configurações externas a esse
container. O Ambinete virtual utilizado no projeto é criado pelo `virtualenv`.

Para instalar o virtualenv abra o prompt de comando, digite a linha abaixo e tecle ``enter``.
```
pip install virtualenv
```
Despois de instalado, vá ao diretório onde o projeto será desenvolvido e crie a pasta que será o ambiente virtual da aplicação
```
c:\projetos> mkdir scaff_av
c:\projetos> cd scaff_av
c:\projetos\scaff_av>
```

Digite o comando a seguir para criar o ambiente;

```

virtualenv .

OU

python -m virtualenv venv

```
Agora é necessário ativar o ambiente para que as configurações necessárias sejam aplicadas a ele. 
Para ativá-lo basta chamar o arquivo `activate` que fica dentro da pasta `bin` ou `Scripts` como na linha abaixo

```
c:\projetos\scaff_av> Scripts\activate
```
O prompt de comando deve mostrar uma linha semelhante a seguida:
```
(scaff_av) c:\projetos\scaff_av>
```

Para desativar o ambiente virtual utilize o termo `deactivate`

##### Sempre que for atualizar algo no projeto é necessário ativar o ambiente virtual.

#### Django e Psycopg
Com o ambiente virtual ativado, instale as outras dependencias utilizando a linha de comando abaixo:
```
pip install django psycopg2
```

Para verificar se todos as dependências do Pyhton estão devidamente instaladas:

pip list

#### Executando o projeto
Agora, dentro do ambiente virtual, faça o clone do projeto no gitlab, e entre na pasta do projeto.
Nesse ponto você já deve estar apto a executar o projeto.
```
pyhton manage.py runserver
```

