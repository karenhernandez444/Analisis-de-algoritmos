import time
import random
import string
import matplotlib.pyplot as plt


# Algoritmo 1: Divide y Vencerás (MEJORADO)
def expand_center(s, left, right):
    """
    Expande desde un centro hacia afuera para encontrar el palíndromo más largo.

    Args:
        s (str): Cadena original
        left (int): Índice izquierdo inicial
        right (int): Índice derecho inicial

    Returns:
        str: Palíndromo expandido desde el centro
    """
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return s[left + 1:right]


def lps_divide_conquer(s):
    """
    Encuentra el palíndromo más largo usando Divide y Vencerás.

    Complejidad: O(n²) en el peor caso, O(1) en espacio

    Args:
        s (str): Cadena de entrada

    Returns:
        str: El palíndromo más largo encontrado
    """
    if not s or len(s) == 0:
        return ""

    longest = ""
    n = len(s)

    for i in range(n):
        # Caso 1: Centro único (palíndromos de longitud impar)
        p1 = expand_center(s, i, i)
        # Caso 2: Centro doble (palíndromos de longitud par)
        p2 = expand_center(s, i, i + 1)

        # Actualizar el palíndromo más largo
        if len(p1) > len(longest):
            longest = p1
        if len(p2) > len(longest):
            longest = p2

    return longest


# Algoritmo 2: Programación Dinámica (MEJORADO)
def lps_dynamic(s):
    """
    Encuentra el palíndromo más largo usando Programación Dinámica.

    Complejidad: O(n²) en tiempo, O(n²) en espacio

    Args:
        s (str): Cadena de entrada

    Returns:
        str: El palíndromo más largo encontrado
    """
    if not s or len(s) == 0:
        return ""

    n = len(s)
    # Caso base: cadena vacía o de un solo carácter
    if n == 1:
        return s

    # Matriz DP donde dp[i][j] indica si s[i:j+1] es palíndromo
    dp = [[False] * n for _ in range(n)]

    # Inicialización: todos los caracteres individuales son palíndromos
    for i in range(n):
        dp[i][i] = True

    start = 0
    max_len = 1

    # Verificar palíndromos de longitud 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start = i
            max_len = 2

    # Verificar palíndromos de longitud 3 o mayor
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Un substring es palíndromo si los extremos son iguales
            # y el substring interno también es palíndromo
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                start = i
                max_len = length

    return s[start:start + max_len]


# FUNCIONES DE PRUEBA Y VALIDACIÓN
def test_algorithms():
    """
    Prueba ambos algoritmos con casos de prueba conocidos.
    """
    test_cases = [
        "babad",  # Esperado: "bab" o "aba"
        "cbbd",  # Esperado: "bb"
        "a",  # Esperado: "a"
        "ac",  # Esperado: "a" o "c"
        "racecar",  # Esperado: "racecar"
        "abcba",  # Esperado: "abcba"
        "aaa",  # Esperado: "aaa"
        "abcd",  # Esperado: "a" (cualquier carácter)
        "",  # Esperado: ""
        "reconocer",  # Esperado: "reconocer"
        "anilina",  # Esperado: "anilina"
        "lobas",  # Esperado: "l"
        "karen",  # Esperado: "k"
        "valentin",  # Esperado: "v"
        "sofia",  # Esperado: "s"
    ]

    print(" PRUEBAS DE VALIDACIÓN")
    print("=" * 60)

    for test_str in test_cases:
        result_dv = lps_divide_conquer(test_str)
        result_dp = lps_dynamic(test_str)

        status = "COINCIDE" if result_dv == result_dp else "NO COINCIDE"
        print(f"{status} Cadena: '{test_str}'")
        print(f"   Divide y Vencerás: '{result_dv}'")
        print(f"   Programación Dinámica: '{result_dp}'")
        print()


