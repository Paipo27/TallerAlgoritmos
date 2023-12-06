import numpy as np

# Definir la matriz de transición de probabilidades
prob_matrix = np.array([
    [[1, 0], [0, 0]],
    [[1, 0], [0, 0]],
    [[0.5, 0.5], [0, 1]],
])

# Estado actual
current_state = np.array([1, 0, 0])

# Función para marginalizar sobre un conjunto de elementos
def marginalize(matrix, indices_to_keep):
    return np.sum(matrix, axis=tuple(indices_to_keep))

# Función para calcular la probabilidad condicional dada la matriz de transición y el estado actual
def calculate_conditional_probability(prob_matrix, current_state):
    num_elements = len(current_state)
    result_matrix = prob_matrix.copy()

    # Marginalizar sobre el estado próximo
    for i in range(num_elements):
        indices_to_keep = [j for j in range(result_matrix.shape[2]) if j != i]
        result_matrix[:, :, i] = marginalize(result_matrix[:, :, i], indices_to_keep)

    # Marginalizar sobre el estado actual
    result_matrix = marginalize(result_matrix, [0])

    return result_matrix

# Calcular la probabilidad condicional para el ejemplo 2
conditional_prob_example2 = calculate_conditional_probability(prob_matrix, current_state)
print("Probabilidad condicional para el ejemplo 2:")
print(conditional_prob_example2)
