import yaml
import json


# Convert yaml file content to json format
def yaml_to_json(yamlPath):
    with open(yamlPath, encoding="utf-8") as f:
        datas = yaml.load(f, Loader=yaml.FullLoader)  # Convert file content to dictionary format
    jsonDatas = json.dumps(datas, indent=5)  # Convert dictionary content to json format string
    return jsonDatas


if __name__ == "__main__":
    yamlPath = 'deepspeed_zero3.yaml'
    with open(yamlPath.replace('.yaml', '.json'), 'w', encoding='utf-8') as f:
        datas = yaml_to_json(yamlPath)
        f.write(datas)
