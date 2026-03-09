from backend.llm_service import stream_chat
from backend.persona.persona_loader import load_personas
from backend.utils.timer import thinking_timer

def run_personas(user_message, memories, stop_event=None):

    personas = load_personas()

    responses = []

    for p in personas:

        if stop_event and stop_event.is_set():
            break

        prompt = f"""
            Persona: {p["name"]}

            {p["prompt"]}

            Relevant memories:
            {memories}

            User:
            {user_message}

            Respond from the perspective of this persona.
            """

        text = ""

        for token in stream_chat(prompt, stop_event):
            text += token

        responses.append((p["name"], text))

    return responses

def run_single_persona(user_message, persona_name, memories, stop_event=None):

    personas = load_personas()

    persona = None

    for p in personas:
        if p["name"].lower() == persona_name.lower():
            persona = p
            break

    if persona is None:
        return f"'{persona_name}' нэртэй persona олдсонгүй."
    
    prompt = f"""
        Persona: {persona["name"]}

        {persona["prompt"]}

        Relevant memories:
        {memories}

        User:
        {user_message}

        Respond only as this persona.
    """

    text = ""

    for token in stream_chat(prompt, stop_event):
        text += token

    return text