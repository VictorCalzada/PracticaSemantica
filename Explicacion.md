## Explicacion 


```python
patron1 = r'^[a-z]*$'
if re.search(patron1,'estoesvalido'):
    print ("Ejercicio 1.1: OK")
if not re.search(patron1,'AQUI NO ESTA (de seguro)'):
    print ("Ejercicio 1.2: OK")
```
