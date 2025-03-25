import os
import argparse

def print_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            forbidden_root = [
                "node_modules",
                ".git",
                "venv",
                ".vscode",
                ".nuxt",
                ".output",
            ]
            if any([f in root for f in forbidden_root]):
                continue

            forbidden_file = [
                "pnpm-lock.yaml",
                ".gitignore"
            ]
            if any([f in filename for f in forbidden_file]):
                continue

            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, directory)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"<{relative_path}>:\n{content}\n")
            except UnicodeDecodeError:
                # sys.stdout.write(f"<{relative_path}>:\n[无法解码文件内容（可能为二进制文件）]\n\n")
                pass
            except PermissionError:
                # sys.stdout.write(f"<{relative_path}>:\n[无权限读取文件]\n\n")
                pass
            except Exception as e:
                # sys.stdout.write(f"<{relative_path}>:\n[读取文件时出错：{str(e)}]\n\n")
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='递归打印目录文件内容')
    parser.add_argument('directory', help='要遍历的目录路径')
    args = parser.parse_args()
    print_files(args.directory)
