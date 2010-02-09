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
        values['recaptcha_response_field'],
        validator.private_key,
        validator.remote_ip
    )

    if not response.is_valid:
        return {'recaptcha_response_field': 'What you typed in was not in the image.'}


class RsvpForm(schema.Schema):
    name = validators.String(notEmpty=True, strip=True)
    email = validators.Email(notEmpty=True, strip=True)

def create_rsvp(data, path):
    if os.path.isdir(path):
        _m = md5.md5(data['name']).hexdigest()
        _f = open(os.path.join(path, _m), 'w+')
        csv.writer(_f).writerow((data['name'], data['email']))
        _f.close()
    else:
        raise os.error('RSVP path does not exist: %s' % path)

def rsvp(private_key, path):
    print "Content-type: application/json"

    form = RsvpForm()
    try:
        data = form.to_python(cgi.SvFormContentDict())
        create_rsvp(data, path)
        print 'Status: 200'
        print 'Content-Length: 0'
        print
    except Invalid, error:
        errors = dict([(k,str(v)) for k,v in error.error_dict.iteritems()])
        json = simplejson.dumps({'errors': errors})
        print 'Status: 400'
        print 'Content-Length: %d' % len(json)
        print
        print json
