"""
Comprehensive Math and Scientific Engine for JARVIS
Handles broad mathematical calculations, geometric formulas, scientific equations,
unit conversions, and general algebraic evaluations.
"""

import math
import re
from typing import Optional

class MathEngine:
    def __init__(self):
        pass

    def solve(self, text: str) -> Optional[str]:
        t = text.lower().strip()
        t = re.sub(r'^(what is|calculate|solve|hitung|berapa|carikan|tentukan|hitunglah|tolong hitung)\s+', '', t)

        # 1. Geometry: Luas Lingkaran (Circle Area) - pi * r^2
        m_circle = re.search(r'(?:luas lingkaran|area of circle).*?(?:jari-jari|radius|r)\s*(\d+(?:\.\d+)?)', t)
        if m_circle:
            r = float(m_circle.group(1))
            area = math.pi * (r ** 2)
            return f"Luas lingkaran dengan jari-jari {r:g} adalah {area:.2f}, Sir."

        # 2. Geometry: Keliling Lingkaran (Circumference) - 2 * pi * r
        m_circ = re.search(r'(?:keliling lingkaran|circumference).*?(?:jari-jari|radius|diameter|d|r)\s*(\d+(?:\.\d+)?)', t)
        if m_circ:
            val = float(m_circ.group(1))
            res = 2 * math.pi * val
            return f"Keliling lingkaran adalah {res:.2f}, Sir."

        # 3. Geometry: Luas Segitiga (Triangle Area) - 1/2 * a * t
        m_tri = re.search(r'(?:luas segitiga|area of triangle).*?(?:alas|base)\s*(\d+(?:\.\d+)?).*?(?:tinggi|height)\s*(\d+(?:\.\d+)?)', t)
        if m_tri:
            a, h = float(m_tri.group(1)), float(m_tri.group(2))
            res = 0.5 * a * h
            return f"Luas segitiga dengan alas {a:g} dan tinggi {h:g} adalah {res:g}, Sir."

        # 4. Geometry: Volume Tabung (Cylinder Volume) - pi * r^2 * h
        m_cyl = re.search(r'(?:volume tabung|cylinder volume).*?(?:jari-jari|radius|r)\s*(\d+(?:\.\d+)?).*?(?:tinggi|height|t)\s*(\d+(?:\.\d+)?)', t)
        if m_cyl:
            r, h = float(m_cyl.group(1)), float(m_cyl.group(2))
            vol = math.pi * (r ** 2) * h
            return f"Volume tabung dengan radius {r:g} dan tinggi {h:g} adalah {vol:.2f}, Sir."

        # 5. Geometry: Volume Bola (Sphere Volume) - 4/3 * pi * r^3
        m_sph = re.search(r'(?:volume bola|sphere volume).*?(?:jari-jari|radius|r)\s*(\d+(?:\.\d+)?)', t)
        if m_sph:
            r = float(m_sph.group(1))
            vol = (4.0 / 3.0) * math.pi * (r ** 3)
            return f"Volume bola dengan radius {r:g} adalah {vol:.2f}, Sir."

        # 6. Geometry: Volume Balok (Rectangular Prism) - p * l * t
        m_box = re.search(r'(?:volume balok).*?(?:panjang|p)\s*(\d+(?:\.\d+)?).*?(?:lebar|l)\s*(\d+(?:\.\d+)?).*?(?:tinggi|t)\s*(\d+(?:\.\d+)?)', t)
        if m_box:
            p, l, h = float(m_box.group(1)), float(m_box.group(2)), float(m_box.group(3))
            vol = p * l * h
            return f"Volume balok {p:g} x {l:g} x {h:g} adalah {vol:g}, Sir."

        # 7. Geometry: Pythagoras - sqrt(a^2 + b^2)
        m_pyth = re.search(r'pythagoras\s*(\d+(?:\.\d+)?)\s*(?:dan|and)\s*(\d+(?:\.\d+)?)', t)
        if m_pyth:
            a, b = float(m_pyth.group(1)), float(m_pyth.group(2))
            c = math.sqrt(a**2 + b**2)
            return f"Sisi miring segitiga siku-siku (Pythagoras) dari {a:g} dan {b:g} adalah {c:.2f}, Sir."

        # 8. Roots: Square Root & Cube Root
        m_cbrt = re.search(r'(?:cube root of|akar pangkat 3 dari|akar pangkat 3)\s*(\d+(?:\.\d+)?)', t)
        if m_cbrt:
            val = float(m_cbrt.group(1))
            res = val ** (1.0 / 3.0)
            return f"Akar pangkat 3 dari {val:g} adalah {res:.2f}, Sir."

        m_sqrt = re.search(r'(?:square root of|akar kuadrat dari|akar dari|akar|sqrt)\s*(\d+(?:\.\d+)?)', t)
        if m_sqrt:
            val = float(m_sqrt.group(1))
            res = math.sqrt(val)
            return f"Akar kuadrat dari {val:g} adalah {res:g}, Sir."

        # 9. Powers & Exponents (pangkat / power)
        m_pow = re.search(r'(\d+(?:\.\d+)?)\s*(?:pangkat|to the power of|power of|\^|\*\*)\s*(\d+(?:\.\d+)?)', t)
        if m_pow:
            base, exp = float(m_pow.group(1)), float(m_pow.group(2))
            if exp <= 100:
                res = math.pow(base, exp)
                return f"{base:g} pangkat {exp:g} adalah {res:g}, Sir."

        # 10. Factorial
        m_fact = re.search(r'(?:factorial of|faktorial)\s*(\d+)|(\d+)\s*(?:factorial|faktorial|!)', t)
        if m_fact:
            val = int(m_fact.group(1) or m_fact.group(2))
            if val <= 30:
                res = math.factorial(val)
                return f"Faktorial dari {val} adalah {res}, Sir."

        # 11. Trigonometry (sin, cos, tan)
        m_trig = re.search(r'(sin|cos|tan)\s*(\d+(?:\.\d+)?)(?:\s*(?:derajat|degrees|deg))?', t)
        if m_trig:
            func, deg = m_trig.group(1), float(m_trig.group(2))
            rad = math.radians(deg)
            if func == "sin": res = math.sin(rad)
            elif func == "cos": res = math.cos(rad)
            elif func == "tan": res = math.tan(rad)
            return f"{func.upper()} dari {deg:g} derajat adalah {res:.4f}, Sir."

        # 12. Logarithms
        m_log = re.search(r'(?:logaritma|log)\s*(?:basis 10)?\s*(\d+(?:\.\d+)?)', t)
        if m_log:
            val = float(m_log.group(1))
            res = math.log10(val)
            return f"Logaritma basis 10 dari {val:g} adalah {res:.4f}, Sir."

        # 13. Percentage Calculations
        m_pct = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent|persen)\s*(?:of|dari)\s*(\d+(?:\.\d+)?)', t)
        if m_pct:
            pct, val = float(m_pct.group(1)), float(m_pct.group(2))
            res = (pct / 100.0) * val
            return f"{pct:g}% dari {val:g} adalah {res:g}, Sir."

        # 14. Conversions: Temperature (Celsius <-> Fahrenheit)
        m_c2f = re.search(r'(\d+(?:\.\d+)?)\s*(?:derajat\s+)?celsius\s+(?:ke|to)\s+fahrenheit', t)
        if m_c2f:
            c = float(m_c2f.group(1))
            f = (c * 9/5) + 32
            return f"{c:g} derajat Celsius sama dengan {f:.1f} derajat Fahrenheit, Sir."

        m_f2c = re.search(r'(\d+(?:\.\d+)?)\s*(?:derajat\s+)?fahrenheit\s+(?:ke|to)\s+celsius', t)
        if m_f2c:
            f = float(m_f2c.group(1))
            c = (f - 32) * 5/9
            return f"{f:g} derajat Fahrenheit sama dengan {c:.1f} derajat Celsius, Sir."

        # 15. Conversions: Distance (Kilometers <-> Miles)
        m_km2m = re.search(r'(\d+(?:\.\d+)?)\s*(?:kilometer|km)\s+(?:ke|to)\s+(?:mil|miles)', t)
        if m_km2m:
            km = float(m_km2m.group(1))
            miles = km * 0.621371
            return f"{km:g} kilometer sama dengan {miles:.2f} mil, Sir."

        # 16. Conversions: Weight (Kilogram <-> Pound / Lbs)
        m_kg2lbs = re.search(r'(\d+(?:\.\d+)?)\s*(?:kilogram|kg)\s+(?:ke|to)\s+(?:pon|pound|lbs)', t)
        if m_kg2lbs:
            kg = float(m_kg2lbs.group(1))
            lbs = kg * 2.20462
            return f"{kg:g} kilogram sama dengan {lbs:.2f} pound, Sir."

        # 17. General Arithmetic & Mathematical Expressions
        # Handles "500 times 8", "1250 dibagi 5", "25 + 75 * 2", etc.
        clean = t
        clean = re.sub(r'\btimes\b|\bdikali\b|\bkali\b|\bx\b', '*', clean)
        clean = re.sub(r'\bdivided\s+by\b|\bdibagi\b|\bbagi\b', '/', clean)
        clean = re.sub(r'\bplus\b|\bditambah\b|\btambah\b', '+', clean)
        clean = re.sub(r'\bminus\b|\bdikurang\b|\bkurang\b', '-', clean)
        clean = re.sub(r'\bpangkat\b|\bpower\b', '**', clean)
        clean = re.sub(r'\bmod\b|\bsisa\s+bagi\b', '%', clean)

        # Sanitize to math symbols only
        sanitized = re.sub(r'[^0-9\+\-\*\/\.\(\)\%\s]', '', clean).strip()

        if sanitized and re.search(r'\d+\s*[\+\-\*\/\%]\s*\d+', sanitized):
            try:
                # Safe eval with restricted globals
                res = eval(sanitized, {"__builtins__": None}, {"math": math})
                if isinstance(res, float):
                    formatted = f"{res:.4f}".rstrip('0').rstrip('.')
                else:
                    formatted = str(res)
                return f"Hasil perhitungan dari {sanitized} adalah {formatted}, Sir."
            except Exception:
                pass

        return None

if __name__ == "__main__":
    me = MathEngine()
    test_cases = [
        "what is 500 times 8",
        "akar dari 144",
        "2 pangkat 8",
        "sin 30 derajat",
        "luas lingkaran dengan jari-jari 7",
        "volume tabung radius 5 tinggi 10",
        "100 celsius ke fahrenheit",
        "10 km ke miles",
        "pythagoras 3 dan 4",
        "25% dari 200000"
    ]
    for c in test_cases:
        print(f"[{c}] -> {me.solve(c)}")
