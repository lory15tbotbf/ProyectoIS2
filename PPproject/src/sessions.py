# -*- coding: utf-8 -*-

# Better/more secure session management (http://flask.pocoo.org/snippets/51)
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature
import time

# to be able to set app.permanent_lifetime_session
from datetime import datetime, timedelta

# for the serializer
try:
   import cPickle as pickle
except:
   import pickle


class ItsdangerousSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False

    def set_lifetime(self, td):
        self.permanent = False
        self['lifetime_seconds'] = td.total_seconds()
        self['timestamp'] = int(time.time())

    def make_permanent(self):
        d("MAKE PERMANENT!!!")
        self.pop('lifetime_seconds', None)
        self.pop('timestamp', None)
        self.permanent = True


class ItsdangerousSessionInterface(SessionInterface):
    salt = 'cookie-session'
    session_class = ItsdangerousSession

    def get_serializer(self, app):
        if not app.secret_key:
            return None
        return URLSafeTimedSerializer(app.secret_key, salt=self.salt,
            serializer=pickle)

    def return_empty_session(self):
        sessdel = self.session_class()
        sessdel.modified = True
        return sessdel

    # Override original method from SessionInterface
    # so that an expiration time is possible on a per-session-basis
    # This expiration time is not for signing the cookie, it is just for the
    # browser.
    def get_expiration_time(self, app, session):
        """A helper method that returns an expiration date for the session
        or `None` if the session is linked to the browser session. The
        default implementation returns now + the permanent session
        lifetime configured on the application.
        """
        if 'lifetime_seconds' in session:
            d("session lifetime set: %s s" % session['lifetime_seconds'])
            return datetime.utcnow() + timedelta(seconds = session['lifetime_seconds'])
        if session.permanent:
            return datetime.utcnow() + app.permanent_session_lifetime

    # Returns an empty session when the session provided is expired.
    # Therefore, check both the global session lifetime and, if available,
    # the lifetime defined within the session cookie
    def open_session(self, app, request):
        s = self.get_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = app.permanent_session_lifetime.total_seconds()
        try:
            data = s.loads(val, max_age=max_age)
            session = self.session_class(data)
            # Global session expiration based on app.permanent_session_lifetime
            # is checked during `s.loads()` above. If we are here, this check
            # was fine. Now, check if there was a session-based expiration time
            # set.
            if 'lifetime_seconds' in session and 'timestamp' in session:
                age = int(time.time()) - session['timestamp']
                if age > session['lifetime_seconds']:
                    # expired, so return empty session, marked modified
                    # so that the cookie gets deleted by save_session
                    d("cookie EXPIRED based on data IN cookie!")
                    return self.return_empty_session()
                # not expired, so update timestamp in order to prolong
                # validity of cookie
                d("cookie VALIDATED based on data IN cookie! Prolong!")
                session['timestamp'] = int(time.time())
            return session
        except BadSignature:
            d("BAD SIGNATURE! Expired based on global session lifetime or tampered.")
            return self.return_empty_session()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        # just a convenience check...
        #if session.permanent:
        #    session.make_permanent()
        expires = self.get_expiration_time(app, session)
        d("new expires value: %s" % expires)
        # dumps serializes the session dict, attaches a timestamp, salt, and
        # secret key, and signs the information
        val = self.get_serializer(app).dumps(dict(session))
        response.set_cookie(app.session_cookie_name, val,
                            expires=expires, httponly=True,
                            domain=domain)