from json import JSONEncoder
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from pathlib import Path
import json
import numpy
import pickle
import os

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def clean_pkl(filename_path,readme_path):
    f = open(filename_path, 'rb')
    sub_dict = pickle.load(f, encoding='latin1')
    f.close()

    del sub_dict['signal']['chest']
    sub_dict['signal'] = sub_dict['signal']['wrist']

    smoker_feature = None
    with open(readme_path, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip()
            if line.find('Are you a smoker?') != -1:
                feature_str = line.rsplit(' ', 1)[-1]
                if feature_str == 'NO':
                    smoker_feature = False
                    break
                elif feature_str == 'YES':
                    smoker_feature = True
                    break

    sub_dict['smoker'] = smoker_feature if smoker_feature is not None else 'null'

    return sub_dict

def get_dir(path):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            yield file

def get_files(path):
    pkl_file = ''
    readme_file = ''
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        if os.path.isfile(filename) and Path(filename).suffix == '.pkl':
            pkl_file = filename
        if file == os.path.basename(path)+'_readme.txt':
            readme_file = filename
    return (pkl_file,readme_file)

def subject_into_json(filename, cleaned_dict):
    filename = filename + '.json'
    print("=| Serialize object into JSON and save it into " + filename)
    # For pretty formatting json set indent=1, separators=(',', ':')
    with open(filename, "w") as write_file: json.dump(cleaned_dict, write_file, cls=NumpyArrayEncoder)
    print("=| Done writing " + filename)
    return filename

def main():
    abs_path = Path().resolve()
    dirs = list()
    for file in get_dir(abs_path):
        dirs.append(file)
    
    json_files = list()
    for dir in dirs:
        (pkl_file, readme_file) = get_files(os.path.join(abs_path, dir))
        sub_dict = clean_pkl(pkl_file,readme_file)
        json_files.append(subject_into_json(Path(pkl_file).stem,sub_dict))
    
    with ZipFile('cleaned_data.zip', 'w') as zipObj:
        for json_f in json_files:
            zipObj.write(json_f,compress_type=ZIP_DEFLATED)
    
    print("=| Created zip archive")

if __name__ == "__main__":
    main()