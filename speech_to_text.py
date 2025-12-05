import os

def whisper_transcribe(audio_path):
    """Transcribe audio using OpenAI Whisper, fallback to None on failure"""
    try:
        import whisper
        model = whisper.load_model('small')
        transcription = model.transcribe(audio_path)
        return transcription['text']
    except Exception as e:
        print("Whisper unavailable or failed:", e)
        return None

def transcribe(audio_path):
    """Get transcript using Whisper, fallback to filename if unavailable"""
    text = whisper_transcribe(audio_path)
    if text is not None:
        return text
    return f"[Automatic fallback transcript for {os.path.basename(audio_path)}]"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to audio file")
    args = parser.parse_args()
    print(transcribe(args.input))
