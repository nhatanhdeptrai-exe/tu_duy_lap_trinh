import unicodedata
import re
import os
import json
from datetime import datetime


# 1. DATABASE DỮ LIỆU CỦA CHƯƠNG TRÌNH


# nơi gán value cho key
BANG_DONG_NGHIA = {
    "thit lon": "thit_lon", "thit heo": "thit_lon", "lon": "thit_lon", "heo": "thit_lon", "pork": "thit_lon",
    "thit bo": "thit_bo", "bo": "thit_bo", "beef": "thit_bo",
    "thit ga": "thit_ga", "ga": "thit_ga", "chicken": "thit_ga",
    "ca": "ca", "fish": "ca",
    "trung": "trung", "egg": "trung",
    "luon": "luon", "vit": "vit", "de": "de",
    "rau": "rau",
    "rau cai": "rau_cai",
    "rau muong": "rau_muong",
    "rau cai ngot": "rau_cai_ngot",
    "dua leo": "dua_leo", "dua chuot": "dua_leo",
    "ca phao": "ca_phao",
    "bau": "bau", "qua bau": "bau",
    "bi": "bi", "qua bi": "bi", "bi dao": "bi", "bi do": "bi",
    "lac": "lac", "dau phong": "lac",
    "khoai tay": "khoai_tay", "khoai": "khoai_tay",
    "ca rot": "ca_rot",
    "hanh": "hanh", "hanh la": "hanh",
    "toi": "toi", "ot": "ot", "gung": "gung",
    "mam": "mam", "nuoc mam": "mam",
    "muoi": "muoi", "tieu": "tieu",
    "mi chinh": "mi_chinh", "bot ngot": "mi_chinh",
    "gia vi": "gia_vi", "bot nem": "gia_vi", "tuong ot": "gia_vi",
    "vung": "vung", "me": "vung",
}

#tên biến của nguyên liệu để  xử lý
DANH_MUC_CHINH = {
    "thit_lon", "thit_bo", "thit_ga", "ca", "trung", "luon", "vit", "de",
    "rau", "khoai_tay", "ca_rot", "rau_cai",
    "rau_muong", "rau_cai_ngot", "dua_leo", "ca_phao", "bau", "bi", "lac"
}
DANH_MUC_PHU = {
    "hanh", "toi", "ot", "gung",
    "mam", "muoi", "gia_vi", "tieu", "mi_chinh",
    "vung"
}

#tên hiển thị trên giao diện cho mỗi món ăn
TEN_HIEN_THI = {
    "thit_lon": "Thịt lợn", "thit_bo": "Thịt bò", "thit_ga": "Thịt gà",
    "ca": "Cá", "trung": "Trứng", "luon": "Lươn", "vit": "Vịt", "de": "Dê",
    "rau": "Rau", "khoai_tay": "Khoai tây", "ca_rot": "Cà rốt", "rau_cai": "Rau cải",
    "rau_muong": "Rau muống", "rau_cai_ngot": "Rau cải ngọt", "dua_leo": "Dưa leo",
    "ca_phao": "Cà pháo", "bau": "Bầu", "bi": "Bí", "lac": "Lạc (Đậu phộng)",
    "hanh": "Hành", "toi": "Tỏi", "ot": "Ớt", "gung": "Gừng",
    "mam": "Mắm", "muoi": "Muối", "gia_vi": "Gia vị", "tieu": "Tiêu", "mi_chinh": "Mì chính",
    "vung": "Vừng (Mè)",
}