def generate_test_string(length, palindromic=False):
    """
    Genera cadenas de prueba, opcionalmente con palíndromos incorporados.

    Args:
        length (int): Longitud de la cadena
        palindromic (bool): Si debe incluir un palíndromo grande

    Returns:
        str: Cadena de prueba generada
    """
    if palindromic and length >= 10:
        # Generar un palíndromo en medio de la cadena
        pal_size = length // 2
        base = ''.join(random.choices(string.ascii_lowercase, k=pal_size))
        palindrome = base + base[::-1]

        # Rellenar si es necesario
        if len(palindrome) < length:
            padding = ''.join(random.choices(string.ascii_lowercase, k=length - len(palindrome)))
            return padding + palindrome
        return palindrome[:length]
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=length))


# COMPARATIVA MEJORADA
def performance_comparison():
    """
    Compara el desempeño de ambos algoritmos con diferentes tamaños de entrada.
    """
    # Rangos más amplios para mejor visualización
    sizes = list(range(100, 1001, 100))  # 100, 200, ..., 1000
    times_divide = []
    times_dynamic = []

    print(" EJECUTANDO COMPARATIVA DE DESEMPEÑO")
    print("=" * 60)
    print(f"{'Tamaño':<8} {'DyV (s)':<12} {'PD (s)':<12} {'DyV/PD':<10}")
    print("-" * 60)

    for size in sizes:
        # Generar cadena de prueba (50% con palíndromos grandes)
        test_str = generate_test_string(size, palindromic=random.choice([True, False]))

        # Medir tiempo Divide y Vencerás
        start_time = time.perf_counter()
        result_dv = lps_divide_conquer(test_str)
        time_dv = time.perf_counter() - start_time
        times_divide.append(time_dv)

        # Medir tiempo Programación Dinámica
        start_time = time.perf_counter()
        result_dp = lps_dynamic(test_str)
        time_dp = time.perf_counter() - start_time
        times_dynamic.append(time_dp)

        # Verificar que ambos algoritmos den el mismo resultado
        if result_dv != result_dp:
            print(f"  DISCREPANCIA en tamaño {size}: '{result_dv}' vs '{result_dp}'")

        ratio = time_dv / time_dp if time_dp > 0 else float('inf')
        print(f"{size:<8} {time_dv:<12.6f} {time_dp:<12.6f} {ratio:<10.2f}")

    return sizes, times_divide, times_dynamic


def plot_comparison(sizes, times_divide, times_dynamic):
    """
    Genera gráficas comparativas de desempeño.

    Args:
        sizes (list): Lista de tamaños de entrada
        times_divide (list): Tiempos de Divide y Vencerás
        times_dynamic (list): Tiempos de Programación Dinámica
    """
    plt.figure(figsize=(12, 6))

    # Gráfica principal
    plt.plot(sizes, times_divide, 'o-', label='Divide y Vencerás (O(n²))', linewidth=2, markersize=6)
    plt.plot(sizes, times_dynamic, 's-', label='Programación Dinámica (O(n²))', linewidth=2, markersize=6)
    plt.xlabel('Tamaño de la cadena (n)')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title('Comparativa de Desempeño: Encontrar el Palíndromo Más Largo')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparativa_palindromos.png', dpi=300, bbox_inches='tight')
    plt.show()


# EJECUCIÓN PRINCIPAL
if  __name__ == "__main__":
    print(" ANÁLISIS DE ALGORITMOS PARA PALÍNDROMO MÁS LARGO")
    print("=" * 60)

    # 1. Validar que los algoritmos funcionen correctamente
    test_algorithms()

    # 2. Ejecutar comparativa de desempeño
    sizes, times_divide, times_dynamic = performance_comparison()

    # 3. Generar gráficas
    plot_comparison(sizes, times_divide, times_dynamic)

    # 4. Análisis final
    print("\n RESUMEN DE RESULTADOS:")
    print(f"• Tamaño máximo probado: {sizes[-1]} caracteres")
    print(f"• Tiempo promedio DyV: {sum(times_divide) / len(times_divide):.6f}s")
    print(f"• Tiempo promedio PD: {sum(times_dynamic) / len(times_dynamic):.6f}s")

    avg_ratio = sum(times_divide) / sum(times_dynamic)
    print(f"• Ratio promedio DyV/PD: {avg_ratio:.2f}")

    if avg_ratio > 1:
        print("• Conclusión: Programación Dinámica es más eficiente en promedio")
    else:
        print("• Conclusión: Divide y Vencerás es más eficiente en promedio")