import os
import sys
from subprocess import Popen, PIPE, DEVNULL, STDOUT
from threading import Timer
from time import sleep

from flask import Flask, request, send_file, Response

app = Flask(__name__)
chunk_size = 1 << 12
timeout = 60


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path, request=request):

    def terminate(popen):
        popen.terminate()
        sleep(1)
        if popen.poll() is None:
            popen.kill()

    try:
        if 'TMPDIR' in os.environ:
            os.chdir(os.environ['TMPDIR'])
        args = 'yt-dlp '
        query_string = request.query_string.decode()
        if '--version' in query_string:
            return send_file('yt-dlp-version')
        opt_idx = query_string.find('--')
        if  opt_idx > -1:
            query_string = query_string[:opt_idx]
        query_string = query_string.strip('&')
        for opt in request.args:
            if opt.startswith('--'):
                args += opt + ' ' + request.args[opt] + ' '
        args += ('-o - ' + path + '?' + query_string).rstrip('?')
        if '--list-' or '--dump-' or '--print-' or '--get-' or '--help' in args:
            stderr = STDOUT
            args += ' --no-warnings '
            content_type = 'text/plain'
        else:
            stderr = None
            content_type = 'video/mpeg'

        def generate(popen):
            chunk = True
            timer = Timer(timeout, terminate, [popen])
            while chunk and popen.poll() is None:
                if timer.is_alive():
                    timer.cancel()
                chunk = popen.stdout.read(chunk_size)
                timer = Timer(timeout, terminate, [popen])
                timer.start()
                yield chunk
            terminate(popen)

        popen = Popen(args.split(), stdout=PIPE, stdin=DEVNULL, stderr=stderr)
        return Response(generate(popen), content_type=content_type)
    except Exception or OSError as exception:
        error = 'Exception {0}: {1}\n'.format(type(exception).__name__,
                                              exception)
        return Response(error, content_type='text/plain')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = 8808
    app.run(debug=True, host='0.0.0.0', port=port)
