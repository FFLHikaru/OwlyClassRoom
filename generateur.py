import matplotlib.pyplot as plt

# Formule LaTeX à afficher
latex_formula = r'$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$'

# Créer une figure
plt.figure(figsize=(4, 2))

# Ajouter le texte LaTeX directement avec le moteur TeX
plt.text(0.5, 0.5, latex_formula, fontsize=16, ha='center', va='center', color='black', usetex=True)

# Masquer les axes
plt.axis("off")

# Afficher la figure
plt.show()
