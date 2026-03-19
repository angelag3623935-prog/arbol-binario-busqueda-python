import csv

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # INSERTAR
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_rec(self.raiz, valor)

    def _insertar_rec(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_rec(nodo.izquierda, valor)
        elif valor > nodo.valor:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_rec(nodo.derecha, valor)

    # BUSCAR
    def buscar(self, valor):
        return self._buscar_rec(self.raiz, valor)

    def _buscar_rec(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_rec(nodo.izquierda, valor)
        else:
            return self._buscar_rec(nodo.derecha, valor)

    # ELIMINAR
    def eliminar(self, valor):
        self.raiz = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_rec(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_rec(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            sucesor = self._min_valor(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_rec(nodo.derecha, sucesor.valor)

        return nodo

    def _min_valor(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    # CARGAR DESDE CSV
    def cargar_csv(self, ruta):
        try:
            with open(ruta, newline='') as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    for valor in fila:
                        try:
                            self.insertar(int(valor))
                        except ValueError:
                            pass
            print("Datos cargados correctamente.")
        except FileNotFoundError:
            print("Archivo no encontrado.")

    # GRAPHVIZ
    def generar_dot(self):
        dot = "digraph ABB {\n"
        dot += self._generar_dot_rec(self.raiz)
        dot += "}\n"
        return dot

    def _generar_dot_rec(self, nodo):
        if nodo is None:
            return ""
        resultado = ""
        if nodo.izquierda:
            resultado += f'    {nodo.valor} -> {nodo.izquierda.valor};\n'
            resultado += self._generar_dot_rec(nodo.izquierda)
        if nodo.derecha:
            resultado += f'    {nodo.valor} -> {nodo.derecha.valor};\n'
            resultado += self._generar_dot_rec(nodo.derecha)
        return resultado

    def guardar_graphviz(self, nombre_archivo="arbol.dot"):
        contenido = self.generar_dot()
        with open(nombre_archivo, "w") as f:
            f.write(contenido)
        print(f"Archivo Graphviz generado: {nombre_archivo}")

# =============================
# MENÚ CLI
# =============================

def menu():
    arbol = ArbolBinarioBusqueda()

    while True:
        print("\n--- MENÚ ABB ---")
        print("1. Insertar")
        print("2. Buscar")
        print("3. Eliminar")
        print("4. Cargar desde CSV")
        print("5. Generar Graphviz (.dot)")
        print("6. Salir")

        try:
            opcion = input("Seleccione una opción: ")
        except OSError:
            print("Error: Este entorno no permite entrada por teclado.")
            print("Ejecute el programa en su consola local (CMD, PowerShell o Terminal).")
            break

        if opcion == "1":
            try:
                valor = int(input("Ingrese número: "))
                arbol.insertar(valor)
                print("Insertado.")
            except:
                print("Entrada inválida.")

        elif opcion == "2":
            try:
                valor = int(input("Ingrese número a buscar: "))
                if arbol.buscar(valor):
                    print("Elemento encontrado.")
                else:
                    print("No encontrado.")
            except:
                print("Entrada inválida.")

        elif opcion == "3":
            try:
                valor = int(input("Ingrese número a eliminar: "))
                arbol.eliminar(valor)
                print("Eliminado.")
            except:
                print("Entrada inválida.")

        elif opcion == "4":
            ruta = input("Ingrese ruta del archivo CSV: ")
            arbol.cargar_csv(ruta)

        elif opcion == "5":
            nombre = input("Nombre del archivo (.dot): ")
            arbol.guardar_graphviz(nombre)

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")

# =============================
# MAIN
# =============================

if __name__ == "__main__":
    menu()
