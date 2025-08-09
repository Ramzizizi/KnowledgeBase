# KnowlageBase
Pet-project for a custom and dynamic knowledge base

### Шаги развертывания

#### Установка зависимостей

##### Pyenv

1. Проверить что есть pyenv. Если его нет, то установить. Вот команда для Ubuntu:
   ```bash
   curl -fsSL https://pyenv.run | bash
   ```

2. Подготовка окружения 
   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
   ```
   
   Если есть `~/.profile`, то запустить команду:
   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
   echo 'eval "$(pyenv init - bash)"' >> ~/.profile
   ```
   
   Если есть `~/.bash_profile`, то запустить команду:
   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
   echo 'eval "$(pyenv init - bash)"' >> ~/.bash_profile
   ```

3. Перезапустить shell с командой: `exec "$SHELL"`

4. Установить зависимости для дальнейшего скачивания версий python (команда для ubuntu)
   ```bash
   sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev curl git \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
   ```

##### Установка необходимой версии python

1. Установка версии
   ```bash
   pyenv install 3.13
   ```
2. внутри проекта прогнать команду `pyenv local 3.13` чтобы использовалась конкретная версия python для проекта

##### Poetry
1. Установка poetry 
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Настраивание конфига, чтобы виртуальное окружение создавалось внутри проекта
   ```bash
   poetry config virtualenvs.create true
   poetry config virtualenvs.in-project true
   ```
3. Установка зависимостей в poetry 
   ```bash
   poetry install --only=main
   ```
   
#### Формирование виртуального окружения
```shell
`poetry env activate`
```

#### Запуск

```shell
cd src
export PYTHONPATH=$PWD
python3 main.py
```