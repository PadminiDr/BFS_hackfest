import os

directory_path = "/workspaces/BFS_hackfest/company"
for root, dirs, files in os.walk(directory_path):
    print(f"root: {root}\n dirs: {dirs}\n files: {files}\n {'-'*10}")
    for file_name in files:
        file_path = os.path.join(root, file_name)
        print(f"file_path : {file_path}")
        relative_path = os.path.relpath(file_path, directory_path)
        print(f"rel_path = {relative_path}")
            # upload_file_to_blob(file_path, container_client, os.path.join(blob_path or "", relative_path))