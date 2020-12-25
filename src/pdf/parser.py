import fitz

from settings import BOTTOM_PADDING


def extract_interest_info(info_words, left, right, top, bottom_ret=False):
    if bottom_ret:
        interest_info = []
    else:
        interest_info = ""
    for i_word in info_words:
        if not bottom_ret:
            if left <= i_word[0] <= right and top <= i_word[1] <= top + BOTTOM_PADDING:
                interest_info += i_word[4] + " "
        else:
            if left <= i_word[0] <= right and top <= i_word[1]:
                interest_info.append([i_word[0], i_word[1], i_word[4]])
    if not bottom_ret:
        interest_info = interest_info[:-1]

    return interest_info


def extract_product_info(line, words, height):
    init_item_info = ""
    for word in words:
        if line - 5 <= word[1] <= line + 1.5 * height:
            init_item_info += word[2] + " "

    return init_item_info[:-1]


def parse_pdf(file_path):
    pdf_info = {"A": ["SPOTLIGHT"], "B": ["SPOTLIGHT"], "C": ["VADAIN,"],
                "D": ["57 MAGNESIUM DRIVE"], "E": ["CRESTMEAD  QLD  4132"],
                "F": ["102288"], "G": ["O"], "H": [], "I": [], "J": [],
                "K": [], "L": [], "M": [], "N": []}

    doc = fitz.open(file_path)
    page = doc[0]
    pdf_words = page.getText("words")
    init_N = ""
    product_info = []
    L_info = []
    qty_info = []
    M_info = []
    ref_left = 0
    ref_right = 0
    ref_top = 0
    for i, word in enumerate(pdf_words):
        if word[4] == "PURCHASE" and pdf_words[i + 1][4] == "ORDER" and pdf_words[i + 2][4] == "DATE":
            H_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 2][2],
                                              top=word[3])
            pdf_info["H"].append(H_info)
        elif word[4] == "PURCHASE" and pdf_words[i + 1][4] == "ORDER" and pdf_words[i + 2][4] == "NO":
            customer_po_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 2][2],
                                                     top=word[3])
            pdf_info["I"].append(customer_po_info)
        elif word[4] == "ORDER" and pdf_words[i + 1][4] == "NO" and pdf_words[i + 2][4] == "CONTACT":
            init_N_info = extract_interest_info(info_words=pdf_words, left=word[0] - 10,
                                                      right=pdf_words[i + 1][2] + 10, top=word[3])
            init_N += init_N_info + "; "
        elif word[4] == "CONTACT" and pdf_words[i + 1][4] == "STORE":
            init_N_info = extract_interest_info(info_words=pdf_words, left=word[0] - 30,
                                                      right=word[2] + 40, top=word[3])
            init_N += init_N_info + "; "
        elif word[4] == "STORE" and pdf_words[i + 1][4] == "NAME":
            init_N_info = extract_interest_info(info_words=pdf_words, left=word[0] - 30,
                                                      right=word[2] + 30, top=word[3])
            init_N += init_N_info + "; "
        elif word[4] == "PRODUCT" and pdf_words[i + 1][4] == "QTY":
            product_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 1][2] - 30,
                                                 top=word[3], bottom_ret=True)
        elif word[4] == "QTY" and pdf_words[i + 1][4] == "UNIT":
            qty_info = extract_interest_info(info_words=pdf_words, left=word[0] - 10, right=word[2] + 3,
                                             top=word[3], bottom_ret=True)
        elif word[4] == "UNIT" and pdf_words[i + 1][4] == "PRICE":
            L_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 1][2] + 10,
                                               top=word[3], bottom_ret=True)
        elif word[4] == "LINE" and pdf_words[i + 1][4] == "TOTAL":
            M_info = extract_interest_info(info_words=pdf_words, left=word[0], right=pdf_words[i + 1][2] + 10,
                                               top=word[3], bottom_ret=True)
        elif word[4] == "REFERENCE":
            ref_left = word[0]
            ref_right = word[2]
            ref_top = word[3]

    ref_lines = []
    for word in pdf_words:
        if ref_left - 10 < word[0] < ref_right and ref_top < word[1] and "POW" in word[4]:
            ref_lines.append([word[1], word[3] - word[1]])

    for r_line_info in ref_lines:
        r_line, r_height = r_line_info
        pdf_info["J"].append(
            extract_product_info(line=r_line, words=product_info, height=r_height).replace("102288.", ""))
        pdf_info["K"].append(extract_product_info(line=r_line, words=qty_info, height=r_height))
        pdf_info["L"].append(extract_product_info(line=r_line, words=L_info, height=r_height).replace("$", ""))
        pdf_info["M"].append(extract_product_info(line=r_line, words=M_info, height=r_height).replace("$", ""))

    pdf_info["N"].append(init_N[:-2])
    pdf_info["A"] = len(pdf_info["J"]) * pdf_info["A"]
    pdf_info["B"] = len(pdf_info["J"]) * pdf_info["B"]
    pdf_info["C"] = len(pdf_info["J"]) * pdf_info["C"]
    pdf_info["D"] = len(pdf_info["J"]) * pdf_info["D"]
    pdf_info["E"] = len(pdf_info["J"]) * pdf_info["E"]
    pdf_info["F"] = len(pdf_info["J"]) * pdf_info["F"]
    pdf_info["G"] = len(pdf_info["J"]) * pdf_info["G"]
    pdf_info["H"] = len(pdf_info["J"]) * pdf_info["H"]
    pdf_info["I"] = len(pdf_info["J"]) * pdf_info["I"]
    pdf_info["N"] = len(pdf_info["J"]) * pdf_info["N"]

    return pdf_info


if __name__ == '__main__':
    parse_pdf(file_path="")
