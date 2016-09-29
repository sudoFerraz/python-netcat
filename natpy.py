"""A simple framework to mimic known features of nectcat written in python."""

import sys
import socket
import getopt
import threading
import subprocess

# definindo algumas variaveis globais
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    """Printa o help e casos de uso."""
    print "             [+]Natpy - Gabriel Augusto Ferraz Martins[+]"
    print "\n Python book - "
    print "\nUso : natpy.py -t host_alvo -p porta"
    print "\n -l --listen +~*~+~*~+~*~+~*~+~* Escuta em um host:porta para as conexoes resultantes"
    print "\n -e --execute=file_to_run +~*~+~*~+~*~+~*~+~* Executa um dado arquivo quando receber uma conexao"
    print "\n -c --command +~*~+~*~+~*~+~*~+~* inicializa uma shell"
    print "\n -u --upload=destination +~*~+~*~+~*~+~*~+~* quando receber uma conexao, fazer o upload de um arquivo e escrever no socket host"
    print "\n"
    print "\n"
    print "\nExamples: "
    print "\nnetpy.py -t 192.168.0.1 -p 5555 -1 -c"
    print "\nnetpy.py -t 192.168.0.1 -u=c :\\target.exe"
    print "\nnetpy.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./netpy.py -t 192.168.11.12 -p 135"
    sys.exit(0)


# Responsavel por manusear argumentos de linha de comando e chamar as outras funcoes
def main():
    """Funcao principal."""
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    # se os parametros nao for maior que um, mandar ajuda
    if not len(sys.argv[1:]):
        usage()

    # le as opcoes de linha de comando
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("=u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Opcao incorreta"

# Vamos apenas escutar ou adicionar data para o stdin?
