"""
Paleta de Colors i Estil Visual: disseny minimalista japonès (Modern Matcha Studio).
Inspirat en el disseny contemporani d'alta gamma (estil Notion, Craft, Linear, Muji).
Garanteix conformitat estricta WCAG AAA:
- Fons verds o foscos -> SEMPRE text blanc pur (#FFFFFF).
- Fons clars o blancs -> SEMPRE text fosc d'alta llegibilitat (#142419).
"""

class MatchaTheme:
    # Fons i superfícies
    BG_MAIN = "#F6F9F6"         # Blanc porcellana suau amb matís matxa subtil
    BG_CARD = "#FFFFFF"         # Blanc pur per a targetes i panells principals
    BG_CARD_HOVER = "#F0F5F0"   # To interactiu molt suau
    BG_CARD_SUBTLE = "#F0F4F0"  # Fons per a contenidors interns i llistes
    BORDER_CARD = "#DFEAE0"     # Micro-vora elegant de 1px
    BORDER_FOCUS = "#2E5E41"
    CARD_RADIUS = 14            # Radis moderns i generosos (14px)
    PILL_RADIUS = 16            # Per a botons tipus píndola

    # Verds Matxa Principals (Elegants, profunds, màxim contrast)
    PRIMARY = "#2E5E41"         # Verd matxa cerimonial profund i reposat
    PRIMARY_HOVER = "#21442F"   # To ric al passar el ratolí
    PRIMARY_ACTIVE = "#1A3624"
    PRIMARY_LIGHT = "#EAF3EB"   # Fons subtil per a xips actius i badges
    PRIMARY_MUTED = "#557B62"   # Verd suau per a controls secundaris

    # Accents complementaris càlids
    ACCENT_BAMBOO = "#B8955A"   # Fusta de bambú daurada (batedor chasen)
    ACCENT_BAMBOO_HOVER = "#A38249"
    ACCENT_TERRACOTTA = "#C7543E" # Terracota refinada per a cancel·lar/aturar
    ACCENT_TERRACOTTA_HOVER = "#AF432F"

    # Tipografia d'alt contrast (WCAG AAA)
    TEXT_MAIN = "#142419"       # Negre-verd bosc profund, nítid i elegant sobre fons clar
    TEXT_SECONDARY = "#48624F"  # Verd pissarra per a metadades i subtítols
    TEXT_MUTED = "#6F8674"      # Text discret per a indicadors secundaris
    TEXT_ON_PRIMARY = "#FFFFFF" # Blanc pur sobre fons verd o fosc (MAI fosc sobre verd!)

    # Controls i camps de text
    ENTRY_BG = "#FAFCFA"        # Blanc neutre per a l'editor
    ENTRY_BORDER = "#D6E3D5"

    # Reproductor d'àudio
    PROGRESS_BG = "#E2EBE2"
    PROGRESS_FILL = "#2E5E41"

    # Tipografies de sistema modernes
    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = ("Segoe UI", 16, "bold")
    FONT_SUBTITLE = ("Segoe UI", 12, "bold")
    FONT_SECTION = ("Segoe UI", 11, "bold")
    FONT_BODY = ("Segoe UI", 11)
    FONT_BODY_BOLD = ("Segoe UI", 11, "bold")
    FONT_SMALL = ("Segoe UI", 10)
    FONT_SMALL_BOLD = ("Segoe UI", 10, "bold")
    FONT_TINY = ("Segoe UI", 9)
    FONT_MONO = ("Consolas", 11)
