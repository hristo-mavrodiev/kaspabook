import subprocess

# List of IP addresses to try to SSH into
ip_addresses = ['192.168.0.1', '192.168.0.100', '192.168.0.101', '192.168.0.108']

# SSH connection parameters
username = 'user'
password = '1'
timeout = '5'

# Try to SSH into each IP address in the list
for ip_address in ip_addresses:
    try:
        # Construct the SSH command
        ssh_command = ['ssh', f'{username}@{ip_address}', '-o', f'ConnectTimeout={timeout}', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null']
        
        # Start the SSH process
        ssh_process = subprocess.Popen(ssh_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Send the password to the SSH process
        ssh_process.stdin.write(f'{password}\n')
        ssh_process.stdin.flush()
        
        # Wait for the SSH process to finish
        stdout, stderr = ssh_process.communicate(timeout=int(timeout))
        
        # If the connection is successful, print a message
        if ssh_process.returncode == 0:
            print(f'Successfully connected to {ip_address}')
        
    except subprocess.TimeoutExpired as e:
        # If the connection times out, print an error message
        print(f'Connection to {ip_address} timed out after {timeout} seconds')
        
    except Exception as e:
        # If the connection fails for any other reason, print an error message
        print(f'Failed to connect to {ip_address}: {str(e)}')