#phần nguyên liệu tạo nên 1 món ăn
DATABASE_MON_AN = [
    {"ten_mon": "Thịt lợn luộc", "nguyen_lieu_chinh_keys": ["thit_lon"], "nguyen_lieu_phu_keys": [],
     "tat_ca_nguyen_lieu_set": {"thit_lon"}},
    {"ten_mon": "Gà luộc", "nguyen_lieu_chinh_keys": ["thit_ga"], "nguyen_lieu_phu_keys": [],
     "tat_ca_nguyen_lieu_set": {"thit_ga"}},
    {"ten_mon": "Trứng luộc", "nguyen_lieu_chinh_keys": ["trung"], "nguyen_lieu_phu_keys": [],
     "tat_ca_nguyen_lieu_set": {"trung"}},
    {"ten_mon": "Dưa leo (ăn sống)", "nguyen_lieu_chinh_keys": ["dua_leo"], "nguyen_lieu_phu_keys": [],  # <-- Món mới
     "tat_ca_nguyen_lieu_set": {"dua_leo"}},
    {"ten_mon": "Thịt lợn rang", "nguyen_lieu_chinh_keys": ["thit_lon"], "nguyen_lieu_phu_keys": ["mam"],
     "tat_ca_nguyen_lieu_set": {"thit_lon", "mam"}},
    {"ten_mon": "Trứng chiên", "nguyen_lieu_chinh_keys": ["trung"], "nguyen_lieu_phu_keys": ["mam"],
     "tat_ca_nguyen_lieu_set": {"trung", "mam"}},
    {"ten_mon": "Cá rán", "nguyen_lieu_chinh_keys": ["ca"], "nguyen_lieu_phu_keys": ["muoi"],
     "tat_ca_nguyen_lieu_set": {"ca", "muoi"}},
    {"ten_mon": "Gà rang gừng", "nguyen_lieu_chinh_keys": ["thit_ga"], "nguyen_lieu_phu_keys": ["gung"],
     "tat_ca_nguyen_lieu_set": {"thit_ga", "gung"}},
    {"ten_mon": "Rau cải luộc", "nguyen_lieu_chinh_keys": ["rau_cai"], "nguyen_lieu_phu_keys": ["muoi"],
     "tat_ca_nguyen_lieu_set": {"rau_cai", "muoi"}},
    {"ten_mon": "Rau muống luộc", "nguyen_lieu_chinh_keys": ["rau_muong"], "nguyen_lieu_phu_keys": ["muoi"],
     "tat_ca_nguyen_lieu_set": {"rau_muong", "muoi"}},
    {"ten_mon": "Bầu luộc", "nguyen_lieu_chinh_keys": ["bau"], "nguyen_lieu_phu_keys": ["muoi"],  # <-- Món mới
     "tat_ca_nguyen_lieu_set": {"bau", "muoi"}},
    {"ten_mon": "Bí luộc", "nguyen_lieu_chinh_keys": ["bi"], "nguyen_lieu_phu_keys": ["muoi"],  # <-- Món mới
     "tat_ca_nguyen_lieu_set": {"bi", "muoi"}},
    {"ten_mon": "Rau xào tỏi", "nguyen_lieu_chinh_keys": ["rau"], "nguyen_lieu_phu_keys": ["toi"],
     "tat_ca_nguyen_lieu_set": {"rau", "toi"}},
    {"ten_mon": "Rau muống xào tỏi", "nguyen_lieu_chinh_keys": ["rau_muong"], "nguyen_lieu_phu_keys": ["toi"],
     "tat_ca_nguyen_lieu_set": {"rau_muong", "toi"}},
    {"ten_mon": "Lạc rang muối", "nguyen_lieu_chinh_keys": ["lac"], "nguyen_lieu_phu_keys": ["muoi"],  # <-- Món mới
     "tat_ca_nguyen_lieu_set": {"lac", "muoi"}},
    {"ten_mon": "Muối vừng", "nguyen_lieu_chinh_keys": [], "nguyen_lieu_phu_keys": ["vung", "muoi"],  # <-- Món mới
     "tat_ca_nguyen_lieu_set": {"vung", "muoi"}},
    {"ten_mon": "Trứng chiên hành", "nguyen_lieu_chinh_keys": ["trung"], "nguyen_lieu_phu_keys": ["hanh", "mam"],
     "tat_ca_nguyen_lieu_set": {"trung", "hanh", "mam"}},
    {"ten_mon": "Muối lạc vừng", "nguyen_lieu_chinh_keys": ["lac"], "nguyen_lieu_phu_keys": ["vung", "muoi"],
     "tat_ca_nguyen_lieu_set": {"lac", "vung", "muoi"}},
    {"ten_mon": "Bầu xào tỏi", "nguyen_lieu_chinh_keys": ["bau"], "nguyen_lieu_phu_keys": ["toi", "hanh"],
     "tat_ca_nguyen_lieu_set": {"bau", "toi", "hanh"}},
    {"ten_mon": "Thịt lợn kho", "nguyen_lieu_chinh_keys": ["thit_lon"], "nguyen_lieu_phu_keys": ["mam", "muoi", "hanh"],
     "tat_ca_nguyen_lieu_set": {"thit_lon", "mam", "muoi", "hanh"}},
    {"ten_mon": "Canh trứng cà rốt", "nguyen_lieu_chinh_keys": ["trung", "ca_rot"],
     "nguyen_lieu_phu_keys": ["hanh", "muoi"], "tat_ca_nguyen_lieu_set": {"trung", "ca_rot", "hanh", "muoi"}},
    {"ten_mon": "Bò xào khoai tây", "nguyen_lieu_chinh_keys": ["thit_bo", "khoai_tay"],
     "nguyen_lieu_phu_keys": ["toi", "hanh", "gia_vi"],
     "tat_ca_nguyen_lieu_set": {"thit_bo", "khoai_tay", "toi", "hanh", "gia_vi"}},
    {"ten_mon": "Canh bí đỏ thịt băm", "nguyen_lieu_chinh_keys": ["bi", "thit_lon"],
     "nguyen_lieu_phu_keys": ["hanh", "mam", "muoi"],
     "tat_ca_nguyen_lieu_set": {"bi", "thit_lon", "hanh", "mam", "muoi"}},
    {"ten_mon": "Cà pháo muối xổi", "nguyen_lieu_chinh_keys": ["ca_phao"],
     "nguyen_lieu_phu_keys": ["mam", "toi", "ot", "gung"],
     "tat_ca_nguyen_lieu_set": {"ca_phao", "mam", "toi", "ot", "gung"}},
]


