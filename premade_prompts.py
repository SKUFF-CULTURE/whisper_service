PROMPT_TEMPLATE_1 = """I need you to do some operations, you now are a pro in song restoration!

1. Here is the lyrics i found in "{song}" by "{artist}", but I likely missed something or made mistakes in words.
Please fix it right in this data format (add new timecodes from original lyrics and words if I missed some, also check if there are logical or orphographical mistakes and fix them)

{lyrics}

2. Then check if lyrics is NSFW, our theme is songs related to WW2. If lyrics i gave you contain sex themes - NSFW;
If explicit or abusive speech in any language - it's automatic NSFW.
For sample, something like "соси" or "хуй" is extremely nsfw.

3. Choose couple tags for this song from this list: {{Sad, Heroic, Positive, Depressive, Patriotic, Victorious, Lyrical}}.

4. Now give me the answer in super strictly this JSON format (no markdown, no extra symbols or new lines, i need raw naked JSON as one string):
Your response MUST ONLY CONTAIN:
JSON{{"is_nsfw" : True/False,"tags": []}}
"""