
import sys

def parsear_linea_gramatica(linea):
    """
    Parsea una línea de gramática (ej: "A -> Aa | b") en las estructuras
    de datos internas (gramática_dict, no_terminales_orden_lista).
    Retorna (None, None) si hay error.
    """
    gramatica = {}
    no_terminales_orden = []

    try:
        linea = linea.strip()
        partes = linea.split(' -> ')
        if len(partes) != 2:
            raise ValueError("Formato inválido. Debe ser 'NT -> ...'")

        no_terminal = partes[0].strip()
        if not no_terminal or ' ' in no_terminal or not no_terminal.isupper():
            raise ValueError(f"No terminal inválido: '{no_terminal}'")

        producciones_str = partes[1].split()
        if not producciones_str:
            raise ValueError("No se encontraron producciones.")

        producciones = []
        for prod in producciones_str:
            if prod == '|':
                continue
            # 'e' o 'E' (para epsilon) se trata como un símbolo
            if prod.lower() == 'e' or prod == 'Îµ':
                 producciones.append(['e']) # Usar 'e' internamente
            else:
                producciones.append(list(prod))  # 'Aa' -> ['A', 'a']

        gramatica[no_terminal] = producciones
        no_terminales_orden.append(no_terminal)

        return gramatica, no_terminales_orden

    except Exception as e:
        print(f"Error al parsear la gramática: {e}", file=sys.stderr)
        return None, None  # Indicar fallo


def run_gramatica(linea_gramatica):
    """
    Procesa una sola línea de gramática, elimina la recursión
    y muestra la salida.
    """
    print("=" * 60)
    print(f"INPUT: {linea_gramatica}")
    print("=" * 60)

    # 1. Parsear la línea
    gramatica, no_terminales_orden = parsear_linea_gramatica(linea_gramatica)

    if gramatica is None:
        print("OUTPUT:\nError en el formato de entrada.")
        print("=" * 60)
        return

    # 2. Ejecutar el algoritmo
    # Nota: Al procesar solo una línea, el algoritmo completo
    # (que maneja recursión indirecta) se simplifica a solo
    # eliminar la recursión inmediata para ESE no terminal,
    # ya que los loops 'j' en 'eliminar_recursion_izquierda' no se ejecutan.
    # Esto es consistente con el comportamiento del script original.
    gramatica_sin_recursion = eliminar_recursion_izquierda(gramatica, no_terminales_orden)

    # 3. Formatear y mostrar salida
    salida = formatear_salida(gramatica_sin_recursion, no_terminales_orden)

    print("OUTPUT:")
    print(salida)
    print("=" * 60)


def iniciar_modo_interactivo():
    """Modo interactivo que procesa una línea de gramática a la vez."""
    print("=" * 60)
    print("ELIMINACIÓN DE RECURSIÓN IZQUIERDA (Modo Interactivo)")
    print("=" * 60)
    print("\nEjemplos de input válido (una regla por línea):")
    print("  A -> Aa | b")
    print("  S -> Sa | Sb | c | e")
    print("  E -> E+T | T")
    print("\nEscribe 'q' o 'quit' para salir.")
    print()

    while True:
        linea_gramatica = input("Ingresa la gramática: ").strip()

        if linea_gramatica.lower() in ['q', 'quit', 'salir']:
            print("\n¡Hasta luego!")
            break

        if linea_gramatica:
            print()
            run_gramatica(linea_gramatica)
            print()
        else:
            print("No ingresaste nada. Intenta de nuevo o 'q' para salir.")
            print()


# --- Lógica Central del Algoritmo (Prácticamente sin cambios) ---

def tiene_recursion_inmediata(producciones, no_terminal):
    """
    Verifica si un no terminal tiene recursión inmediata por la izquierda.
    Retorna True si alguna producción comienza con el mismo no terminal.
    """
    for prod in producciones:
        if len(prod) > 0 and prod[0] == no_terminal:
            return True
    return False


def eliminar_recursion_inmediata(gramatica, no_terminal, no_terminales_usados):
    """
    Elimina la recursión inmediata por la izquierda de un no terminal.
    Si A -> Aα1 | Aα2 | ... | Aαm | β1 | β2 | ... | βn
    Lo convierte en:
    A -> β1A' | β2A' | ... | βnA'
    A' -> α1A' | α2A' | ... | αmA' | ε
    """
    producciones = gramatica[no_terminal]

    recursivas = []
    no_recursivas = []

    for prod in producciones:
        if len(prod) > 0 and prod[0] == no_terminal:
            recursivas.append(prod[1:])  # Guarda el 'α'
        else:
            no_recursivas.append(prod)  # Guarda el 'β'

    if len(recursivas) == 0:
        return  # No hay recursión inmediata

    # Genera un nuevo NT (ej: A')
    nuevo_no_terminal = generar_nuevo_no_terminal(no_terminales_usados)
    no_terminales_usados.add(nuevo_no_terminal)

    # Crear nuevas producciones para A (A -> βA')
    nuevas_producciones_A = []
    if no_recursivas:
        for prod in no_recursivas:
            if prod == ['e']: # Si β es epsilon, A -> A'
                nuevas_producciones_A.append([nuevo_no_terminal])
            else:
                nuevas_producciones_A.append(prod + [nuevo_no_terminal])
    else:
        # Si no hay β (ej: A -> Aα), la única regla es A -> A'
        nuevas_producciones_A.append([nuevo_no_terminal])

    gramatica[no_terminal] = nuevas_producciones_A

    # Crear producciones para A' (A' -> αA' | ε)
    producciones_A_prima = []
    for prod in recursivas:
        if not prod: # Si α era vacío (ej: A -> A)
            producciones_A_prima.append([nuevo_no_terminal])
        else:
            producciones_A_prima.append(prod + [nuevo_no_terminal])
    
    producciones_A_prima.append(['e'])  # A' -> ε

    gramatica[nuevo_no_terminal] = producciones_A_prima


