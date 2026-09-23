"""
Mòdul de Normalització de Text per al Català (Text Normalizer).
Inspirat en les regles lingüístiques del Projecte AINA i el BSC-LT.
Converteix xifres, decimals, dates, monedes, percentatges, ordinals
i abreviatures a la seva forma ortogràfica oral en català.
"""

import re
from typing import Dict, List, Tuple

class CatalanTextNormalizer:
    """
    Normalitzador especialitzat de text català per a síntesi de veu (TTS).
    """

    UNITS = {
        0: "zero", 1: "un", 2: "dos", 3: "tres", 4: "quatre",
        5: "cinc", 6: "sis", 7: "set", 8: "vuit", 9: "nou"
    }

    UNITS_FEM = {
        1: "una", 2: "dues"
    }

    TEENS = {
        10: "deu", 11: "onze", 12: "dotze", 13: "tretze", 14: "catorze",
        15: "quinze", 16: "setze", 17: "disset", 18: "divuit", 19: "dinou"
    }

    TENS = {
        20: "vint", 30: "trenta", 40: "quaranta", 50: "cinquanta",
        60: "seixanta", 70: "setanta", 80: "vuitanta", 90: "noranta"
    }

    HUNDREDS = {
        100: "cent", 200: "dos-cents", 300: "tres-cents", 400: "quatre-cents",
        500: "cinc-cents", 600: "sis-cents", 700: "set-cents", 800: "vuit-cents", 900: "nou-cents"
    }

    ORDINALS_MASC = {
        1: "primer", 2: "segon", 3: "tercer", 4: "quart", 5: "cinquè",
        6: "sisè", 7: "setè", 8: "vuitè", 9: "novè", 10: "desè",
        11: "onzè", 12: "dotzè", 20: "vintè", 100: "centè"
    }

    ORDINALS_FEM = {
        1: "primera", 2: "segona", 3: "tercera", 4: "quarta", 5: "cinquena",
        6: "sisena", 7: "setena", 8: "vuitena", 9: "novena", 10: "desena"
    }

    ABBREVIATIONS = [
        (re.compile(r"\bp\.?\s*ex\.?\b", re.IGNORECASE), "per exemple"),
        (re.compile(r"\bex\.?\b", re.IGNORECASE), "exemple"),
        (re.compile(r"\betc\.?\b", re.IGNORECASE), "etcètera"),
        (re.compile(r"\bDr\.\s*", re.IGNORECASE), "doctor "),
        (re.compile(r"\bDra\.\s*", re.IGNORECASE), "doctora "),
        (re.compile(r"\bProf\.\s*", re.IGNORECASE), "professor "),
        (re.compile(r"\bProfa\.\s*", re.IGNORECASE), "professora "),
        (re.compile(r"\bSr\.\s*", re.IGNORECASE), "senyor "),
        (re.compile(r"\bSra\.\s*", re.IGNORECASE), "senyora "),
        (re.compile(r"\bpàgs?\.\s*", re.IGNORECASE), "pàgina "),
        (re.compile(r"\bpàg\.\s*", re.IGNORECASE), "pàgina "),
        (re.compile(r"\bnúm\.\s*", re.IGNORECASE), "número "),
        (re.compile(r"\bnº\s*", re.IGNORECASE), "número "),
        (re.compile(r"\baprox\.\s*", re.IGNORECASE), "aproximadament "),
        (re.compile(r"\bvol\.\s*", re.IGNORECASE), "volum "),
        (re.compile(r"\bcap\.\s*", re.IGNORECASE), "capítol "),
        (re.compile(r"\bart\.\s*", re.IGNORECASE), "article "),
        (re.compile(r"\bkm/h\b", re.IGNORECASE), "quilòmetres per hora"),
        (re.compile(r"\bkm\b", re.IGNORECASE), "quilòmetres"),
        (re.compile(r"\bkg\b", re.IGNORECASE), "quilos"),
        (re.compile(r"\bcm\b", re.IGNORECASE), "centímetres"),
        (re.compile(r"\bmm\b", re.IGNORECASE), "mil·límetres"),
        (re.compile(r"\bmin\b", re.IGNORECASE), "minuts"),
        (re.compile(r"\bseg\b", re.IGNORECASE), "segons"),
        (re.compile(r"(\d+)\s*h\b", re.IGNORECASE), r"\1 hores"),
        (re.compile(r"\bIA\b"), "intel·ligència artificial"),
        (re.compile(r"\bTIC\b"), "tecnologies de la informació i la comunicació"),
        (re.compile(r"\bESO\b"), "educació secundària obligatòria"),
        (re.compile(r"\bURL\b"), "u r ela"),
        (re.compile(r"\bPDF\b"), "pe de efa"),
        (re.compile(r"\bMP3\b"), "ema pe tres"),
        (re.compile(r"\bWAV\b"), "ve doble a ve"),
        (re.compile(r"\bTTS\b"), "te te essa"),
        (re.compile(r"\bBSC\b"), "be essa ce"),
        (re.compile(r"\bUB\b"), "u be"),
        (re.compile(r"\bUAB\b"), "u a be"),
        (re.compile(r"\bUPC\b"), "u pe ce"),
        (re.compile(r"\bUPF\b"), "u pe efa"),
        (re.compile(r"\bUdG\b"), "u de ge"),
        (re.compile(r"\bUdL\b"), "u de ela"),
        (re.compile(r"\bURV\b"), "u erra ve"),
        (re.compile(r"\bUOC\b"), "u o ce")
    ]

    def __init__(self):
        pass

    def number_to_catalan(self, n: int, feminine: bool = False) -> str:
        """Converteix un enter positiu (fins a 999.999.999) en lletres en català."""
        if n < 0:
            return "menys " + self.number_to_catalan(abs(n), feminine)
        if n in self.UNITS:
            if feminine and n in self.UNITS_FEM:
                return self.UNITS_FEM[n]
            return self.UNITS[n]
        if n in self.TEENS:
            return self.TEENS[n]
        if n in self.TENS:
            return self.TENS[n]

        if 21 <= n <= 29:
            unit = self.number_to_catalan(n % 10, feminine)
            return f"vint-i-{unit}"

        if 31 <= n <= 99:
            ten = self.TENS[(n // 10) * 10]
            unit = self.number_to_catalan(n % 10, feminine)
            return f"{ten}-{unit}"

        if n == 100:
            return "cent"

        if 101 <= n <= 199:
            rest = self.number_to_catalan(n - 100, feminine)
            return f"cent {rest}"

        if 200 <= n <= 999:
            hundreds_val = (n // 100) * 100
            prefix = self.HUNDREDS.get(hundreds_val, f"{self.number_to_catalan(n // 100)}-cents")
            rem = n % 100
            if rem == 0:
                return prefix
            return f"{prefix} {self.number_to_catalan(rem, feminine)}"

        if 1000 <= n <= 1999:
            rem = n - 1000
            if rem == 0:
                return "mil"
            return f"mil {self.number_to_catalan(rem, feminine)}"

        if 2000 <= n <= 999999:
            thousands = n // 1000
            rem = n % 1000
            th_str = self.number_to_catalan(thousands, feminine=False)
            if rem == 0:
                return f"{th_str} mil"
            return f"{th_str} mil {self.number_to_catalan(rem, feminine)}"

        if 1000000 <= n <= 1999999:
            rem = n - 1000000
            if rem == 0:
                return "un milió"
            return f"un milió {self.number_to_catalan(rem, feminine)}"

        if 2000000 <= n <= 999999999:
            millions = n // 1000000
            rem = n % 1000000
            m_str = self.number_to_catalan(millions, feminine=False)
            if rem == 0:
                return f"{m_str} milions"
            return f"{m_str} milions {self.number_to_catalan(rem, feminine)}"

        return str(n)

    def replace_ordinals(self, text: str) -> str:
        """Substitueix ordinals com 1r, 2a, 3r, 4t, 5è."""
        def ord_repl(match):
            num = int(match.group(1))
            suffix = match.group(2).lower()
            if suffix == "a":
                return self.ORDINALS_FEM.get(num, self.number_to_catalan(num) + "ena")
            else:
                return self.ORDINALS_MASC.get(num, self.number_to_catalan(num) + "è")

        pattern = r"\b(\d{1,2})\s*(r|n|t|è|a)\b"
        return re.sub(pattern, ord_repl, text, flags=re.IGNORECASE)

    def replace_percentages(self, text: str) -> str:
        """Substitueix percentatges com 25% o 3,5%."""
        def pct_repl(match):
            val_str = match.group(1).replace(",", ".")
            if "." in val_str:
                parts = val_str.split(".")
                integer_part = self.number_to_catalan(int(parts[0]))
                decimal_part = self.number_to_catalan(int(parts[1]))
                return f"{integer_part} coma {decimal_part} per cent"
            else:
                integer_part = self.number_to_catalan(int(val_str))
                return f"{integer_part} per cent"

        return re.sub(r"(\d+(?:[.,]\d+)?)\s*%", pct_repl, text)

    def replace_currencies(self, text: str) -> str:
        """Substitueix monedes (€, $, £)."""
        def euro_repl(match):
            val = match.group(1).replace(",", ".")
            if "." in val:
                parts = val.split(".")
                euros = self.number_to_catalan(int(parts[0]))
                cents = self.number_to_catalan(int(parts[1][:2]))
                return f"{euros} euros amb {cents} cèntims"
            n = int(val)
            noun = "euro" if n == 1 else "euros"
            return f"{self.number_to_catalan(n)} {noun}"

        text = re.sub(r"(\d+(?:[.,]\d+)?)\s*€", euro_repl, text)
        text = re.sub(r"€\s*(\d+(?:[.,]\d+)?)", euro_repl, text)
        text = re.sub(r"\$\s*(\d+)", lambda m: f"{self.number_to_catalan(int(m.group(1)))} dòlars", text)
        return text

    def replace_decimals(self, text: str) -> str:
        """Substitueix números decimals amb coma o punt (p. ex. 3,14 -> tres coma catorze)."""
        def dec_repl(match):
            whole = int(match.group(1))
            dec = int(match.group(2))
            return f"{self.number_to_catalan(whole)} coma {self.number_to_catalan(dec)}"

        return re.sub(r"\b(\d+)[,.](\d+)\b", dec_repl, text)

    def replace_cardinals(self, text: str) -> str:
        """Substitueix xifres cardinals soltes (p. ex. 2026 -> dos mil vint-i-sis)."""
        def num_repl(match):
            n = int(match.group(0))
            return self.number_to_catalan(n)

        return re.sub(r"\b\d+\b", num_repl, text)

    def normalize(self, text: str) -> str:
        """
        Executa el pipeline complet de normalització en català.
        Preserva etiquetes de marcatge i neteja caràcters especials.
        """
        if not text:
            return ""

        # 1. Abreviatures i sigles docents
        for regex, replacement in self.ABBREVIATIONS:
            text = regex.sub(replacement, text)

        # 2. Ordinals (1r, 2a, etc.)
        text = self.replace_ordinals(text)

        # 3. Percentatges (25%)
        text = self.replace_percentages(text)

        # 4. Monedes (10€, $5)
        text = self.replace_currencies(text)

        # 5. Decimals (3,14)
        text = self.replace_decimals(text)

        # 6. Cardinals (12 -> dotze)
        text = self.replace_cardinals(text)

        # 7. Símbols matemàtics comuns
        text = re.sub(r"\s*\+\s*", " més ", text)
        text = re.sub(r"\s*=\s*", " és igual a ", text)
        text = re.sub(r"\s*/\s*", " partit per ", text)

        # 8. Unificació d'espais
        text = re.sub(r"\s+", " ", text).strip()

        return text
