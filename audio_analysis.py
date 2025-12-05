import os
import numpy as np
import librosa

def load_audio_file(file_path, sampling_rate=22050):
    audio, sr = librosa.load(file_path, sr=sampling_rate)
    return audio, sr

def get_pause_ratio(audio, sr, top_db=30):
    intervals = librosa.effects.split(audio, top_db=top_db)
    voiced_time = sum((end - start) for start, end in intervals) / sr
    total_time = len(audio) / sr
    silent_time = max(0.0, total_time - voiced_time)
    return silent_time / total_time

def get_pitch_statistics(audio, sr):
    try:
        f0, voiced_flag, voiced_prob = librosa.pyin(audio, 
                                                    fmin=librosa.note_to_hz('C2'),
                                                    fmax=librosa.note_to_hz('C7'))
        f0_values = f0[~np.isnan(f0)]
        if len(f0_values) == 0:
            return {'mean_f0': 0.0, 'std_f0': 0.0}
        return {'mean_f0': float(np.mean(f0_values)), 'std_f0': float(np.std(f0_values))}
    except Exception:
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
        return {'mean_f0': float(np.mean(spectral_centroid)), 'std_f0': float(np.std(spectral_centroid))}

def get_energy_features(audio, frame_len=2048, hop_len=512):
    magnitude, phase = librosa.magphase(librosa.stft(audio))
    rms_energy = librosa.feature.rms(S=magnitude)
    return float(np.std(rms_energy)), float(np.mean(rms_energy))

def count_fillers(transcript_text, fillers=None):
    if fillers is None:
        fillers = ['um', 'uh', 'umm', 'like', 'you know', 'so', 'actually']
    text_lower = transcript_text.lower()
    total = sum(text_lower.count(f) for f in fillers)
    return total

def calculate_tone_score(pause_ratio, pitch_stats, energy_std, filler_num, duration):
    score = 50.0
    score -= 30.0 * min(1.0, pause_ratio / 0.2)
    pitch_std = pitch_stats.get('std_f0', 0.0)
    score += 10.0 * min(1.0, pitch_std / 20.0)
    score += 10.0 * min(1.0, energy_std / 0.01)
    score -= 3.0 * min(10, filler_num)
    return round(max(0.0, min(100.0, score)), 2)

def analyze_audio_file(file_path, transcript="", sr=22050):
    audio, sr = load_audio_file(file_path, sr)
    duration = len(audio) / sr
    pause_ratio = get_pause_ratio(audio, sr)
    pitch_stats = get_pitch_statistics(audio, sr)
    energy_std, energy_mean = get_energy_features(audio)
    filler_num = count_fillers(transcript)
    tone_score = calculate_tone_score(pause_ratio, pitch_stats, energy_std, filler_num, duration)

    features_dict = {
        'pause_rate': pause_ratio,
        'pitch_mean': pitch_stats.get('mean_f0', 0.0),
        'pitch_std': pitch_stats.get('std_f0', 0.0),
        'energy_std': energy_std,
        'energy_mean': energy_mean,
        'filler_count': filler_num,
        'duration': duration,
        'tone_score': tone_score
    }
    return features_dict

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    print(analyze_audio_file(args.input))
