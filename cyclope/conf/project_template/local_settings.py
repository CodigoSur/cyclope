# add real email account setup here for registration to work properly

EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='anon.email.noreply'
EMAIL_HOST_PASSWORD='anon.email'
EMAIL_PORT='587'
#DEFAULT_FROM_EMAIL = ""
#SERVER_EMAIL = ""
EMAIL_USE_TLS = True  # we set this to True for the sample email config

CYCLOPE_PAGINATION = { 'TEASER' : 3, 'LABELED_ICON' : 5,
                       'FORUM' : 2}

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''
