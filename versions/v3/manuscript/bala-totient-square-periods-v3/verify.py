import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import comb, factorial, gcd
from pathlib import Path


def multiply(left, right, limit, modulus=None):
    result = [0] * limit
    for left_degree, left_value in enumerate(left[:limit]):
        if not left_value:
            continue
        for right_degree, right_value in enumerate(right[:limit - left_degree]):
            result[left_degree + right_degree] += left_value * right_value
    if modulus:
        result = [value % modulus for value in result]
    return result


def power(series, exponent, limit):
    result = [1] + [0] * (limit - 1)
    for factor in range(exponent):
        result = multiply(result, series, limit)
    return result


def ode_coefficients(parameter, limit):
    cosine = [Fraction(0)] * limit
    sine = [Fraction(0)] * limit
    cosine[0] = Fraction(1)
    for degree in range(limit - 1):
        cosine_power = power(cosine, parameter, degree + 1)
        cosine[degree + 1] = multiply(cosine_power, sine, degree + 1)[degree] / (degree + 1)
        sine[degree + 1] = power(cosine, parameter + 1, degree + 1)[degree] / (degree + 1)
    return cosine, sine


def exact_column(parameter, exponent, last_index):
    state = {exponent: 1}
    values = []
    for index in range(last_index + 1):
        values.append(sum(state.values()))
        next_state = {}
        for degree, coefficient in state.items():
            if not degree:
                continue
            upper = degree + 2 * parameter
            lower = upper - 2
            next_state[upper] = next_state.get(upper, 0) + coefficient * degree * (degree + parameter)
            next_state[lower] = next_state.get(lower, 0) - coefficient * degree * (degree + parameter - 1)
        state = next_state
    return values


def shifted_operator(parameter, modulus):
    principal = [comb(2 * parameter + 2, degree) - (comb(2 * parameter, degree) if degree <= 2 * parameter else 0) for degree in range(2 * parameter + 3)]
    drift = [(parameter + 1) * comb(2 * parameter + 1, degree) - (parameter * comb(2 * parameter - 1, degree) if degree <= 2 * parameter - 1 else 0) for degree in range(2 * parameter + 2)]

    def apply(state):
        first = [(degree + 1) * state[degree + 1] for degree in range(modulus - 1)]
        second = [(degree + 2) * (degree + 1) * state[degree + 2] for degree in range(modulus - 2)]
        principal_part = multiply(principal, second, modulus, modulus)
        drift_part = multiply(drift, first, modulus, modulus)
        return [(left + right) % modulus for left, right in zip(principal_part, drift_part)]

    return apply


def modular_values(parameter, exponent, modulus, last_index):
    apply = shifted_operator(parameter, modulus)
    state = [(comb(exponent, degree) if degree <= exponent else 0) % modulus for degree in range(modulus)]
    values = []
    for index in range(last_index + 1):
        values.append(state[0])
        state = apply(state)
    return values


def totient(modulus):
    return sum(gcd(value, modulus) == 1 for value in range(1, modulus + 1))


def prime_divisors(number):
    return [candidate for candidate in range(2, number + 1) if number % candidate == 0 and all(candidate % divisor for divisor in range(2, candidate))]


def period_certificate(sequence, parameter, exponent, modulus, period, start, offset):
    origin = start - offset
    values = modular_values(parameter, exponent, modulus, origin + period + modulus)
    differences = [(values[index + period] - values[index]) % modulus for index in range(origin, origin + modulus)]
    assert differences == [0] * modulus
    witnesses = []
    for prime in prime_divisors(period):
        shift = period // prime
        index = next(index for index in range(origin, origin + modulus) if values[index + shift] != values[index])
        witnesses.append({'prime_divisor': prime, 'excluded_shift': shift, 'index': index + offset, 'values': [values[index], values[index + shift]]})
    return {'sequence': sequence, 'modulus': modulus, 'least_period': period, 'start_index': start, 'dimension': modulus, 'zero_differences': differences, 'minimality_witnesses': witnesses}


