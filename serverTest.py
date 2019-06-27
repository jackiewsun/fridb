from bottle import route, run, template, SimpleTemplate, static_file

@route('/')
def index():
    with open('ind.template', 'r') as f:
        template = SimpleTemplate('\n'.join(f.readlines()))
    with open('allresults_new.json', 'r') as f:
        data = ''.join(f.readlines())
    with open('text.html', 'r') as f:
        text = ''.join(f.readlines())
    with open('graphing.html', 'r') as f:
        config = ''.join(f.readlines())
    return template.render(text = text, data = data, config = config)

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

run(host='localhost', port=8080)
