import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict


class ProfileJSONRenderer(JSONRenderer):
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
                return super(ProfileJSONRenderer, self).render(data)
            else:
                # here, the errors key was not found and will be added manually
                errors = dict(errors=dict(detail=errors))
                return super(ProfileJSONRenderer, self).render(errors)

        # if bio or image is an empty string, set them to None so that they
        # are displayed as "null" in the Response object
        if data.get('bio') is "":
            data['bio'] = None
        if data.get('image') is "":
            data['image'] = None

        # Finally, we can render our data under the "profile" namespace.
        return json.dumps({'profile': data})


class FollowersJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        # Render our data under the "followers" namespace.
        return json.dumps({'followers': data})


class FollowingJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Render our data under the "followers" namespace.
        return json.dumps({'following': data})
