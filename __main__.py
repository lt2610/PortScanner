"""
:)
~~~~~
Scan All Open Ports Of The Target IP
""" if __name__ == '__main__' else quit()

from os import get_terminal_size
from datetime import datetime
from time import sleep
from sys import argv
from socket import ( socket, gaierror, error, setdefaulttimeout, gethostbyname, AF_INET, SOCK_STREAM as TCP, SOCK_DGRAM as UDP, SOCK_RAW as ICMP )

def date():
  date = str(datetime.now()).split(' ')
  date[-1] = date[-1].split('.')[0]
  return ' '.join(date)

wt, ht = get_terminal_size()

def check_port_open(__address: tuple,stype):
  try:
    connection = socket(AF_INET, stype)
    setdefaulttimeout(.7)
    result = connection.connect_ex(__address)
    connection.close()
    return True if result==0 else False
  except error:quit("Couldn't connect to the server.")

ErrArgv = "Invalid amount of arguments!>\nSyntax: python3 PortScanner --help"

try:
  if (len(argv) <= 1):quit(ErrArgv)
  if (len(argv) == 2):
    if argv[1]=='--developer' or argv[1]=='-D':quit("\n"+"GitHub : https://github.com/MSFPT/PortScanner".center(wt,' ')+"\n")
    elif argv[1]=='--help' or argv[1]=='-H':quit(f'''
{'[ Commands ]'.center(wt,'-')}\n
Usage: Python3 PortScanner [options] or [args...]
   --help or -H
   --developer or -D

Args:
   --hostname or -h # required
   --port or -p # optional
   --maximum-port or -max-port # optional
   --minimum-port or -min-port # optional
   --protocol # TCP , UDP , ... # optional
\n{'-'*wt}
''')

  if '--hostname' in argv or '-h' in argv :
    try:hostname = gethostbyname(argv[argv.index('--hostname' if '--hostname' in argv else '-h')+1])
    except IndexError:quit('Error -> hostname not find.')
  else:quit('Error -> HostName not find.')

  if '--protocol' in argv :
    try:
      s_protocol = str(argv[argv.index('--protocol')+1]).upper()
      if s_protocol=='TCP':protocol = TCP
      elif s_protocol=='UDP':protocol = UDP
      elif s_protocol=='ICMP'or s_protocol=='RAW'or s_protocol=='IP':protocol = ICMP
      else:quit(f'Error -> {s_protocol} is not Protocol')
    except IndexError:quit('Error -> Protocol not find.')
  else:protocol = TCP

  if '--minimum-port' in argv or '-min-port' in argv :
    try:min_port = int(argv[argv.index('--minimum-port' if '--minimum-port' in argv else '-min-port')+1])
    except IndexError:quit('Error -> MinPort not find.')
  else:min_port = 1


  if '--maximum-port' in argv or '-max-port' in argv :
    try:max_port = int(argv[argv.index('--maximum-port' if '--maximum-port' in argv else '-max-port')+1])
    except IndexError:quit('Error -> MaxPort not find.')
  else:max_port = 65535

  if '--port' in argv or '-p' in argv :
    try:
      s_port = argv[argv.index('--port' if '--port' in argv else '-p')+1]
      min_port, max_port = s_port, s_port
    except IndexError:quit('Error -> Port not find.')

  if '--filter' in argv or '-f' in argv :
    try:
      filter = str(argv[argv.index('--filter' if '--filter' in argv else '-f')+1]).lower()
      ... if (filter=='all')or(filter=='open')or(filter=='closed') else quit('Error -> filter not find.')
    except IndexError:quit('Error -> filter not find.')

  print(f"""
{'-'.center(wt,'-')}
{('Scanning : '+hostname).center(wt,' ')}
{('Time started : '+date()).center(wt,' ')}
{'-'.center(wt,'-')}
""")
  for port in range(int(min_port), int(max_port)+1 ):
    port_status = check_port_open((hostname, port),protocol)
    status = 'open ' if port_status else 'closed'
    if filter == 'open' : 
      if port_status == False : continue
    elif filter == 'closed' : 
      if port_status : continue
    
    if protocol==UDP:sleep(.12)
    mrg = 8
    print('\n'+f"{' '*mrg}Port {port}"+' '.center((wt-((6+mrg+len(str(port)))+(len(status)+7))),' ')+f"{status}{' '*mrg}")
  print(end='\r\n')
except KeyboardInterrupt:quit("\n")
except EOFError:pass
except gaierror:quit("The hostname couldn't be resolved.")
except TypeError:quit(ErrArgv)
except ValueError:quit(ErrArgv)