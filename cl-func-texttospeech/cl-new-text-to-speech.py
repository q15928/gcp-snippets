"""
Cloud function to convert the input text to speech and save to the designated 
storage bucket.

Env variables:
BUCKET_NAME
"""

import os
import uuid
from google.cloud import storage
from google.cloud import texttospeech

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {} in bucket {}.'.format(
        source_file_name,
        destination_blob_name,
        bucket_name))


def convert_text_to_speech(text=None, lang_code='en-US'):
    """
    Convert the text to speech with the language code. 
    Save the audio file to a publice accessible bucket.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    if text is None:
        text = "Hello, World!"
    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=lang_code,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    try:
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        source_file_name = f'/tmp/{uuid.uuid4()}.mp3'
        # The response's audio_content is binary.
        with open(source_file_name, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{source_file_name}"')
        
        # upload to storage bucket
        bucket_name = os.getenv("BUCKET_NAME")
        dest_blob_name = os.path.basename(source_file_name)
        upload_blob(bucket_name, source_file_name, dest_blob_name)

        # return the url for the audio file
        audio_url = os.path.join("https://storage.googleapis.com", 
            bucket_name, dest_blob_name)
        audio_link = f'<a href="{audio_url}">The audio file</a>'
        return audio_link
    except Exception as e:
        print("error while converting text to speech")
        raise e

def post_new_text(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'text' in request.args:
        text = request.args.get('text')
    elif request_json and 'text' in request_json:
        text = request_json['text']
    else:
        text = None
    
    try:
        return convert_text_to_speech(text)
    except Exception as e:
        print("error occurs: ", e)
