import argparse
from hashlib import sha256
import json
from math import factorial
from pathlib import Path

from verify import exact_column, modular_values, ode_coefficients, power, totient


def verify_general():
    cases = []
    for parameter in range(1, 9):
        cosine, sine = ode_coefficients(parameter, 25)
        for exponent in sorted({0, 1, 2, parameter + 1}):
            values = exact_column(parameter, exponent, 64)
            series = power(cosine, exponent, 25)
            for index in range(13):
                assert series[2 * index] * factorial(2 * index) == values[index]
            if exponent == parameter + 1:
                for index in range(12):
                    assert sine[2 * index + 1] * factorial(2 * index + 1) == values[index]
            certificates = []
            for modulus in range(2, 17):
                period = totient(modulus) ** 2
                start = modulus ** 2
                residues = modular_values(parameter, exponent, modulus, max(64, start + period + modulus))
                assert residues[:65] == [value % modulus for value in values]
                differences = [(residues[index + period] - residues[index]) % modulus for index in range(start, start + modulus)]
                assert differences == [0] * modulus
                certificates.append({'modulus': modulus, 'column_start': start, 'period': period, 'zero_differences': differences})
            cases.append({'parameter': parameter, 'exponent': exponent, 'ode_column_indices': [0, 12], 'exact_column_index': 64, 'exact_value_sha256': sha256(str(values[64]).encode()).hexdigest(), 'all_index_period_certificates': certificates})
    specifications = [
        ('A281428', 4, 1, 0), ('A281427', 4, 5, 1),
        ('A281436', 6, 1, 0), ('A281435', 6, 7, 1),
        ('A281444', 8, 1, 0), ('A281443', 8, 9, 1),
        ('A281431', 5, 6, 1), ('A281182', 3, 1, 0),
    ]
    source_checks = []
    for sequence, parameter, exponent, offset in specifications:
        terms = SOURCE_TERMS[sequence]
        if sequence == 'A281182':
            even_values = exact_column(3, 1, len(terms))
            odd_values = exact_column(3, 4, len(terms))
            calculated = [even_values[index // 2] if index % 2 == 0 else odd_values[index // 2] for index in range(len(terms))]
        else:
            calculated = exact_column(parameter, exponent, len(terms) - 1)
        assert terms == calculated
        source_checks.append({'sequence': sequence, 'source_offset': offset, 'displayed_terms': len(terms), 'status': 'pass'})
    return {'schema_version': 1, 'status': 'pass', 'arithmetic': 'exact integers and rational numbers', 'parameter_range': [1, 8], 'cases': cases, 'source_checks': source_checks, 'scope': 'The characteristic-polynomial recurrence propagates each matrix certificate to all later column indices. The theorem for every positive integer exponent and every modulus is supplied by the written proof.'}


SOURCE_TERMS = {'A281428': [1, 1, 17, 865, 88865, 15335425, 3993275825, 1462392957025, 716611617346625, 452780458211706625, 358439197464543820625, 347486061804813737430625, 404905203733448633060470625, 558379985997479451541000890625, 899457522079287575519574474640625, 1673555570600439849976672764510390625, 3562028724551236205811767300836022890625], 'A281427': [1, 5, 145, 10325, 1357825, 284963525, 87274812625, 36716097543125, 20309401097610625, 14290053364475013125, 12462411363013047060625, 13192751210140624100103125, 16663953549286540157926890625, 24756557919279291667433199453125, 42733906625427778939437818074140625, 84814104213422372894487597292655703125], 'A281436': [1, 1, 25, 1921, 301105, 79715041, 31953352585, 18055521444961, 13675020394100065, 13371875150000047681, 16399205085221871057145, 24649278939856374854251201, 44562940283889239727355265425, 95400484808911059939339873215521, 238677467614161144737008148697894505, 690019785744332320572996561216607892641, 2282793490173453501140213827073151244641985], 'A281435': [1, 7, 301, 32347, 6476281, 2080072687, 978357441061, 633671918506627, 540647648053353841, 587611403828850167767, 792504001599034713809821, 1298643416767164198145121707, 2541154725546790383213482500201, 5852376595008692595588309106586047, 15669400182952350735653156519506572181, 48261540873448422135971738449165162450387, 169430327422451431526680101559949211638388961], 'A281444': [1, 1, 33, 3393, 715329, 255419649, 138324673377, 105723078203457, 108400924932329601, 143589514674637260801, 238670525628280806487713, 486411018516606613409744193, 1192731112687557517714202303169, 3464267964203640308372312350830849, 11761665286319167564660531957187772897, 46153563625764407361666349419808431496257, 207288280492672493893642973836751374267592961], 'A281443': [1, 9, 513, 73737, 19832769, 8579840841, 5445003346497, 4764370917991113, 5496694973220383361, 8084246464894865788809, 14762694711793154790084993, 32769963553535754858524377737, 86898373859771331049009442719809, 271302297590897772500098532033111241, 985007641595004757219829801609866106817, 4114936376199336730220297730026151662954313, 19598505312024077134206058809303825114147365121], 'A281431': [1, 6, 216, 19296, 3200256, 849678336, 329902212096, 176210323070976, 123889924672782336, 110895584511900450816, 123119226530619884568576, 166015794146482719037587456, 267231655288799665792971964416, 506138971421813256899173596266496, 1114219301421887004276203102410899456, 2821068813384522963411318522740301889536, 8139956209849296948206537756832040061239296], 'A281182': [1, 1, 1, 4, 13, 88, 493, 4672, 37369, 454144, 4732249, 70084096, 901188997, 15728822272, 240798388357, 4836914249728, 85948640603761, 1952137912385536, 39504564917358001, 1000749157519458304, 22726779729476308093, 635146072839001735168, 15998009117983994065693, 488855521088102855606272, 13526765851190230940840809, 448599416591747486039670784, 13528070218935445806530640649]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    arguments.output.write_text(json.dumps(verify_general(), indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
