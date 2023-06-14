# Sample IBAN account numbers.
# -----------------------------
# BE31435411161155
# CH5108686001256515001
# GB35MIDL40253432144670
# GB33BUKB20201555555555
# Dictionaries - Refer to ISO 7064 mod 97-10
letter_dic = {
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 18,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "O": 24,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "U": 30,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
}

# ISO 3166-1 alpha-2 country code
country_dic = {
    "AL": [28, "Albania"],
    "AD": [24, "Andorra"],
    "AT": [20, "Austria"],
    "BE": [16, "Belgium"],
    "BA": [20, "Bosnia"],
    "BG": [22, "Bulgaria"],
    "HR": [21, "Croatia"],
    "CY": [28, "Cyprus"],
    "CZ": [24, "Czech Republic"],
    "DK": [18, "Denmark"],
    "EE": [20, "Estonia"],
    "FO": [18, "Faroe Islands"],
    "FI": [18, "Finland"],
    "FR": [27, "France"],
    "DE": [22, "Germany"],
    "GI": [23, "Gibraltar"],
    "GR": [27, "Greece"],
    "GL": [18, "Greenland"],
    "HU": [28, "Hungary"],
    "IS": [26, "Iceland"],
    "IE": [22, "Ireland"],
    "IL": [23, "Israel"],
    "IT": [27, "Italy"],
    "LV": [21, "Latvia"],
    "LI": [21, "Liechtenstein"],
    "LT": [20, "Lithuania"],
    "LU": [20, "Luxembourg"],
    "MK": [19, "Macedonia"],
    "MT": [31, "Malta"],
    "MU": [30, "Mauritius"],
    "MC": [27, "Monaco"],
    "ME": [22, "Montenegro"],
    "NL": [18, "Netherlands"],
    "NO": [15, "Northern Ireland"],
    "PL": [28, "Poland"],
    "PT": [25, "Portugal"],
    "RO": [24, "Romania"],
    "SM": [27, "San Marino"],
    "SA": [24, "Saudi Arabia"],
    "RS": [22, "Serbia"],
    "SK": [24, "Slovakia"],
    "SI": [19, "Slovenia"],
    "ES": [24, "Spain"],
    "SE": [24, "Sweden"],
    "CH": [21, "Switzerland"],
    "TR": [26, "Turkey"],
    "TN": [24, "Tunisia"],
    "GB": [22, "United Kingdom"],
}


def iban_check(IBAN: int):
    IBAN = "".join(IBAN.split())
    print(IBAN, "- ", end="")

    prefix = IBAN[:2].upper()
    if prefix.isalpha():
        if prefix not in country_dic.keys():
            return f"Error no such country code {prefix}"

        goodlen = country_dic.get(prefix)[0]
        if len(IBAN) != goodlen:
            return f" Incorrect length {len(IBAN)} for country {prefix} with {goodlen}"

        country_code = "".join(str(letter_dic.get(x)) for x in list(prefix))
        checksum = IBAN[2:4]
        acc_num = IBAN[4:]
        if not acc_num.isdigit():
            acc_num = "".join(str(letter_dic.get(x, x)) for x in acc_num)
        IBAN_rev = acc_num + country_code + checksum
        print(IBAN_rev, end="")
        if int(IBAN_rev) % 97 == 1:
            return " - Correct account number."
        else:
            return " - Incorrect account number."
    else:
        return "ERROR: Need correct IBAN format starting with country, ie GB35MIDL40253432144670."


if __name__ == "__main__":
    print(iban_check("PL 77 1600 1462 1891 2670 5005 4475"))  # Wrong acc
    print(iban_check("GB 35 MIDL 4025 3432 1446 70"))  # OK
    print(iban_check("DE 46 1090 2851 0000 0001 4292 2866"))  # Wrong prefix
