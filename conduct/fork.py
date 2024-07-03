import shutil
import subprocess
import os

FLAG = "SECRET_"

class Fork:
    """Forks repository from source with embedded secrets."""

    def __init__(self, src, dst, secrets):
        """Initialise Fork class."""
        self.src = src
        self.dst = dst
        self.secrets = secrets

    def __enter__(self):
        """Clone source repository with embedded secrets."""
        def embed_secret(line):
            """Embed secret in line if it contains a flag."""
            # Get position of secret
            flag_start = line.find(FLAG)
            if flag_start != -1:
                # Get secret start index
                secret_start = flag_start + 7
                secret_end = line.find('"', secret_start)
                # Get secret end index
                if secret_end == -1:
                    if "\n" in line:
                        secret_end = len(line) - 1
                    else:
                        secret_end = len(line)
                # Get key from secret
                key = line[secret_start:secret_end].upper()
                # Construct new line
                line = f"{line[:flag_start]}{self.secrets[key]}{line[secret_end:]}"
            return line

        # Fork directories
        for src_root, dirs, files in os.walk(self.src):
            dst_root = src_root.replace(self.src, self.dst, 1)
            if not os.path.exists(dst_root):
                os.makedirs(dst_root)
            # Fork files within a directory
            for file in files:
                src_file_path = os.path.join(src_root, file)
                dst_file_path = os.path.join(dst_root, file)
                with open(src_file_path, "r") as src_file, open(dst_file_path, "w") as dst_file:
                    # Embed secrets
                    for line in src_file:
                        dst_file.write(embed_secret(line))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Remove the cloned repository."""
        shutil.rmtree(self.dst)
    
    def execute(self, command):
        """Execute command in a shell."""
        process = subprocess.Popen(command, shell=True, cwd=self.dst)
        process.wait()