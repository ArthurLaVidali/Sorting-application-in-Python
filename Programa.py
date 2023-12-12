import ast
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTextEdit, QVBoxLayout, QFileDialog, QComboBox


#Implementação da árvore
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key


def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if key < root.value:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root


def inorder_traversal(root):
    result = []
    if root:
        result += inorder_traversal(root.left)
        result.append(root.value)
        result += inorder_traversal(root.right)
    return result


#Implementação do QuickSort
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


class SortingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ordenação de Números')
        self.setGeometry(100, 100, 400, 400)

        # Botão para abrir o arquivo
        open_button = QPushButton('Abrir Arquivo', self)
        open_button.clicked.connect(self.open_file)

        # Área de texto para exibir a lista
        self.entry = QTextEdit(self)
        self.entry.setPlaceholderText("Insira a lista aqui")

        # Combo Box para escolher o algoritmo
        algorithm_label = QLabel("Escolha o algoritmo:", self)
        self.algorithm_options = ["---Escolha um Algoritmo--","Sorted(TimSort)", "QuickSort", "Árvore"]
        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.addItems(self.algorithm_options)

        # Botão para ordenar e salvar
        sort_button = QPushButton('Ordenar e Salvar', self)
        sort_button.clicked.connect(self.sort_and_save)

        # Rótulo para exibir resultados
        self.result_label = QLabel(self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(open_button)
        layout.addWidget(self.entry)
        layout.addWidget(algorithm_label)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(sort_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def open_file(self):
        options = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Arquivos de Texto (*.txt)")
        file_path = options[0]
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                try:
                    self.numbers = ast.literal_eval(content)
                    self.entry.clear()
                    self.entry.insertPlainText(str(self.numbers))
                except (ValueError, SyntaxError):
                    self.result_label.setText("Formato do arquivo inválido!")

    def sort_and_save(self):
        try:
            numbers = ast.literal_eval(self.entry.toPlainText())
            selected_algorithm = self.algorithm_combo.currentText()

            if selected_algorithm == "Sorted(TimSort)":
                sorted_numbers = sorted(numbers)
            elif selected_algorithm == "QuickSort":
                sorted_numbers = quicksort(numbers)
            elif selected_algorithm == "Árvore":
                self.root = None  # Resetar a árvore para cada operação
                for number in numbers:
                    self.root = insert(self.root, number)
                sorted_numbers = inorder_traversal(self.root)
            else:
                self.result_label.setText("Selecione um algoritmo válido!")
                return

            save_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Arquivos de Texto (*.txt)")
            if save_path:
                with open(save_path, 'w') as file:
                    file.write(str(sorted_numbers))
                self.result_label.setText(f"Arquivo salvo em: {save_path}")
        except (ValueError, SyntaxError):
            self.result_label.setText("Formato da lista inválido!")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SortingApp()
    window.show()
    sys.exit(app.exec_())
