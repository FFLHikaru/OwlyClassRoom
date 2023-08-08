import matplotlib.pyplot as plt

# Formule LaTeX à afficher
latex_formula = r'$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$'

# Créer une figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Ajouter le texte LaTeX à l'axe
ax.text(0.5, 0.5, latex_formula, fontsize=16, ha='center', va='center', color='black', usetex=True)

# Masquer les axes
ax.axis("off")

# Afficher la figure
plt.show()
