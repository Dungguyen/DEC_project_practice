import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import Counter
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def def_word_cnt(text):
    """
    Đếm số lần xuất hiện của mỗi từ trong chuỗi
    """
    words = re.findall(r'[\wÀ-ỹ]+', text)
    return dict(Counter(words))

def create_xml(word_count, filename):
    """
    Tạo file XML từ dictionary word_count
    """
    root = ET.Element("word_count")
    
    for word, count in word_count.items():
        word_elem = ET.SubElement(root, "word")
        word_elem.set("name", word)
        word_elem.set("count", str(count))
    
    xml_str = ET.tostring(root, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"✅ Đã tạo file: {filename}")

def send_email(filename, to_email, from_email, password):
    """
    Gửi email với file đính kèm
    """
    try:
        # Tạo email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "Ket qua dem tu"

        # Đính kèm file
        with open(filename, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            # SỬA: attachment (không có 'l' thừa)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)

        # Gửi email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        
        print(f"📧 Đã gửi email với file {filename} đến {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")
        return False

def generate_100_files(word_count):
    """
    Tạo 100 file XML không dùng vòng lặp
    """
    def generate_file(index):
        filename = f"result_{index}.xml"
        create_xml(word_count, filename)
        return filename
    
    # Dùng map để tạo 100 file (không dùng vòng lặp for)
    files = list(map(generate_file, range(1, 101)))
    print(f"✅ Đã tạo {len(files)} file XML thành công!")
    print(f"File đầu tiên: result_1.xml")
    print(f"File cuối cùng: result_100.xml")
    return files

# ========== MAIN ==========
if __name__ == "__main__":
    # Input string
    input_string = "Bạn là thí sinh tuyệt vời nhất mà tôi từng gặp. Bạn quá xuất sắc, quá tuyệt vời!"
    
    # 1. Đếm từ
    word_count = def_word_cnt(input_string)
    print("Kết quả đếm từ:")
    print(word_count)
    print()
    
    # 2. Tạo file result.xml
    create_xml(word_count, "result.xml")
    
    # 3. Gửi email (CHÚ Ý: Sửa đúng thứ tự tham số)
    # send_email(filename, to_email, from_email, password)
    #             ↑          ↑         ↑           ↑
    #          file gửi   người nhận  người gửi  mật khẩu
    
    send_email(
        "result.xml",           # filename: file đính kèm
        "ngannguyenhtqp.1020@gmail.com",         # to_email: email người nhận
        "dungvippro1711@gmail.com",       # from_email: email người gửi (email của bạn)
        "Dung@1711"         # password: mật khẩu email của bạn
    )
    
    # 4. Tạo 100 file (không dùng vòng lặp)
    generate_100_files(word_count)