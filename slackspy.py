from slackclient import SlackClient
from datetime import datetime
import time
import json
import os

def main():
  with open(os.path.join(os.path.dirname(__file__), 'token.txt')) as F:
    token = F.read().strip()

  sleep_period = 5*60
  write_every = 50
  sc = SlackClient(token)

  observations = []

  while True:
    status = sc.api_call('users.list', presence=1)
    status = dict([(u['name'], u['presence']) for u in status['members'] if 'presence' in u])
    timestamp = int(time.time())
    observations.append({ 'status': status, 'time': timestamp })

    if len(observations) >= write_every:
      with open('%s.json' % timestamp, 'w') as outf:
        json.dump(observations, outf)
      observations = []

    print('Got status at %s' % datetime.now())
    time.sleep(sleep_period)

main()
