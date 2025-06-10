def isValidCpf(cpf: int):
    total_of_digits = 11
    cpf = ''.join(filter(str.isdigit, cpf))  

    if len(cpf) != total_of_digits or cpf == cpf[0] * total_of_digits: 
        return False

    digits_multiplication = 10
    total = 0 
    for i in range(9):
        total += int(cpf[i]) * digits_multiplication
        digits_multiplication -= 1

    verification = (total*10) % total_of_digits

    if(verification == int(cpf[9])):
        return True

    if(verification != cpf[9]):
        return False