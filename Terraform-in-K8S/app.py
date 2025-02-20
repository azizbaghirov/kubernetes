import subprocess
import threading

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/run-terraform', methods=['POST'])
def run_terraform():
    date = request.args.get('date')  # pattern yyyy/mm/dd
    public_ip = request.args.get('publicIp')
    exam_name = request.args.get('examName')
    exam_session_id = request.args.get('examSessionId')

    template_path = f'/tda-terraform/{exam_name}/*'
    new_template_path = f'/tda-terraform/exams/{exam_name}/{date}/{exam_session_id}/'

    # fixme : create directory if not exists
    #  if public_ip not exists handle it
    create_instance_copy = f'mkdir -p {new_template_path} && cp -r {template_path} {new_template_path}'
    run_terraform_instance = f'cd {new_template_path} && terraform init && terraform apply -auto-approve'  # -var "userpublicip={public_ip}"'

    def run_terraform_async():
        try:
            subprocess.run(create_instance_copy, shell=True, text=True, capture_output=True)
            subprocess.run(run_terraform_instance, shell=True, text=True, capture_output=True)
        except Exception as e:
            print(e)

    thread = threading.Thread(target=run_terraform_async)
    thread.start()

    return jsonify({'examTemplatePath': new_template_path, 'error': ""}), 200


@app.route('/instance-public-ip', methods=['GET'])
def get_instance_ip():
    env_path = request.args.get("examEnvPath")

    get_instance_public_ip = f'cd {env_path} && echo $(terraform output -raw master_public_dns)'

    try:
        result = subprocess.run(get_instance_public_ip, shell=True, text=True, capture_output=True)

        return jsonify({'output': result.stdout, 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/start-instance', methods=['POST'])
def start_instance():
    env_path = request.args.get("examEnvPath")

    start_existing_instance = f'cd {env_path} && aws ec2 start-instances --instance-ids $(terraform output -json worker_ids | jq -r ".[]") $(terraform output -raw master_id)'
    refresh_and_get_new_dns = f'cd {env_path} && terraform refresh && echo $(terraform output -raw master_public_dns)'

    try:
        subprocess.run(start_existing_instance, shell=True, text=True, capture_output=True)
        result = subprocess.run(refresh_and_get_new_dns, shell=True, text=True, capture_output=True)

        return jsonify({'output': result.stdout, 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stop-terraform', methods=['POST'])
def stop_terraform():
    env_path = request.args.get("examEnvPath")

    stop_existing_instance = f'cd {env_path} && aws ec2 stop-instances --instance-ids $(terraform output -json worker_ids | jq -r ".[]") $(terraform output -raw master_id)'

    def stop_terraform_async():
        try:
            result = subprocess.run(stop_existing_instance, shell=True, text=True, capture_output=True)
            print(jsonify({'output': result.stdout, 'error': result.stderr}), 200)
        except Exception as e:
            print(e)

    thread = threading.Thread(target=stop_terraform_async)
    thread.start()

    return jsonify({'output': "stopping instance", 'error': ""}), 200


@app.route('/destroy-instance', methods=['POST'])
def destroy_terraform():
    env_path = request.args.get("examEnvPath")

    destroy_terraform_instance = f'cd {env_path} && terraform destroy -auto-approve'

    try:
        result = subprocess.run(destroy_terraform_instance, shell=True, text=True, capture_output=True)

        return jsonify({'output': result.stdout, 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
