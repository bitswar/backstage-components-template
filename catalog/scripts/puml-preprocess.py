# !/usr/bin/env python3
import os
import pickle
import sys

extensions = [".puml"]


class Env:
    include_folders: list[str]
    src_folder: str

    def __init__(self) -> None:
        self.__setup_envs()

    def __setup_envs(self) -> None:
        env_dict = self.__get_env_dict()

        self.include_folders = self.__get_env_from_dict(
            env_dict, 'PUML_INCLUDE_DIR'
        )

        self.env_src_dir = self.__get_env_from_dict(
            env_dict, 'PUML_ROOT_DIR'
        )

    def __get_env_from_dict(self, envs: dict[str, str], key: str) -> str:
        try:
            return envs[key]
        except KeyError:
            raise KeyError(f'Environment variable {key} not found')

    def __get_env_dict(self) -> dict[str, str]:
        envs = self.__get_dirty_env_dict()
        for key in envs:
            envs[key] = self.__sanitize_path(envs[key])
        return envs

    def __get_dirty_env_dict(self) -> dict[str, str]:
        envs = {}
        with open('.env', 'r') as file:
            for line in file.read().split('\n'):
                splitted_line = line.split('=')
                if len(splitted_line) < 2 or len(splitted_line) > 2:
                    continue

                key, value = splitted_line
                if not key == '' and not value == '':
                    envs[key] = value

        return envs

    def __sanitize_path(self, path: str) -> str:
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        if path[-1] == '/':
            path = path[:-1]
        return path

    def __str__(self) -> str:
        return f'Env: {self.include_folders}, {self.env_src_dir}'

    def __repr__(self) -> str:
        return self.__str__()


class Processer:
    dump_file_name = "dump.pkl"
    env = Env()

    def preprocess(self):
        diagrams, utils = self.__get_diagrams_dict_and_utils()

        for path in diagrams:
            self.__dump_sources(path)
            print('Dumped: ', path)

            self.__preprocess_file(path, utils)
            print('Pre-processed: ', path)

    def __get_diagrams_dict_and_utils(self) -> \
            tuple[dict[str, str], dict[str, str]]:
        diagrams = self.__get_all_diagram_files(self.env.src_folder)
        utils = {}
        for folder in self.env.include_folders:
            utils.update(self.__get_all_diagram_files(folder))

        for u in utils.keys():
            for i in diagrams.keys():
                if i == u:
                    diagrams.pop(i)
                    break

        return (diagrams.values(), utils)

    def __get_all_diagram_files(self, start_path: str) -> dict[str, str]:
        result = {}
        for item in os.walk(start_path):
            for file in item[2]:
                for ext in extensions:
                    if file.find(ext) == -1:
                        continue
                    result[file] = f"{item[0]}/{file}"
        return result

    def __preprocess_file(self, filepath: str, utils: dict[str, str]) -> None:
        content = ""
        with open(filepath, "r") as file:
            content = file.read().split("\n")

        for line in range(len(content)):
            for key in utils:
                if content[line].find(key) == -1:
                    continue

                with open(utils[key], "r") as template:
                    template_line = template.read().split("\n")[1:-1]
                    content[line] = "\n".join(template_line)

        with open(filepath, "w") as file:
            file.write("\n".join(content))

    def __dump_sources(self, path: str) -> None:
        data: FileData
        with open(path, "r") as file:
            data = FileData(path, path.split("/")[-1], file.read())

        with open(self.dump_file_name, "ab+") as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

    def __load_dumped(self) -> list["FileData"]:
        loaded = []
        diagrams, _ = self.__get_diagrams_dict_and_utils()
        try:
            with open(self.dump_file_name, "rb") as file:
                for _ in range(len(diagrams)):
                    object = pickle.load(file)
                    loaded.append(object)
        except FileNotFoundError:
            print('File not found')
        return loaded

    def restore(self) -> None:
        files = self.__load_dumped()
        for file in files:
            with open(file.path, "w") as dest:
                dest.write(file.content)
                print('Restored: ', file.path)


class FileData:
    content: str
    path: str
    filename: str

    def __init__(self, path: str, filename: str, content: str) -> None:
        self.content = content
        self.filename = filename
        self.path = path


if __name__ == "__main__":
    envs = Env()
    if len(sys.argv) > 1 and sys.argv[1] == "process":
        processer = Processer()
        processer.preprocess()
        print("Process")
    elif len(sys.argv) > 1 and sys.argv[1] == "restore":
        print("Restore")
        processer = Processer()
        processer.restore()
    else:
        print(
            [
                "Not passes action argument.",
                f"Common usage: python {sys.argv[0]} [process|restore]",
            ],
            sep="\n",
        )
