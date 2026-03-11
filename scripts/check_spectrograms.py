from app import create_app
from app.models.models import SoundAnalysis

app = create_app()

with app.app_context():
    analyses = SoundAnalysis.query.all()
    print('Total analyses:', len(analyses))
    for analysis in analyses:
        print(f'ID: {analysis.id}')
        print(f'  Spectrogram path: {analysis.spectrogram_path}')
        print(f'  JSON spectrogram path: {analysis.json_spectrogram_path}')
        
        # Check if JSON spectrogram file exists
        if analysis.json_spectrogram_path:
            import os
            # Normalize the path
            normalized_path = analysis.json_spectrogram_path.replace('/', os.sep).replace('\\', os.sep)
            print(f'  Normalized path: {normalized_path}')
            
            # Check in uploads directory
            json_path1 = os.path.join('uploads', normalized_path)
            print(f'  Checking path 1: {json_path1} - Exists: {os.path.exists(json_path1)}')
            
            # Check with absolute path
            json_path2 = os.path.abspath(json_path1)
            print(f'  Checking path 2: {json_path2} - Exists: {os.path.exists(json_path2)}')
            
            # Check if the file exists with just the filename in the spectrograms directory
            filename = os.path.basename(normalized_path)
            json_path3 = os.path.join('uploads', 'sounds', 'spectrograms', filename)
            print(f'  Checking path 3: {json_path3} - Exists: {os.path.exists(json_path3)}')
            
            # Check with absolute path for path 3
            json_path4 = os.path.abspath(json_path3)
            print(f'  Checking path 4: {json_path4} - Exists: {os.path.exists(json_path4)}')
            
            if os.path.exists(json_path4):
                # Show first few lines of the JSON file
                try:
                    with open(json_path4, 'r') as f:
                        import json
                        data = json.load(f)
                        print(f'  JSON keys: {list(data.keys())}')
                        print(f'  Times length: {len(data["times"])}')
                        print(f'  Frequencies length: {len(data["frequencies"])}')
                        print(f'  Sxx shape: ({len(data["Sxx"])}, {len(data["Sxx"][0]) if data["Sxx"] else 0})')
                except Exception as e:
                    print(f'  Error reading JSON file: {e}')
        print()