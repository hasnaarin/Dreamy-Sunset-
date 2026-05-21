from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# ══════════════════════════════════════
#  ROUTE — HALAMAN UTAMA
# ══════════════════════════════════════
@app.route('/')
def index():
    return render_template('index.html')


# ══════════════════════════════════════
#  ROUTE — KALKULATOR ARITMATIKA
# ══════════════════════════════════════
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    # Unary function (sin, cos, sqrt, dll)
    if 'fn' in data:
        val = float(data.get('val', 0))
        fn  = data.get('fn')
        result, formula, steps = apply_unary(fn, val)
        return jsonify({'result': result, 'formula': formula, 'steps': steps})

    # Binary operation (+, -, *, /, **, %, //, AND, OR, dll)
    a   = float(data.get('a', 0))
    b   = float(data.get('b', 0))
    op  = data.get('op', '+')

    result, formula, steps = apply_binary(a, b, op)
    return jsonify({'result': result, 'formula': formula, 'steps': steps})


# ══════════════════════════════════════
#  ROUTE — KONVERSI BASIS BILANGAN
# ══════════════════════════════════════
@app.route('/api/basis', methods=['POST'])
def basis():
    data    = request.get_json()
    nilai   = data.get('nilai', '0')
    from_base = int(data.get('from_base', 10))

    try:
        dec = int(nilai, from_base)
        return jsonify({
            'desimal': dec,
            'biner'  : bin(dec)[2:],
            'oktal'  : oct(dec)[2:],
            'hex'    : hex(dec)[2:].upper(),
            'steps'  : [
                f"Input: {nilai} (basis {from_base})",
                f"Konversi ke Desimal: {dec}",
                f"Biner  : {bin(dec)[2:]}",
                f"Oktal  : {oct(dec)[2:]}",
                f"Hex    : {hex(dec)[2:].upper()}"
            ]
        })
    except ValueError:
        return jsonify({'error': 'Input tidak valid'}), 400


# ══════════════════════════════════════
#  ROUTE — KONVERSI SUHU
# ══════════════════════════════════════
@app.route('/api/suhu', methods=['POST'])
def suhu():
    data  = request.get_json()
    nilai = float(data.get('nilai', 0))
    dari  = data.get('dari', 'C')   # C / F / K / R

    # Konversi semua ke Celsius dulu
    if dari == 'C': c = nilai
    elif dari == 'F': c = (nilai - 32) * 5 / 9
    elif dari == 'K': c = nilai - 273.15
    elif dari == 'R': c = nilai * 5 / 4
    else: return jsonify({'error': 'Satuan tidak valid'}), 400

    hasil = {
        'celsius'   : round(c, 4),
        'fahrenheit': round(c * 9/5 + 32, 4),
        'kelvin'    : round(c + 273.15, 4),
        'reamur'    : round(c * 4/5, 4),
    }
    hasil['steps'] = [
        f"Input: {nilai} °{dari}",
        f"→ Celsius    : {hasil['celsius']} °C",
        f"→ Fahrenheit : {hasil['fahrenheit']} °F  |  Rumus: (C×9/5)+32",
        f"→ Kelvin     : {hasil['kelvin']} K       |  Rumus: C+273.15",
        f"→ Réaumur    : {hasil['reamur']} °Ré     |  Rumus: C×4/5",
    ]
    return jsonify(hasil)


# ══════════════════════════════════════
#  ROUTE — KONVERSI MATA UANG
# ══════════════════════════════════════
RATES_TO_IDR = {
    'IDR': 1,
    'USD': 16200,
    'EUR': 17500,
    'SGD': 12000,
    'JPY': 108,
    'GBP': 20400,
    'MYR': 3500,
    'AUD': 10500,
}

@app.route('/api/kurs', methods=['POST'])
def kurs():
    data   = request.get_json()
    jumlah = float(data.get('jumlah', 0))
    dari   = data.get('dari', 'IDR').upper()
    ke     = data.get('ke',   'USD').upper()

    if dari not in RATES_TO_IDR or ke not in RATES_TO_IDR:
        return jsonify({'error': 'Mata uang tidak tersedia'}), 400

    in_idr  = jumlah * RATES_TO_IDR[dari]
    result  = round(in_idr / RATES_TO_IDR[ke], 6)
    rate    = round(RATES_TO_IDR[dari] / RATES_TO_IDR[ke], 6)

    return jsonify({
        'result': result,
        'rate'  : rate,
        'steps' : [
            f"Input: {jumlah} {dari}",
            f"Konversi ke IDR: {jumlah} × {RATES_TO_IDR[dari]} = Rp {in_idr:,.0f}",
            f"Konversi ke {ke}: Rp {in_idr:,.0f} ÷ {RATES_TO_IDR[ke]} = {result} {ke}",
            f"Rate: 1 {dari} = {rate} {ke}  (statis 2025)"
        ]
    })


# ══════════════════════════════════════
#  ROUTE — FAKTORIAL
# ══════════════════════════════════════
@app.route('/api/faktorial', methods=['POST'])
def faktorial():
    data = request.get_json()
    n    = int(data.get('n', 0))

    if n < 0 or n > 170:
        return jsonify({'error': 'n harus 0–170'}), 400

    result = math.factorial(n)
    steps  = [f"{i}! = {math.factorial(i)}" for i in range(min(n+1, 6))]
    if n > 5:
        steps.append('...')
        steps.append(f"{n}! = {result}")

    return jsonify({
        'result': str(result),
        'steps' : steps,
        'formula': f"{n}! = {' × '.join(str(i) for i in range(n, 0, -1))} × 1"
                   if n <= 10 else f"{n}! = {n} × (n−1) × … × 1"
    })