TEP_NGUYEN_LIEU_MOI = "du_lieu/nguyen_lieu_moi.jsonl" #địa chỉ lưu file mặc định nếu không có sẵn (có thể đổi)



# 2. hàm xử lý chuẩn hóa từ input

def _ghi_json_line(path, obj):
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except Exception as e:
        pass


def luu_nguyen_lieu_moi(loai, raw, norm):
    if not (raw and norm): return
    rec = {"time": datetime.now().isoformat(timespec="seconds"), "Nguyên liệu": loai, "raw": raw}
    _ghi_json_line(TEP_NGUYEN_LIEU_MOI, rec)


def bo_dau(s):
    s_norm = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s_norm if not unicodedata.combining(ch))


def chuan_hoa_tu(token):
    t = (token or "").strip().lower()
    t = bo_dau(t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return BANG_DONG_NGHIA.get(t, t)


def tach_danh_sach(chuoi):
    if not chuoi:
        return []

    danh_sach_ket_qua = []
    cac_muc_tho = chuoi.split(",")
    for m in cac_muc_tho:
        muc_sach = m.strip()
        if muc_sach:
            danh_sach_ket_qua.append(muc_sach)
    return danh_sach_ket_qua



# 3. hàm CHÍNH để bắt đầu xử lý (giao diện)


def tim_kiem_mon_an(input_nguyen_lieu_chung):

    ds_raw = tach_danh_sach(input_nguyen_lieu_chung)

    chinh_da_chuan_hoa = set()
    phu_da_chuan_hoa = set()
    tat_ca_khong_biet = set()


    for raw_token in ds_raw:
        norm_token = chuan_hoa_tu(raw_token)

        if norm_token in DANH_MUC_CHINH:
            chinh_da_chuan_hoa.add(norm_token)
        elif norm_token in DANH_MUC_PHU:
            phu_da_chuan_hoa.add(norm_token)

        elif norm_token:
            luu_nguyen_lieu_moi("chung", raw_token, norm_token)
            tat_ca_khong_biet.add(raw_token)

    # 3. Tìm kiếm món ăn  trong database
    danh_sach_goi_y = []
    cac_mon_chinh_nguoi_dung_co = chinh_da_chuan_hoa
    cac_mon_phu_nguoi_dung_co = phu_da_chuan_hoa

    for mon_an in DATABASE_MON_AN:
        set_chinh_yeu_cau = set(mon_an["nguyen_lieu_chinh_keys"])
        set_phu_yeu_cau = set(mon_an["nguyen_lieu_phu_keys"])

        la_mon_goi_y = False

        if cac_mon_chinh_nguoi_dung_co:
            if any(item in set_chinh_yeu_cau for item in cac_mon_chinh_nguoi_dung_co):
                la_mon_goi_y = True

        elif not cac_mon_chinh_nguoi_dung_co and cac_mon_phu_nguoi_dung_co:
            if any(item in set_phu_yeu_cau for item in cac_mon_phu_nguoi_dung_co):
                if not set_chinh_yeu_cau:
                    la_mon_goi_y = True

        if la_mon_goi_y:
            ten_nl_chinh = ", ".join([TEN_HIEN_THI.get(key, key) for key in mon_an["nguyen_lieu_chinh_keys"]])
            ten_nl_phu = ", ".join([TEN_HIEN_THI.get(key, key) for key in mon_an["nguyen_lieu_phu_keys"]])
            mon_an_tim_thay = {"ten": mon_an["ten_mon"], "chinh": ten_nl_chinh if ten_nl_chinh else "Không có",
                               "phu": ten_nl_phu if ten_nl_phu else "Không có"}
            danh_sach_goi_y.append(mon_an_tim_thay)

    # 4. nguyên liệu đã nhận diện (chuỗi)


    chinh_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in chinh_da_chuan_hoa]
    phu_nhan_dien_list = [TEN_HIEN_THI.get(key, key) for key in phu_da_chuan_hoa]
    str_hien_thi_chung = ""

    if chinh_nhan_dien_list:
        str_hien_thi_chung += f" {', '.join(chinh_nhan_dien_list)}"

    if phu_nhan_dien_list:
        if str_hien_thi_chung:
            str_hien_thi_chung += " | "
        str_hien_thi_chung += f"Phụ: {', '.join(phu_nhan_dien_list)}"

    if not str_hien_thi_chung:
        str_hien_thi_chung = "(Chưa nhận diện được nguyên liệu nào)"
    return (str_hien_thi_chung, danh_sach_goi_y, tat_ca_khong_biet)