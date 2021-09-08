class WordsSolver:
    """
    Класс, который находит все слова на поле размером NxN

    Атрибуты
    -------
    dictionary : Dictionary
        Словарь всех слов
    board : Board
        Игровое поле
    min_length : int
        Минимальная длина слов, которые необходимо найти
    found_words : set
        Множество всех найденных слов (заполняется после применения метода find_words)

    Методы
    ------
    find_words()
        Находит все слова, длина которых не менее min_length, на игровом поле
    """
    def __init__(self, letter_list, min_length=3):
        """
        Параметры
        ---------
        letter_list : list[str]
            Список всех букв игрового поля слева направо сверху вниз
        min_length : int
            Минимальная длина слов, которые необходимо найти (По умолчанию 3)
        """
        self.dictionary = Dictionary('dictionary/words_rus.txt')
        self.board = Board(letter_list)
        self.min_length = min_length
        self.found_words = set()

    def find_words(self):
        """Находит все слова, длина которых не менее min_length, на игровом поле"""
        for row in range(self.board.side_length):
            for column in range(self.board.side_length):
                self._find_words(Word.new(row, column), row, column)

    def _find_words(self, word, row, column):
        """
        Находит все слова, длина которых не менее min_length, с позиции
        row, column

        Параметры
        ---------
        word : Word
            Формируемое слово
        row : int
            Номер строки
        column : int
            Номер столбца

        Возвращает
        ----------
        None
        """
        # добавляем текущую букву в формируемое слово
        word.add_letter(self.board[row][column], row, column)

        # добавляем формируемое слово на текущем шаге, если оно валидно
        if self._can_add_word(word):
            self.found_words.add(word.letter_sequence)

        for row, column in self._get_valid_coordinates(word, row, column):
            # если формируемое слово вместе со следующей буквой могут образовать слово,
            # то производим поиск слов дальше
            if self.dictionary.contains_subword(word.letter_sequence + self.board[row][column]):
                self._find_words(Word.new_from_word(word), row, column)

    def _can_add_word(self, word):
        """
        Проверяет, можем ли мы добавить текущее слово в итоговое множество

        Параметры
        ---------
        word : Word
            Формируемое слово

        Возвращает
        ----------
        bool
        """
        return len(word) >= self.min_length and self.dictionary.contains_word(word.letter_sequence)

    def _get_valid_coordinates(self, word, row, column):
        """
        Выдает значение координат следующей позиции на поле

        Параметры
        ---------
        word : Word
            Формируемое слово
        row : int
            Номер строки
        column : int
            Номер столбца

        Возвращает
        ----------
        tuple[int, int]
           Координаты следующей позиции на поле
        """
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if r in range(self.board.side_length) and c in range(self.board.side_length):
                    if (r, c) not in word.used_board_coordinates:
                        yield r, c


class Board:
    """
    Класс, который представляет игровое поле с буквами

    Атрибуты
    --------
    side_length : int
        Длина стороны игрового поля
    board : list[list[str]]
        Игровое поле (Квадратная матрица из букв)
    """
    def __init__(self, letter_list):
        """
        Параметры
        ---------
        letter_list : list[str]
            Список всех букв игрового поля слева направо сверху вниз
        """
        # Находим сторону игрового поля
        self.side_length = len(letter_list) ** .5
        # Проверяем, являются ли сторороны поля равными и целыми
        if self.side_length != int(self.side_length):
            raise Exception("Board must have equal sides! (4x4, 5x5, ...)")
        else:
            self.side_length = int(self.side_length)

        # Создаем игровое поле
        self.board = []
        # Заполняем поле буквами
        for i, row in enumerate(range(self.side_length)):
            # Добавляем очередную строку
            self.board.append([])
            for j, column in enumerate(range(self.side_length)):
                self.board[row].append(letter_list[i * self.side_length + j])

    def __getitem__(self, row):
        return self.board[row]


class Word:
    """
    Класс, который представляет формируемое слово

    Атрибуты
    --------
    letter_sequence : str
        Формируемое слово
    used_board_coordinates : set[tuple[int, int]]
        Множество всех используемых координат
    """
    def __init__(self):
        """
        Параметры
        ---------
        """
        self.letter_sequence = ''
        self.used_board_coordinates = set()

    @classmethod
    def new(cls, row, column):
        """
        Формирует новое пустое слово

        Параметры
        ---------
        row : int
            Номер строки
        column : int
            Номер столбца

        Возвращает
        ----------
        Word
           Новое формируемое слово
        """
        word = cls()
        # учитываем то, что текущая позиция на игровом
        # поле уже посещена
        word.used_board_coordinates.add((row, column))
        return word

    @classmethod
    def new_from_word(cls, word):
        """
        Формирует новое слово на основе переданного

        Параметры
        ---------
        word : Word
            Слово, на основе которого формируется новое

        Возвращает
        ----------
        Word
           Новое формируемое слово на основе переданного
        """
        new_word = cls()
        # формируемое слово вначале будет совпадать с переданным
        new_word.letter_sequence += word.letter_sequence
        # учитываем посещенные позиции игрового поля
        new_word.used_board_coordinates.update(word.used_board_coordinates)
        return new_word

    def add_letter(self, letter, row, column):
        """
        Добавляет букву к формируемому слову

        Параметры
        ---------
        letter : str
            Буква, которую мы добавляем в конец формируемого слова
        row : int
            Номер строки
        column : int
            Номер столбца

        Возвращает
        ----------
        None
        """
        self.letter_sequence += letter
        # позиция игрового поля, на которой была буква,
        # считается посещенной
        self.used_board_coordinates.add((row, column))

    def __str__(self):
        return self.letter_sequence

    def __len__(self):
        return len(self.letter_sequence)


class Dictionary:
    """
    Класс, представляющий словарь слов

    Атрибуты
    --------
    words : set[str]
        Множество всех слов
    subwords : set[str]
        Множество всех подслов, которые можно получить из слов
        путем взятия первых n букв, где 0 < n <= длина слова
    """
    def __init__(self, dictionary_file):
        """
        Параметры
        ---------
        dictionary_file : str
            Путь к словарю
        """
        self.words = set()
        self.subwords = set()
        # открываем файл со словарем
        word_file = open(dictionary_file, "r")
        # добавляем все слова и подслова
        for word in word_file.read().splitlines():
            self.words.add(word)
            for index in range(len(word) + 1):
                self.subwords.add(word[:index])

    def contains_word(self, word):
        """
        Проверяет наличие слова во множестве слов

        Параметры
        ---------
        word : str
            Слово, которое необходимо проверить

        Возвращает
        ----------
        bool
        """
        return word in self.words

    def contains_subword(self, subword):
        """
        Проверяет наличие подслова во множестве подслов

        Параметры
        ---------
        subword : str
            Подслово, которое необходимо проверить

        Возвращает
        ----------
        bool
        """
        return subword in self.subwords
