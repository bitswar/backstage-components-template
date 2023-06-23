import os
import pickle
import sys

extensions = ['.puml']


class Env:
    include_folders: list[str]
    src_folder: str

    env_folder_pattern = 'PUML_INCLUDE_DIR'
    env_src_dir = 'PUML_ROOT_DIR'

    def __init__(self) -> None:
        self.include_folders = self.__load_envs()

    def __trim_path(self, path: str) -> str:
        if path[-1] == '/':
            path = path[:-1]
        if path[0] == '/':
            path = path[1:]
        return path

    def __load_envs(self) -> list[str]:
        envs = []
        with open('.env', 'r') as file:
            envs = file.read().split('\n')

        folders = []
        for line in envs:
            path = line.split('=')[-1]
            if not line.find(self.env_folder_pattern) == -1:
                folders.append(self.__trim_path(path))
            if not line.find(self.env_src_dir) == -1:
                self.src_folder = self.__trim_path(path)

        return folders


class Processer:
    dump_file_name = 'dump.pkl'
    env = Env()

    def preprocess(self):
        diagrams = self.__get_all_diagram_files(self.env.env_src_dir)
        utils = {}
        for folder in self.env.include_folders:
            utils.update(self.__get_all_diagram_files(folder))

        for u in utils.keys():
            for i in diagrams.keys():
                if i == u:
                    diagrams.pop(i)
                    break

        for path in diagrams.values():
            self.__dump_sources(path)
            self.__preprocess_file(path, utils)

    def __get_all_diagram_files(self, start_path: str) -> dict[str, str]:
        result = {}
        for item in os.walk(start_path):
            for file in item[2]:
                for ext in extensions:
                    if not file.find(ext) == -1:
                        result[file] = f'{item[0]}/{file}'
        return result

    def __preprocess_file(self, filepath: str, utils: dict[str, str]) -> None:
        content = ''
        with open(filepath, 'r') as file:
            content = file.read().split('\n')

        for line in range(len(content)):
            for key in utils:
                if not content[line].find(key) == -1:
                    with open(utils[key], 'r') as template:
                        content[line] = '\n'.join(
                            template.read().split('\n')[1:-1]
                        )

        with open(filepath, 'w') as file:
            file.write('\n'.join(content))

    def __dump_sources(self, path: str) -> None:
        with open(path, 'r') as file:
            data = FileData(
                path,
                path.split('/')[-1],
                file.read()
            )

        with open(self.dump_file_name, 'ab+') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

    def __load_dumped(self) -> list['FileData']:
        loaded = []
        with open(self.dump_file_name, 'rb') as file:
            try:
                object = pickle.load(file)
                loaded.append(object)
            except Exception:
                pass
        return loaded

    def restore(self) -> None:
        files = self.__load_dumped()
        for file in files:
            with open(file.path, 'w') as dest:
                dest.write(file.content)


class FileData:
    content: str
    path: str
    filename: str

    def __init__(self, path: str, filename: str, content: str) -> None:
        self.content = content
        self.filename = filename
        self.path = path


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'process':
        processer = Processer()
        processer.preprocess()
        print('Process')
    elif len(sys.argv) > 1 and sys.argv[1] == 'restore':
        print('Restore')
        processer = Processer()
        processer.restore()
    else:
        print([
            'Not passes action argument.',
            f'Common usage: python {sys.argv[0]} [process|restore]',
        ], sep='\n')