def generar_nuevo_no_terminal(usados):
    """
    Genera un nuevo símbolo no terminal que no haya sido usado.
    Usa letras mayúsculas del alfabeto en orden.
    Si se acaban, usa A1, A2...
    """
    for letra in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letra not in usados:
            return letra
    
    # Si se acaban las letras simples
    for i in range(1, 100):
        for letra in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            nuevo_nt = f"{letra}{i}"
            if nuevo_nt not in usados:
                return nuevo_nt
                
    raise Exception("Se superó el límite de no terminales generados.")


def sustituir_producciones(gramatica, no_terminal_i, no_terminal_j):
    """
    Sustituye las producciones de la forma Ai -> Aj γ
    por Ai -> δ1 γ | δ2 γ | ... | δk γ
    donde Aj -> δ1 | δ2 | ... | δk son todas las producciones de Aj.
    """
    # En el modo de una línea, gramatica[no_terminal_j] no existirá.
    # Esta función solo es relevante para gramáticas multi-línea
    # procesadas todas juntas.
    if no_terminal_j not in gramatica:
        return

    producciones_i = gramatica[no_terminal_i]
    producciones_j = gramatica[no_terminal_j]

    nuevas_producciones = []

    for prod_i in producciones_i:
        if len(prod_i) > 0 and prod_i[0] == no_terminal_j:
            gamma = prod_i[1:]
            for prod_j in producciones_j:
                if prod_j == ['e']:
                    # Si Aj -> e, entonces Ai -> γ
                    nuevas_producciones.append(gamma if gamma else ['e'])
                else:
                    nuevas_producciones.append(prod_j + gamma)
        else:
            nuevas_producciones.append(prod_i)

    gramatica[no_terminal_i] = nuevas_producciones


def eliminar_recursion_izquierda(gramatica, no_terminales_orden):
    """
    Implementa el algoritmo completo de eliminación de recursión por la izquierda.
    """
    
    # Corrección: El set de 'usados' debe incluir TODOS los símbolos
    # (izq y der) para evitar colisiones al generar nuevos NT.
    # El original solo usaba set(no_terminales_orden), lo cual era un bug.
    no_terminales_usados = set()
    for nt in gramatica.keys():
        no_terminales_usados.add(nt)
    for producciones_lista in gramatica.values():
        for prod in producciones_lista:
            for simbolo in prod:
                if 'A' <= simbolo <= 'Z':  # Asume NTs son mayúsculas
                    no_terminales_usados.add(simbolo)

    n = len(no_terminales_orden)

    for i in range(n):
        no_terminal_i = no_terminales_orden[i]

        for j in range(i):
            no_terminal_j = no_terminales_orden[j]
            # (Este loop no se ejecutará en modo de una línea)
            sustituir_producciones(gramatica, no_terminal_i, no_terminal_j)

        if tiene_recursion_inmediata(gramatica[no_terminal_i], no_terminal_i):
            eliminar_recursion_inmediata(gramatica, no_terminal_i, no_terminales_usados)

    return gramatica


def formatear_salida(gramatica, no_terminales_orden):
    """
    Formatea la gramática resultante para imprimirla según el formato requerido.
    Formato: <no_terminal> -> <prod1> <prod2> ... <prodn>
    """
    resultado = []

    # Muestra primero el no-terminal original
    todos_no_terminales = []
    for nt in no_terminales_orden:
        if nt in gramatica:
            todos_no_terminales.append(nt)

    # Luego añade los nuevos no-terminales generados, ordenados
    for nt in sorted(gramatica.keys()):
        if nt not in todos_no_terminales:
            todos_no_terminales.append(nt)

    for no_terminal in todos_no_terminales:
        if no_terminal not in gramatica:
            continue

        producciones = gramatica[no_terminal]
        prods_str = []

        for prod in producciones:
            prods_str.append(''.join(prod))

        # El formato original usaba espacios, no '|'
        linea = f"{no_terminal} -> {' '.join(prods_str)}"
        resultado.append(linea)

    return '\n'.join(resultado)


# --- Punto de Entrada (Modificado) ---

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo 1: Pasaste la gramática como argumento
        # Une todos los argumentos en caso de que la gramática tuviera espacios
        # Ej: python script.py "A -> A a | b"
        linea_gramatica = " ".join(sys.argv[1:])
        run_gramatica(linea_gramatica)
    else:
        # Modo 2: Interactivo
        iniciar_modo_interactivo()