from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# =========================================================
# API ARITHMETIC
# =========================================================

@app.route('/api/arithmetic', methods=['POST'])
def arithmetic():

    data = request.get_json()

    a = float(data.get('a', 0))
    b = data.get('b')
    op = data.get('operation')

    if b not in [None, '']:
        b = float(b)

    try:

        if op == 'add':
            result = a + b
            formula = 'a + b'
            expr = f'{a} + {b}'

        elif op == 'sub':
            result = a - b
            formula = 'a - b'
            expr = f'{a} - {b}'

        elif op == 'mul':
            result = a * b
            formula = 'a × b'
            expr = f'{a} × {b}'

        elif op == 'div':
            if b == 0:
                return jsonify({'error': 'Pembagian dengan nol!'})

            result = a / b
            formula = 'a ÷ b'
            expr = f'{a} ÷ {b}'

        elif op == 'pow':
            result = a ** b
            formula = 'a^b'
            expr = f'{a}^{b}'

        elif op == 'sqrt':
            if a < 0:
                return jsonify({'error': 'Input harus ≥ 0'})

            result = math.sqrt(a)
            formula = '√a'
            expr = f'√{a}'

        elif op == 'mod':
            if b == 0:
                return jsonify({'error': 'Modulus dengan nol!'})

            result = a % b
            formula = 'a mod b'
            expr = f'{a} mod {b}'

        elif op == 'fdiv':
            if b == 0:
                return jsonify({'error': 'Floor div dengan nol!'})

            result = a // b
            formula = '⌊a ÷ b⌋'
            expr = f'{a} // {b}'

        else:
            return jsonify({'error': 'Operator tidak valid'})

        return jsonify({
            'success': True,
            'result': result,
            'formula': formula,
            'expression': expr,
            'steps': [
                f'Input A = {a}',
                f'Input B = {b}' if b is not None else 'Single input operation',
                f'Operasi = {op}',
                f'Hasil = {result}'
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)})


# =========================================================
# API LOGIC
# =========================================================

@app.route('/api/logic', methods=['POST'])
def logic():

    data = request.get_json()

    a = int(data.get('a', 0))
    b = data.get('b')
    op = data.get('operation')

    if b not in [None, '']:
        b = int(b)

    try:

        if op == 'and':
            result = a & b

        elif op == 'or':
            result = a | b

        elif op == 'xor':
            result = a ^ b

        elif op == 'not':
            result = ~a

        elif op == 'nand':
            result = ~(a & b)

        elif op == 'nor':
            result = ~(a | b)

        else:
            return jsonify({'error': 'Operator tidak valid'})

        return jsonify({
            'success': True,
            'result': result,
            'binary': bin(result),
            'steps': [
                f'A = {a} ({bin(a)})',
                f'B = {b} ({bin(b)})' if b is not None else 'Unary operation',
                f'Hasil = {result}'
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)})
# =========================================================
# API BASE CONVERSION
# =========================================================

@app.route('/api/base', methods=['POST'])
def base_conversion():
    data = request.get_json()
    v = data.get('value', '').strip()
    try:
        from_base = int(data.get('from_base', 10))
    except (ValueError, TypeError):
        return jsonify({'error': 'Basis tidak valid'})

    if not v:
        return jsonify({'error': 'Masukkan nilai'})

    try:
        dec = int(v, from_base)
    except ValueError:
        return jsonify({'error': 'Input tidak valid untuk basis tersebut'})

    binary_val = bin(dec)[2:]
    octal_val = oct(dec)[2:]
    hex_val = hex(dec)[2:].upper()

    return jsonify({
        'success': True,
        'decimal': dec,
        'binary': binary_val,
        'octal': octal_val,
        'hexadecimal': hex_val
    })


# =========================================================
# API CURRENCY
# =========================================================

@app.route('/api/currency', methods=['POST'])
def currency_conversion():
    data = request.get_json()
    try:
        value = float(data.get('value'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Masukkan jumlah yang valid'})

    from_currency = data.get('from_currency', 'IDR')

    rates = {
        'IDR': 1.0,
        'USD': 1.0 / 15800.0,
        'EUR': 1.0 / 17200.0,
        'SGD': 1.0 / 11700.0,
        'MYR': 1.0 / 3400.0,
        'JPY': 1.0 / 105.0,
        'GBP': 1.0 / 20100.0,
        'AUD': 1.0 / 10400.0
    }

    if from_currency not in rates:
        return jsonify({'error': 'Mata uang tidak didukung'})

    idr_val = value / rates[from_currency]

    result = {}
    for code, rate in rates.items():
        result[code] = idr_val * rate

    return jsonify({
        'success': True,
        'result': result,
        'idr_value': idr_val
    })


# =========================================================
# API TEMPERATURE
# =========================================================

@app.route('/api/temperature', methods=['POST'])
def temperature():

    data = request.get_json()

    value = float(data.get('value'))
    unit = data.get('unit')

    try:

        if unit == 'celsius':
            c = value

        elif unit == 'fahrenheit':
            c = (value - 32) * 5 / 9

        elif unit == 'kelvin':
            c = value - 273.15

        elif unit == 'reamur':
            c = value * 5 / 4

        else:
            return jsonify({'error': 'Unit tidak valid'})

        result = {
            'celsius': round(c, 2),
            'fahrenheit': round((c * 9 / 5) + 32, 2),
            'kelvin': round(c + 273.15, 2),
            'reamur': round(c * 4 / 5, 2)
        }

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': str(e)})


# =========================================================
# API FACTORIAL
# =========================================================

@app.route('/api/factorial', methods=['POST'])
def factorial():

    data = request.get_json()

    n = int(data.get('n'))

    if n < 0:
        return jsonify({'error': 'n harus positif'})

    result = math.factorial(n)

    return jsonify({
        'success': True,
        'result': result
    })


# =========================================================
# API FIBONACCI
# =========================================================

@app.route('/api/fibonacci', methods=['POST'])
def fibonacci():

    data = request.get_json()

    n = int(data.get('n'))

    if n <= 0:
        return jsonify({'error': 'n harus > 0'})

    seq = [0, 1]

    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])

    return jsonify({
        'success': True,
        'sequence': seq[:n]
    })


if __name__ == '__main__':
    app.run(debug=True)