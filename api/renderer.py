from rest_framework import renderers


class StreamingRenderer(renderers.JSONRenderer):
    media_type = "text/event-stream"
