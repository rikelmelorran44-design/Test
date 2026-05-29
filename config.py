# config.py — Configurações Globais e Custos Fixos

APP_NAME = "Rikelme Drop"
APP_VERSION = "1.0.0"

CUSTOS_FIXOS = {
    "Fornecedor":           140.00,
    "Endereço Comercial":    80.00,
    "Bling ERP":             55.00,
    "MEI DAS":               73.40,
}

TOTAL_CUSTOS_FIXOS = sum(CUSTOS_FIXOS.values())  # R$ 348,40

MARKETPLACES = ["Kwai Shop", "TikTok Shop", "Amazon", "Shopee"]

MARKETPLACE_CORES = {
    "Kwai Shop":   "#FF6B35",
    "TikTok Shop": "#00F2EA",
    "Amazon":      "#FF9900",
    "Shopee":      "#EE4D2D",
}
