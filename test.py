#!/usr/bin/env python

#test

import os
import glob
import bottle as b
import cPickle as pickle
import hashlib
import optparse
import commands
import json

def checkCode(code):
    codes = [c.strip() for c in open('codes.txt', 'r').readlines()]
    if code in codes:
        return True
    return False

def checkUser(username):
    usernames = [u.strip() for u in open('users.txt', 'r').readlines()]
    if username in usernames:
        return True
    return False


def saveResult(result):
    key = "%d/%s/%s/%s/%s" % (result['a1'], result['M1'], result['a2'], result['M2'], result['result_type'])
    data = json.load(open('allresults_new.json', 'r'))
    data[key] = result
    json.dump(data, open('allresults_new.json', 'w'))


@b.post('/insert')
def insert():
    data = pickle.loads(b.request.forms.get('data'))
    if not checkCode(data['code']):
        return 'Error: that code does not exist.'
    if not os.path.isdir(os.path.join('database', data['code'])):
        try:
            os.mkdir(os.path.join('database', data['code']))
        except OSError:
            # Someone else made the directory before us.
            pass
    md5 = hashlib.md5(data['tarball']).hexdigest()
    try:
        os.mkdir(os.path.join('database', data['code'], md5))
    except OSError:
        # That tarball already exists in the database.
        return "Error: That data has already been submitted to the database with that code."
    tarfile = open(os.path.join('database', data['code'], md5, 'data.tar.gz'), 'w')
    tarfile.write(data['tarball'])
    tarfile.close()
    path1 = os.path.join('database', data['code'], md5)
    path2 = os.path.join(path1, 'data.tar.gz')
    os.system('tar -xf %s -C %s' % (path2, path1))
    os.system('rm %s' % path2)
    # Get the metadata
    lines = open(os.path.join(path1, 'metadata.txt'), 'r').readlines()
    metadata = dict ( username = lines[0].strip(),
                      hostname = lines[1].strip(),
                      pwd = lines[2].strip(),
                      timestamp = lines[3].strip() )
    lines = commands.getoutput('python calculations.py %s' % data['code'])
    if len(lines) > 0:
        for line in lines.split('\n'):
            if len(line) > 0:
                try:
                    result = json.loads(line)
                    result['username'] = metadata['username']
                    saveResult(result)
                except:
                    pass
    return "Success."

@b.get('/')
def index():
    with open('ind.template', 'r') as f:
        template = b.SimpleTemplate('\n'.join(f.readlines()))
    with open('allresults_new.json', 'r') as f:
        data = ''.join(f.readlines())
    with open('text.html', 'r') as f:
        text = ''.join(f.readlines())
    with open('graphing.html', 'r') as f:
        config = ''.join(f.readlines())
    return template.render(text = text, data = data, config = config)


@b.post('/checkcode')
def check_code():
    code = b.request.forms.get('code')
    if checkCode(code):
        return 'true'
    return 'false'


@b.post('/checkuser')
def check_user():
    username = b.request.forms.get('username')
    if checkUser(username):
        return 'true'
    return 'false'

@b.route('/static/<filename>')
def server_static(filename):
    return b.static_file(filename, root='./static')

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', dest='debug', action='store_true',
                      default=False, help='Run server on localhost.')
    (options, arguments) = parser.parse_args()
    if not os.path.isdir('database'):
        os.mkdir('database')
    if not os.path.isfile('allresults_new.json'):
        f = open('allresults_new.json', 'w')
        f.write('{}')
        f.close()
    if options.debug:
        print 'Debug ON'
        b.run(reloader=True)
    else:
        b.run(server='cgi')