# ══════════════════════════════════════
#  ROUTE — FIBONACCI
# ══════════════════════════════════════
@app.route('/api/fibonacci', methods=['POST'])
def fibonacci():
    data = request.get_json()
    n    = int(data.get('n', 1))

    if n < 1 or n > 78:
        return jsonify({'error': 'n harus 1–78'}), 400

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    fib = fib[:n]

    return jsonify({
        'deret'  : [str(x) for x in fib],
        'suku_ke': str(fib[-1]),
        'steps'  : [
            "Rumus: F(n) = F(n−1) + F(n−2)",
            "F(0) = 0, F(1) = 1",
            f"Deret {n} suku: {', '.join(str(x) for x in fib[:8])}" +
            (' ...' if n > 8 else ''),
            f"Suku ke-{n}: {fib[-1]}"
        ]
    })


# ══════════════════════════════════════
#  ROUTE — LOGIKA BITWISE
# ══════════════════════════════════════
@app.route('/api/logika', methods=['POST'])
def logika():
    data = request.get_json()
    op   = data.get('op', 'AND').upper()
    a    = int(data.get('a', 0))
    b    = int(data.get('b', 0)) if op != 'NOT' else None

    ops = {
        'AND' : (a & b,  f"{a} AND {b}"),
        'OR'  : (a | b,  f"{a} OR {b}"),
        'XOR' : (a ^ b,  f"{a} XOR {b}"),
        'NAND': (~(a & b) & 0xFFFFFFFF, f"NOT({a} AND {b})"),
        'NOR' : (~(a | b) & 0xFFFFFFFF, f"NOT({a} OR {b})"),
        'NOT' : (~a & 0xFFFFFFFF,        f"NOT {a}"),
    }

    if op not in ops:
        return jsonify({'error': 'Operator tidak valid'}), 400

    result, formula = ops[op]
    return jsonify({
        'result' : result,
        'formula': f"{formula} = {result}",
        'biner_a': bin(a & 0xFF)[2:].zfill(8),
        'biner_b': bin(b & 0xFF)[2:].zfill(8) if b is not None else None,
        'biner_r': bin(result & 0xFF)[2:].zfill(8),
        'steps'  : [
            f"A = {a}  → Biner: {bin(a & 0xFF)[2:].zfill(8)}",
            f"B = {b}  → Biner: {bin(b & 0xFF)[2:].zfill(8)}" if b is not None else "Operasi NOT (unary)",
            f"Terapkan {op} bit-per-bit",
            f"Hasil = {result}  (Biner: {bin(result & 0xFF)[2:].zfill(8)})"
        ]
    })


# ══════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════
def apply_unary(fn, val):
    ops = {
        'sqrt'  : (math.sqrt(val),       f"√{val}"),
        'cbrt'  : (val**(1/3),           f"∛{val}"),
        'sq'    : (val**2,               f"{val}²"),
        'inv'   : (1/val if val else None, f"1/{val}"),
        'abs'   : (abs(val),             f"|{val}|"),
        'sin'   : (math.sin(math.radians(val)), f"sin({val}°)"),
        'cos'   : (math.cos(math.radians(val)), f"cos({val}°)"),
        'tan'   : (math.tan(math.radians(val)), f"tan({val}°)"),
        'log'   : (math.log10(val) if val > 0 else None, f"log({val})"),
        'ln'    : (math.log(val)   if val > 0 else None, f"ln({val})"),
        'negate': (-val,                 f"−({val})"),
        'pct'   : (val/100,             f"{val}%"),
    }
    if fn not in ops:
        return 'Error', fn, []

    result, label = ops[fn]
    if result is None:
        return 'Error', label, ['Input tidak valid untuk operasi ini']

    result  = round(result, 10)
    formula = f"{label} = {result}"
    steps   = [f"Fungsi: {fn}", f"Input: {val}", f"Hasil: {result}"]
    return result, formula, steps


def apply_binary(a, b, op):
    try:
        if op == '+':  result = a + b
        elif op == '-': result = a - b
        elif op == '*': result = a * b
        elif op == '/':
            if b == 0: return 'Error', f"{a}÷0", ['Pembagian dengan nol tidak diizinkan']
            result = a / b
        elif op == '**': result = a ** b
        elif op == '%':
            if b == 0: return 'Error', f"{a} mod 0", ['Modulus dengan nol tidak valid']
            result = a % b
        elif op == '//':
            if b == 0: return 'Error', f"⌊{a}÷0⌋", ['Floor division dengan nol tidak valid']
            result = math.floor(a / b)
        else:
            return 'Error', op, ['Operator tidak dikenal']

        result  = round(result, 10)
        sym     = {'+':'+','-':'−','*':'×','/':'÷','**':'^','%':'mod','//':'÷÷'}
        formula = f"{a} {sym.get(op, op)} {b} = {result}"
        steps   = [
            f"Operasi: {op}",
            f"A = {a}, B = {b}",
            f"Hasil: {result}"
        ]
        return result, formula, steps

    except Exception as e:
        return 'Error', str(e), [str(e)]


# ══════════════════════════════════════
#  RUN
# ══════════════════════════════════════
if __name__ == '__main__':
    app.run()