def verify():
    source_terms = {
        'A281180': [1, 4, 88, 4672, 454144, 70084096, 15728822272, 4836914249728],
        'A281181': [1, 1, 13, 493, 37369, 4732249, 901188997, 240798388357],
        'A281183': [1, 2, 32, 1376, 114176, 15519488, 3132551168, 879422726144],
        'A281184': [1, 3, 57, 2739, 246801, 35822307, 7636142793, 2246286827091],
        'A281440': [1, 1, 29, 2605, 478745, 148838425, 70130095925, 46612385237125],
    }
    specifications = [('A281180', 3, 4, 1), ('A281181', 3, 1, 0), ('A281183', 3, 2, 0), ('A281184', 3, 3, 0), ('A281440', 7, 1, 0)]
    columns = {}
    identities = []
    for sequence, parameter, exponent, offset in specifications:
        values = exact_column(parameter, exponent, 256)
        columns[sequence] = values
        assert values[:8] == source_terms[sequence]
        cosine, sine = ode_coefficients(parameter, 25)
        series = power(cosine, exponent, 25)
        for index in range(13):
            assert series[2 * index] * factorial(2 * index) == values[index]
        if sequence == 'A281180':
            for index in range(12):
                assert sine[2 * index + 1] * factorial(2 * index + 1) == values[index]
        for modulus in range(2, 25):
            residues = modular_values(parameter, exponent, modulus, 64)
            assert residues == [value % modulus for value in values[:65]]
        numeral = str(values[256])
        identities.append({'sequence': sequence, 'ode_agreement_indices': [offset, 12 + offset], 'source_initial_terms': 8, 'exact_index': 256 + offset, 'exact_digits': len(numeral), 'exact_value_sha256': sha256(numeral.encode()).hexdigest(), 'exact_value_mod_97': values[256] % 97})
    lifted_periods = []
    for modulus in range(2, 25):
        period = totient(modulus) ** 2
        start = modulus ** 2
        for sequence, parameter, exponent, offset in specifications:
            values = modular_values(parameter, exponent, modulus, start + period + modulus)
            assert all(values[index + period] == values[index] for index in range(start, start + modulus))
        lifted_periods.append({'modulus': modulus, 'period': period, 'column_start': start, 'columns': len(specifications), 'consecutive_zero_differences': modulus})
    certificates = [
        period_certificate('A281180', 3, 4, 7, 18, 1, 1),
        period_certificate('A281181', 3, 1, 10, 8, 0, 0),
        period_certificate('A281181', 3, 1, 9, 3, 1, 0),
        period_certificate('A281181', 3, 1, 13, 72, 0, 0),
        period_certificate('A281183', 3, 2, 11, 25, 1, 0),
        period_certificate('A281184', 3, 3, 11, 25, 1, 0),
        period_certificate('A281440', 7, 1, 13, 72, 0, 0),
    ]
    values = modular_values(3, 1, 12, 12)
    assert values == [1] * 13
    values = modular_values(3, 1, 13, 19)
    ratio_differences = [(values[index + 6] - 7 * values[index]) % 13 for index in range(13)]
    assert ratio_differences == [0] * 13
    return {'schema_version': 1, 'status': 'pass', 'arithmetic': 'exact integers and rational numbers', 'coefficient_identities': identities, 'all_index_finite_modulus_certificates': lifted_periods, 'least_period_certificates': certificates, 'constant_residue_certificate': {'sequence': 'A281181', 'modulus': 12, 'value': 1, 'initial_zero_differences': 12}, 'geometric_column_certificate': {'sequence': 'A281181', 'modulus': 13, 'shift': 6, 'multiplier': 7, 'zero_differences': ratio_differences}, 'scope': 'The finite-dimensional certificates imply the listed congruences for all subsequent indices by Cayley-Hamilton. The proof for arbitrary moduli and all odd parameters is the written argument in note.tex.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    content = json.dumps(verify(), indent=2, sort_keys=True) + '\n'
    if arguments.output:
        arguments.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
