import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import User
from authors.apps.core.token import generate_token


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` may or may not contain an `errors` key.
        #  We want the default JSONRenderer to handle rendering errors,
        # so we need to check for this case.

        # checks for the 'detail' key from the data given, then checks for
        # the 'errors' key. If both are not found then errors is set to None
        errors = data.get('detail') if data.get('detail', None) is not None \
            else data.get('errors', None)
        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            if isinstance(errors, ReturnDict):
                # here, the 'errors' key was found and will be used in the
                # response
                return super(UserJSONRenderer, self).render(data)
            else:
                # here, the errors key was not found and will be added manually
                errors = dict(errors=dict(detail=errors))
                return super(UserJSONRenderer, self).render(errors)
        try:
            confirm_user = data['email']
            user_db = User.objects.get(email=confirm_user)
            if user_db.is_active is False:
                return json.dumps({
                    'Message':
                        "Please confirm your email address "
                        "to complete the registration"
                })
        except KeyError:
            pass

        token = generate_token(data)
        data['token'] = token

        # Finally, we can render our data under the "user" namespace.
        return json.dumps({'user': data})


class EmailJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        errors = data.get('errors', None)

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            if isinstance(errors, ReturnDict):
                # here, the 'errors' key was found and will be used in the
                # response
                return super(EmailJSONRenderer, self).render(data)

            else:
                # here, the errors key was not found and will be added manually
                errors = dict(errors=dict(detail=errors))
                return super(EmailJSONRenderer, self).render(errors)

        return json.dumps({
            'Message':
                "Please confirm your email address for further instruction."
        })
