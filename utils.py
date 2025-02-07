def is_valid_imei(imei):
    """
    Проверяет IMEI на валидность с использованием алгоритма Луна.
    """
    if not imei.isdigit() or len(imei) != 15:
        return False

    digits = [int(d) for d in imei]
    checksum = 0
    parity = len(digits) % 2

    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0