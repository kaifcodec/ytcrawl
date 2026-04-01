import base64


def get_initial_token(video_id):
    """Manually constructs the Protobuf string for the comments section."""
    raw = f'\x12\r\x12\x0b{video_id}\x18\x062\'"\x11"\x0b{video_id}0\x00x\x020\x00B\x10comments-section'
    return base64.b64encode(raw.encode()).decode()
