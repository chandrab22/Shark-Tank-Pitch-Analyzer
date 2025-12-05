import os
import argparse
from pathlib import Path

# local module imports
from audio_analysis import analyze_audio
from speech_to_text import transcribe
from nlp_scoring import score_business
from shark_agents import persona_feedback

def process_audio_pipeline(audio_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Starting transcription...")
    transcript_text = transcribe(audio_file)
    transcript_path = output_dir / (Path(audio_file).stem + "_transcript.txt")
    transcript_path.write_text(transcript_text)

    print("Performing audio analysis...")
    tone_metrics = analyze_audio(audio_file, transcript_text)

    print("Evaluating business content...")
    business_info = score_business(transcript_text)
    # ensure consistent key naming
    business_info['business_score'] = business_info.get('business_score', 0.0)

    print("Generating persona feedback...")
    persona_comments, recommendation = persona_feedback(transcript_text, tone_metrics, business_info)

    # compile final report
    report_lines = []
    report_lines.append(f"Audio file: {audio_file}")
    report_lines.append(f"Tone features: {tone_metrics}")
    report_lines.append(f"Business details: {business_info}")
    report_lines.append("\nPersona Feedback:")
    for section, content in persona_comments.items():
        report_lines.append(f"\n--- {section} ---\n{content}\n")
    report_lines.append(f"Final recommendation: {recommendation}\n")

    report_file = output_dir / (Path(audio_file).stem + "_analysis_report.txt")
    report_file.write_text('\n'.join(report_lines))
    print("Report successfully written to", report_file)
    return report_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to .wav audio file")
    parser.add_argument("--out", default="demo_outputs", help="Directory to save outputs")
    args = parser.parse_args()
    process_audio_pipeline(args.input, args.out)
