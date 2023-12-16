import subprocess
subprocess.run(["apt-get", "install", '-y', "ffmpeg"])

import whisper

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Optional
from tempfile import NamedTemporaryFile


app = FastAPI()


model = whisper.load_model("tiny")

class TranscriptionOutput(BaseModel):
  transcription: str = ''
  error: Optional[str] = None


@app.post("/transcribe")
def transcribe(file: UploadFile):
  # check if file has audio extension
  if file.filename.split(".")[-1] not in ["wav", "mp3", "ogg", "flac"]:
    return dict(error="Invalid file type")

  # Save the file to a temporary location
  with NamedTemporaryFile(delete=True) as temp:
    temp.write(file.file.read())
    temp_path = temp.name
    audio = whisper.load_audio(temp_path)

  return dict(transcription=model.transcribe(audio)['text'].strip())


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="localhost", port=8000, reload=True)