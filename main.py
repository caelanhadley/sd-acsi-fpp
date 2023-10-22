
ACCEPTED_TONES = np.array(
    [
        ["normal", 1],
        ["chat", 1],
        ["cheerful", 0.7],
        ["excited", 1.0],
        ["angry", 0.5],
        ["sad", 1.4],
        ["empatehtic", 1],
        ["friendly", 1],
        ["terrified", 0.45],
        ["shouting", 0.55],
        ["unfriendly", 1.2],
        ["whispering", 1],
        ["hopeful", 1.2],
    ]
)

def build_ssml(text):
    reading = False
    token = ""
    tone_buffer = ""
    buffer = ""
    messages = []

    for char in text:
        if char == "{":
            reading = False
            if buffer != "":
                messages.append([tone_buffer, buffer.strip()])
                buffer = ""
                tone_buffer = ""
            token += " "
        else:
            if not reading:
                if char == "}":
                    token = token.strip()
                    if token in ACCEPTED_TONES[:, 0]:
                        print(f"Tone:{token}")
                        tone_buffer = token
                        reading = True
                    else:
                        tone_buffer = "normal"
                        reading = True
                    token = ""
                elif token != "":
                    token += char
            else:
                if reading and char != "}":
                    buffer += char
    if buffer != "":
        messages.append([tone_buffer, buffer.strip()])

    # Generate Message
    if len(messages) == 0:
        return open("ssml.xml", "r").read().replace("{input_text}", text)

    ssml_message = ""
    for msg in messages:
        if msg[0] in ACCEPTED_TONES[:, 0]:
            ssml_message += generate_style(msg[1], msg[0])
        else:
            ssml_message += generate_chat_xml(msg[1])

    ssml_template = (
        open("ssml_template.xml", "r").read().replace("{input}", ssml_message)
    )
    return ssml_template