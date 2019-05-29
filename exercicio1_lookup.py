#Definindo as regioes geopoliticas
def lookup_regiao(estado):
  norte = ['AC', 'RO', 'AM', 'RR', 'PA', 'AP', 'TO']
  nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
  centro_oeste =['MT', 'MS', 'GO', 'DF']
  sudeste = ['MG', 'ES', 'RJ', 'SP']
  sul = ['PR', 'SC', 'RS']

  if estado in norte :
    return "Norte"
  elif estado in nordeste:
    return "Nordeste"
  elif estado in centro_oeste:
    return "Centro-Oeste"
  elif estado in sudeste:
    return "Sudeste"
  elif estado in sul:
    return "Sul"