"""
Non-interactive test for input length validation.
"""
import gestor_inventario as g

a100 = "a" * 100
a101 = "a" * 101

print("len 100 valid:", g.validar_nombre(a100))
print("len 101 valid:", g.validar_nombre(a101))
