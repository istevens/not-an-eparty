import cgi
import cgitb
import csv
import md5
import os
cgitb.enable()

from formencode import schema, validators, Invalid
import simplejson

def validate_recaptcha(values, recaptcha_response, validator):
    from recaptcha.client import captcha
    response = captcha.submit(
        values['recaptcha_challenge_field'],
        recaptcha_response,
        validator.private_key,
        validator.remote_ip
    )
    if response.error_code:
        return {'recaptcha_response_field': 'What you typed in was not in the image.'}


class RsvpForm(schema.Schema):
    name = validators.String(notEmpty=True, strip=True)
    email = validators.Email(notEmpty=True, strip=True)
    recaptcha_challenge_field = validators.String(notEmpty=True)
    recaptcha_response_field = validators.String(notEmpty=True)

    def __init__(self, private_key, remote_ip):
        _rc = schema.SimpleFormValidator(validate_recaptcha)
        _rc.private_key = private_key
        _rc.remote_ip = remote_ip
        self.add_chained_validator(_rc)

def create_rsvp(data, path):
    if os.path.isdir(path):
        _m = md5.md5(data['name']).hexdigest()
        _f = open(os.path.join(path, _m), '+w')
        csv.writer(_f).writerow(data['name'], data['email'])
        _f.close()
    else:
        raise os.error('RSVP path does not exist: %s' % path)

def rsvp(private_key, path):
    print "Content-type: application/json"

    form = RsvpForm(private_key, os.environ["REMOTE_ADDR"])
    try:
        data = form.to_python(cgi.SvFormContentDict())
        create_rsvp(data)
        print 'Status: 200'
        print
    except Invalid, error:
        print 'Status: 400'
        print
        errors = dict([(k,str(v)) for k,v in error.error_dict.iteritems()])
        print simplejson.dumps({'errors': errors})
