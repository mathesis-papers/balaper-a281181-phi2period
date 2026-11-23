import argparse
from hashlib import sha256
import json
from math import factorial
from pathlib import Path

from verify import exact_column, modular_values, ode_coefficients, power, totient


def verify_siblings():
    specifications = [
        ('A281432', 5, 1, 0, [1, 1, 21, 1341, 173961, 38032281, 12572222301, 5853055718421]),
        ('A281439', 7, 8, 1, [1, 8, 400, 50240, 11785600, 4441856000, 2454008012800, 1868290095104000]),
    ]
    results = []
    for sequence, parameter, exponent, offset, source_terms in specifications:
        values = exact_column(parameter, exponent, 256)
        assert values[:len(source_terms)] == source_terms
        cosine, sine = ode_coefficients(parameter, 27)
        series = power(cosine, exponent, 27)
        for index in range(13):
            assert series[2 * index] * factorial(2 * index) == values[index]
        if sequence == 'A281439':
            for index in range(13):
                assert sine[2 * index + 1] * factorial(2 * index + 1) == values[index]
        certificates = []
        for modulus in range(2, 25):
            period = totient(modulus) ** 2
            start = modulus ** 2
            residues = modular_values(parameter, exponent, modulus, max(64, start + period + modulus))
            assert residues[:65] == [value % modulus for value in values[:65]]
            differences = [(residues[index + period] - residues[index]) % modulus for index in range(start, start + modulus)]
            assert differences == [0] * modulus
            certificates.append({'modulus': modulus, 'period': period, 'source_start': start + offset, 'zero_differences': differences})
        results.append({'sequence': sequence, 'parameter': parameter, 'exponent': exponent, 'source_offset': offset, 'source_initial_terms': len(source_terms), 'ode_agreement_column_indices': [0, 12], 'exact_column_index': 256, 'exact_value_sha256': sha256(str(values[256]).encode()).hexdigest(), 'all_index_period_certificates': certificates})
    return {'schema_version': 1, 'status': 'pass', 'arithmetic': 'exact integers and rational numbers', 'sequences': results, 'scope': 'The finite-dimensional certificates imply the stated tail congruences by the Cayley-Hamilton argument in note.tex; the written theorem covers every modulus.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    arguments.output.write_text(json.dumps(verify_siblings(), indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
